"""Entrypoint for the OpenDAPI CLI."""

import click
import sentry_sdk

from opendapi.adapters.dapi_server import DAPIRequests
from opendapi.cli.enrich.main import cli as enrich_cli
from opendapi.cli.generate import cli as generate_cli
from opendapi.cli.init import cli as init_cli
from opendapi.cli.options import (
    BASE_COMMIT_SHA_PARAM_NAME_WITH_OPTION,
    CATEGORIES_PARAM_NAME_WITH_OPTION,
    DAPI_PARAM_NAME_WITH_OPTION,
    DATASTORES_PARAM_NAME_WITH_OPTION,
    PURPOSES_PARAM_NAME_WITH_OPTION,
    SUBJECTS_PARAM_NAME_WITH_OPTION,
    TEAMS_PARAM_NAME_WITH_OPTION,
    construct_change_trigger_event,
    construct_dapi_server_config,
    dapi_server_options,
    features_options,
    git_options,
    github_options,
    minimal_schema_options,
    opendapi_run_options,
)
from opendapi.cli.register import cli as register_cli
from opendapi.cli.run import cli as run_cli
from opendapi.feature_flags import FeatureFlag, set_feature_flags
from opendapi.features import load_from_raw_dict, set_feature_to_status
from opendapi.logging import logger, sentry_init


@click.group()
@dapi_server_options
@features_options
@git_options
@github_options
@minimal_schema_options
@opendapi_run_options
def cli(**kwargs):
    """
    OpenDAPI CLI is a command-line interface to initialize and run OpenDAPI projects.\n\n

    This tool helps autogenerate DAPI files and associated configuration files,
    and interacts with DAPI servers to bring the power of AI to your data documentation.\n\n

    Use `opendapi [COMMAND] --help` for more information about a command.
    """

    dapi_server_config = construct_dapi_server_config(kwargs)
    change_trigger_event = construct_change_trigger_event(kwargs)
    dapi_requests = None

    BASE_COMMIT_SHA_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(
        kwargs, change_trigger_event.before_change_sha
    )

    if not kwargs.get("skip_client_config"):
        try:
            # Initialize sentry and fetch Feature flags
            # This fails silently if the client config is not available
            # This is temporary to monitor if this actually breaks
            dapi_requests = DAPIRequests(
                dapi_server_config=dapi_server_config,
                trigger_event=change_trigger_event,
            )

            sentry_tags = {
                "cmd": click.get_current_context().invoked_subcommand,
                "gh_workspace": change_trigger_event.workspace,
                "gh_event_name": change_trigger_event.event_type,
                "gh_run_id": change_trigger_event.run_id,
                "gh_run_attempt": change_trigger_event.run_attempt,
                "gh_repo": change_trigger_event.repository,
            }
            client_config = dapi_requests.get_client_config_from_server()
            sentry_tags.update(client_config.get("sentry_tags", {}))
            sentry_init(
                client_config.get("sentry", {}),
                tags=sentry_tags,
            )

            if client_config.get("fetch_feature_flags", False):
                feature_flags: dict = (
                    dapi_requests.get_client_feature_flags_from_server(
                        [f.value for f in FeatureFlag]
                    )
                )
                set_feature_flags(
                    {
                        FeatureFlag(f): val
                        for f, val in feature_flags.items()
                        if FeatureFlag.has_value(f)
                    }
                )
        except Exception as exp:  # pylint: disable=broad-except
            logger.error("Error fetching client config: %s", exp)

    all_params_present = all(
        kwargs.get(param.name) is not None
        for param in (
            CATEGORIES_PARAM_NAME_WITH_OPTION,
            DAPI_PARAM_NAME_WITH_OPTION,
            DATASTORES_PARAM_NAME_WITH_OPTION,
            PURPOSES_PARAM_NAME_WITH_OPTION,
            SUBJECTS_PARAM_NAME_WITH_OPTION,
            TEAMS_PARAM_NAME_WITH_OPTION,
        )
    )
    fetched_repo_features_info = None
    if not all_params_present and not kwargs.get("skip_server_minimal_schemas"):
        # we do not try/catch here, since if they are not set to skipped then they are required
        # for the run
        dapi_requests = dapi_requests or DAPIRequests(
            dapi_server_config=dapi_server_config,
            trigger_event=change_trigger_event,
        )
        fetched_repo_features_info = dapi_requests.get_repo_features_info_from_server()
        enabled_schemas = fetched_repo_features_info.enabled_schemas
        CATEGORIES_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(
            kwargs, enabled_schemas.categories
        )
        DAPI_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(kwargs, enabled_schemas.dapi)
        DATASTORES_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(
            kwargs, enabled_schemas.datastores
        )
        PURPOSES_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(
            kwargs, enabled_schemas.purposes
        )
        SUBJECTS_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(
            kwargs, enabled_schemas.subjects
        )
        TEAMS_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(
            kwargs, enabled_schemas.teams
        )

    raw_feature_to_status = kwargs.get("feature_to_status")
    # not set, load from dapi server
    if raw_feature_to_status is None:
        if not fetched_repo_features_info:
            dapi_requests = dapi_requests or DAPIRequests(
                dapi_server_config=dapi_server_config,
                trigger_event=change_trigger_event,
            )
            fetched_repo_features_info = (
                dapi_requests.get_repo_features_info_from_server()
            )

        feature_to_status = fetched_repo_features_info.feature_to_status

    # set, load from env var raw dict
    else:
        feature_to_status = load_from_raw_dict(raw_feature_to_status)

    set_feature_to_status(feature_to_status)


def cli_wrapper():
    """A wrapper for all commands so we can capture exceptions and log them"""
    try:
        cli()
    except Exception as exp:  # pylint: disable=broad-except
        # This catches all the exceptions that are uncaught by click.
        # For eg: If an application developer raises click.Abort(), click handles
        # it and exits the program. This is expected behavior and we will not send
        # these to sentry. However, if the application fails due to an internal
        # error, we will catch it and log it.
        sentry_sdk.capture_exception(exp)
        raise exp


# Add commands to the CLI
cli.add_command(init_cli, name="init")
cli.add_command(generate_cli, name="generate")
cli.add_command(enrich_cli, name="enrich")
cli.add_command(register_cli, name="register")
cli.add_command(run_cli, name="run")
