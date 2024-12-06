"""Shared options used by OpenDAPI CLI."""

import functools
import os
from dataclasses import dataclass
from typing import Any, Callable, Optional, TypeVar

import click

from opendapi.adapters.dapi_server import DAPIServerConfig
from opendapi.adapters.git import ChangeTriggerEvent
from opendapi.utils import (
    decode_base64_to_json,
    encode_json_to_base64,
    read_yaml_or_json,
)

S = TypeVar("S")
T = TypeVar("T")


def construct_dapi_server_config(kwargs: dict) -> DAPIServerConfig:
    """Construct the DAPI server configuration from the CLI arguments."""
    return DAPIServerConfig(
        server_host=kwargs["dapi_server_host"],
        api_key=kwargs["dapi_server_api_key"],
        mainline_branch_name=kwargs["mainline_branch_name"],
        register_on_merge_to_mainline=kwargs["register_on_merge_to_mainline"],
        suggest_changes=kwargs["suggest_changes"],
        enrich_batch_size=kwargs["enrich_batch_size"],
        ignore_suggestions_cache=kwargs["ignore_suggestions_cache"],
        register_batch_size=kwargs["register_batch_size"],
        analyze_impact_batch_size=kwargs["analyze_impact_batch_size"],
        pr_sync_batch_size=kwargs["pr_sync_batch_size"],
        revalidate_all_files=kwargs["revalidate_all_files"],
        require_committed_changes=kwargs["require_committed_changes"],
        woven_integration_mode=kwargs["woven_integration_mode"],
        woven_configuration=kwargs["woven_configuration"],
        feature_validate_dapi_batch_size=kwargs["feature_validate_dapi_batch_size"],
    )


def construct_change_trigger_event(kwargs: dict) -> ChangeTriggerEvent:
    """Construct the change trigger event from the CLI arguments."""

    github_event_name = kwargs.get("github_event_name")
    github_event_path = kwargs.get("github_event_path")
    github_token = kwargs.get("github_token")
    if github_event_name is None or github_event_path is None or github_token is None:
        return ChangeTriggerEvent(
            where="local",
            before_change_sha=kwargs["mainline_branch_name"],
            after_change_sha="HEAD",
        )
    github_event = read_yaml_or_json(kwargs["github_event_path"])
    return ChangeTriggerEvent(
        where="github",
        event_type=github_event_name,
        repo_api_url=github_event["repository"]["url"],
        repo_html_url=github_event["repository"]["html_url"],
        repo_owner=github_event["repository"]["owner"]["login"],
        before_change_sha=(
            github_event["before"]
            if github_event_name == "push"
            else github_event["pull_request"]["base"]["sha"]
        ),
        after_change_sha=(
            github_event["after"]
            if github_event_name == "push"
            else github_event["pull_request"]["head"]["sha"]
        ),
        git_ref=(
            github_event["ref"]
            if github_event_name == "push"
            else github_event["pull_request"]["head"]["ref"]
        ),
        pull_request_number=(
            github_event["pull_request"]["number"]
            if github_event_name == "pull_request"
            else None
        ),
        auth_token=github_token,
        markdown_file=kwargs["github_step_summary"],
        workspace=kwargs["github_workspace"],
        run_id=int(kwargs["github_run_id"]) if kwargs.get("github_run_id") else None,
        run_attempt=(
            int(kwargs["github_run_attempt"])
            if kwargs.get("github_run_attempt")
            else None
        ),
        head_sha=kwargs["github_head_sha"] if kwargs.get("github_head_sha") else None,
        repository=kwargs["github_repository"],
        repo_full_name=github_event["repository"]["full_name"],
        pull_request_link=(
            github_event["pull_request"]["html_url"]
            if github_event_name == "pull_request"
            else None
        ),
    )


def _load_base64_json(
    ctx: click.Context,  # pylint: disable=unused-argument
    param: click.Option,  # pylint: disable=unused-argument
    value: Optional[str],
) -> Optional[dict]:
    """Decode a base64 encoded JSON string."""
    return None if value is None else decode_base64_to_json(value)


def _safe_encode_base64_json(value: Optional[dict]) -> str:
    """Encode a JSON object to a base64 string."""
    return encode_json_to_base64(value)


@dataclass
class ParamNameWithOption:
    """Dataclass to hold the name and option for a parameter."""

    option: Callable[[Callable], click.Option]
    convert_to_argument: Callable[[S], T] = lambda x: x

    @functools.cached_property
    def name(self) -> str:
        """Get the name of the parameter from the option."""
        return self.option(lambda: True).__click_params__[0].name

    @functools.cached_property
    def envvar(self) -> str:
        """Get the environment variable name of the parameter from the option."""
        return self.option(lambda: True).__click_params__[0].envvar

    def extract_from_kwargs(self, kwargs: dict) -> Optional[Any]:
        """Extract the value from the kwargs."""
        return kwargs.get(self.name)

    def set_as_envvar_if_none(self, kwargs: dict, value: S):
        """Set the value as an environment variable if it does not exist in kwargs."""
        if kwargs.get(self.name) is None:
            os.environ[self.envvar] = self.convert_to_argument(value)


TEAMS_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--teams-minimal-schema",
        envvar="TEAMS_MINIMAL_SCHEMA",
        show_envvar=True,
        default=None,
        help=(
            "The minimal schema that opendapi generate should use in "
            "constructing a skeleton teams file, as a base64 encoded JSON"
        ),
        callback=_load_base64_json,
    ),
    convert_to_argument=_safe_encode_base64_json,
)

DATASTORES_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--datastores-minimal-schema",
        envvar="DATASTORES_MINIMAL_SCHEMA",
        show_envvar=True,
        default=None,
        help=(
            "The minimal schema that opendapi generate should use in "
            "constructing a skeleton datastores file, as a base64 encoded JSON"
        ),
        callback=_load_base64_json,
    ),
    convert_to_argument=_safe_encode_base64_json,
)

PURPOSES_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--purposes-minimal-schema",
        envvar="PURPOSES_MINIMAL_SCHEMA",
        show_envvar=True,
        default=None,
        help=(
            "The minimal schema that opendapi generate should use in "
            "constructing a skeleton purposes file, as a base64 encoded JSON"
        ),
        callback=_load_base64_json,
    ),
    convert_to_argument=_safe_encode_base64_json,
)

DAPI_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--dapi-minimal-schema",
        envvar="DAPI_MINIMAL_SCHEMA",
        show_envvar=True,
        default=None,
        help=(
            "The minimal schema that opendapi generate should use in "
            "constructing a skeleton dapi files, as a base64 encoded JSON"
        ),
        callback=_load_base64_json,
    ),
    convert_to_argument=_safe_encode_base64_json,
)

SUBJECTS_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--subjects-minimal-schema",
        envvar="SUBJECTS_MINIMAL_SCHEMA",
        show_envvar=True,
        default=None,
        help=(
            "The minimal schema that opendapi generate should use in "
            "constructing a skeleton subject files, as a base64 encoded JSON"
        ),
        callback=_load_base64_json,
    ),
    convert_to_argument=_safe_encode_base64_json,
)

CATEGORIES_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--categories-minimal-schema",
        envvar="CATEGORIES_MINIMAL_SCHEMA",
        show_envvar=True,
        default=None,
        help=(
            "The minimal schema that opendapi generate should use in "
            "constructing a skeleton categories files, as a base64 encoded JSON"
        ),
        callback=_load_base64_json,
    ),
    convert_to_argument=_safe_encode_base64_json,
)


def minimal_schema_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the minimal schema."""
    for option in (
        CATEGORIES_PARAM_NAME_WITH_OPTION.option,
        DAPI_PARAM_NAME_WITH_OPTION.option,
        DATASTORES_PARAM_NAME_WITH_OPTION.option,
        PURPOSES_PARAM_NAME_WITH_OPTION.option,
        SUBJECTS_PARAM_NAME_WITH_OPTION.option,
        TEAMS_PARAM_NAME_WITH_OPTION.option,
        click.option(
            "--skip-server-minimal-schemas",
            envvar="SKIP_SERVER_MINIMAL_SCHEMAS",
            show_envvar=True,
            is_flag=True,
            default=False,
            help="Do not require minimal schemas for the DAPI files",
        ),
    ):
        func = option(func)
    return func


def features_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for features."""
    for option in (
        click.option(
            "--feature-to-status",
            envvar="FEATURE_TO_STATUS",
            show_envvar=True,
            default=None,
            help="Base64 encoded JSON of features to their status",
            callback=_load_base64_json,
        ),
    ):
        func = option(func)
    return func


def dev_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for most commands."""
    options = [
        click.option(
            "--local-spec-path",
            default=None,
            envvar="LOCAL_SPEC_PATH",
            help="Use specs in the local path instead of the DAPI server",
            show_envvar=False,
        ),
        click.option(
            "--always-write-generated-dapis",
            is_flag=True,
            default=False,
            envvar="ALWAYS_WRITE_GENERATED_DAPIS",
            help="Write the generated dapis even if they have not changed",
            show_envvar=False,
        ),
    ]
    for option in reversed(options):
        func = option(func)
    return func


def dapi_server_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the dapi server commands."""
    options = [
        click.option(
            "--dapi-server-host",
            envvar="DAPI_SERVER_HOST",
            show_envvar=True,
            default="https://api.wovencollab.com",
            help="The host of the DAPI server",
        ),
        click.option(
            "--dapi-server-api-key",
            envvar="DAPI_SERVER_API_KEY",
            show_envvar=True,
            help="The API key for the DAPI server",
        ),
    ]
    for option in reversed(options):
        func = option(func)
    return func


BASE_COMMIT_SHA_PARAM_NAME_WITH_OPTION = ParamNameWithOption(
    option=click.option(
        "--base-commit-sha",
        envvar="BASE_COMMIT_SHA",
        show_envvar=True,
        default=None,
        help="The SHA of the base commit",
    )
)


def git_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the git commands."""
    for option in (BASE_COMMIT_SHA_PARAM_NAME_WITH_OPTION.option,):
        func = option(func)
    return func


def github_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the enrich command."""
    options = [
        click.option(
            "--github-event-name",
            type=click.Choice(
                ["push", "pull_request", "schedule", "workflow_dispatch"],
                case_sensitive=True,
            ),
            envvar="GITHUB_EVENT_NAME",
            show_envvar=False,
        ),
        click.option(
            "--github-run-attempt",
            envvar="GITHUB_RUN_ATTEMPT",
            show_envvar=False,
        ),
        click.option(
            "--github-run-id",
            envvar="GITHUB_RUN_ID",
            show_envvar=False,
        ),
        click.option(
            "--github-head-sha",
            envvar="GITHUB_HEAD_SHA",
            show_envvar=False,
        ),
        click.option(
            "--github-repository",
            envvar="GITHUB_REPOSITORY",
            show_envvar=False,
        ),
        click.option(
            "--github-workspace",
            envvar="GITHUB_WORKSPACE",
            show_envvar=False,
        ),
        click.option(
            "--github-step-summary",
            envvar="GITHUB_STEP_SUMMARY",
            show_envvar=False,
        ),
        click.option(
            "--github-event-path",
            envvar="GITHUB_EVENT_PATH",
            show_envvar=False,
        ),
        click.option("--github-token", envvar="GITHUB_TOKEN", show_envvar=False),
    ]
    for option in reversed(options):
        func = option(func)
    return func


def opendapi_run_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the client commands for debugging."""
    options = [
        click.option(
            "--mainline-branch-name",
            default="main",
            envvar="MAINLINE_BRANCH_NAME",
            show_envvar=True,
            help="The name of the mainline branch to compare against",
        ),
        click.option(
            "--enrich-batch-size",
            default=5,
            envvar="ENRICH_BATCH_SIZE",
            help="Batch size for validating and enriching DAPI files",
            show_envvar=False,
        ),
        click.option(
            "--register-batch-size",
            default=30,
            envvar="REGISTER_BATCH_SIZE",
            help="Batch size for validating and enriching DAPI files",
            show_envvar=False,
        ),
        click.option(
            "--analyze-impact-batch-size",
            default=15,
            envvar="ANALYZE_IMPACT_BATCH_SIZE",
            help="Batch size for analyzing impact of DAPI files",
            show_envvar=False,
        ),
        click.option(
            "--pr-sync-batch-size",
            default=5,
            envvar="PR_SYNC_BATCH_SIZE",
            help="Batch size for syncing PR and DAPI files",
            show_envvar=False,
        ),
        click.option(
            "--feature-validate-dapi-batch-size",
            default=5,
            envvar="FEATURE_VALIDATE_DAPI_BATCH_SIZE",
            help="Batch size for validating DAPI files for features",
            show_envvar=False,
        ),
        click.option(
            "--suggest-changes",
            is_flag=True,
            default=True,
            envvar="SUGGEST_CHANGES",
            show_envvar=True,
            help="Suggest changes to the DAPI files",
        ),
        click.option(
            "--revalidate-all-files",
            is_flag=True,
            default=False,
            envvar="REVALIDATE_ALL_FILES",
            help="Revalidate all files, not just the ones that have changed",
            show_envvar=True,
        ),
        click.option(
            "--require-committed-changes",
            is_flag=True,
            default=False,
            envvar="REQUIRE_COMMITTED_CHANGES",
            help="Do not Overwrite uncommitted DAPI files with server suggestions",
            show_envvar=True,
        ),
        click.option(
            "--ignore-suggestions-cache",
            is_flag=True,
            default=False,
            envvar="IGNORE_SUGGESTIONS_CACHE",
            help="Ignore suggestions cache and fetch fresh suggestions",
            show_envvar=False,
        ),
        click.option(
            "--register-on-merge-to-mainline",
            is_flag=True,
            default=True,
            envvar="REGISTER_ON_MERGE_TO_MAINLINE",
            help="Register DAPI files on merge to mainline branch",
            show_envvar=False,
        ),
        click.option(
            "--woven-integration-mode",
            type=click.Choice(["shadow", "active", "disabled"], case_sensitive=True),
            default="active",
            envvar="WOVEN_INTEGRATION_MODE",
            help="Woven Integration Mode",
            show_envvar=False,
        ),
        click.option(
            "--woven-configuration",
            type=click.Choice(["done", "in_progress"], case_sensitive=True),
            default="done",
            envvar="WOVEN_CONFIGURATION",
            help="Is Woven's configuration done or in progress",
            show_envvar=False,
        ),
        click.option(
            "--skip-client-config",
            is_flag=True,
            default=False,
            envvar="SKIP_CLIENT_CONFIG",
            help="Skip fetching client config from the server",
            show_envvar=False,
        ),
    ]
    for option in reversed(options):
        func = option(func)
    return func


def third_party_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the third-party integrations."""
    options = [
        click.option(
            "--dbt-cloud-url",
            envvar="DAPI_DBT_CLOUD_URL",
            show_envvar=True,
            help="The host of the dbt Cloud integration",
        ),
        click.option(
            "--dbt-cloud-api-key",
            envvar="DAPI_DBT_CLOUD_API_KEY",
            show_envvar=True,
            help="The API key for the dbt cloud integration",
        ),
        click.option(
            "--dbt-cloud-retry-count",
            envvar="DAPI_DBT_CLOUD_RETRY_COUNT",
            show_envvar=True,
            help="The retry count for dbt cloud integration",
        ),
        click.option(
            "--dbt-cloud-retry-interval",
            envvar="DAPI_DBT_CLOUD_RETRY_INTERVAL",
            show_envvar=True,
            help="The retry interval for dbt cloud integration",
        ),
    ]
    for option in reversed(options):
        func = option(func)
    return func
