"""SqlAlchemy DAPI validator module"""

# pylint: disable=duplicate-code

import copy
import importlib
import os
import sys
from dataclasses import dataclass
from functools import cached_property
from multiprocessing import Pipe, Process, connection
from typing import TYPE_CHECKING, Dict, List, Optional

from opendapi.config import (
    construct_dapi_source_sink_from_playbooks,
    construct_owner_team_urn_from_playbooks,
    construct_project_full_path,
    get_project_path_from_full_path,
    is_model_in_allowlist,
)
from opendapi.defs import OPENDAPI_SPEC_URL
from opendapi.logging import logger
from opendapi.models import OverrideConfig
from opendapi.utils import find_files_with_suffix
from opendapi.validators.dapi.base import DapiValidator
from opendapi.validators.dapi.models import ProjectInfo

if TYPE_CHECKING:
    from sqlalchemy import MetaData, Table  # pragma: no cover

PROCESS_TIMEOUT = 120


@dataclass
class SqlAlchemyProjectInfo(ProjectInfo):
    """Data class for a sqlalchemy project information"""

    metadata_variable: Optional[str] = None

    def _sqlalchemy_column_type_to_dapi_datatype(self, column_type: str) -> str:
        """Convert the SQLAlchemy column type to DAPI data type"""
        return str(column_type).lower()

    def build_fields_for_table(self, table: "Table") -> List[Dict]:
        """Build the fields for the table"""
        fields = []
        for column in table.columns:
            fields.append(
                {
                    "name": str(column.name),
                    "data_type": self._sqlalchemy_column_type_to_dapi_datatype(
                        column.type
                    ),
                    "description": None,
                    "is_nullable": column.nullable,
                    "is_pii": None,
                    "access": "private",
                    "data_subjects_and_categories": [],
                    "sensitivity_level": None,
                    "is_personal_data": None,
                    "is_direct_identifier": None,
                }
            )
        fields.sort(key=lambda x: x["name"])
        return fields

    def build_primary_key_for_table(self, table: "Table") -> List[str]:
        """Build the primary key for the table"""
        primary_key = []
        for column in table.columns:
            if column.primary_key:
                primary_key.append(str(column.name))
        return primary_key

    def _get_tables(self):
        """Get the tables for the project"""
        # Import the module
        sys.path.append(self.full_path)
        module = importlib.import_module(self.override.artifact_path.replace("/", "."))
        metadata = getattr(module, self.metadata_variable)

        parsed_tables = [
            {
                "name": table.name,
                "fullname": table.fullname,
                "fields": self.build_fields_for_table(table),
                "primary_key": self.build_primary_key_for_table(table),
                "schema": table.schema,
            }
            for table in metadata.sorted_tables
        ]
        return parsed_tables

    def _tables(self, conn: connection.Connection):
        """Get the tables for the project"""
        # Import the module
        try:
            conn.send(self._get_tables())
        except Exception:
            logger.error(
                "Error generating tables from within %s:%s in %s",
                self.override.artifact_path,
                self.metadata_variable,
                self.full_path,
            )
            raise

    @cached_property
    def tables(self) -> List["Table"]:
        """Get the tables for the project"""

        # We import project levels modules in a separate process to avoid any side effects
        # that may occur when importing modules
        parent_conn, child_conn = Pipe(duplex=False)
        process = Process(target=self._tables, args=(child_conn,))
        process.start()
        process.join(PROCESS_TIMEOUT)

        if process.exitcode:
            raise ImportError(
                f"Error generating tables: {self.override.artifact_path}:{self.metadata_variable} "
                f"in {self.full_path}"
            )

        # Receive the sorted tables from the child process
        sorted_tables = parent_conn.recv()
        return sorted_tables


class SqlAlchemyDapiValidator(DapiValidator):
    """Validator class for DAPI files created for SQLAlchemy datasets"""

    INTEGRATION_NAME = "sqlalchemy"

    # App identifiers are comma separated values specified as the following:
    # "path.to.module:metadata"
    # "alembic/env.py:target_metadata
    # "path/to/app.py:metadata"
    # "path/to/sql_imports.py:sql_metadata"
    APP_IDENTIFIERS = "alembic/env.py:target_metadata"

    # Ignore the following file patterns when searching for schema files
    EXCLUDE_DIRS = []

    def build_datastores_for_table(
        self, project: SqlAlchemyProjectInfo, table_name: str
    ) -> Dict:
        """Build the datastores for the table"""
        return (
            construct_dapi_source_sink_from_playbooks(
                project.override.playbooks, table_name
            )
            if project.override.playbooks
            else {"sources": [], "sinks": []}
        )

    def build_urn_for_table(self, project: SqlAlchemyProjectInfo, table_name) -> str:
        """Build the urn for the table"""
        project_path = project.override.project_path
        return f"{project.org_name_snakecase}.{self.INTEGRATION_NAME}.{project_path}.{table_name}"

    def get_project(self, override_config: OverrideConfig) -> SqlAlchemyProjectInfo:
        """Given an project override configuration, return the project config"""

        override = copy.deepcopy(override_config)

        project_full_path = construct_project_full_path(
            self.root_dir, override.project_path
        )

        if override.artifact_path is None:
            raise ValueError("artifact_path is required in the configuration")

        artifact_path, metadata = override.artifact_path.split(":")

        if artifact_path.endswith(".py"):
            artifact_full_path = os.path.join(project_full_path, artifact_path)
            artifact_path = artifact_path[0:-3]
        else:
            artifact_full_path = artifact_path

        override.artifact_path = artifact_path

        project = SqlAlchemyProjectInfo(
            org_name_snakecase=self.config.org_name_snakecase,
            root_path=self.root_dir,
            override=override,
            full_path=project_full_path,
            artifact_full_path=artifact_full_path,
            metadata_variable=metadata,
        )

        return project

    def get_all_projects(self) -> List[SqlAlchemyProjectInfo]:
        """Get projects from all prisma schema files."""

        # App identifiers are comma separated values specified as the following:
        # "alembic/env.py:target_metadata
        # "path/to/app.py:metadata"
        # "path/to/sql_imports.py:sql_metadata"

        artifacts = [
            x.strip()
            for x in f"{self.settings.artifact_path or self.APP_IDENTIFIERS}".split(",")
        ]
        projects = []

        for entry in artifacts:
            app, metadata = entry.split(":")
            file_pattern = f"/{app}"
            import_files = find_files_with_suffix(
                self.root_dir, [file_pattern], exclude_dirs=self.EXCLUDE_DIRS
            )

            for import_file in import_files:
                base_dir = import_file.replace(file_pattern, "")
                project_path = get_project_path_from_full_path(self.root_dir, base_dir)
                artifact_path = get_project_path_from_full_path(base_dir, import_file)
                artifact_path = f"{artifact_path}:{metadata}"

                override = OverrideConfig(
                    project_path=project_path, artifact_path=artifact_path
                )
                projects.append(self.get_project(override))

        return projects

    def validate_projects(self, projects: List[SqlAlchemyProjectInfo]):
        """Verify that all projects and their schema files exist"""
        for project in projects:
            if not os.path.exists(project.full_path):
                raise FileNotFoundError(
                    f"Project path {project.full_path} does not exist"
                )

            if project.artifact_full_path.endswith(".py") and not os.path.exists(
                project.artifact_full_path
            ):
                raise FileNotFoundError(
                    f"Artifact path {project.artifact_full_path} does not exist"
                )

            if not project.metadata_variable:
                raise ValueError(
                    f"artifact_path misconfiguration for {project.override.project_path}"
                )

    def _get_dapis_for_project(self, project: SqlAlchemyProjectInfo) -> Dict[str, Dict]:
        """Build the base template for autoupdate for a given project"""
        result = {}

        for table in project.tables:

            if not is_model_in_allowlist(
                table["name"], project.full_path, project.override.model_allowlist
            ):
                continue

            # Note this includes the schema as well
            table_full_name = table["fullname"]

            result[project.construct_dapi_location(table_full_name)] = {
                "schema": OPENDAPI_SPEC_URL.format(
                    version=self.SPEC_VERSION,
                    entity="dapi",
                ),
                "urn": self.build_urn_for_table(project, table_full_name),
                "type": "entity",
                "description": None,
                "owner_team_urn": construct_owner_team_urn_from_playbooks(
                    project.override.playbooks, table_full_name, project.full_path
                ),
                "datastores": self.build_datastores_for_table(project, table_full_name),
                "fields": table["fields"],
                "primary_key": table["primary_key"],
                # TODO: Figure out how to get the service name and relative model path  # pylint: disable=W0511
                "context": {
                    "integration": self.INTEGRATION_NAME,
                    "db_schema": table["schema"],
                },
            }
        return result

    def _get_base_generated_files(self) -> Dict[str, Dict]:
        """Build the base template for autoupdate"""
        result = {}

        for project in self.selected_projects():
            result.update(self._get_dapis_for_project(project))

        return result
