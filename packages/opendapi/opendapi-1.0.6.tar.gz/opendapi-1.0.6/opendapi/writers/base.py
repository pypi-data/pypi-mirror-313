"""Writers"""

import os
from typing import Dict, List, Optional, Tuple

from opendapi.config import OpenDAPIConfig
from opendapi.utils import YAML, fetch_schema, sorted_yaml_dump
from opendapi.validators.defs import CollectedFile


class BaseFileWriter:
    """Base Writer class for DAPI and related files"""

    def __init__(
        self,
        root_dir: str,
        collected_files: Dict[str, CollectedFile],
        override_config: OpenDAPIConfig = None,
        base_collected_files: Optional[Dict[str, CollectedFile]] = None,
        always_write: bool = False,
    ):
        self.yaml = YAML()
        self.root_dir = root_dir
        self.collected_files = collected_files
        self.config: OpenDAPIConfig = override_config or OpenDAPIConfig(root_dir)
        self.base_collected_files = base_collected_files or {}
        self.always_write = always_write

    def skip(
        self, collected_file: CollectedFile
    ) -> bool:  # pylint: disable=unused-argument
        """Skip file update if the content is the same"""
        return collected_file.original == collected_file.merged

    def write_files(self) -> Tuple[List[str], List[str]]:
        """Create or update the files"""
        written_files = []
        skipped_files = []
        for filepath, collected_file in self.collected_files.items():
            self.config.assert_dapi_location_is_valid(filepath)
            if self.always_write or not self.skip(collected_file):
                # Create the directory if it does not exist
                dir_name = os.path.dirname(filepath)
                os.makedirs(dir_name, exist_ok=True)

                written_files.append(filepath)
                with open(filepath, "w", encoding="utf-8") as file_handle:
                    jsonschema_ref = collected_file.merged.get("schema")
                    json_spec = fetch_schema(jsonschema_ref) if jsonschema_ref else None
                    sorted_yaml_dump(
                        collected_file.merged,
                        file_handle,
                        json_spec=json_spec,
                        yaml=self.yaml,
                    )
            else:
                skipped_files.append(filepath)
        return written_files, skipped_files
