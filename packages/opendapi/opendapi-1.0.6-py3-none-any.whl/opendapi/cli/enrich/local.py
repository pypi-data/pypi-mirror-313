# pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-function-args
"""Local enricher to work with `opendapi enrich` command."""
from functools import cached_property
from typing import Callable, List, Optional

import click

from opendapi.adapters.dapi_server import (
    DAPIRequests,
    DAPIServerConfig,
    DAPIServerMeta,
    DAPIServerResponse,
)
from opendapi.adapters.file import OpenDAPIFileContents
from opendapi.adapters.git import (
    ChangeTriggerEvent,
    add_untracked_opendapi_files,
    check_if_uncommitted_changes_exist,
)
from opendapi.cli.common import Schemas, print_cli_output
from opendapi.config import OpenDAPIConfig
from opendapi.features import Feature, is_feature_on


class Enricher:
    """
    Enrich DAPIs after interacting with the DAPI server.
    Register when appropriate.
    """

    add_all_untracked_files = True

    def __init__(
        self,
        config: OpenDAPIConfig,
        dapi_server_config: DAPIServerConfig,
        trigger_event: ChangeTriggerEvent,
        revalidate_all_files: bool = False,
        require_committed_changes: bool = False,
        minimal_schemas_for_validation: Optional[Schemas] = None,
    ) -> None:
        """Initialize the adapter."""
        self.config = config
        self.root_dir = config.root_dir
        self.dapi_server_config = dapi_server_config
        self.trigger_event = trigger_event
        self.revalidate_all_files = revalidate_all_files
        self.require_committed_changes = require_committed_changes
        self.minimal_schemas_for_validation = minimal_schemas_for_validation

        # Initialize the responses
        self.validate_response: Optional[DAPIServerResponse] = None
        self.analyze_impact_response: Optional[DAPIServerResponse] = None

        # Pull up and set the files
        self.all_files: OpenDAPIFileContents = self._get_all_files()

        # all_files_enriched is set after enriching
        self.all_files_enriched: Optional[OpenDAPIFileContents] = None

        # changed files are defined prior to enriching, as we ensure what we consider
        # 'changes' are due to generate only (defines the schema scaffold) rather
        # than the enriching process (since enrichment may suggest a new description etc.,
        # but that is not a change as it pertains to the schema scaffold)
        # note that they are compared to the current_sha, since we want to know if
        # generate created any changes from the most recent commit (note base etc)
        # - since if so we need to alert the user.
        self.changed_files: OpenDAPIFileContents = self._get_changed_files()

        # changes from the base
        self.changed_files_from_base: OpenDAPIFileContents = (
            self._get_changed_files_from_base()
        )

        # the state of the DAPI files at the current commit (before generation)
        # used by Portal devX to highlight minimal changes
        self.current_commit_files = self._get_current_commit_files()

        # the state of the DAPI files at the base commit (before generation or any commits)
        # used by Portal devX and Dapi Server to highlight various changes
        self.base_commit_files = self._get_base_commit_files()

        self.dapi_requests = DAPIRequests(
            dapi_server_config=self.dapi_server_config,
            trigger_event=self.trigger_event,
            opendapi_config=self.config,
            error_msg_handler=lambda msg: self.print_markdown_and_text(msg, "red"),
            error_exception_cls=click.ClickException,
            txt_msg_handler=lambda msg: self.print_markdown_and_text(
                msg, no_markdown=True
            ),
            markdown_msg_handler=lambda msg: self.print_markdown_and_text(
                msg, no_text=True
            ),
        )

    def print_markdown_and_text(
        self,
        message: str,
        color: str = "green",
        bold: bool = False,
        no_text: bool = False,
        no_markdown: bool = False,
    ):
        """Print errors."""
        print_cli_output(
            message,
            color=color,
            bold=bold,
            markdown_file=self.trigger_event.markdown_file,
            no_text=no_text,
            no_markdown=no_markdown,
        )

    def _get_all_files(self) -> OpenDAPIFileContents:
        """Get all the OpenDAPI files."""
        return OpenDAPIFileContents.build_from_all_files(self.config)

    def _get_changed_files(self) -> OpenDAPIFileContents:
        """Get the changed OpenDAPI files."""
        if self.revalidate_all_files:
            self.print_markdown_and_text("Tackling all DAPI files", "green")
            return self.all_files
        self.print_markdown_and_text("Tackling only the changed DAPI files", "green")

        # Add untracked opendapi files created by `opendapi generate` or the user
        if self.add_all_untracked_files:
            add_untracked_opendapi_files(self.root_dir)

        return self.all_files.filter_changed_files(self.trigger_event.after_change_sha)

    def _get_changed_files_from_base(self) -> OpenDAPIFileContents:
        """Get the changed OpenDAPI files from the base commit"""
        # Add untracked opendapi files created by `opendapi generate` or the user
        if self.add_all_untracked_files:
            add_untracked_opendapi_files(self.root_dir)

        return self.all_files.filter_changed_files(self.trigger_event.before_change_sha)

    def _get_current_commit_files(self) -> OpenDAPIFileContents:
        """Get the state of the opendapi files at the current commit state."""
        return OpenDAPIFileContents.build_from_all_files_at_commit(
            self.config, self.trigger_event.after_change_sha
        )

    def _get_base_commit_files(self) -> OpenDAPIFileContents:
        """Get the state of the opendapi files at the base commit state."""
        return OpenDAPIFileContents.build_from_all_files_at_commit(
            self.config, self.trigger_event.before_change_sha
        )

    def _check_if_files_need_to_be_committed(self) -> None:
        """
        Check if the files need to be committed.
        Sometimes, we do not want to overwrite the developer's changes.
        """
        if self.require_committed_changes and check_if_uncommitted_changes_exist(
            self.root_dir
        ):
            raise click.ClickException(
                "Uncommitted changes found. Please commit your changes before running this command"
                " or do not set the `--require-committed-changes` flag. Exiting...",
            )

    def _are_there_files_to_process(self) -> bool:
        """Check if there are files to process."""
        if self.all_files.is_empty:
            self.print_markdown_and_text(
                "No OpenDAPI files found. "
                "Run `opendapi generate` to generate OpenDAPI files.",
                color="yellow",
            )
            return False

        # Consider all the changed files from base if it is a push event
        files_to_process = (
            self.changed_files_from_base
            if self.trigger_event.is_push_event
            else self.changed_files
        )

        if files_to_process.is_empty and not self.revalidate_all_files:
            self.print_markdown_and_text(
                "\n\nNo changes to OpenDAPI files found. "
                "\nSet `--revalidate-all-files` if you wish to revalidate all files.",
                color="yellow",
            )
            return False
        return True

    def should_enrich(self) -> bool:
        """Check if we should enrich the DAPI files."""
        return self.dapi_server_config.suggest_changes

    def print_dapi_server_progress(self, progressbar, progress: int):
        """Print the progress bar for validation."""
        progressbar.update(progress)

    def validate_and_enrich(self) -> DAPIServerResponse:
        """Validate and enrich the DAPI files."""

        self.print_markdown_and_text(
            f"\n\nProcessing {len(self.changed_files.dapis)} DAPI files in"
            f" batch size of {self.dapi_server_config.enrich_batch_size}",
            color="green",
        )
        with click.progressbar(length=len(self.changed_files.dapis)) as progressbar:

            def _notify(progress: int):
                """Notify the user to the progress."""
                return self.print_dapi_server_progress(
                    progressbar, progress
                )  # pragma: no cover

            self.validate_response = self.dapi_requests.validate(
                all_files=self.all_files,
                changed_files=self.changed_files,
                commit_hash=self.trigger_event.after_change_sha,
                suggest_changes_override=self.should_enrich(),
                ignore_suggestions_cache=self.dapi_server_config.ignore_suggestions_cache,
                notify_function=_notify,
                minimal_schemas_for_validation=self.minimal_schemas_for_validation,
            )

        if self.should_enrich():
            self.all_files_enriched = self.all_files.update_dapis_with_suggestions(
                self.validate_response.suggestions
            )

        return self.validate_response

    def should_analyze_impact(self) -> bool:
        """Check if we should analyze the impact."""
        return is_feature_on(Feature.IMPACT_ANALYSIS_V1)

    def analyze_impact(self) -> DAPIServerResponse:
        """Analyze the impact of the DAPI files."""
        changed_files_from_base = self.changed_files_from_base

        self.print_markdown_and_text(
            f"\n\nAnalyzing impact of {len(changed_files_from_base.dapis)} DAPI files in"
            f" batch size of {self.dapi_server_config.analyze_impact_batch_size}",
            color="green",
        )
        with click.progressbar(
            length=len(changed_files_from_base.dapis)
        ) as progressbar:

            def _notify(progress: int):
                """Notify the user to the progress."""
                return self.print_dapi_server_progress(
                    progressbar, progress
                )  # pragma: no cover

            analyze_impact_resp = self.dapi_requests.analyze_impact(
                changed_files=changed_files_from_base,
                notify_function=_notify,
            )

            return analyze_impact_resp

    def maybe_analyze_impact(self) -> None:
        """Maybe analyze the impact."""
        if self.should_analyze_impact():
            self.analyze_impact_response = self.analyze_impact()

    @cached_property
    def dapi_server_meta(self) -> DAPIServerMeta:
        """
        Get the server meta.
        Fallback to the DAPI server explicit API if the response is not available.
        """
        return (
            (self.validate_response and self.validate_response.server_meta)
            or (
                self.analyze_impact_response
                and self.analyze_impact_response.server_meta
            )
            or (self.dapi_requests.get_dapi_server_meta())
        )

    @property
    def base_functions_to_run(self) -> List[Callable[[], Optional[DAPIServerResponse]]]:
        """The functions that are run by the base Enricher"""
        return [
            self.validate_and_enrich,
            self.maybe_analyze_impact,
        ]

    def functions_to_run(self) -> List[Callable[[], Optional[DAPIServerResponse]]]:
        """Check if we should run the action."""
        return self.base_functions_to_run if self._are_there_files_to_process() else []

    def run(self):
        """Run the action."""

        self._check_if_files_need_to_be_committed()

        # Run enrich only PR contains OpenDAPI files and there are changes
        for func in self.functions_to_run():
            func()

        self.print_markdown_and_text("All done!", "green")
