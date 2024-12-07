"""Teams validator module"""

from typing import Dict, List, Tuple

from opendapi.defs import DATASTORES_SUFFIX, OPENDAPI_SPEC_URL, OpenDAPIEntity
from opendapi.validators.base import BaseValidator


class DatastoresValidator(BaseValidator):
    """
    Validator class for datastores files
    """

    SUFFIX = DATASTORES_SUFFIX
    SPEC_VERSION = "0-0-1"
    ENTITY = OpenDAPIEntity.DATASTORES

    # Paths & keys to use for uniqueness check within a list of dicts when merging
    MERGE_UNIQUE_LOOKUP_KEYS: List[Tuple[List[str], str]] = [(["datastores"], "urn")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.datastores_urn = self._collect_datastores_urn()

    def _collect_datastores_urn(self) -> List[str]:
        """Collect all the datastores urns"""
        datastores_urn = []
        for _, content in self.merged_file_state.items():
            for datastore in content["datastores"]:
                datastores_urn.append(datastore["urn"])
        return datastores_urn

    def _get_base_generated_files(self) -> Dict[str, Dict]:
        """Set Autoupdate templates in {file_path: content} format"""
        return {
            f"{self.base_destination_dir}/{self.config.org_name_snakecase}.datastores.yaml": {
                "schema": OPENDAPI_SPEC_URL.format(
                    version=self.SPEC_VERSION, entity="datastores"
                ),
                "datastores": [],
            }
        }
