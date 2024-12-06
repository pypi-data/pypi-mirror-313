"""CLI for validating and enriching DAPI files: `opendapi enrich`."""

# pylint: disable=duplicate-code

import click

from opendapi.cli.common import Schemas, get_opendapi_config_from_root
from opendapi.cli.enrich.github import GithubEnricher
from opendapi.cli.enrich.github_shadow import GithubShadowModeEnricher
from opendapi.cli.enrich.local import Enricher
from opendapi.cli.options import (
    CATEGORIES_PARAM_NAME_WITH_OPTION,
    DAPI_PARAM_NAME_WITH_OPTION,
    DATASTORES_PARAM_NAME_WITH_OPTION,
    PURPOSES_PARAM_NAME_WITH_OPTION,
    SUBJECTS_PARAM_NAME_WITH_OPTION,
    TEAMS_PARAM_NAME_WITH_OPTION,
    construct_change_trigger_event,
    construct_dapi_server_config,
    dapi_server_options,
    dev_options,
    github_options,
    minimal_schema_options,
    opendapi_run_options,
)
from opendapi.logging import LogDistKey, Timer


@click.command()
@dev_options
@opendapi_run_options
@dapi_server_options
@github_options
@minimal_schema_options
def cli(**kwargs):
    """
    This command will find all the DAPI files in the repository to
        1. validate them for compliance with the company policies
        2. enrich data semantics and classification using AI.
        3. pull forward downstream impact of the changes.

    This interacts with the DAPI server, and thus needs
    the server host and API key as environment variables or CLI options.
    """
    opendapi_config = get_opendapi_config_from_root(kwargs.get("local_spec_path"))
    dapi_server_config = construct_dapi_server_config(kwargs)
    change_trigger_event = construct_change_trigger_event(kwargs)
    minimal_schemas = Schemas(
        teams=TEAMS_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        datastores=DATASTORES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        purposes=PURPOSES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        dapi=DAPI_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        subjects=SUBJECTS_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        categories=CATEGORIES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
    )

    # Check when to use GitHub enricher
    if change_trigger_event.where == "github":
        enricher_cls = (
            GithubShadowModeEnricher
            if dapi_server_config.is_repo_in_shadow_mode
            else GithubEnricher
        )
    else:
        enricher_cls = Enricher

    enricher = enricher_cls(
        config=opendapi_config,
        dapi_server_config=dapi_server_config,
        trigger_event=change_trigger_event,
        revalidate_all_files=dapi_server_config.revalidate_all_files,
        require_committed_changes=dapi_server_config.require_committed_changes,
        minimal_schemas_for_validation=minimal_schemas,
    )

    enricher.print_markdown_and_text(
        "\nGetting ready to validate and enrich your DAPI files...",
        color="green",
    )
    metrics_tags = {
        "org_name": opendapi_config.org_name_snakecase,
        "where": change_trigger_event.where,
        "event_type": change_trigger_event.event_type,
    }
    with Timer(dist_key=LogDistKey.CLI_ENRICH, tags=metrics_tags):
        enricher.run()
