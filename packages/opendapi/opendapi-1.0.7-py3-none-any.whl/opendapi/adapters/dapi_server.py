# pylint: disable=too-many-instance-attributes, too-many-locals, broad-exception-caught
""""Adapter to interact with the DAPI Server."""
from __future__ import annotations

import itertools
import time
from collections import defaultdict
from dataclasses import dataclass, field, fields
from enum import Enum
from importlib.metadata import version
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type
from urllib.parse import urljoin

import requests
from deepmerge import always_merger
from requests.adapters import HTTPAdapter
from snakemd import Document as MDDocument
from urllib3.util.retry import Retry

from opendapi.adapters.file import OpenDAPIFileContents
from opendapi.adapters.git import ChangeTriggerEvent
from opendapi.cli.common import OpenDAPIEntity, Schemas
from opendapi.config import OpenDAPIConfig
from opendapi.defs import HTTPMethod
from opendapi.features import Feature, FeatureStatus, load_from_raw_dict
from opendapi.logging import (
    LogCounterKey,
    LogDistKey,
    Timer,
    increment_counter,
    sentry_sdk,
)
from opendapi.utils import make_api_w_query_and_body

TOTAL_RETRIES = 5
RETRY_BACKOFF_FACTOR = 10


def _simple_iter_chunks(data, size=1):
    """Helper for chunking data into lists of size `size`."""
    iterator = iter(data)
    for _ in range(0, len(data), size):
        yield list(itertools.islice(iterator, size))


def _chunks(data, size=1):
    """Helper for splicing a dictionary into smaller dictionaries of size `size`."""
    iterator = iter(data)
    for _ in range(0, len(data), size):
        yield {k: data[k] for k in itertools.islice(iterator, size)}


@dataclass
class DAPIServerConfig:
    """Configuration for the DAPI Server."""

    server_host: str
    api_key: str
    mainline_branch_name: str
    register_on_merge_to_mainline: bool = True
    suggest_changes: bool = True
    enrich_batch_size: int = 5
    ignore_suggestions_cache: bool = False
    # we do impact related analysis at register,
    # so make this match analyze_impact_batch_size
    register_batch_size: int = 15
    analyze_impact_batch_size: int = 15
    pr_sync_batch_size: int = 5
    revalidate_all_files: bool = False
    require_committed_changes: bool = False
    woven_integration_mode: str = None
    woven_configuration: str = None
    feature_validate_dapi_batch_size: int = 5

    @property
    def is_repo_in_shadow_mode(self) -> bool:
        """Check if the repo is marked as active."""
        return self.woven_integration_mode == "shadow"

    @property
    def is_repo_onboarded(self) -> bool:
        """Check if the repo is onboarded."""
        return self.woven_integration_mode == "active"

    @property
    def repo_being_configured(self) -> bool:
        """Check if the repo is configured."""
        return self.woven_configuration == "in_progress"


@dataclass
class DAPIServerMeta:
    """Metadata about the DAPI server"""

    name: str
    url: str
    github_user_name: str
    github_user_email: str
    logo_url: Optional[str] = None
    suggestions_cta_url: Optional[str] = None
    www_url: Optional[str] = None
    portal_url: Optional[str] = None


class DAPIServerRequestType(Enum):
    """Enum for DAPI Server Request Types."""

    SERVER_META = "/v1/registry/meta"
    CLIENT_CONFIG = "/v1/config/client/opendapi"
    CLIENT_FEATURE_FLAGS = "/v1/config/client/opendapi/feature_flags"
    VALIDATE = "/v1/registry/validate"
    REGISTER = "/v1/registry/register"
    UNREGISTER = "/v1/registry/unregister"
    ANALYZE_IMPACT = "/v1/registry/impact"
    FEATURES = "/v1/github/repo/features"
    PERSIST_PR_ENTITIES = "/v1/github/pull-requests/entities"
    GET_PR = "/v1/github/pull-requests"
    UPSERT_PR = "/v1/github/pull-requests/upsert"
    VALIDATE_FEATURES = "/v1/cicd/features/validate"
    NOTIFY = "/v1/registry/notify"


@dataclass
class PersistedPullRequestEntity:
    """
    A PullRequestEntity that was persisted and associated with a PR
    in the DAPI server
    """

    pr_link: str
    id: str
    filepath: str
    previous_content: Optional[dict]
    content_state_at_base: Optional[dict]
    new_blob_sha: str
    new_content: Dict
    new_generated_by: str
    entity: OpenDAPIEntity
    changed_from_current: bool
    commit_data: str
    actions: List[Action] = field(default_factory=list)

    def get_metadata_for_upsert(self) -> dict:
        """Get the metadata for the upsert request."""
        return {
            "id": self.id,
            "commit_data": self.commit_data,
        }

    @staticmethod
    def _convert(key: str, val: Any) -> Any:
        if key == "entity":
            return OpenDAPIEntity(val)
        if key == "actions":
            return [Action.create_from_dapi_server(action) for action in val]
        return val

    @classmethod
    def create_from_dapi_server(cls, kwargs: Dict) -> PersistedPullRequestEntity:
        """Create a PersistedPullRequestEntity from the DAPI server response."""
        # the Dapi Server uses a property to set `is_new`, amongst others. therefore
        # only instantiate with the fields that are actually defined on the dataclass
        # if a value does not exist then keyerror is appropriate, as none have defaults
        return cls(
            **{
                field.name: cls._convert(field.name, kwargs[field.name])
                for field in fields(cls)
                if field.name in kwargs
            }
        )


@dataclass
class PersistedGithubPullRequest:
    """A GithubPullRequest that was persisted to the DAPI server."""

    repo_name: str
    number: int
    link: str
    woven_comment_id: Optional[int]
    branch: str
    branch_head_commit_sha: str
    base_commit_sha: str
    head_commit_sha: str
    pull_request_entity_ids: Set[str]
    state: str
    title: str

    @classmethod
    def create_from_dapi_server(cls, kwargs: Dict) -> PersistedGithubPullRequest:
        """Create a PersistedGithubPullRequest from the DAPI server response."""
        return cls(
            **{
                field.name: kwargs[field.name]
                for field in fields(cls)
                if field.name in kwargs
            }
        )


@dataclass
class RepoFeaturesInfo:
    """Information about the features in a repo."""

    feature_to_status: Dict[Feature, FeatureStatus]
    enabled_schemas: Schemas
    enabled_and_pilot_schemas: Schemas


@dataclass(eq=True, frozen=True)
class Action:
    """Actions from Features"""

    entity: OpenDAPIEntity
    filepath: str
    # tuple necessary to be hashable
    path: Tuple[str | int]
    action: str

    def __lt__(self, other: Action) -> bool:
        """Sort by filepath and then by path."""
        if self.filepath != other.filepath:
            raise ValueError("Cannot compare actions with different filepaths")

        try:
            return self.path < other.path
        except TypeError:
            return [x for x in self.path if not isinstance(x, int)] < [
                x for x in other.path if not isinstance(x, int)
            ]

    @staticmethod
    def _convert(key: str, val: Any) -> Any:
        if key == "entity":
            return OpenDAPIEntity(val)
        if key == "path":
            return tuple(val)
        return val

    @classmethod
    def create_from_dapi_server(cls, kwargs: Dict) -> Action:
        """Create a Action from the DAPI server response."""
        return cls(
            **{
                field.name: cls._convert(field.name, kwargs[field.name])
                for field in fields(cls)
            }
        )

    @property
    def compiled_markdown(self) -> str:
        """Get the compiled markdown."""
        # list looks better upon printing
        return f"- {list(self.path)}: {self.action}"

    @property
    def as_dict(self) -> dict:
        """Convert to dict."""
        return {
            "entity": self.entity.value,
            "filepath": self.filepath,
            "path": list(self.path),
            "action": self.action,
        }


@dataclass
class FeatureValidationResult:
    """Response from the DAPI server for validating features"""

    feature: Feature
    actions: List[Action]
    passed: bool

    @classmethod
    def create_from_dapi_server(
        cls,
        feature_id_str: str,
        raw_actions: List[Dict],
        passed: bool,
    ) -> FeatureValidationResult:
        """Create a FeatureValidationResult from the DAPI server response."""
        return cls(
            feature=Feature(feature_id_str),
            actions=[Action.create_from_dapi_server(action) for action in raw_actions],
            passed=passed,
        )

    @property
    def compiled_markdown(self) -> str:
        """Get the compiled markdown."""
        md = f"### {self.feature.value}:\n"

        actions_by_filepath = defaultdict(list)
        for action in self.actions:
            actions_by_filepath[action.filepath].append(action)

        for filepath in sorted(actions_by_filepath.keys()):
            md += f"#### {filepath}\n"
            for action in sorted(actions_by_filepath[filepath]):
                md += f"{action.compiled_markdown}\n"

        return md


@dataclass
class DAPIChangeNotification:
    """Metadata required to send notifications about changes in DAPIs"""

    created_dapis: Set[str] = field(default_factory=set)
    updated_dapis: Set[str] = field(default_factory=set)
    deprecated_dapis: Set[str] = field(default_factory=set)
    created_models: Set[str] = field(default_factory=set)
    updated_models: Set[str] = field(default_factory=set)
    deleted_models: Set[str] = field(default_factory=set)
    impacted_tables: Dict[str, Set[str]] = field(default_factory=dict)

    def as_json(self) -> dict:
        """Convert to json."""
        return {
            "created_dapis": list(self.created_dapis),
            "updated_dapis": list(self.updated_dapis),
            "deprecated_dapis": list(self.deprecated_dapis),
            "created_models": list(self.created_models),
            "updated_models": list(self.updated_models),
            "deleted_models": list(self.deleted_models),
            "impacted_tables": {
                urn: list(tables) for urn, tables in self.impacted_tables.items()
            },
        }

    def merge(self, other: Optional[DAPIChangeNotification]) -> DAPIChangeNotification:
        """Combine two notifications."""
        if not other:
            return self

        total_impacted_tables = defaultdict(set)
        for impacted_tables in (self.impacted_tables, other.impacted_tables):
            for location, tables in impacted_tables.items():
                total_impacted_tables[location] |= tables

        return DAPIChangeNotification(
            created_dapis=self.created_dapis | other.created_dapis,
            updated_dapis=self.updated_dapis | other.updated_dapis,
            deprecated_dapis=self.deprecated_dapis | other.deprecated_dapis,
            created_models=self.created_models | other.created_models,
            updated_models=self.updated_models | other.updated_models,
            deleted_models=self.deleted_models | other.deleted_models,
            impacted_tables=total_impacted_tables,
        )

    @classmethod
    def safe_merge(
        cls,
        first: Optional[DAPIChangeNotification],
        second: Optional[DAPIChangeNotification],
    ) -> Optional[DAPIChangeNotification]:
        """Merge two notifications."""
        if not first:
            return second
        return first.merge(second)

    @staticmethod
    def _convert(key: str, val: Any) -> Any:
        if key == "impacted_tables":
            return {k: set(v) for k, v in val.items()}
        elif key in (
            "created_dapis",
            "updated_dapis",
            "deprecated_dapis",
            "created_models",
            "updated_models",
            "deleted_models",
        ):
            return set(val)
        return val

    @classmethod
    def create_from_dapi_server(cls, kwargs: Dict) -> DAPIChangeNotification:
        """Create a DAPIChangeNotification from the DAPI server response."""
        return cls(
            **{
                field.name: cls._convert(field.name, kwargs[field.name])
                for field in fields(cls)
                if field.name in kwargs
            }
        )


@dataclass
class DAPIServerResponse:
    """DAPI server Response formatted"""

    request_type: DAPIServerRequestType
    status_code: int
    server_meta: DAPIServerMeta
    suggestions: Optional[dict] = None
    info: Optional[dict] = None
    errors: Optional[dict] = None
    text: Optional[str] = None
    markdown: Optional[str] = None
    dapi_change_notification: Optional[DAPIChangeNotification] = None

    @property
    def error(self) -> bool:
        """Check if there is an error in the response."""
        return self.errors is not None and len(self.errors) > 0

    @property
    def compiled_markdown(self) -> str:
        """Get the compiled markdown."""
        if (
            self.request_type is DAPIServerRequestType.ANALYZE_IMPACT
            and self.info
            and len(self.info)
        ):
            impact_md = MDDocument()
            impact_md.add_heading(":exclamation: Impact analysis", 2)
            impact_md.add_paragraph(
                "The schema change in this PR might impact an analytics use case. "
                "Please reach out to affected users.\n"
            )
            impact_md.add_table(
                header=[
                    "Dataset",
                    "Datastore",
                    "Impacted Users",
                    "Impacted Tables",
                ],
                data=[
                    [
                        dapi_urn,
                        datastore_urn,
                        (
                            f":warning: <b>{len(compiled_impact['impacted_users'])} users</b>"
                            f"<br>{', '.join(compiled_impact['impacted_users'])}"
                            if compiled_impact["impacted_users"]
                            else ":white_check_mark: No users"
                        ),
                        (
                            f":warning: <b>{len(compiled_impact['impacted_tables'])} tables</b>"
                            f"<br>{', '.join(compiled_impact['impacted_tables'])}"
                            if compiled_impact["impacted_tables"]
                            else ":white_check_mark: No tables"
                        ),
                    ]
                    for dapi_urn, datastore_impact in self.info.items()
                    for datastore_urn, compiled_impact in datastore_impact.items()
                ],
            )
            return str(impact_md)
        return self.markdown

    @property
    def compiled_text(self) -> str:
        """Get the compiled text."""
        return self.text

    def merge(self, other: "DAPIServerResponse") -> "DAPIServerResponse":
        """Merge two responses."""

        def merge_text_fn(this_text, other_text):
            if not this_text or not other_text:
                return other_text or this_text

            return (
                "\n\n".join([this_text, other_text])
                if this_text != other_text
                else other_text
            )

        def merge_dict(this_dict, other_dict):
            if not this_dict or not other_dict:
                return other_dict or this_dict

            return always_merger.merge(this_dict, other_dict)

        if self.request_type != other.request_type:
            raise ValueError(
                f"Cannot merge responses of different types: {self.request_type} and {other.request_type}"
            )

        return DAPIServerResponse(
            request_type=other.request_type or self.request_type,
            status_code=other.status_code or self.status_code,
            server_meta=other.server_meta or self.server_meta,
            errors=merge_dict(self.errors, other.errors),
            suggestions=merge_dict(self.suggestions, other.suggestions),
            info=merge_dict(self.info, other.info),
            text=merge_text_fn(self.text, other.text),
            markdown=merge_text_fn(self.markdown, other.markdown),
            dapi_change_notification=DAPIChangeNotification.safe_merge(
                self.dapi_change_notification, other.dapi_change_notification
            ),
        )


class DAPIRequests:
    """Class to handle requests to the DAPI Server."""

    def __init__(
        self,
        dapi_server_config: DAPIServerConfig,
        trigger_event: ChangeTriggerEvent,
        opendapi_config: Optional[OpenDAPIConfig] = None,
        error_msg_handler: Optional[Callable[[str], None]] = None,
        error_exception_cls: Optional[Type[Exception]] = None,
        txt_msg_handler: Optional[Callable[[str], None]] = None,
        markdown_msg_handler: Optional[Callable[[str], None]] = None,
    ):  # pylint: disable=too-many-arguments
        self.dapi_server_config = dapi_server_config
        self.opendapi_config = opendapi_config
        self.trigger_event = trigger_event
        self.error_msg_handler = error_msg_handler
        self.error_exception_cls = error_exception_cls or Exception
        self.txt_msg_handler = txt_msg_handler
        self.markdown_msg_handler = markdown_msg_handler

        self.session = requests.Session()
        # Add retry once after 60s for 500, 502, 503, 504
        # This is to handle the case where the server is starting up
        # or when any AI per-minute token limits are hit
        kwargs = {
            "total": TOTAL_RETRIES,
            "backoff_factor": RETRY_BACKOFF_FACTOR,
            "status_forcelist": [500, 502, 503, 504],
            "allowed_methods": ["POST"],
        }

        # Add some more options for urllib3 2.0.0 and above
        urllib3_version = version("urllib3").split(".")
        if int(urllib3_version[0]) >= 2:  # pragma: no cover
            kwargs.update(
                {
                    "backoff_jitter": 15,
                    "backoff_max": 360,  # Default is 120
                }
            )

        retries = Retry(**kwargs)
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    @staticmethod
    def _construct_schemas_from_dict(schemas_dict: dict) -> Schemas:
        """Construct Schemas from a dictionary."""
        return Schemas(
            teams=schemas_dict.get("teams"),
            datastores=schemas_dict.get("datastores"),
            purposes=schemas_dict.get("purposes"),
            dapi=schemas_dict.get("dapi"),
            subjects=schemas_dict.get("subjects"),
            categories=schemas_dict.get("categories"),
        )

    def get_repo_features_info_from_server(self) -> RepoFeaturesInfo:
        """Get the config from the DAPI Server."""
        response, _ = self.raw_send_request_to_dapi_server(
            request_path=DAPIServerRequestType.FEATURES.value,
            method=HTTPMethod.GET,
            query_params={"repo_name": self.trigger_event.repo_full_name},
        )
        response.raise_for_status()
        json_response = response.json()

        enabled_schemas = self._construct_schemas_from_dict(
            json_response.get("enabled_schemas", {})
        )
        enabled_and_pilot_schemas = self._construct_schemas_from_dict(
            json_response.get("enabled_and_pilot_schemas", {})
        )

        raw_features_to_status = {
            feature: info["status"]
            for feature, info in json_response.get("features", {}).items()
        }
        feature_to_status = load_from_raw_dict(raw_features_to_status)

        return RepoFeaturesInfo(
            feature_to_status=feature_to_status,
            enabled_schemas=enabled_schemas,
            enabled_and_pilot_schemas=enabled_and_pilot_schemas,
        )

    def get_client_config_from_server(self) -> dict:
        """Get the config from the DAPI Server."""
        response, _ = self.raw_send_request_to_dapi_server(
            request_path=DAPIServerRequestType.CLIENT_CONFIG.value,
            method=HTTPMethod.GET,
        )
        response.raise_for_status()
        return response.json()

    def get_client_feature_flags_from_server(
        self,
        feature_flag_names: List[str],
    ) -> dict:
        """Get the feature flags from the DAPI Server."""
        response, _ = self.raw_send_request_to_dapi_server(
            request_path=DAPIServerRequestType.CLIENT_FEATURE_FLAGS.value,
            method=HTTPMethod.POST,
            query_params=None,
            body_json={
                "feature_flag_names": feature_flag_names,
                "client_context": self.build_client_context(
                    self.dapi_server_config, self.trigger_event
                ),
            },
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def build_client_context(
        dapi_server_config: DAPIServerConfig,
        trigger_event: ChangeTriggerEvent,
    ) -> dict:
        """Build the client context."""
        return {
            "meta": {
                "type": "opendapi",
                "version": f"opendapi-{version('opendapi')}",
                "integration_mode": dapi_server_config.woven_integration_mode,
                "repo_being_configured": dapi_server_config.repo_being_configured,
            },
            "change_trigger_event": {
                "source": trigger_event.integration_type,
                "repository": trigger_event.repo_full_name,
                "where": trigger_event.where,
                "event_type": trigger_event.event_type,
                "before_change_sha": trigger_event.before_change_sha,
                "after_change_sha": trigger_event.after_change_sha,
                "repo_html_url": trigger_event.repo_html_url,
                "pull_request_number": trigger_event.pull_request_number,
                "pull_request_link": trigger_event.pull_request_link,
            },
        }

    def handle_server_message(self, resp, should_print: bool = True) -> None:
        """Handle a message from the server."""
        # Show the messages
        message = resp.json()
        status_code = resp.status_code
        if message.get("errors"):
            sentry_sdk.capture_message(
                f"There were errors: {message.get('errors')}",
                level="error",
                tags={
                    "request_path": message.get("request_path"),
                    "response_status": status_code,
                    "org_name": self.opendapi_config
                    and self.opendapi_config.org_name_snakecase,
                },
            )
            if self.error_msg_handler:
                self.error_msg_handler(f"There were errors: {message.get('errors')}")

        if should_print:
            if message.get("md") and self.markdown_msg_handler:
                self.markdown_msg_handler(
                    f'<br>{message.get("md", message.get("text"))}'
                )

            if message.get("text") and self.txt_msg_handler:
                self.txt_msg_handler(f'\n{message.get("text")}')

    def raw_send_request_to_dapi_server(
        self,
        request_path: str,
        method: HTTPMethod,
        query_params: Optional[dict] = None,
        body_json: Optional[dict] = None,
    ) -> Tuple[requests.Response, Dict]:
        headers = {
            "Content-Type": "application/json",
            "X-DAPI-Server-API-Key": self.dapi_server_config.api_key,
        }
        # measure the time it takes to get a response from the server in milliseconds
        metrics_tags = {
            "request_path": request_path,
            "org_name": self.opendapi_config
            and self.opendapi_config.org_name_snakecase,
        }

        with Timer(LogDistKey.ASK_DAPI_SERVER) as _timer:
            response, _ = make_api_w_query_and_body(
                urljoin(self.dapi_server_config.server_host, request_path),
                headers=headers,
                query_params=query_params,
                body_json=body_json,
                method=method,
                timeout=60,
                req_session=self.session,
            )
            metrics_tags["status_code"] = response.status_code
            _timer.set_tags(metrics_tags)

        return response, metrics_tags

    def _handle_api_error(self, request_path: str, status_code: int) -> None:
        """Handle an error message."""
        msg = f"Something went wrong! API failure with {status_code} for {request_path}"
        if self.error_msg_handler:
            self.error_msg_handler(msg)
        raise self.error_exception_cls(msg)

    def ask_dapi_server(
        self,
        request_type: DAPIServerRequestType,
        payload: dict,
        request_method: HTTPMethod = HTTPMethod.POST,
        print_txt_markdown: bool = True,
    ) -> DAPIServerResponse:
        """Ask the DAPI Server for something."""
        request_path = request_type.value
        if request_method == HTTPMethod.POST:
            payload["client_context"] = self.build_client_context(
                self.dapi_server_config, self.trigger_event
            )
        response, metrics_tags = self.raw_send_request_to_dapi_server(
            request_path=request_path,
            body_json=payload,
            method=request_method,
        )
        for payload_type in [
            "teams",
            "datastores",
            "purposes",
            "dapis",
            "subjects",
            "categories",
        ]:
            if payload_type in payload:
                increment_counter(
                    key=LogCounterKey.ASK_DAPI_SERVER_PAYLOAD_ITEMS,
                    value=len(payload[payload_type]),
                    tags=always_merger.merge(
                        metrics_tags, {"payload_type": payload_type}
                    ),
                )
        # Server responds with a detailed error on 400, so only error when status > 400
        if response.status_code > 400:
            self._handle_api_error(request_path, response.status_code)

        message = response.json()

        server_meta = message.get("server_meta", {})

        self.handle_server_message(
            response, (print_txt_markdown or response.status_code >= 400)
        )

        return DAPIServerResponse(
            request_type=request_type,
            status_code=response.status_code,
            server_meta=DAPIServerMeta(
                name=server_meta.get("name", "DAPI Server"),
                url=server_meta.get("url", "https://opendapi.org"),
                github_user_name=server_meta.get("github_user_name", "github-actions"),
                github_user_email=server_meta.get(
                    "github_user_email", "github-actions@github.com"
                ),
                logo_url=server_meta.get("logo_url"),
                suggestions_cta_url=server_meta.get("suggestions_cta_url"),
                www_url=server_meta.get("www_url"),
                portal_url=server_meta.get("portal_url"),
            ),
            errors=message.get("errors"),
            suggestions=message.get("suggestions"),
            info=message.get("info"),
            markdown=message.get("md"),
            text=message.get("text"),
            dapi_change_notification=(
                DAPIChangeNotification.create_from_dapi_server(dcn)
                if (dcn := message.get("dapi_change_notification")) is not None
                else None
            ),
        )

    def get_dapi_server_meta(self) -> DAPIServerMeta:
        """Get the DAPI Server metadata."""
        return self.ask_dapi_server(
            DAPIServerRequestType.SERVER_META, {}, request_method=HTTPMethod.GET
        ).server_meta

    def validate(
        self,
        all_files: OpenDAPIFileContents,
        changed_files: OpenDAPIFileContents,
        commit_hash: str,
        suggest_changes_override: Optional[bool] = None,
        ignore_suggestions_cache: bool = False,
        notify_function: Optional[Callable[[int], None]] = None,
        minimal_schemas_for_validation: Optional[Schemas] = None,
    ) -> DAPIServerResponse:
        """Validate OpenDAPI files with the DAPI Server."""
        all_files = all_files.for_server()
        changed_files = changed_files.for_server()
        chunk_size = self.dapi_server_config.enrich_batch_size
        suggest_changes = (
            self.dapi_server_config.suggest_changes
            if suggest_changes_override is None
            else suggest_changes_override
        )

        def _build_validate_payload(
            updates: dict, include_minimal_schemas: bool
        ) -> dict:
            return {
                "dapis": {},
                "teams": {},
                "datastores": {},
                "purposes": {},
                "subjects": {},
                "categories": {},
                "suggest_changes": suggest_changes,
                "commit_hash": commit_hash,
                "ignore_suggestions_cache": ignore_suggestions_cache,
                "additional_schemas": (
                    minimal_schemas_for_validation.as_dict
                    if (minimal_schemas_for_validation and include_minimal_schemas)
                    else {}
                ),
                **updates,
            }

        # First, we validate the non-dapi files
        # all files just schema validation, no additional validation
        payload = _build_validate_payload(
            {
                "teams": all_files["teams"],
                "datastores": all_files["datastores"],
                "purposes": all_files["purposes"],
                "subjects": all_files["subjects"],
                "categories": all_files["categories"],
            },
            include_minimal_schemas=False,
        )
        resp = self.ask_dapi_server(
            DAPIServerRequestType.VALIDATE,
            payload,
            request_method=HTTPMethod.POST,
            print_txt_markdown=False,
        )

        # then we validate the changed non-dapi files with the additional schemas
        payload = _build_validate_payload(
            {
                "teams": changed_files["teams"],
                "datastores": changed_files["datastores"],
                "purposes": changed_files["purposes"],
                "subjects": changed_files["subjects"],
                "categories": changed_files["categories"],
            },
            include_minimal_schemas=True,
        )
        resp = resp.merge(
            self.ask_dapi_server(
                DAPIServerRequestType.VALIDATE,
                payload,
                request_method=HTTPMethod.POST,
                print_txt_markdown=False,
            )
        )

        # Then we validate the changed dapi files in batches, with additional schema validation
        for dapi_chunk in _chunks(changed_files["dapis"], chunk_size):
            for dapi_loc in dapi_chunk:
                all_files["dapis"].pop(dapi_loc, None)
            try:
                payload = _build_validate_payload(
                    {"dapis": dapi_chunk}, include_minimal_schemas=True
                )
                this_resp = self.ask_dapi_server(
                    DAPIServerRequestType.VALIDATE, payload, print_txt_markdown=False
                )
                resp = resp.merge(this_resp)
            except self.error_exception_cls:
                # In case of errors (likely from AI timeouts), validate one by one
                # but first sleep for RETRY_BACKOFF_FACTOR to give the server time to recover
                time.sleep(RETRY_BACKOFF_FACTOR)
                for loc, item in dapi_chunk.items():
                    payload = _build_validate_payload(
                        {"dapis": {loc: item}}, include_minimal_schemas=True
                    )
                    this_resp = self.ask_dapi_server(
                        DAPIServerRequestType.VALIDATE,
                        payload,
                        print_txt_markdown=False,
                    )
                    resp = resp.merge(this_resp)

            if notify_function is not None:
                notify_function(chunk_size)

        # Finally, we validate all of the dapi files without suggestions, without additional
        # schema validation
        if all_files["dapis"]:
            for dapi_chunk in _chunks(all_files["dapis"], chunk_size):
                payload = _build_validate_payload(
                    {"dapis": dapi_chunk, "suggest_changes": False},
                    include_minimal_schemas=False,
                )
                this_resp = self.ask_dapi_server(
                    DAPIServerRequestType.VALIDATE,
                    payload,
                    print_txt_markdown=False,
                )
                resp = resp.merge(this_resp)

                if notify_function is not None:
                    notify_function(chunk_size)

        return resp

    def analyze_impact(
        self,
        changed_files: OpenDAPIFileContents,
        notify_function: Optional[Callable[[int], None]] = None,
    ) -> DAPIServerResponse:
        """Analyze the impact of changes on the DAPI Server."""
        server_files = changed_files.for_server()
        chunk_size = self.dapi_server_config.analyze_impact_batch_size
        resp: DAPIServerResponse = self.ask_dapi_server(
            DAPIServerRequestType.ANALYZE_IMPACT,
            {
                "dapis": {},
                "teams": server_files["teams"],
                "datastores": server_files["datastores"],
                "purposes": server_files["purposes"],
                "subjects": server_files["subjects"],
                "categories": server_files["categories"],
            },
            request_method=HTTPMethod.POST,
        )

        for dapi_chunk in _chunks(server_files["dapis"], chunk_size):
            this_resp = self.ask_dapi_server(
                DAPIServerRequestType.ANALYZE_IMPACT,
                {
                    "dapis": dapi_chunk,
                    "teams": {},
                    "datastores": {},
                    "purposes": {},
                    "subjects": {},
                    "categories": {},
                },
                request_method=HTTPMethod.POST,
            )
            resp = resp.merge(this_resp) if resp else this_resp
            if notify_function is not None:
                notify_function(chunk_size)
        return resp

    def register(
        self,
        all_files: OpenDAPIFileContents,
        onboarded_files: OpenDAPIFileContents,
        commit_hash: str,
        source: str,
        notify_function: Optional[Callable[[int], None]] = None,
        minimal_schemas_for_validation: Optional[Schemas] = None,
    ) -> Optional[DAPIServerResponse]:
        """Register OpenDAPI files with the DAPI Server."""
        all_files = all_files.for_server()
        chunk_size = self.dapi_server_config.register_batch_size
        onboarded_urns = [d["urn"] for d in onboarded_files.dapis.values()]

        resp: DAPIServerResponse = self.ask_dapi_server(
            DAPIServerRequestType.REGISTER,
            {
                "dapis": {},
                "teams": all_files["teams"],
                "datastores": all_files["datastores"],
                "purposes": all_files["purposes"],
                "subjects": all_files["subjects"],
                "categories": all_files["categories"],
                "commit_hash": commit_hash,
                "source": source,
                "onboarded_urns": onboarded_urns,
                "additional_schemas": (
                    minimal_schemas_for_validation.as_dict
                    if minimal_schemas_for_validation
                    else {}
                ),
            },
            request_method=HTTPMethod.POST,
        )

        for dapi_chunk in _chunks(all_files["dapis"], chunk_size):
            this_resp = self.ask_dapi_server(
                DAPIServerRequestType.REGISTER,
                {
                    "dapis": dapi_chunk,
                    "teams": {},
                    "datastores": {},
                    "purposes": {},
                    "subjects": {},
                    "categories": {},
                    "commit_hash": commit_hash,
                    "source": source,
                    "onboarded_urns": onboarded_urns,
                    "additional_schemas": (
                        minimal_schemas_for_validation.as_dict
                        if minimal_schemas_for_validation
                        else {}
                    ),
                },
                request_method=HTTPMethod.POST,
            )
            resp = resp.merge(this_resp) if resp else this_resp
            if notify_function is not None:
                notify_function(chunk_size)
        return resp

    def unregister(self, source: str, except_dapi_urns: List[str]):
        """Unregister missing DAPIs from the DAPI Server."""
        return self.ask_dapi_server(
            DAPIServerRequestType.UNREGISTER,
            {
                "source": source,
                "except_dapi_urns": except_dapi_urns,
            },
            request_method=HTTPMethod.POST,
        )

    def notify(self, dapi_change_notification: Optional[DAPIChangeNotification]):
        """Notify the DAPI Server of changes."""
        return self.ask_dapi_server(
            DAPIServerRequestType.NOTIFY,
            (dapi_change_notification or DAPIChangeNotification()).as_json(),
            request_method=HTTPMethod.POST,
        )

    def mark_repo_as_configured(self) -> None:
        """Let the dapi server know that a github repo's config PR has been merged"""
        request_path = "/v1/github/onboarding/pr/done"

        response, _ = self.raw_send_request_to_dapi_server(
            request_path=request_path,
            query_params={"repo_name": self.trigger_event.repo_full_name},
            method=HTTPMethod.POST,
        )

        if response.status_code != 200:
            self._handle_api_error(request_path, response.status_code)

    def get_or_create_gh_pull_request(self) -> PersistedGithubPullRequest:
        """Get or create a GithubPullRequest entity from the DAPI Server"""

        response, _ = self.raw_send_request_to_dapi_server(
            request_path=DAPIServerRequestType.GET_PR.value,
            query_params={
                "repo_name": self.trigger_event.repo_full_name,
                "number": self.trigger_event.pull_request_number,
            },
            method=HTTPMethod.GET,
        )

        if response.status_code == 200:
            return PersistedGithubPullRequest.create_from_dapi_server(
                response.json()["pull_request"]
            )

        elif response.status_code == 404:
            response, _ = self.raw_send_request_to_dapi_server(
                request_path=DAPIServerRequestType.GET_PR.value,
                query_params={
                    "repo_name": self.trigger_event.repo_full_name,
                    "number": self.trigger_event.pull_request_number,
                },
                body_json={
                    "link": self.trigger_event.pull_request_link,
                    "base_commit_sha": self.trigger_event.before_change_sha,
                    "head_commit_sha": self.trigger_event.after_change_sha,
                },
                method=HTTPMethod.POST,
            )

        # no validation here, so anything 400 and above is an error
        if response.status_code >= 400:
            self._handle_api_error(
                DAPIServerRequestType.GET_PR.value, response.status_code
            )

        return PersistedGithubPullRequest.create_from_dapi_server(
            response.json()["pull_request"]
        )

    def create_gh_pull_request_entities(
        self,
        all_files: OpenDAPIFileContents,
        base_commit_files: OpenDAPIFileContents,
        current_commit_files: OpenDAPIFileContents,
        changed_files_from_base: OpenDAPIFileContents,
        changed_files: OpenDAPIFileContents,
        enriched_files: Optional[OpenDAPIFileContents],
        notify_function: Optional[Callable[[int], None]] = lambda _: None,
        feature_validate_responses: Optional[List[FeatureValidationResult]] = None,
    ) -> List[PersistedPullRequestEntity]:
        """Register OpenDAPI files with the DAPI Server."""

        actions_dict_by_filepath = defaultdict(list)
        for feature_validate_response in feature_validate_responses or []:
            for action in feature_validate_response.actions:
                actions_dict_by_filepath[action.filepath].append(action.as_dict)

        all_files = all_files.for_server(writeable_location=True)
        base_commit_files = base_commit_files.for_server(writeable_location=True)
        current_commit_files = current_commit_files.for_server(writeable_location=True)
        changed_files_from_base = changed_files_from_base.for_server(
            writeable_location=True
        )
        changed_files = changed_files.for_server(writeable_location=True)
        enriched_files = (
            enriched_files.for_server(writeable_location=True) if enriched_files else {}
        )

        OPENDAPI_TYPE_TO_BODY_KEY = {
            "teams": "teams_pr_entities",
            "datastores": "datastores_pr_entities",
            "purposes": "purposes_pr_entities",
            "dapis": "dapi_pr_entities",
            "subjects": "subjects_pr_entities",
            "categories": "categories_pr_entities",
        }

        # for model ownership we must always associate the all teams entities with the PR
        # - changed or not - so that they are available in the Portal.
        # similarly, for data classification we must always associate the all categories and
        # subjects entities with the PR - changed or not - so that they are available in the Portal.
        # We therefore ensure that they are always sent, but their being changed or not is still
        # determined by changed_files
        ALWAYS_SEND_ENTITIES = {"teams", "categories", "subjects"}

        # iterate over files from base, since want to be able to show all changed files
        # in the portal, even though we default to toggling only the changed from current
        body_key_w_filepath_w_raw_md_tuples = []
        for (
            opendapi_type,
            all_json_by_file,
        ) in all_files.items():

            if opendapi_type in ALWAYS_SEND_ENTITIES:
                changed_json_by_file_from_base = all_json_by_file
            else:
                changed_json_by_file_from_base = changed_files_from_base[opendapi_type]

            base_json_by_file = base_commit_files[opendapi_type]
            current_json_by_file = current_commit_files[opendapi_type]
            changed_json_by_file = changed_files[opendapi_type]
            # may have been the empty dict if initially was None, so safe access
            enriched_json_by_file = enriched_files.get(opendapi_type, {})
            body_key = OPENDAPI_TYPE_TO_BODY_KEY[opendapi_type]

            # we want to add the the GithubPullRequest opendapi entities that
            # were changed in this PR, which are the ones with changes from base, even if they
            # no longer are changed from current.

            # However, we must also consider the situation where the user is undoing a change.
            # In this case, the generated dapi may no longer be changed from base, but is
            # different from the current state [which was synced pre undoing the change],
            # and we need to offer the user the ability to re-sync this now undone dapi.

            # the manner in which we do this is to iterate over all_files rather than
            # unioning changed_files_from_base and changed_files since we want to
            # demonstrate the continue case explicitly

            # Note that all files does not include deleted dapis
            for filepath in all_json_by_file.keys():

                # this file was changed from base. undergo usual flow where we show this file
                # in the portal - even if it is not changed from current - so folks can make
                # further edits
                if filepath in changed_json_by_file_from_base:
                    preliminary_new_content = changed_json_by_file_from_base[filepath]

                # not changed from base, but is changed now. Means someone undid a change,
                # and we show this in the portal to allow them to re-sync
                elif filepath in changed_json_by_file:
                    preliminary_new_content = changed_json_by_file[filepath]

                # this dapi file is either synced (as it is not in changed_files_from_base
                # nor changed_files) or should not exist (table was removed, we do not
                # generate anything for it but the Dapi still exists)
                # In either case, there is nothing to be done here.
                else:
                    # this no cover is due to this issue:
                    # https://github.com/nedbat/coveragepy/issues/198
                    continue  # pragma: no cover

                # if a file that was changed from base is changed from current, it means
                # that the user is not up to date merging the metadata changes.
                changed_from_current = filepath in changed_json_by_file

                # for us to say that changes were generated by AI, the file must have been
                # enriched and it still must be different than the current state, since if the
                # current state is not different it means that a human committed it,
                # meaning that the AI suggestion was accepted, at which point it is owned
                # by the user
                maybe_enriched_json = enriched_json_by_file.get(filepath)
                generated_by_ai = maybe_enriched_json and changed_from_current

                base_content = base_json_by_file.get(filepath)
                # the portal will only diff against the current content if there was a change,
                # and the PREntity only stores the previous content if there was a change,
                # since it only needs it in that event. Therefore,
                # we only need to store the current content if there was a change, otherwise
                # send None
                current_content = (
                    current_json_by_file.get(filepath) if changed_from_current else None
                )

                # if the file was enriched, we use that state, but otherwise the state should
                # not be different (the only time we yaml dump after generate is for enrich)
                # and so we default to the state after generate which is changed_json_from_base
                new_content = maybe_enriched_json or preliminary_new_content

                raw_pr_entity_metadata = {
                    "previous_content": current_content,
                    "content_state_at_base": base_content,
                    "new_content": new_content,
                    "changed_from_current": changed_from_current,
                    "new_generated_by": "ai" if generated_by_ai else "user",
                    "actions": actions_dict_by_filepath.get(filepath) or [],
                }
                body_key_w_filepath_w_raw_md_tuples.append(
                    (body_key, filepath, raw_pr_entity_metadata)
                )

        persisted_pr_entities = []
        chunk_size = self.dapi_server_config.pr_sync_batch_size

        for chunked_files in _simple_iter_chunks(
            body_key_w_filepath_w_raw_md_tuples, chunk_size
        ):
            body = defaultdict(dict)
            for body_key, file_path, raw_pr_entity_metadata in chunked_files:
                body[body_key][file_path] = raw_pr_entity_metadata

            response, _ = self.raw_send_request_to_dapi_server(
                request_path=DAPIServerRequestType.PERSIST_PR_ENTITIES.value,
                query_params={
                    "repo_name": self.trigger_event.repo_full_name,
                    "number": self.trigger_event.pull_request_number,
                },
                body_json=body,
                method=HTTPMethod.POST,
            )

            if response.status_code == 200:
                persisted_pr_entities.extend(
                    (
                        PersistedPullRequestEntity.create_from_dapi_server(entity)
                        for entity in response.json()["pull_request_entities"]
                    )
                )
            # even though we return validation errors as a 400, they should not happen at
            # this point in the flow, since we already validated. This would therefore be
            # a hard failure
            if response.status_code >= 400:
                self._handle_api_error(
                    DAPIServerRequestType.PERSIST_PR_ENTITIES.value,
                    response.status_code,
                )

            notify_function(chunk_size)

        return persisted_pr_entities

    def upsert_gh_pull_request(
        self,
        woven_comment_id: Optional[int],
        persisted_pr_entities_to_upsert: List[PersistedPullRequestEntity],
    ) -> PersistedGithubPullRequest:
        """Upsert a GithubPullRequest entity to the DAPI Server"""

        response, _ = self.raw_send_request_to_dapi_server(
            request_path=DAPIServerRequestType.UPSERT_PR.value,
            query_params={
                "repo_name": self.trigger_event.repo_full_name,
                "number": self.trigger_event.pull_request_number,
            },
            body_json={
                "link": self.trigger_event.pull_request_link,
                "woven_comment_id": woven_comment_id,
                "base_commit_sha": self.trigger_event.before_change_sha,
                "head_commit_sha": self.trigger_event.after_change_sha,
                "persisted_entities": [
                    entity.get_metadata_for_upsert()
                    for entity in persisted_pr_entities_to_upsert
                ],
            },
            method=HTTPMethod.POST,
        )

        if response.status_code >= 400:
            self._handle_api_error(
                DAPIServerRequestType.UPSERT_PR.value, response.status_code
            )

        return PersistedGithubPullRequest.create_from_dapi_server(
            response.json()["pull_request"]
        )

    def validate_features(
        self,
        all_files: OpenDAPIFileContents,
        changed_files: OpenDAPIFileContents,
        changed_files_from_base: OpenDAPIFileContents,
        base_commit_files: OpenDAPIFileContents,
        current_commit_files: OpenDAPIFileContents,
        notify_function: Optional[Callable[[int], None]] = lambda _: None,
    ) -> List[FeatureValidationResult]:
        """Validate features with the DAPI Server."""

        all_files = all_files.for_server(writeable_location=True)
        changed_from_head_filepaths = changed_files.for_server_filepaths(
            writeable_location=True
        )
        changed_from_base_filepaths = changed_files_from_base.for_server_filepaths(
            writeable_location=True
        )
        files_at_base = base_commit_files.for_server(writeable_location=True)
        files_at_head = current_commit_files.for_server(writeable_location=True)

        # logic below doesnt assume the dapi exists in any of the files, and so to get
        # feature validation to run at least once we default to a nonexistent dapi filepath
        total_dapi_filepaths = (
            set(all_files["dapis"].keys())
            | set(changed_from_head_filepaths["dapis"])
            | set(changed_from_base_filepaths["dapis"])
            | set(files_at_base["dapis"].keys())
            | set(files_at_head["dapis"].keys())
        ) or {"nonexistent_dapi_filepath"}

        total_feature_validation_results_by_feature = defaultdict(list)
        chunk_size = self.dapi_server_config.feature_validate_dapi_batch_size
        for dapi_filepaths in _simple_iter_chunks(total_dapi_filepaths, chunk_size):
            response, _ = self.raw_send_request_to_dapi_server(
                request_path=DAPIServerRequestType.VALIDATE_FEATURES.value,
                query_params={
                    "repo_name": self.trigger_event.repo_full_name,
                },
                body_json={
                    "all_files": {
                        "teams": all_files["teams"],
                        "datastores": all_files["datastores"],
                        "purposes": all_files["purposes"],
                        "subjects": all_files["subjects"],
                        "categories": all_files["categories"],
                        "dapis": (
                            {
                                df: dapi
                                for df in dapi_filepaths
                                if (dapi := all_files["dapis"].get(df))
                            }
                        ),
                    },
                    "changed_from_head_filepaths": {
                        "teams": changed_from_head_filepaths["teams"],
                        "datastores": changed_from_head_filepaths["datastores"],
                        "purposes": changed_from_head_filepaths["purposes"],
                        "dapis": (
                            [
                                df
                                for df in dapi_filepaths
                                if df in changed_from_head_filepaths["dapis"]
                            ]
                        ),
                        "subjects": changed_from_head_filepaths["subjects"],
                        "categories": changed_from_head_filepaths["categories"],
                    },
                    "changed_from_base_filepaths": {
                        "teams": changed_from_base_filepaths["teams"],
                        "datastores": changed_from_base_filepaths["datastores"],
                        "purposes": changed_from_base_filepaths["purposes"],
                        "dapis": (
                            [
                                df
                                for df in dapi_filepaths
                                if df in changed_from_base_filepaths["dapis"]
                            ]
                        ),
                        "subjects": changed_from_base_filepaths["subjects"],
                        "categories": changed_from_base_filepaths["categories"],
                    },
                    "files_at_base": {
                        "teams": files_at_base["teams"],
                        "datastores": files_at_base["datastores"],
                        "purposes": files_at_base["purposes"],
                        "dapis": (
                            {
                                df: dapi
                                for df in dapi_filepaths
                                if (dapi := files_at_base["dapis"].get(df))
                            }
                        ),
                        "subjects": files_at_base["subjects"],
                        "categories": files_at_base["categories"],
                    },
                    "files_at_head": {
                        "teams": files_at_head["teams"],
                        "datastores": files_at_head["datastores"],
                        "purposes": files_at_head["purposes"],
                        "dapis": (
                            {
                                df: dapi
                                for df in dapi_filepaths
                                if (dapi := files_at_head["dapis"].get(df))
                            }
                        ),
                        "subjects": files_at_head["subjects"],
                        "categories": files_at_head["categories"],
                    },
                },
                method=HTTPMethod.POST,
            )

            if response.status_code >= 400:
                self._handle_api_error(
                    DAPIServerRequestType.VALIDATE_FEATURES.value, response.status_code
                )

            for feature_id_str, raw_result in response.json()[
                "feature_ids_to_result"
            ].items():
                if not Feature.is_feature(feature_id_str):
                    continue
                feature = Feature(feature_id_str)
                total_feature_validation_results_by_feature[feature].append(
                    FeatureValidationResult.create_from_dapi_server(
                        feature_id_str,
                        raw_result["actions"],
                        raw_result["passed"],
                    )
                )

            notify_function(len(dapi_filepaths))

        aggregated_feature_validation_results = []
        for (
            feature,
            results,
        ) in total_feature_validation_results_by_feature.items():

            aggregated_feature_validation_results.append(
                FeatureValidationResult(
                    feature=feature,
                    # since we are aggregating, for non-dapi files we need to dedup, since errors will appear
                    # multiple times for the same file
                    actions=list(
                        {action for result in results for action in result.actions}
                    ),
                    passed=all(result.passed for result in results),
                )
            )

        return aggregated_feature_validation_results
