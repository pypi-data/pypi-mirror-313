"""File adapter for OpenDAPI."""

import os
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

from opendapi.adapters.git import (
    add_named_stash,
    get_checked_out_branch_or_commit,
    get_git_diff_filenames,
    pop_named_stash,
    run_git_command,
)
from opendapi.config import OpenDAPIConfig
from opendapi.utils import write_to_yaml_or_json
from opendapi.validators.categories import CategoriesValidator
from opendapi.validators.dapi import BaseDapiValidator
from opendapi.validators.datastores import DatastoresValidator
from opendapi.validators.purposes import PurposesValidator
from opendapi.validators.subjects import SubjectsValidator
from opendapi.validators.teams import TeamsValidator


@dataclass
class OpenDAPIFileContents:
    """Set of OpenDAPI files."""

    teams: Dict[str, Dict]
    dapis: Dict[str, Dict]
    datastores: Dict[str, Dict]
    purposes: Dict[str, Dict]
    subjects: Dict[str, Dict]
    categories: Dict[str, Dict]
    config: OpenDAPIConfig

    @property
    def root_dir(self):
        """Return the root directory."""
        return self.config.root_dir

    def contents_as_dict(self):
        """Convert to a dictionary."""
        return {
            "teams": self.teams,
            "dapis": self.dapis,
            "datastores": self.datastores,
            "purposes": self.purposes,
            "subjects": self.subjects,
            "categories": self.categories,
        }

    def path_pruned_contents_as_dict(self):
        """Convert to a dictionary with the root dir pruned."""
        result = {}
        for result_key, contents in self.contents_as_dict().items():
            result[result_key] = {
                self.build_qualified_location_from_fullpath(location): json_content
                for location, json_content in contents.items()
            }
        return result

    @property
    def dapi_set(self):
        """Return the set of DAPIs."""
        return set(self.dapis.keys())

    @property
    def qualified_location_prefix(self):
        """Return the repository name."""
        return f"{self.config.urn}::"

    def build_qualified_location_from_fullpath(self, fullpath: str):
        """
        Build a qualified location from the full path.
        This is what DAPI server expects as the location.

        qualified location is my_config.my_repo::path/to/file
        example:
        root_dir = /tmp/repo
        config.urn = my_config.my_repo
        fullpath = /tmp/repo/path/to/file
        qualified location = my_config.my_repo::path/to/file
        """
        path_from_root = re.sub(self.root_dir, "", fullpath)
        return "".join([self.qualified_location_prefix, path_from_root.lstrip("/")])

    def build_fullpath_from_qualified_location(self, qualified_location: str):
        """
        Build a full path from the qualified location.

        full path is root_dir/path/to/file
        example:
        root_dir = /tmp/repo
        config.urn = my_config.my_repo
        qualified location = my_config.my_repo::path/to/file
        fullpath = /tmp/repo/path/to/file
        """
        location_without_repo = re.sub(
            self.qualified_location_prefix, "", qualified_location
        )
        return os.path.join(
            self.root_dir.rstrip("/"), location_without_repo.lstrip("/")
        )

    def build_location_without_repo_from_fullpath(self, fullpath: str):
        """
        Build a full path from the qualified location.

        full path is root_dir/path/to/file
        example:
        root_dir = /tmp/repo
        fullpath = /tmp/repo/path/to/file
        return path/to/file
        """
        return re.sub(self.root_dir, "", fullpath).lstrip("/")

    def for_server(self, writeable_location=False):
        """Convert to a format ready for the DAPI Server."""
        build_location = (
            self.build_location_without_repo_from_fullpath
            if writeable_location
            else self.build_qualified_location_from_fullpath
        )
        result = {}
        for result_key, contents in self.contents_as_dict().items():
            result[result_key] = {
                build_location(location): json_content
                for location, json_content in contents.items()
            }
        return result

    def for_server_filepaths(self, writeable_location=False):
        """Convert to a format ready for the DAPI Server."""
        files_for_server = self.for_server(writeable_location)
        return {
            opendapi_type: list(files.keys())
            for opendapi_type, files in files_for_server.items()
        }

    @property
    def is_empty(self):
        """Check if the contents are empty."""
        return len(self) == 0

    def __len__(self):
        length = 0
        for val in self.contents_as_dict().values():
            length += len(val)
        return length

    @classmethod
    def build_from_all_files(
        cls, repo_config: OpenDAPIConfig
    ) -> "OpenDAPIFileContents":
        """Get files from git state"""

        result: Dict[str, Dict[str, Dict]] = {}
        for result_key, validator_cls in {
            "teams": TeamsValidator,
            "dapis": BaseDapiValidator,
            "datastores": DatastoresValidator,
            "purposes": PurposesValidator,
            "subjects": SubjectsValidator,
            "categories": CategoriesValidator,
        }.items():
            result[result_key] = validator_cls(
                repo_config.root_dir,
                enforce_existence_at=None,
                override_config=repo_config,
            ).original_file_state
        return cls(**result, config=repo_config)

    @classmethod
    def build_from_all_files_at_commit(
        cls,
        repo_config: OpenDAPIConfig,
        commit: str,
    ) -> "OpenDAPIFileContents":
        """
        Get files from git state at a specific commit.
        To not conflict with generated/enriched state, we must stash and unstash wips.
        """
        branch_or_commit = get_checked_out_branch_or_commit(repo_config.root_dir)
        stash_created = add_named_stash(
            repo_config.root_dir, "build_from_all_files_at_commit"
        )
        run_git_command(repo_config.root_dir, ["git", "checkout", commit])
        od_fc = cls.build_from_all_files(repo_config)
        run_git_command(repo_config.root_dir, ["git", "checkout", "-"])
        if stash_created:
            pop_named_stash(repo_config.root_dir, "build_from_all_files_at_commit")
        run_git_command(repo_config.root_dir, ["git", "checkout", branch_or_commit])
        return od_fc

    def filter_changed_files(
        self, base_ref: str, current_ref: Optional[str] = None
    ) -> "OpenDAPIFileContents":
        """Get files changed between between two commits."""

        changed_files = get_git_diff_filenames(self.root_dir, base_ref, current_ref)
        result: Dict[str, Dict[str, Dict]] = {}
        for result_key, files in self.contents_as_dict().items():
            result[result_key] = {}
            for filename, file_contents in files.items():
                for changed_file in changed_files:
                    if filename.endswith(changed_file):
                        result[result_key][filename] = file_contents
        return OpenDAPIFileContents(**result, config=self.config)

    def update_dapis_with_suggestions(
        self, suggestions: Dict[str, Any]
    ) -> "OpenDAPIFileContents":
        """Update the DAPI files."""
        suggestions_with_full_path = {
            self.build_fullpath_from_qualified_location(filename): file_contents
            for filename, file_contents in suggestions.items()
        }
        dapis = self.dapis.copy()
        for filename, file_contents in suggestions_with_full_path.items():
            if filename in dapis:
                dapis[filename] = file_contents
                write_to_yaml_or_json(filename, file_contents)
        return OpenDAPIFileContents(
            teams=self.teams,
            dapis=dapis,
            datastores=self.datastores,
            purposes=self.purposes,
            config=self.config,
            subjects=self.subjects,
            categories=self.categories,
        )
