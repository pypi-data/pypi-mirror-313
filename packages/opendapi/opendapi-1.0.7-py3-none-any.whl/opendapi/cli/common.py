"""Common utilities for the OpenDAPI CLI."""

import os
from dataclasses import dataclass
from typing import List, Optional, Protocol, Type, Union

import click
from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for

from opendapi.config import OpenDAPIConfig
from opendapi.defs import CONFIG_FILEPATH_FROM_ROOT_DIR, OpenDAPIEntity


class BaseValidatorWithSuffix(Protocol):  # pylint: disable=too-few-public-methods
    """
    Protocol for all Validators with an ENTITY.

    Added to not include a circular import with BaseValidator.
    """

    ENTITY: OpenDAPIEntity


@dataclass
class Schemas:
    """
    Schemas for various OpenDAPI entities.
    """

    teams: Optional[dict] = None
    datastores: Optional[dict] = None
    purposes: Optional[dict] = None
    dapi: Optional[dict] = None
    subjects: Optional[dict] = None
    categories: Optional[dict] = None

    def __post_init__(self):
        """Validate the schemas."""
        self.validate_schemas()

    def validate_schemas(self):
        """Validate the schemas against their meta schema."""
        errors = []
        for schema_name in ("teams", "datastores", "purposes", "dapi"):
            schema = getattr(self, schema_name)
            if schema:
                validator_cls = validator_for(schema)
                try:
                    validator_cls.check_schema(schema)
                except SchemaError as exc:
                    errors.append(f"Schema for {schema_name} is invalid: {exc}")
        if errors:
            print_cli_output(
                "OpenDAPI: Encountered validation errors",
                color="red",
                bold=True,
            )
            for error in errors:
                print_cli_output(error, color="red", bold=True)
            raise TypeError("\n".join(errors))

    def minimal_schema_for(
        self,
        validator_cls: Union[BaseValidatorWithSuffix, Type[BaseValidatorWithSuffix]],
    ) -> Optional[dict]:
        """Get the minimal schema for the given validator class."""
        if not hasattr(validator_cls, "SUFFIX"):
            raise ValueError(f"Unknown validator class: {validator_cls}")

        if validator_cls.ENTITY is OpenDAPIEntity.TEAMS:
            return self.teams
        if validator_cls.ENTITY is OpenDAPIEntity.DATASTORES:
            return self.datastores
        if validator_cls.ENTITY is OpenDAPIEntity.PURPOSES:
            return self.purposes
        if validator_cls.ENTITY is OpenDAPIEntity.DAPI:
            return self.dapi
        if validator_cls.ENTITY is OpenDAPIEntity.SUBJECTS:
            return self.subjects
        if validator_cls.ENTITY is OpenDAPIEntity.CATEGORIES:
            return self.categories

        raise ValueError(f"Unknown validator class: {validator_cls}")

    @property
    def as_dict(self):
        """Return the schemas as a dictionary."""
        return {
            "teams": self.teams,
            "datastores": self.datastores,
            "purposes": self.purposes,
            "dapi": self.dapi,
            "subjects": self.subjects,
            "categories": self.categories,
        }


def check_command_invocation_in_root():
    """Check if the `opendapi` CLI command is invoked from the root of the repository."""
    if not (os.path.isdir(".github") or os.path.isdir(".git")):
        click.secho(
            "  This command must be run from the root of your repository. Exiting...",
            fg="red",
        )
        raise click.Abort()
    click.secho(
        "  We are in the root of the repository. Proceeding...",
        fg="green",
    )
    return True


def get_opendapi_config_from_root(
    local_spec_path: Optional[str] = None,
    validate_config: bool = False,
) -> OpenDAPIConfig:
    """Get the OpenDAPI configuration object."""
    root_dir = os.getcwd()
    check_command_invocation_in_root()

    try:
        config = OpenDAPIConfig(root_dir, local_spec_path=local_spec_path)
        click.secho(
            f"  Found the {CONFIG_FILEPATH_FROM_ROOT_DIR} file. Proceeding...",
            fg="green",
        )
        if validate_config:
            check_if_opendapi_config_is_valid(config)
        return config
    except FileNotFoundError as exc:
        click.secho(
            f"  The {CONFIG_FILEPATH_FROM_ROOT_DIR} file does not exist. "
            "Please run `opendapi init` first. Exiting...",
            fg="red",
        )
        raise click.Abort() from exc


def check_if_opendapi_config_is_valid(config: OpenDAPIConfig) -> bool:
    """Check if the `opendapi.config.yaml` file is valid."""
    try:
        config.validate()
    except Exception as exc:
        click.secho(
            f"  The `{CONFIG_FILEPATH_FROM_ROOT_DIR}` file is not valid. "
            f"`opendapi init` may rectify. {exc}. Exiting...",
            fg="red",
        )
        raise click.Abort()
    click.secho(
        f"  The {CONFIG_FILEPATH_FROM_ROOT_DIR} file is valid. Proceeding...",
        fg="green",
    )
    return True


def pretty_print_errors(errors: List[Exception]):
    """Prints all the errors"""
    if errors:
        print_cli_output(
            "OpenDAPI: Encountered validation errors",
            color="red",
            bold=True,
        )
    for error in errors:
        print_cli_output(
            f"OpenDAPI: {error.prefix_message}",
            color="red",
            bold=True,
        )
        for err in error.errors:
            print_cli_output(err)


def print_cli_output(
    message: str,
    color: str = "green",
    bold: bool = False,
    markdown_file: Optional[str] = None,
    no_text: bool = False,
    no_markdown: bool = False,
):
    """Print errors."""
    # Text message
    if not no_text:
        click.secho(message, fg=color, bold=bold)

    # Markdown message
    if markdown_file and not no_markdown:
        with open(
            markdown_file,
            "a",
            encoding="utf-8",
        ) as m_file:
            print(f"{message}\n\n", file=m_file)
