"""Enricher to work from Github as part of `opendapi enrich` CLI command."""

# pylint: disable=unnecessary-pass, too-many-public-methods
import functools
import json
import urllib.parse
from typing import Callable, List, Optional

import click
import sentry_sdk

from opendapi.adapters.dapi_server import DAPIServerResponse, FeatureValidationResult
from opendapi.adapters.git import (
    add_untracked_opendapi_files,
    get_changed_opendapi_filenames,
    get_git_diff_filenames,
    run_git_command,
)
from opendapi.adapters.github import GithubAdapter
from opendapi.cli.enrich.local import Enricher
from opendapi.feature_flags import FeatureFlag, get_feature_flag
from opendapi.features import Feature, is_feature_on
from opendapi.logging import LogCounterKey, increment_counter


class GithubEnricherException(click.ClickException):
    """Exception raised due to errors in the Github enricher."""

    pass


class FailGithubAction(click.ClickException):
    """Exception that will be raised to fail the Github action."""

    pass


class FailSilently(click.ClickException):
    """Exception that will be raised to fail silently."""

    exit_code = 0


class GithubEnricher(Enricher):
    """Enricher to work from Github as part of `opendapi enrich` CLI command."""

    GENERATED_COMMENT_IDENTIFIER = "<!-- OpenDAPI Comment Identifier -->"

    def __init__(self, *args, **kwargs):
        """Initialize the adapter."""
        super().__init__(*args, **kwargs)
        self.github_adapter: GithubAdapter = GithubAdapter(
            self.trigger_event.repo_api_url,
            self.trigger_event.auth_token,
            exception_cls=click.ClickException,
        )
        self.autoupdate_pr_number: Optional[int] = None
        self.feature_validate_responses: Optional[List[FeatureValidationResult]] = None

    def should_enrich(self) -> bool:
        """Should we enrich the DAPI files?"""
        return (
            self.dapi_server_config.suggest_changes
            and self.trigger_event.is_pull_request_event
        )

    def should_analyze_impact(self) -> bool:
        return self.trigger_event.is_pull_request_event and is_feature_on(
            Feature.IMPACT_ANALYSIS_V1
        )

    def print_dapi_server_progress(self, progressbar, progress: int):
        """Print the progress bar for validation."""
        progressbar.update(progress)
        self.print_markdown_and_text(
            f"\nFinished {round(progressbar.pct * 100)}% with {progressbar.format_eta()} remaining",
            color="green",
            bold=True,
        )

    def get_current_branch_name(self):
        """Get the current branch name."""
        return (
            run_git_command(self.root_dir, ["git", "rev-parse", "--abbrev-ref", "HEAD"])
            .decode("utf-8")
            .strip()
        )

    def get_autoupdate_branch_name(self):
        """Get the autoupdate branch name."""
        return f"opendapi-autoupdate-for-{self.trigger_event.pull_request_number}"

    def add_pull_request_comment(self, message: str):
        """Add a comment to the pull request."""
        message_with_identifier = f"{message}{self.GENERATED_COMMENT_IDENTIFIER}"
        self.github_adapter.add_pull_request_comment(
            self.trigger_event.pull_request_number, message_with_identifier
        )

    def update_pull_request_comment(self, comment_id: int, message: str):
        """Update a comment on the pull request."""
        message_with_identifier = f"{message}{self.GENERATED_COMMENT_IDENTIFIER}"
        self.github_adapter.update_pull_request_comment(
            comment_id, message_with_identifier
        )

    @functools.cached_property
    def existing_opendapi_comment_id(self) -> Optional[int]:
        """Get the existing OpenDAPI comment id."""
        # NOTE: we should create a PR entity on the server, to store things like
        # opendapi comment_id, last checked time, etc. - this is an interim solution

        # the comment user is just github-bot, would not know its Woven related, hack for now
        comment_id_index = -1 * len(self.GENERATED_COMMENT_IDENTIFIER)
        for comment in self.github_adapter.get_pull_request_comments(
            self.trigger_event.pull_request_number
        ):
            if (comment["body"] or "")[
                comment_id_index:
            ] == self.GENERATED_COMMENT_IDENTIFIER:
                return comment["id"]

        return None

    def add_or_update_pull_request_comment(self, message: str):
        """Add or update a comment on the pull request."""
        if comment_id := self.existing_opendapi_comment_id:
            self.update_pull_request_comment(comment_id, message)
        else:
            self.add_pull_request_comment(message)

    def _git_helper_sentry_log(self, msg: str):
        """
        Helper to log various git state to sentry
        """
        data_common = {
            "repo_owner": self.trigger_event.repo_owner,
            "pull_request_number": self.trigger_event.pull_request_number,
            "after_change_sha": self.trigger_event.after_change_sha,
            "before_change_sha": self.trigger_event.before_change_sha,
            "current_branch": run_git_command(
                self.root_dir, ["git", "rev-parse", "--abbrev-ref", "HEAD"]
            )
            .decode("utf-8")
            .strip(),
            "dapi_git_status": get_changed_opendapi_filenames(self.root_dir),
            "are_there_files_to_process": self._are_there_files_to_process(),
        }
        sentry_sdk.add_breadcrumb(
            category="enrich",
            message=msg,
            data={
                "git_diff": [
                    {
                        "help": "base_ref is PR base",
                        "base_ref": self.trigger_event.before_change_sha,
                        "diff_output": get_git_diff_filenames(
                            self.root_dir, self.trigger_event.before_change_sha
                        ),
                    },
                    {
                        "help": "base ref is current_sha",
                        "base_ref": self.trigger_event.after_change_sha,
                        "diff_output": get_git_diff_filenames(
                            self.root_dir, self.trigger_event.after_change_sha
                        ),
                    },
                ],
                **data_common,
            },
        )
        sentry_sdk.add_breadcrumb(
            category="enrich",
            message=msg,
            data={
                "git_diff_cached": [
                    {
                        "help": "base_ref is PR base",
                        "base_ref": self.trigger_event.before_change_sha,
                        "diff_output": get_git_diff_filenames(
                            self.root_dir,
                            self.trigger_event.before_change_sha,
                            cached=True,
                        ),
                    },
                    {
                        "help": "base_ref is current_sha",
                        "base_ref": self.trigger_event.after_change_sha,
                        "diff_output": get_git_diff_filenames(
                            self.root_dir,
                            self.trigger_event.after_change_sha,
                            cached=True,
                        ),
                    },
                ],
                **data_common,
            },
        )

    def create_pull_request_for_changes(self) -> int:
        """
        Create a pull request for any changes made to the DAPI files.
        """

        self._git_helper_sentry_log(
            "In create_pull_request_for_changes, prior to git status check"
        )
        # if there are no dapi file changes, there is nothing to create a PR for
        if not get_changed_opendapi_filenames(self.root_dir):
            raise GithubEnricherException(
                "No OpenDAPI files found to create a pull request"
            )

        self.print_markdown_and_text(
            "Creating a pull request for the changes...",
            color="green",
        )

        # Set git user and email
        git_config_map = {
            "user.email": self.dapi_server_meta.github_user_email,
            "user.name": self.dapi_server_meta.github_user_name,
        }
        for config, value in git_config_map.items():
            run_git_command(self.root_dir, ["git", "config", "--global", config, value])

        # get current branch name
        current_branch_name = self.get_current_branch_name()

        # Unique name for the new branch
        update_branch_name = self.get_autoupdate_branch_name()

        # Checkout new branch. Force reset if branch already exists,
        # including uncommited changes
        run_git_command(self.root_dir, ["git", "checkout", "-B", update_branch_name])

        self._git_helper_sentry_log(
            (
                "In create_pull_request_for_changes, after git checkout -B, "
                "before re-adding untracked files"
            )
        )

        # Add the relevant files
        add_untracked_opendapi_files(
            self.root_dir, files_patterns=self.changed_files.dapis.keys()
        )

        self._git_helper_sentry_log(
            "In create_pull_request_for_changes, after re-adding untracked files, before git commit"
        )

        # Commit the changes
        run_git_command(
            self.root_dir,
            [
                "git",
                "commit",
                "-m",
                f"OpenDAPI updates for {self.trigger_event.pull_request_number}",
            ],
        )

        # Push the changes. Force push to overwrite any existing branch
        run_git_command(
            self.root_dir,
            [
                "git",
                "push",
                "-f",
                "origin",
                f"HEAD:refs/heads/{update_branch_name}",
            ],
        )

        # construct the PR body

        # NOTE: current iteration no longer includes Title markdown
        # please reference commits before 2024-06-05 for the previous implementation

        # IMPORTANT section
        body = (
            "> [!IMPORTANT]\n"
            "> **This PR was auto-generated to sync your metadata with "
            f"schema changes in PR #{self.trigger_event.pull_request_number}.** Please review, "
            "revise[^HowToEditDAPI], and merge this PR to your branch.\n"
            ">\n"
            "> Code-synced metadata instills trust[^WhyMetadataMatters] in "
            "data discovery, quality, and compliance. If you have "
            "questions, reach out to Data Engineering.[^Feedback]\n\n"
        )

        # Footer
        body += (
            "[^WhyMetadataMatters]: Learn more about why code-synced metadata matters "
            "[here](https://www.wovencollab.com/docs)\n"
            "[^HowToEditDAPI]: Watch "
            "[a quick video](https://www.wovencollab.com/howto/edit-metadata-in-github) "
            "to see how to revise metadata suggestions\n"
            "[^Feedback]: Did you find this useful? If you found a bug or have an idea to "
            "improve the DevX, [let us know](https://www.wovencollab.com/feedback)"
        )

        self.autoupdate_pr_number = (  # pylint: disable=attribute-defined-outside-init
            self.github_adapter.create_pull_request_if_not_exists(
                self.trigger_event.repo_owner,
                title=(
                    f"Metadata updates for #{self.trigger_event.pull_request_number}"
                ),
                body=body,
                base=current_branch_name,
                head=update_branch_name,
            )
        )

        # ALWAYS Reset by checking out the original branch
        run_git_command(self.root_dir, ["git", "checkout", current_branch_name])
        return self.autoupdate_pr_number

    @staticmethod
    def _create_summary_comment(body: str):
        """Create a summary comment."""
        header = (
            "> [!WARNING]\n"
            "> This PR updates a data schema. You are responsible for keeping schema metadata "
            "in-sync with source code and keeping stakeholders informed.\n\n"
        )
        footer = (
            "<hr>\n\n"
            "<sup>Did you find this useful? If you found a bug or have an idea to improve the "
            "DevX, [let us know](https://www.wovencollab.com/feedback)</sup>"
        )
        return f"{header}{body}{footer}"

    def _get_failed_features(self) -> List[FeatureValidationResult]:
        """Get the failed features."""
        return [
            result
            for result in (self.feature_validate_responses or [])
            if not result.passed
        ]

    def _create_feature_validation_comment_section(self) -> str:
        """Create a feature validation comment section."""
        comment_md = ""

        if self.feature_validate_responses is None:
            return comment_md

        if not self.feature_validate_responses:
            comment_md += "# Feature Validation Passed! :tada:\n\n"
            comment_md += "No features were found to validate against.\n\n"
            return comment_md

        failed_features = self._get_failed_features()
        if not failed_features:
            comment_md += "# Feature Validation Passed! :tada:\n\n"
            comment_md += "Your files passed validation for the following features:\n"
            sorted_feature_names = sorted(
                {result.feature.value for result in self.feature_validate_responses}
            )
            comment_md += "\n".join(
                f"- {feature_name}" for feature_name in sorted_feature_names
            )
            comment_md += "\n\n"
            return comment_md

        sorted_failed_features = sorted(failed_features, key=lambda x: x.feature.value)
        comment_md += "# Feature Validation Failed"
        comment_md += (
            " :warning:\n\n"
            "Your files failed validation for the following features:\n"
        )
        for result in sorted_failed_features:
            comment_md += result.compiled_markdown
            # each one already includes newline at end
        return comment_md

    def create_or_update_summary_comment_metadata_synced(self):
        """
        Create a summary comment on the pull request for when metadata updates merged,
        though just because they were merged doesnt mean they are entirely valid
        """

        feature_validation_failed = bool(self._get_failed_features())

        if self.use_portal_based_devx:

            if feature_validation_failed:
                pr_comment_md = "# Update your schema metadata\n\n"
                pr_comment_md += (
                    "This PR contains a schema change. Suggestions from "
                    f"[the portal]({self.portal_metadata_update_link}) were committed "
                    "to this branch, but additional action is required to ensure your metadata "
                    "passes all feature-related validation.\n\n"
                )

            else:
                pr_comment_md = "# Schema metadata synced! :tada:\n\n"
                pr_comment_md += (
                    "This PR contains a schema change. Suggestions from "
                    f"[the portal]({self.portal_metadata_update_link}) were committed "
                    "to this branch to keep your metadata in-sync with these changes "
                    "and all of your company's enabled features.\n\n"
                )

        else:
            merged_prs = self.github_adapter.get_merged_pull_requests_cached(
                self.trigger_event.repo_owner,
                self.get_current_branch_name(),
                self.get_autoupdate_branch_name(),
            )

            # if we are in the else clause, there should be a merged PR, but just in case
            pr_stanza = (
                f"PR #{merged_prs[0]['number']}"
                if merged_prs
                else "A Woven-generated PR"
            )

            if feature_validation_failed:
                pr_comment_md = "# Update your schema metadata\n\n"
                pr_comment_md += (
                    f"This PR contains a schema change. {pr_stanza} was merged into this branch "
                    "to keep your metadata in-sync with these changes. However, additional action "
                    "is required to ensure your metadata passes all feature-related validation.\n\n"
                )

            else:
                pr_comment_md = "# Schema metadata synced! :tada:\n\n"
                pr_comment_md += (
                    f"This PR contains a schema change. {pr_stanza} was merged into this branch "
                    "to keep your metadata in-sync with these changes.\n\n"
                )

        # Impact Response
        if (
            self.analyze_impact_response
            and self.analyze_impact_response.compiled_markdown
        ):
            pr_comment_md += self.analyze_impact_response.compiled_markdown
            pr_comment_md += "\n\n"

        pr_comment_md += self._create_feature_validation_comment_section()

        self.add_or_update_pull_request_comment(
            self._create_summary_comment(pr_comment_md)
        )

    @functools.cached_property
    def use_portal_based_devx(self) -> bool:
        """Check if we should use the portal based devx."""
        return True

    def create_or_update_summary_comment_metadata_unsynced(
        self,
    ):
        """Create a summary comment on the pull request for when metadata updates not in sync"""

        # Update schema section

        # tiered rollout - keep off switch for now
        if self.use_portal_based_devx:
            link_url = self.portal_metadata_update_link
            pr_comment_md = (
                "# Update your schema metadata\n\n"
                "This PR contains a schema change. Suggestions were auto-generated "
                "to keep your metadata in-sync with these changes. "
                f"Please [visit the portal]({link_url}) to review, revise, and "
                "commit these metadata updates to this branch.\n\n"
            )

        else:
            link_url = (
                f"{self.trigger_event.repo_html_url}/pull/{self.autoupdate_pr_number}"
            )
            pr_comment_md = (
                "# Update your schema metadata\n\n"
                f"This PR contains a schema change. PR #{self.autoupdate_pr_number} "
                "was auto-generated to keep your metadata in-sync with these changes. "
                "Please review, revise, and merge this metadata update into this branch.\n\n"
            )

        # Review suggestion button
        pr_comment_md += (
            f'<a href="{link_url}">'
            f'<img src="{self.dapi_server_meta.suggestions_cta_url}" '
            'width="140"/></a>'
            "\n\n"
        )

        # Impact Response
        if (
            self.analyze_impact_response
            and self.analyze_impact_response.compiled_markdown
        ):
            pr_comment_md += self.analyze_impact_response.compiled_markdown
            pr_comment_md += "\n\n"

        pr_comment_md += self._create_feature_validation_comment_section()

        self.add_or_update_pull_request_comment(
            self._create_summary_comment(pr_comment_md)
        )

    @functools.cached_property
    def portal_metadata_update_link(self) -> str:
        """the link to the portal metadata update page"""
        repo_path = urllib.parse.quote(self.trigger_event.repo_full_name, safe="")
        number = self.trigger_event.pull_request_number
        return urllib.parse.urljoin(
            str(self.dapi_server_meta.portal_url),
            f"/github/pull-requests/{repo_path}/{number}",
        )

    def upsert_persisted_pull_request_with_entities(self):
        """Upsert the persisted pull request on the DAPI server with the current entities."""

        # while we are dual writing, we want to capture and log all errors to sentry but
        # to keep going. Therefore we catch all exceptions, capture/log them to sentry, and
        # return in the instance of an error
        try:
            self.print_markdown_and_text(
                "\n\nBegin syncing to enable Woven Portal DevX...",
                color="green",
            )

            # the files that need to be persisted for udpating in the FE are:
            # - all files that have changed from the base commit
            # - all files that have changed from the current commit, even if
            #   they are now unchanged from the base commit
            # - plus all teams files
            all_changed_filepaths_from_base = {
                loc
                for loc_to_content in self.changed_files_from_base.contents_as_dict().values()
                for loc in loc_to_content.keys()
            }
            all_changed_filepaths_from_current = {
                loc
                for loc_to_content in self.changed_files.contents_as_dict().values()
                for loc in loc_to_content.keys()
            }
            teams_filepaths = set(self.all_files.teams.keys())
            subjects_filepaths = set(self.all_files.subjects.keys())
            categories_filepaths = set(self.all_files.categories.keys())
            number_persisted_files = len(
                all_changed_filepaths_from_base
                | all_changed_filepaths_from_current
                | teams_filepaths
                | subjects_filepaths
                | categories_filepaths
            )

            self.print_markdown_and_text(
                f"\nPersisting {number_persisted_files} OpenDAPI files in"
                f" batch size of {self.dapi_server_config.pr_sync_batch_size}",
                color="green",
            )

            # ensure that the PR is created, which is necessary for persisting entities
            self.dapi_requests.get_or_create_gh_pull_request()

            with click.progressbar(length=number_persisted_files) as progressbar:

                def _notify(progress: int):
                    """Notify the user to the progress."""
                    return self.print_dapi_server_progress(
                        progressbar, progress
                    )  # pragma: no cover

                persisted_pr_entities = (
                    self.dapi_requests.create_gh_pull_request_entities(
                        all_files=self.all_files,
                        base_commit_files=self.base_commit_files,
                        current_commit_files=self.current_commit_files,
                        changed_files_from_base=self.changed_files_from_base,
                        changed_files=self.changed_files,
                        enriched_files=self.all_files_enriched,
                        notify_function=_notify,
                        feature_validate_responses=self.feature_validate_responses,
                    )
                )

            self.print_markdown_and_text(
                "\nSuccess!\nNow updating the Woven Portal to reflect the changes...",
                color="green",
            )

            self.dapi_requests.upsert_gh_pull_request(
                woven_comment_id=self.existing_opendapi_comment_id,
                persisted_pr_entities_to_upsert=persisted_pr_entities,
            )

            self.print_markdown_and_text(
                "\nSuccess!",
                color="green",
            )

        except Exception as e:  # pylint: disable=broad-except
            self.print_markdown_and_text(str(e), color="red")
            sentry_sdk.capture_exception(e)
            # if we are in a dual write scenario, we want to continue even if there is an error
            # but if we are rolling out the portal based devx, we want to fail the action
            if self.use_portal_based_devx:
                raise e

    def create_empty_pr(self):
        """
        To be used if the PR has no schema changes.
        We still want the GithubPullRequest to be created for the PR, and to be in sync
        with commit_shas, and we must clear it of all previous persisted_pull_request_entities
        it was associated with.
        """
        self.print_markdown_and_text(
            "\n\nThis PR has no schema changes. Logging this for Woven Portal Observability.",
            color="yellow",
        )
        self.dapi_requests.upsert_gh_pull_request(
            woven_comment_id=self.existing_opendapi_comment_id,
            persisted_pr_entities_to_upsert=[],
        )

    def functions_to_run(self) -> List[Callable[[], Optional[DAPIServerResponse]]]:
        """Check if we should run the action."""
        # if this is not a pull request event, we only do things if there are files to process
        if self.trigger_event.is_push_event:

            if self._are_there_files_to_process():
                return [
                    *self.base_functions_to_run,
                    self.validate_features,
                    self.possibly_fail_github_action,
                ]
            return []

        # this is a pull request event

        # if there are files to process, so we run the entire validation and enrichment flow
        if self._are_there_files_to_process():
            # Dual write if portal based devX is not turned on
            if self.use_portal_based_devx:
                fns = [*self.base_functions_to_run]
            else:
                fns = [
                    *self.base_functions_to_run,
                    self.create_metadata_pr,
                ]

            return [
                *fns,
                self.validate_features,
                self.upsert_persisted_pull_request_with_entities,
                self.create_or_update_summary_comment_metadata_unsynced,
                self.possibly_fail_github_action,
            ]

        # there are no files to process, but there are schema changes, and so
        # we must comment with impact analysis etc.
        if not self.changed_files_from_base.is_empty:
            self.print_markdown_and_text(
                "\n\nThis PR contains schema changes, continuing with non-metadata analysis.",
                color="yellow",
            )
            return [
                self.maybe_analyze_impact,
                self.validate_features,
                # we must also update the persisted PR with the entities to ensure that the
                # head commit is up to date with the PR state, since otherwise
                # the commit will not be a fast forward, which is an issue
                # open question of if we just want to upsert with the current IDs or totally
                # rewrite the file state. since the content itself should not have changed, this
                # is the safest thing to do, since it ensures that "changed_from_current"
                # etc. is up to date. we can revisit this later if all we want to do is
                # update the head commit
                self.upsert_persisted_pull_request_with_entities,
                self.create_or_update_summary_comment_metadata_synced,
                self.possibly_fail_github_action,
            ]

        # the PR has no schema changes. We still want the GithubPullRequest to be created for the
        # PR, and to be in sync with commit_shas, and we must clear it of all
        # previous persisted_pull_request_entities it was associated with
        no_schema_changes_fns = [
            self.create_empty_pr,
        ]

        # the PR has no schema changes, we must delete opendapi comments if applicable
        # I.E. the PR had schema changes, but they were reverted, and so comment should be deleted
        if self.existing_opendapi_comment_id:
            self.print_markdown_and_text(
                "\n\nThis PR no longer contains schema changes, cleaning up PR presence.",
                color="yellow",
            )
            return [
                *no_schema_changes_fns,
                lambda: self.github_adapter.delete_comment(
                    self.existing_opendapi_comment_id
                ),
            ]

        return no_schema_changes_fns

    def validate_features(self) -> Optional[List[FeatureValidationResult]]:
        """
        Validate the features.
        """

        if not get_feature_flag(FeatureFlag.FEATURE_VALIDATION_ENABLED):
            return self.feature_validate_responses

        self.print_markdown_and_text(
            "\n\nValidating features...",
            color="green",
        )

        # get the validation response
        self.feature_validate_responses = self.dapi_requests.validate_features(
            all_files=self.all_files,
            changed_files=self.changed_files,
            changed_files_from_base=self.changed_files_from_base,
            base_commit_files=self.base_commit_files,
            current_commit_files=self.current_commit_files,
        )

        return self.feature_validate_responses

    def possibly_fail_github_action(self):
        """Check if we should fail the Github action on a pull request or push"""
        error_messages = []

        if not self.changed_files.is_empty:
            unsynced_dapis = sorted(self.changed_files.dapis.keys())
            txt = (
                "\n\nThe following DAPIs' metadata is not in sync with schema changes:"
            )
            for dapi in unsynced_dapis:
                txt += f"\n\t- {dapi}"  # pylint: disable=consider-using-join

            if self.trigger_event.is_pull_request_event and self.autoupdate_pr_number:
                pr_stanza = (
                    f"PR #{self.autoupdate_pr_number}"
                    if self.autoupdate_pr_number
                    else "A Woven-generated PR"
                )
                txt += (
                    f"\n{pr_stanza} with suggested metadata "
                    "updates was created for you to review."
                )

            self.print_markdown_and_text(
                txt,
                color="red",
            )
            error_messages.append("\n\t- Metadata is not in sync.")

        if self.validate_response and self.validate_response.errors:
            self.print_markdown_and_text(
                "\n\nYour DAPI files have validation errors, as listed "
                f"below:\n{json.dumps(self.validate_response.errors, indent=2)}",
                color="red",
            )
            error_messages.append(
                "\n\t- There are validation errors in the DAPI files."
            )

        if self._get_failed_features():
            self.print_markdown_and_text(
                "\n\nYour files have feature validation errors, as listed: "
                f"{self._create_feature_validation_comment_section()}",
                color="red",
            )
            error_messages.append(
                "\n\t- There are feature related validation errors in the DAPI files."
            )

        if error_messages:
            raise FailGithubAction("".join(error_messages))

    def create_metadata_pr(self):
        """
        In PRs, spin up another Auto-generated Github PR with new changes
        and leave a comment with that PR number and details on downstream impact
        """

        metrics_tags = {"org_name": self.config.org_name_snakecase}
        increment_counter(LogCounterKey.SUGGESTIONS_PR_CREATED, tags=metrics_tags)
        suggestions_count = len(self.validate_response.suggestions)
        increment_counter(
            LogCounterKey.SUGGESTIONS_FILE_COUNT,
            value=suggestions_count,
            tags=metrics_tags,
        )
        try:
            self.create_pull_request_for_changes()
        except RuntimeError as e:
            # only swalling the git commit issue
            if "git command ['git', 'commit', '-m'" in str(e):
                sentry_sdk.capture_exception(e)
                raise FailSilently(  # pylint: disable=raise-missing-from
                    "There was an error committing changes to the autoupdate branch",
                )
            raise e
        except GithubEnricherException as e:
            sentry_sdk.capture_exception(e)
            # this error already fails silently
            raise e

    def run(self):
        if self.trigger_event.is_pull_request_event:
            metrics_tags = {"org_name": self.config.org_name_snakecase}
            increment_counter(LogCounterKey.USER_PR_CREATED, tags=metrics_tags)
        super().run()
