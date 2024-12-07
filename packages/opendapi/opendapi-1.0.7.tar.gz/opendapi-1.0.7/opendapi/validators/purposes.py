"""Teams validator module"""

from typing import Dict, List, Tuple

from opendapi.defs import OPENDAPI_SPEC_URL, PURPOSES_SUFFIX, OpenDAPIEntity
from opendapi.validators.base import BaseValidator


class PurposesValidator(BaseValidator):
    """
    Validator class for Purposes files
    """

    SUFFIX = PURPOSES_SUFFIX
    SPEC_VERSION = "0-0-1"
    ENTITY = OpenDAPIEntity.PURPOSES

    # Paths & keys to use for uniqueness check within a list of dicts when merging
    MERGE_UNIQUE_LOOKUP_KEYS: List[Tuple[List[str], str]] = [(["purposes"], "urn")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.purposes_urn = self._collect_purposes_urn()

    def _collect_purposes_urn(self) -> List[str]:
        """Collect all the purposes urns"""
        purposes_urn = []
        for _, content in self.merged_file_state.items():
            for purpose in content["purposes"]:
                purposes_urn.append(purpose["urn"])
        return purposes_urn

    def _get_base_generated_files(self) -> Dict[str, Dict]:
        """Set Autoupdate templates in {file_path: content} format"""
        return {
            f"{self.base_destination_dir}/{self.config.org_name_snakecase}.purposes.yaml": {
                "schema": OPENDAPI_SPEC_URL.format(
                    version=self.SPEC_VERSION, entity="purposes"
                ),
                "purposes": [],
            }
        }
