# pylint: disable=too-many-instance-attributes
"""DAPI validator module"""

import copy
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property
from typing import Dict, List, Optional

from opendapi.config import (
    construct_dapi_source_sink_from_playbooks,
    construct_owner_team_urn_from_playbooks,
    construct_project_full_path,
    get_project_path_from_full_path,
    is_model_in_allowlist,
)
from opendapi.defs import OPENDAPI_SPEC_URL
from opendapi.feature_flags import FeatureFlag, get_feature_flag
from opendapi.logging import logger
from opendapi.models import OverrideConfig
from opendapi.utils import find_files_with_suffix, read_yaml_or_json
from opendapi.validators.dapi.base import DapiValidator
from opendapi.validators.dapi.mixins import DBTCloudMixin
from opendapi.validators.dapi.models import ProjectInfo

DBT_CONFIG_YML = "dbt_project.yml"
DBT_ARTIFACTS_DIR = "target"
DBT_MANIFEST_JSON = "manifest.json"
DBT_CATALOG_JSON = "catalog.json"


class ColumnTestType(Enum):
    """Column test type"""

    UNIQUE = "unique"
    NOT_NULL = "not_null"


class ConstraintType(Enum):
    """Constraint type"""

    PRIMARY_KEY = "primary_key"
    NOT_NULL = "not_null"


def _use_tests_for_base_template() -> bool:
    """Check if tests should be used for the base template"""
    return get_feature_flag(FeatureFlag.DBT_WRITEBACK_ENABLED)


@dataclass
class DBTProjectInfo(ProjectInfo):
    """DBT project"""

    name: Optional[str] = None
    dbt_config: Dict = field(default_factory=dict)

    @property
    def manifest_filename(self) -> str:
        """Get the manifest filename"""
        return DBT_MANIFEST_JSON

    @property
    def catalog_filename(self) -> str:
        """Get the catalog filename"""
        return DBT_CATALOG_JSON

    @property
    def catalog_path(self) -> str:
        """Get the catalog path"""
        return os.path.join(self.artifact_full_path, self.catalog_filename)

    @property
    def manifest_path(self) -> str:
        """Get the manifest path"""
        return os.path.join(self.artifact_full_path, self.manifest_filename)

    @cached_property
    def manifest(self) -> Dict:
        """Get the manifest"""
        return read_yaml_or_json(self.manifest_path)

    @cached_property
    def catalog(self) -> Dict:
        """Get the catalog"""
        return read_yaml_or_json(self.catalog_path)


@dataclass
class DBTColumn:
    """DBT column"""

    name: str
    catalog_info: Dict
    manifest_info: Dict
    tests_from_manifest: List[str]

    @property
    def data_type(self) -> str:
        """Get the data type"""
        return self.catalog_info["type"].lower()

    @property
    def manifest_description(self) -> str:
        """Get the description from the manifest"""
        return self.manifest_info.get("description")

    @property
    def has_primary_key_constraint(self) -> bool:
        """Check if the column has a primary key constraint"""
        if self.manifest_info.get("constraints"):
            for contract in self.manifest_info["constraints"]:
                if contract.get("type") == ConstraintType.PRIMARY_KEY.value:
                    return True
        if _use_tests_for_base_template():
            if ColumnTestType.UNIQUE.value in self.tests_from_manifest:
                return True
        return False

    @property
    def manifest_is_nullable(self) -> bool:
        """Check if the column is nullable"""
        if self.manifest_info.get("constraints"):
            for contract in self.manifest_info["constraints"]:
                if contract.get("type") == ConstraintType.NOT_NULL.value:
                    return False
        if _use_tests_for_base_template():
            if ColumnTestType.NOT_NULL.value in self.tests_from_manifest:
                return False
        return True

    @property
    def manifest_is_pii(self) -> bool:
        """Check if the column contains PII"""
        return self.manifest_info.get("meta", {}).get("contains_pii")

    def for_dapi(self) -> Dict:
        """Get the column for DAPI"""
        return {
            "name": self.name,
            "data_type": self.data_type,
            "description": self.manifest_description or None,
            "is_nullable": self.manifest_is_nullable,
            "is_pii": self.manifest_is_pii,
            "access": "private",
            "data_subjects_and_categories": [],
            "sensitivity_level": None,
            "is_personal_data": None,
            "is_direct_identifier": None,
        }


@dataclass
class DBTModel:
    """DBT model"""

    name: str
    unique_id: str
    project: DBTProjectInfo
    is_allowlisted: bool = True

    def _property_from_manifest(self, property_name: str) -> str:
        """Get a property from the manifest"""
        return self.project.manifest["nodes"][self.unique_id][property_name]

    def _property_from_catalog(self, property_name: str) -> str:
        """Get a property from the catalog"""
        return self.project.catalog["nodes"][self.unique_id][property_name]

    def get_column_tests_from_manifest(self) -> Dict[str, List[str]]:
        """Get the tests from the manifest"""
        tests_by_column_names = {}
        for node in self.project.manifest["nodes"].values():
            model_unique_id = node.get("attached_node")
            if (
                node.get("resource_type") == "test"
                and model_unique_id == self.unique_id
            ):
                test_name = node.get("test_metadata", {}).get("name")
                if test_name:
                    column_name = node.get("column_name")
                    tests_by_column_names.setdefault(column_name, []).append(test_name)
        return tests_by_column_names

    @property
    def schema(self) -> str:
        """Get the schema from the manifest"""
        return self._property_from_manifest("schema")

    @property
    def model_path(self) -> str:
        """Get the model path"""
        return f"{self.project.full_path}/{self._property_from_manifest('original_file_path')}"

    @property
    def doc_path(self) -> Optional[str]:
        """Get the doc path"""
        patch_path = self._property_from_manifest("patch_path")
        if patch_path:
            return f"{self.project.full_path}/{patch_path.split('://')[1]}"
        return None

    @property
    def manifest_table_description(self) -> str:
        """Get the table description from the manifest"""
        return self._property_from_manifest("description")

    @staticmethod
    def extract_columns_from_artifacts(
        manifest_columns: Dict,
        catalog_columns: Dict,
        column_tests: Dict[str, List[str]],
    ) -> List[DBTColumn]:
        """Extract column info from manifest and catalog columns"""
        columns = []
        for column_name, catalog_info in catalog_columns.items():
            manifest_info = manifest_columns.get(
                column_name.lower(),
                manifest_columns.get(column_name, {}),
            )
            columns.append(
                DBTColumn(
                    name=column_name.lower(),
                    catalog_info=catalog_info,
                    manifest_info=manifest_info,
                    tests_from_manifest=column_tests.get(column_name.lower(), []),
                )
            )
        return columns

    @property
    def columns(self) -> List[DBTColumn]:
        """Get the columns from the manifest and catalog"""
        manifest_columns = self._property_from_manifest("columns")
        catalog_columns = self._property_from_catalog("columns")
        column_tests = self.get_column_tests_from_manifest()
        return self.extract_columns_from_artifacts(
            manifest_columns, catalog_columns, column_tests
        )

    @property
    def primary_keys(self) -> List[str]:
        """Get the primary keys"""
        model_constraints = self._property_from_manifest("constraints")
        for constraint in model_constraints:
            if constraint.get("type") == ConstraintType.PRIMARY_KEY.value:
                return [x.lower() for x in constraint.get("columns")]
        column_names = []
        for column in self.columns:
            if column.has_primary_key_constraint:
                column_names.append(column.name.lower())
        return column_names

    def reconcile_custom_target_schema(self, target_schema: str) -> str:
        """
        Figure out production schema from the CI/dev manifest and config
        https://docs.getdbt.com/docs/build/custom-schemas
        """
        custom_schema = self._property_from_manifest("config").get("schema")
        current_schema = self.schema
        production_target_schema = target_schema
        if custom_schema:
            if not current_schema.endswith(custom_schema):
                # custom schema is not used in this current environment. But production uses it.
                # staging -> production_marketing
                return f"{production_target_schema}_{custom_schema}"
            current_schema_prefix = current_schema.split(custom_schema)[0]
            if current_schema_prefix:
                non_word_suffix = re.search(r"[\-\_]+$", current_schema_prefix)
                if non_word_suffix:
                    # replace target schema to production env
                    # but keep the non-word connector, typically underscore.
                    # staging_marketing -> production_marketing
                    return self.schema.replace(
                        current_schema_prefix,
                        f"{target_schema}{non_word_suffix.group(0)}",
                    )
            # target schema is not prefixed to the custom schema according to DBT setup.
            # marketing -> marketing
            return self.schema
        # No custom schema override so just use the target schema.
        # staging -> production
        return target_schema

    def construct_urn(self) -> str:
        """Construct the urn"""
        return f"{self.project.org_name_snakecase}.dbt.{self.project.name}.{self.name}"

    def construct_datastores(self) -> Dict:
        """Construct the datastores"""
        datastores = (
            construct_dapi_source_sink_from_playbooks(
                self.project.override.playbooks, self.name
            )
            if self.project.override.playbooks
            else {"sources": [], "sinks": []}
        )
        for source in datastores["sources"]:
            namespace = source.get("data", {}).get("namespace")
            if namespace:
                # some datastores don't have a db.schema namespace but just a schema
                if "." in namespace:
                    database, schema = namespace.split(".")[:2]
                    source["data"][
                        "namespace"
                    ] = f"{database}.{self.reconcile_custom_target_schema(schema)}"
                else:
                    source["data"]["namespace"] = self.reconcile_custom_target_schema(
                        namespace
                    )
        return datastores

    def construct_owner_team_urn(self) -> Optional[str]:
        """Construct the owner team urn"""
        return (
            construct_owner_team_urn_from_playbooks(
                self.project.override.playbooks, self.name, self.model_path
            )
            if self.project.override.playbooks
            else None
        )


class DbtDapiValidator(DapiValidator, DBTCloudMixin):
    """
    Validator class for DAPIs created from DBT models

    """

    INTEGRATION_NAME = "dbt"

    def get_all_dbt_config_files(self) -> List[str]:
        """Get all the dbt config files"""
        return find_files_with_suffix(
            self.root_dir,
            [f"/{self.settings.artifact_path or DBT_CONFIG_YML}"],
            exclude_dirs=["dbt_packages"],
        )

    def get_owner_team_urn_for_table(self, table: DBTModel) -> Optional[str]:
        """Get the owner team urn for the table"""

    def get_all_projects(self) -> List[DBTProjectInfo]:
        """List the DBT projects to generate documentation for"""
        projects = []

        for config_full_path in self.get_all_dbt_config_files():
            # glob for a file called dbt_project.yml within the dbt project
            project_full_path = os.path.normpath(os.path.dirname(config_full_path))

            override = OverrideConfig(
                project_path=get_project_path_from_full_path(
                    self.root_dir, project_full_path
                ),
                artifact_path=DBT_ARTIFACTS_DIR,
            )

            projects.append(self.get_project(override))

        return projects

    def get_project(self, override_config: OverrideConfig) -> DBTProjectInfo:
        """Given a project override config, return an ProjectConfig object"""

        override = copy.deepcopy(override_config)
        project_full_path = construct_project_full_path(
            self.root_dir, override.project_path
        )

        override.artifact_path = override.artifact_path or DBT_ARTIFACTS_DIR
        artifact_full_path = os.path.join(project_full_path, override.artifact_path)

        config_full_path = os.path.join(project_full_path, DBT_CONFIG_YML)
        dbt_config = read_yaml_or_json(config_full_path)

        return DBTProjectInfo(
            org_name_snakecase=self.config.org_name_snakecase,
            name=dbt_config["name"],
            dbt_config=dbt_config,
            root_path=self.root_dir,
            override=override_config,
            full_path=os.path.normpath(project_full_path),
            artifact_full_path=artifact_full_path,
        )

    def _sync_from_external_sources(self, projects: List[DBTProjectInfo]) -> None:
        """This function will sync the dbt projects from external sources"""

        print("DBT: About to check external sources for artifacts")
        # We will run through all the external sync functions, in order, till any function
        # returns True
        self.sync_dbt_cloud_artifacts(projects)
        # or self.sync_dbt_snowflake_artifacts(projects)
        # or self.sync_dbt_bigquery_artifacts(projects)

    def _assert_necessary_files_exist(self, projects: List[DBTProjectInfo]) -> None:
        """Assert that the necessary files exist"""
        errors = []
        for project in projects:
            try:
                project.manifest
            except FileNotFoundError:
                errors.append(
                    f"Manifest file not found for project {project.name} at {project.full_path}"
                )

            try:
                project.catalog
            except FileNotFoundError:
                errors.append(
                    f"Catalog file not found for project {project.name} at {project.full_path}"
                )

        if errors:
            raise FileNotFoundError("\n".join(errors))

    def validate_projects(self, projects: List[DBTProjectInfo]):
        """Verify that all projects and their schema files exist"""
        self._assert_necessary_files_exist(projects)

    def selected_projects(self, validate: bool = False) -> List[DBTProjectInfo]:
        """Get the selected projects"""

        # Get the projects, but do not validate them yet. If we are using
        # integrations like dbt cloud, we might have to wait till later to
        # ensure all the files are synced
        projects = super().selected_projects(validate=validate)

        # Try getting dbt files from dbt cloud or other sources. If integrated
        # with various other projects, the manifest and catalog files will be
        # synced from those sources.
        self._sync_from_external_sources(projects)

        # Validate that the selected projects exist
        self.validate_projects(projects)

        return projects

    def get_dbt_models(self) -> List[Dict]:
        """Get the DBT models from manifest.json and enrich with catalog.json"""
        dbt_models = []
        models_missing_in_catalog = []
        for project in self.selected_projects():
            for unique_model_name, model in project.manifest["nodes"].items():
                if (
                    model["resource_type"] == "model"
                    and model["config"]["materialized"] != "ephemeral"
                ):
                    if unique_model_name not in project.catalog["nodes"]:
                        # Log a warning if the model is not found in the catalog
                        models_missing_in_catalog.append(unique_model_name)
                        continue
                    dbt_model = DBTModel(
                        name=model["name"],
                        unique_id=unique_model_name,
                        project=project,
                        is_allowlisted=is_model_in_allowlist(
                            model["name"],
                            os.path.join(
                                project.full_path, model["original_file_path"]
                            ),
                            project.override.model_allowlist,
                        ),
                    )
                    dbt_models.append(dbt_model)
        if models_missing_in_catalog:
            logger.warning(
                "%s models are missing in catalog.json - "
                "please run the following to fix:"
                "\n\n1. dbt run --models %s"
                "\n\n2. dbt docs generate",
                len(models_missing_in_catalog),
                " ".join(models_missing_in_catalog),
            )
        return dbt_models

    def _get_base_generated_files(self) -> Dict[str, Dict]:
        result = {}
        for table in self.get_dbt_models():
            if table.is_allowlisted:
                dapi_location = table.project.construct_dapi_location(table.name)

                context = {
                    "service": table.project.name,
                    "integration": "dbt",
                    "rel_model_path": os.path.relpath(
                        table.model_path,
                        os.path.dirname(dapi_location),
                    ),
                }
                if table.doc_path:
                    context["rel_doc_path"] = os.path.relpath(
                        table.doc_path,
                        os.path.dirname(dapi_location),
                    )

                result[dapi_location] = {
                    "schema": OPENDAPI_SPEC_URL.format(
                        version=self.SPEC_VERSION,
                        entity="dapi",
                    ),
                    "urn": table.construct_urn(),
                    "type": "entity",
                    "description": table.manifest_table_description or None,
                    "owner_team_urn": table.construct_owner_team_urn()
                    or self.get_owner_team_urn_for_table(table),
                    "datastores": table.construct_datastores(),
                    "fields": [field.for_dapi() for field in table.columns],
                    "primary_key": table.primary_keys,
                    "context": context,
                }
        return result
