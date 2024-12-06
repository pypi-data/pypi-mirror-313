"""Entrypoint for the OpenDAPI CLI `opendapi generate` command."""

# pylint: disable=duplicate-code

from typing import List, Type

import click

from opendapi.cli.common import (
    Schemas,
    get_opendapi_config_from_root,
    pretty_print_errors,
    print_cli_output,
)
from opendapi.cli.options import (
    BASE_COMMIT_SHA_PARAM_NAME_WITH_OPTION,
    CATEGORIES_PARAM_NAME_WITH_OPTION,
    DAPI_PARAM_NAME_WITH_OPTION,
    DATASTORES_PARAM_NAME_WITH_OPTION,
    PURPOSES_PARAM_NAME_WITH_OPTION,
    SUBJECTS_PARAM_NAME_WITH_OPTION,
    TEAMS_PARAM_NAME_WITH_OPTION,
    dev_options,
    git_options,
    minimal_schema_options,
)
from opendapi.logging import LogDistKey, Timer
from opendapi.validators.base import BaseValidator
from opendapi.validators.categories import CategoriesValidator
from opendapi.validators.dapi import (
    ALWAYS_RUN_DAPI_VALIDATORS,
    DAPI_INTEGRATIONS_VALIDATORS,
)
from opendapi.validators.datastores import DatastoresValidator
from opendapi.validators.defs import FileSet
from opendapi.validators.subjects import SubjectsValidator
from opendapi.validators.teams import TeamsValidator
from opendapi.writers.utils import get_writer_for_entity


@click.command()
@minimal_schema_options
@dev_options
@git_options
def cli(**kwargs):  # pylint: disable=too-many-locals
    """
    Generate DAPI files for integrations specified in the OpenDAPI configuration file.

    For certain integrations such as DBT and PynamoDB, this command will also run
    additional commands in the respective integration directories to generate DAPI files.
    """
    print_cli_output(
        "Generating DAPI files for your integrations per `opendapi.config.yaml` configuration",
        color="green",
    )
    opendapi_config = get_opendapi_config_from_root(
        local_spec_path=kwargs.get("local_spec_path"), validate_config=True
    )

    minimal_schemas = Schemas(
        teams=TEAMS_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        datastores=DATASTORES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        purposes=PURPOSES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        dapi=DAPI_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        subjects=SUBJECTS_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        categories=CATEGORIES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
    )

    # determine all of the required validators
    validators: List[Type[BaseValidator]] = [
        TeamsValidator,
        DatastoresValidator,
        CategoriesValidator,
        SubjectsValidator,
        *ALWAYS_RUN_DAPI_VALIDATORS,
    ]

    print_cli_output(
        "Identifying your integrations...",
        color="yellow",
    )
    for intg, validator in DAPI_INTEGRATIONS_VALIDATORS.items():
        if opendapi_config.has_integration(intg):
            if validator is not None:
                validators.append(validator)
            print_cli_output(f"  Found {intg}...", color="green")

    print_cli_output(
        "Generating DAPI files for your integrations...",
        color="yellow",
    )
    metrics_tags = {"org_name": opendapi_config.org_name_snakecase}
    with Timer(dist_key=LogDistKey.CLI_GENERATE, tags=metrics_tags):

        total_errors = []

        # if the base commit is known, determine the file state at that commit,
        # as this is useful in determining if files should be written or not
        base_commit_sha = kwargs.get(BASE_COMMIT_SHA_PARAM_NAME_WITH_OPTION.name)
        base_collected_files = {}
        if base_commit_sha:
            print_cli_output(
                "Tackling base commit...",
                color="yellow",
            )
            base_collected_files, errors = BaseValidator.run_validators(
                validators=validators,
                root_dir=opendapi_config.root_dir,
                enforce_existence_at=None,
                # may not exist at base commit
                override_config=opendapi_config,
                minimal_schemas=minimal_schemas,
                commit_sha=base_commit_sha,
            )
            total_errors.extend(errors)

        # now collect for the current state
        print_cli_output(
            "Tackling current state...",
            color="yellow",
        )
        current_collected_files, errors = BaseValidator.run_validators(
            validators=validators,
            root_dir=opendapi_config.root_dir,
            enforce_existence_at=FileSet.MERGED,
            override_config=opendapi_config,
            minimal_schemas=minimal_schemas,
            # we will use the state of the repo at the time Generate was invoked
            commit_sha=None,
        )
        total_errors.extend(errors)

        if total_errors:
            pretty_print_errors(total_errors)
            # fails with exit code 1 - meaning it blocks merging - but as a ClickException
            # it does not go to sentry, which is appropriate, as this is not an error condition
            raise click.ClickException("Encountered one or more validation errors")

        # actually write
        always_write = kwargs.get("always_write_generated_dapis", False)
        for entity, collected_files in current_collected_files.items():
            writer_cls = get_writer_for_entity(entity)
            writer = writer_cls(
                root_dir=opendapi_config.root_dir,
                collected_files=collected_files,
                override_config=opendapi_config,
                base_collected_files=base_collected_files.get(entity),
                always_write=always_write,
            )
            written, skipped = writer.write_files()
            print_cli_output(
                f"{entity.value}: {len(written)} written, {len(skipped)} skipped",
                color="green",
            )

    print_cli_output(
        "Successfully generated DAPI files for your integrations",
        color="green",
    )
