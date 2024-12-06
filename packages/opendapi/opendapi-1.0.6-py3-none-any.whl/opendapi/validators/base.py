# pylint: disable=too-many-instance-attributes
"""Validator class for DAPI and related files"""

from __future__ import annotations

import functools
import os
from abc import ABC, abstractmethod
from collections import defaultdict
from contextlib import contextmanager
from copy import deepcopy
from typing import Dict, Iterable, List, Optional, Set, Tuple, Type

import requests
from deepmerge import STRATEGY_END, Merger, extended_set
from jsonschema import ValidationError as JsonValidationError
from jsonschema import validate as jsonschema_validate

from opendapi.adapters.git import GitCommitStasher
from opendapi.cli.common import Schemas
from opendapi.config import OpenDAPIConfig
from opendapi.defs import DEFAULT_DAPIS_DIR, OpenDAPIEntity
from opendapi.logging import LogCounterKey, increment_counter
from opendapi.utils import (
    YAML,
    fetch_schema,
    find_files_with_suffix,
    prune_additional_properties,
    read_yaml_or_json,
    sort_dict_by_keys,
)
from opendapi.validators.defs import (
    CollectedFile,
    FileSet,
    MultiValidationError,
    ValidationError,
)


class BaseValidator(ABC):
    """Base validator class for DAPI and related files"""

    SUFFIX: List[str] = NotImplemented

    # Paths & keys to use for uniqueness check within a list of dicts when merging
    MERGE_UNIQUE_LOOKUP_KEYS: List[Tuple[List[str], str]] = []

    # Paths to disallow new entries when merging
    MERGE_DISALLOW_NEW_ENTRIES_PATH: List[List[str]] = []

    SPEC_VERSION: str = NotImplemented
    ENTITY: OpenDAPIEntity = NotImplemented

    def __init__(
        self,
        root_dir: str,
        enforce_existence_at: Optional[FileSet] = None,
        override_config: Optional[OpenDAPIConfig] = None,
        schema_to_prune_generated: Optional[Dict] = None,
        commit_sha: Optional[str] = None,
    ):
        self.schema_cache = {}
        self.yaml = YAML()
        self.root_dir = root_dir
        self.enforce_existence_at = enforce_existence_at
        self.config: OpenDAPIConfig = override_config or OpenDAPIConfig(root_dir)
        self.schema_to_prune_generated = schema_to_prune_generated
        self.commit_sha = commit_sha

        # we run file collection at __init__ time,
        # so that there is no confusion what the results will be if
        # collected_files is accessed later on
        _ = self.collected_files

    @property
    def base_destination_dir(self) -> str:
        """Get the base directory for the spec files"""
        return os.path.join(self.root_dir, DEFAULT_DAPIS_DIR)

    def _get_merger(self):
        """
        Get the merger object for deepmerge

        NOTE: merge() mutates - defend if necessary
        """

        def _get_match_using_lookup_keys(
            list_to_match: List, itm: Dict, lookup_keys: List[str]
        ) -> List[Dict]:
            """Get the match from the list using the lookup keys"""
            lookup_vals = [(k, itm.get(k)) for k in lookup_keys if itm.get(k)]
            return [
                n
                for n in list_to_match
                if lookup_vals and n.get(lookup_vals[0][0]) == lookup_vals[0][1]
            ]

        def _autoupdate_merge_strategy_for_dict_lists(config, path, base, nxt):
            """append items without duplicates in nxt to base and handles dict appropriately"""
            if (base and not isinstance(base[0], dict)) or (
                nxt and not isinstance(nxt[0], dict)
            ):
                return STRATEGY_END
            result = []
            autoupdate_unique_lookup_keys_for_path = [
                v for k, v in self.MERGE_UNIQUE_LOOKUP_KEYS if k == path
            ]
            for idx, itm in enumerate(base):
                filter_nxt_items = _get_match_using_lookup_keys(
                    nxt, itm, autoupdate_unique_lookup_keys_for_path
                )
                if filter_nxt_items:
                    result.append(
                        config.value_strategy(path + [idx], itm, filter_nxt_items[0])
                    )
                else:
                    result.append(itm)

            if path in self.MERGE_DISALLOW_NEW_ENTRIES_PATH:
                return result

            # Sort dict by keys to prevent duplicates because of YAML re-ordering
            result_as_set = extended_set.ExtendedSet(
                [sort_dict_by_keys(itm) for itm in result]
            )

            # This deduplicates the result - although not the intent, it is probably okay
            addable_candidates = [
                n for n in nxt if sort_dict_by_keys(n) not in result_as_set
            ]

            to_be_added = []

            if autoupdate_unique_lookup_keys_for_path:
                # Add only items from nxt ONLY
                # if they are not already merged earlier using the lookup keys
                #   OR if they are not already present in the result
                for itm in addable_candidates:
                    result_match = _get_match_using_lookup_keys(
                        result, itm, autoupdate_unique_lookup_keys_for_path
                    ) or _get_match_using_lookup_keys(
                        to_be_added, itm, autoupdate_unique_lookup_keys_for_path
                    )
                    if result_match:
                        continue

                    to_be_added.append(itm)
            else:
                to_be_added = addable_candidates

            return result + to_be_added

        return Merger(
            [
                (list, [_autoupdate_merge_strategy_for_dict_lists, "append_unique"]),
                (dict, "merge"),
                (set, "union"),
            ],
            ["override"],
            ["override"],
        )

    def _get_files_for_suffix(self, suffixes: List[str]):
        """Get all files in the root directory with given suffixes"""
        all_files = find_files_with_suffix(self.root_dir, suffixes)
        return [
            file
            for file in all_files
            if not file.endswith(OpenDAPIConfig.config_full_path(self.root_dir))
        ]

    def _read_yaml_or_json(self, file: str):
        """Read the file as yaml or json"""
        try:
            return read_yaml_or_json(file, self.yaml)
        except ValueError as exc:
            raise ValidationError(f"Unsupported file type for {file}") from exc

    @contextmanager
    def _maybe_git_commit_stash(self):
        """Stash the git commit if necessary"""
        if self.commit_sha:
            with GitCommitStasher(self.root_dir, "opendapi-validate", self.commit_sha):
                yield
        else:
            yield

    def _get_file_contents_for_suffix(self, suffixes: List[str]):
        """Get the contents of all files in the root directory with given suffixes"""
        files = self._get_files_for_suffix(suffixes)
        return {file: self._read_yaml_or_json(file) for file in files}

    def validate_existance_at(self, override: Optional[FileSet] = None):
        """Validate that the files exist"""
        fileset_map = {
            FileSet.ORIGINAL: self.original_file_state,
            FileSet.GENERATED: self.generated_file_state,
            FileSet.MERGED: self.merged_file_state,
        }
        check_at = override or self.enforce_existence_at
        if check_at and not fileset_map[check_at]:
            raise ValidationError(
                f"OpenDAPI {self.__class__.__name__} error: No files found in {self.root_dir}"
            )

    def _fetch_schema(self, jsonschema_ref: str) -> dict:
        """Fetch a schema from a URL and cache it in the requests cache"""
        try:
            self.schema_cache[jsonschema_ref] = self.schema_cache.get(
                jsonschema_ref
            ) or fetch_schema(jsonschema_ref)
        except requests.exceptions.RequestException as exc:
            error_message = f"Error fetching schema {jsonschema_ref}: {str(exc)}"
            raise ValidationError(error_message) from exc

        return self.schema_cache[jsonschema_ref]

    def validate_schema(self, file: str, content: Dict):
        """Validate the yaml file for schema adherence"""
        if "schema" not in content:
            raise ValidationError(f"Schema not found in {file}")

        jsonschema_ref = content["schema"]

        try:
            schema = self._fetch_schema(jsonschema_ref)
        except ValidationError as exc:
            error_message = f"Validation error for {file}: \n{str(exc)}"
            raise ValidationError(error_message) from exc

        try:
            jsonschema_validate(content, schema)
        except JsonValidationError as exc:
            error_message = f"Validation error for {file}: \n{str(exc)}"
            raise ValidationError(error_message) from exc

    @abstractmethod
    def _get_base_generated_files(self) -> Dict[str, Dict]:
        """
        Set Autoupdate templates in {file_path: content} format

        NOTE: unsafe to call this method directly, since if not checkout out
              to the correct commit, the output will be incorrect.
        """
        raise NotImplementedError

    @functools.cached_property
    def original_file_state(self) -> Dict[str, Dict]:
        """Collect the original file state"""
        with self._maybe_git_commit_stash():
            return self._get_file_contents_for_suffix(self.SUFFIX)

    @functools.cached_property
    def generated_file_state(self) -> Dict[str, Dict]:
        """Collect the raw generated file state"""
        with self._maybe_git_commit_stash():
            base_gen_files = self._get_base_generated_files()
            if self.schema_to_prune_generated:
                for file, content in base_gen_files.items():
                    # does no validation, just prunes the additional properties.
                    base_gen_files[file] = prune_additional_properties(
                        content, self.schema_to_prune_generated
                    )
            return {
                self.config.assert_dapi_location_is_valid(file): base_content
                for file, base_content in base_gen_files.items()
            }

    @functools.cached_property
    def merged_file_state(self) -> Dict[str, Dict]:
        """Merge the original and raw generated file states"""
        original_file_state = self.original_file_state
        generated_file_state = self.generated_file_state

        merged_file_state = {}
        for file in self.total_filepaths:
            self.config.assert_dapi_location_is_valid(file)
            original_content = original_file_state.get(file)
            generated_content = generated_file_state.get(file)

            if original_content is None:
                merged_content = generated_content

            elif generated_content is None:
                merged_content = original_content

            else:
                merged_content = self._get_merger().merge(
                    deepcopy(generated_content), deepcopy(original_content)
                )

            merged_file_state[file] = merged_content

        return merged_file_state

    def custom_content_validations(self, file: str, content: Dict):
        """Custom content validations if any desired"""

    def validate_content(self, file: str, content: Dict):
        """Validate the content of the files"""
        self.custom_content_validations(file, content)

    @property
    def base_tags(self) -> Dict:
        """Get the base tags for the validator"""
        return {
            "validator_type": self.__class__.__name__,
            "org_name": self.config.org_name_snakecase,
        }

    def _collect_validation_errors(
        self, file_to_content: Dict[str, Dict], fileset: FileSet
    ) -> List[str]:
        """Run the validators"""
        # Update the files after autoupdate
        # NOTE: think about if we want to use the minimal schema to validate
        #       here as well. Since dapi server does this, and since in
        #       the future we may want to validate after features run,
        #       we omit this for now.

        # Check if the files exist if enforce_existence is True
        if self.enforce_existence_at:
            self.validate_existance_at()

        # Collect the errors for all the files
        errors = []
        for file, content in file_to_content.items():
            try:
                self.validate_schema(file, content)
            except ValidationError as exc:
                errors.append(str(exc))
            else:
                try:
                    self.validate_content(file, content)
                except ValidationError as exc:
                    errors.append(str(exc))

        # Increment the counter for the number of items validated
        tags = {
            **self.base_tags,
            "fileset": fileset.value,
        }
        increment_counter(
            LogCounterKey.VALIDATOR_ITEMS,
            value=len(file_to_content),
            tags=tags,
        )
        return errors

    @functools.cached_property
    def _validation_errors(self) -> List[MultiValidationError]:
        """
        All of the validation errors
        """
        errors = self._collect_validation_errors(
            self.original_file_state, FileSet.ORIGINAL
        )
        errors.extend(
            self._collect_validation_errors(
                self.generated_file_state, FileSet.GENERATED
            )
        )
        errors.extend(
            self._collect_validation_errors(self.merged_file_state, FileSet.MERGED)
        )
        return errors

    def validate(self):
        """Validate the files"""
        errors = self._validation_errors
        if errors:
            # Increment the counter for the number of errors
            increment_counter(
                LogCounterKey.VALIDATOR_ERRORS,
                value=len(errors),
                tags=self.base_tags,
            )
            raise MultiValidationError(
                errors, f"OpenDAPI {self.__class__.__name__} error"
            )

    def get_validated_files(self) -> Dict[str, CollectedFile]:
        """Validate and return files"""
        self.validate()
        return self.collected_files

    @property
    def total_filepaths(self) -> Set[str]:
        """Get the total filepaths"""
        return self.original_file_state.keys() | self.generated_file_state.keys()

    @functools.cached_property
    def collected_files(self) -> Dict[str, CollectedFile]:
        """Return collected files"""
        return {
            file: CollectedFile(
                original=self.original_file_state.get(file),
                generated=self.generated_file_state.get(file),
                merged=self.merged_file_state[file],
                filepath=file,
                commit_sha=self.commit_sha,
                entity=self.ENTITY,
            )
            for file in self.total_filepaths
        }

    @staticmethod
    def _organize(
        results: List[CollectedFile],
    ) -> Dict[OpenDAPIEntity, Dict[str, CollectedFile]]:
        """Organize the results"""
        organized_results = defaultdict(dict)
        for result in results:
            if result.filepath in organized_results[result.entity]:
                raise ValueError(
                    f"Multiple results for {result.filepath} in {result.entity}"
                )
            organized_results[result.entity][result.filepath] = result
        return organized_results

    @classmethod
    def run_validators(
        cls,
        validators: Iterable[Type[BaseValidator]],
        root_dir: str,
        enforce_existence_at: Optional[FileSet] = None,
        override_config: Optional[OpenDAPIConfig] = None,
        minimal_schemas: Optional[Schemas] = None,
        commit_sha: Optional[str] = None,
    ) -> Tuple[
        Dict[OpenDAPIEntity, Dict[str, CollectedFile]], List[MultiValidationError]
    ]:
        """
        Run the validators, returning an output organized by entity, and sanity checking that
        there are no duplicate filepaths across entities.
        """
        collected_files = []
        errors = []
        for validator in validators:
            inst = validator(
                root_dir=root_dir,
                enforce_existence_at=enforce_existence_at,
                override_config=override_config,
                schema_to_prune_generated=(
                    minimal_schemas.minimal_schema_for(validator)
                    if minimal_schemas
                    else None
                ),
                commit_sha=commit_sha,
            )
            try:
                collected_files.extend(inst.get_validated_files().values())
            except MultiValidationError as e:
                errors.append(e)

        return cls._organize(collected_files), errors
