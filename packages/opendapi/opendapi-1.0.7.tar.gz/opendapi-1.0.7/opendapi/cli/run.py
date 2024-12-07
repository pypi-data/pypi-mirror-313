"""CLI for generating, validating and enriching DAPI files: `opendapi run`."""

from collections import namedtuple

import click

from opendapi.cli.common import print_cli_output
from opendapi.cli.enrich.main import cli as enrich_cli
from opendapi.cli.generate import cli as generate_cli
from opendapi.cli.options import (
    dapi_server_options,
    dev_options,
    git_options,
    github_options,
    minimal_schema_options,
    opendapi_run_options,
    third_party_options,
)
from opendapi.cli.register import cli as register_cli

RunCommand = namedtuple("RunCommand", ["command", "description", "skip_condition"])


def _should_skip_generate_for_dbt_cloud(**kwargs):
    """
    Check if the `generate` command should be skipped

    Skip scenarios:
    1. If integrated with dbt Cloud
        a. Skip if pull request event and the run is the first attempt
        b. Skip if push event
    """

    should_wait_on_dbt_cloud = kwargs.get("dbt_cloud_url") is not None
    run_attempt = (
        int(kwargs.get("github_run_attempt")) if kwargs.get("github_run_attempt") else 0
    )
    is_push_event = kwargs.get("github_event_name") == "push"

    if should_wait_on_dbt_cloud and is_push_event:
        return True

    if should_wait_on_dbt_cloud and run_attempt == 1:
        return True

    return False


@click.command()
@dev_options
@opendapi_run_options
@dapi_server_options
@git_options
@github_options
@minimal_schema_options
@third_party_options
def cli(**kwargs):
    """
    This command combines the `opendapi generate` and `opendapi enrich` commands.

    This interacts with the DAPI server, and thus needs
    the server host and API key as environment variables or CLI options.
    """

    # Run register last to ensure the DAPI files are registered and unregistered
    # Register will also validate the DAPI files in the backend
    commands = {
        "generate": RunCommand(
            command=generate_cli,
            description="generate DAPI files",
            skip_condition=_should_skip_generate_for_dbt_cloud,
        ),
        "enrich": RunCommand(
            command=enrich_cli,
            description="validate and enrich DAPI files",
            skip_condition=_should_skip_generate_for_dbt_cloud,
        ),
        "register": RunCommand(
            command=register_cli,
            description="register DAPI files",
            skip_condition=None,
        ),
    }

    for command_name, command_info in commands.items():
        if command_info.skip_condition and command_info.skip_condition(**kwargs):
            print_cli_output(
                f"Skipping {command_info.description} command",
                color="yellow",
                bold=True,
            )
            continue

        print_cli_output(
            f"Running `opendapi {command_name}` to {command_info.description}...",
            color="green",
            bold=True,
        )
        command = command_info.command
        command_params = command.params
        # run's params should always be a superset of all the children's params,
        # and therefore we do unsafe dict access as to not swallow any discrepancies
        command_kwargs = {key.name: kwargs[key.name] for key in command_params}
        with click.Context(command) as ctx:
            ctx.invoke(command, **command_kwargs)
