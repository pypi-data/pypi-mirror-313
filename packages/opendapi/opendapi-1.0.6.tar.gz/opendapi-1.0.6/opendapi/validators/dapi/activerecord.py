# pylint: disable=too-many-locals, too-many-function-args, duplicate-code
"""ActiveRecord DAPI validators."""

import copy
import os
from dataclasses import dataclass
from typing import Dict, List
from typing import Optional as OptionalType

from pyparsing import Dict as DictParser
from pyparsing import (
    Group,
    Literal,
    OneOrMore,
    Optional,
    QuotedString,
    Regex,
    Suppress,
    Word,
    ZeroOrMore,
    alphanums,
    nums,
)

from opendapi.config import (
    construct_dapi_source_sink_from_playbooks,
    construct_owner_team_urn_from_playbooks,
    construct_project_full_path,
    get_project_path_from_full_path,
    is_model_in_allowlist,
)
from opendapi.defs import OPENDAPI_SPEC_URL
from opendapi.models import OverrideConfig, PlaybookConfig
from opendapi.utils import find_files_with_suffix
from opendapi.validators.dapi.base import DapiValidator
from opendapi.validators.dapi.models import ProjectInfo


@dataclass
class Column:
    """Data class for a column in a table in a rails project schema."""

    column_type: str
    column_name: str
    column_options: dict

    def for_dapi(self) -> dict:
        """Return the column as a dictionary for DAPI."""
        return {
            "name": self.column_name,
            "data_type": self.column_type,
            "description": None,
            "is_pii": None,
            "is_nullable": not self.column_options.get("null") == "false",
            "access": "private",
            "data_subjects_and_categories": [],
            "sensitivity_level": None,
            "is_personal_data": None,
            "is_direct_identifier": None,
        }


@dataclass
class Index:
    """Data class for an index in a table in a rails project schema."""

    table_name: str
    index_columns: List[str]
    index_options: dict


@dataclass
class Table:  # pylint: disable=too-many-instance-attributes
    """Data class for a table in a rails project schema."""

    table_name: str
    table_options: dict
    parsed_columns: List[Column]
    parsed_indices: List[Index]
    project_full_path: str
    schema_full_path: str
    org_name_snakecase: str
    playbooks: OptionalType[List[PlaybookConfig]] = None
    is_allowlisted: bool = True

    def construct_urn(self) -> str:
        """Construct the URN for the table."""
        return f"{self.org_name_snakecase}.activerecord.{self.project_name}.{self.table_name}"

    def construct_datastores(self) -> List[str]:
        """Get the datastores for the table."""
        return (
            construct_dapi_source_sink_from_playbooks(self.playbooks, self.table_name)
            if self.playbooks
            else {"sources": [], "sinks": []}
        )

    def construct_team_urn(self) -> OptionalType[str]:
        """Construct the team URN for the table."""
        return (
            construct_owner_team_urn_from_playbooks(
                self.playbooks, self.table_name, self.schema_full_path
            )
            if self.playbooks
            else None
        )

    @property
    def columns(self) -> List[Column]:
        """Get the columns in the table."""
        additional_columns = self.parsed_columns.copy()
        id_option = self.table_options.get("id", "true")
        primary_key_option = self.table_options.get("primary_key", "id")
        if id_option != "false":
            if id_option == "true":
                additional_columns.append(
                    Column("bigint", "id", {"null": "false", "primary_key": "true"})
                )
            elif isinstance(primary_key_option, str):
                additional_columns.append(
                    Column(
                        id_option,
                        primary_key_option,
                        {"null": "false", "primary_key": "true"},
                    )
                )
            else:
                additional_columns.append(
                    Column(id_option, "id", {"null": "false", "primary_key": "true"})
                )

        return additional_columns

    @property
    def primary_keys(self) -> List[str]:
        """Get the primary keys in the table."""
        table_option_primary_key = self.table_options.get("primary_key")
        if table_option_primary_key:
            if isinstance(table_option_primary_key, str):
                return [table_option_primary_key]
            return list(table_option_primary_key)

        # Case when the primary key is not specified in the table options
        columns_with_primary_key = []
        for column in self.columns:
            if column.column_options.get("primary_key") == "true":
                columns_with_primary_key.append(column.column_name)
        return list(columns_with_primary_key)

    @property
    def project_name(self) -> str:
        """Get the name of the project."""
        return os.path.basename(self.project_full_path)


@dataclass
class ActiveRecordProjectInfo(ProjectInfo):
    """Data class for a rails project information"""

    @property
    def tables(self) -> List[Table]:
        """Get the tables in the schema."""

        # Define pyparsing elements
        integer_or_float = Word(nums + ".")
        boolean = Literal("true") | Literal("false")
        nil = Literal("nil")
        identifier = Word(alphanums + "_")
        quoted_string = QuotedString('"', escChar="\\")
        string_array = Group(
            Suppress("[")
            + ZeroOrMore(quoted_string + Optional(Suppress(",")))
            + Suppress("]")
        )
        arrows = Literal("->") | Literal("=>")
        ruby_symbol = Suppress(":") + identifier
        comment_line = Suppress("#") + Regex(".*")
        non_matching_character = Regex(".{1,}")

        option_val_simple = (
            quoted_string
            | integer_or_float
            | boolean
            | string_array
            | ruby_symbol
            | nil
        )
        # t.primary_key "id", :uuid, default: { "gen_random_uuid()" }
        option_val_set = (
            Suppress("{")
            + OneOrMore(option_val_simple + Optional(Suppress(",")))
            + Suppress("}")
        )
        # t.primary_key "id", :uuid, default: -> { key1: "gen_random_uuid()" }
        option_val_dict = DictParser(
            ZeroOrMore(
                Group(
                    Suppress("{")
                    + identifier
                    + Suppress(":")
                    + Optional(Suppress(arrows))
                    + option_val_simple
                    + Optional(Suppress(","))
                    + Suppress("}")
                )
            )
        )
        option_value = option_val_simple | option_val_set | option_val_dict
        options = DictParser(
            ZeroOrMore(
                Group(
                    identifier
                    + Suppress(":")
                    + Optional(Suppress(arrows))
                    + option_value
                    + Optional(Suppress(","))
                )
            )
        )

        # create_table "table_name", id: :uuid, primary_key: "custom_id", force: true do |t|
        table_start = Group(
            Suppress("create_table")
            + quoted_string("table_name")
            + Optional(Suppress(",") + options("table_options"))
            + Suppress("do")
            + Suppress("|t|")
        )

        # t.string "column_name", limit: 255, null: false
        column_parser = Group(
            Suppress("t.")
            + identifier("column_type")
            + quoted_string("column_name")
            + Optional(Suppress(","))
            + Optional(options("column_options"))
        )
        t_index_parser = Group(
            Suppress("t.index")
            + (quoted_string | string_array)("index_columns")
            + Optional(Suppress(","))
            + Optional(options("index_options"))
        )
        t_primary_key_parser = Group(
            Suppress("t.primary_key")
            + (quoted_string | string_array)("primary_key")
            + Optional(Suppress(","))
            + Optional(quoted_string | ruby_symbol)("primary_key_type")
            + Optional(Suppress(","))
            + Optional(options("primary_key_options"))
        )
        non_matching_column_parser = Suppress("t.") + non_matching_character
        columns_parser = ZeroOrMore(
            t_primary_key_parser
            | t_index_parser
            | column_parser
            | Suppress(comment_line)
            | Suppress(non_matching_column_parser)
        )

        # end
        table_end = Suppress("end")

        # ActiveRecord::Schema.define(version: 202202062227) do
        # ActiveRecord::Schema[7.1].define(version: 2024_01_10_212207) do
        rails_version = Suppress("[") + Word(alphanums + ".") + Suppress("]")
        version_parser = (
            Suppress("ActiveRecord::Schema")
            + Optional(rails_version)
            + Suppress(".define(version:")
            + integer_or_float("version")
            + Suppress(") do")
        )

        # Comment parser
        comments_parser = Group(comment_line)

        # Group the table elements
        tables_parser = Group(
            table_start("table_info") + columns_parser("columns") + table_end
        ).setResultsName("table")

        # add_index "table_name", ["column_name", "column_name"], name: "index_name"
        index_column = string_array | quoted_string
        add_indices_parser = Group(
            Suppress("add_index")
            + quoted_string("table_name")
            + Suppress(",")
            + index_column("index_columns")
            + Optional(Suppress(","))
            + Optional(options("index_options"))
        )

        # Combine the parsers
        full_parser = ZeroOrMore(
            version_parser
            | comments_parser
            | tables_parser
            | add_indices_parser
            | non_matching_character
        )("elements")

        # Parse the Ruby schema.rb content
        result = full_parser.parseFile(self.artifact_full_path)

        # Extract tables and indices separately
        tables = []
        for table in result["elements"]:
            if "table_info" in table:
                table_name = table["table_info"]["table_name"]
                table_options = table["table_info"]["table_options"]
                columns = {}
                # construct obvious columns
                for column in table["columns"]:
                    if "column_name" in column:
                        columns[column["column_name"]] = Column(
                            column["column_type"],
                            column["column_name"],
                            column["column_options"],
                        )
                # Parse the t.primary_key and add the primary key to the columns
                for column in table["columns"]:
                    # Found t.primary_key - just update the table options accordingly
                    if "primary_key" in column:
                        table_options["primary_key"] = column["primary_key"]
                        table_options["id"] = column.get("primary_key_type", "bigint")
                        table_options["primary_key_options"] = column.get(
                            "primary_key_options", {}
                        )
                # Gather indices
                indices = []
                for index in result["elements"]:
                    if "index_columns" in index and str(index["table_name"]) == str(
                        table_name
                    ):
                        indices.append(
                            Index(
                                str(index["table_name"]),
                                dict(index["index_columns"]),
                                dict(index["index_options"]),
                            )
                        )

                # Parse the t.index and add to indices
                for column in table["columns"]:
                    if "index_columns" in column:
                        indices.append(
                            Index(
                                table_name,
                                dict(column["index_columns"]),
                                dict(column["index_options"]),
                            )
                        )

                tables.append(
                    Table(
                        str(table_name),
                        dict(table_options),
                        list(columns.values()),
                        indices,
                        self.full_path,
                        self.artifact_full_path,
                        self.org_name_snakecase,
                        self.override.playbooks,
                        is_model_in_allowlist(
                            str(table_name),
                            self.artifact_full_path,
                            self.override.model_allowlist,
                        ),
                    )
                )

        return tables


class ActiveRecordDapiValidator(DapiValidator):
    """
    Validator class for DAPI files created for Rails ActiveRecord.
    """

    INTEGRATION_NAME = "activerecord"
    SCHEMA_FILE_PATH_SUFFIX = "db/schema.rb"

    def _assert_schema_files_exist(self, projects: List[ActiveRecordProjectInfo]):
        """Assert that the schema files exist."""
        errors = []
        for project in projects:
            if not os.path.exists(project.artifact_full_path):
                errors.append(
                    f"ActiveRecord Schema file {project.artifact_full_path} "
                    f"not found for project {project.full_path}"
                )
        if errors:
            raise FileNotFoundError("/n".join(errors))

    def get_all_projects(self) -> List[ActiveRecordProjectInfo]:
        """Generate a list of all projects that this validator should check"""

        schema_file_suffix = (
            f"/{self.settings.artifact_path or self.SCHEMA_FILE_PATH_SUFFIX}"
        )
        all_schema_files = find_files_with_suffix(self.root_dir, [schema_file_suffix])

        projects = []
        for schema_file in all_schema_files:
            base_dir = schema_file.replace(schema_file_suffix, "")
            project_path = get_project_path_from_full_path(self.root_dir, base_dir)
            artifact_path = get_project_path_from_full_path(base_dir, schema_file)

            override = OverrideConfig(
                project_path=project_path, artifact_path=artifact_path
            )

            projects.append(self.get_project(override))

        return projects

    def get_project(self, override_config: OverrideConfig) -> ActiveRecordProjectInfo:
        """Given a project override config, return an ProjectConfig object"""

        override = copy.copy(override_config)
        project_full_path = construct_project_full_path(
            self.root_dir, override.project_path
        )

        override.artifact_path = (
            override.artifact_path or f"{self.SCHEMA_FILE_PATH_SUFFIX}"
        )

        return ActiveRecordProjectInfo(
            org_name_snakecase=self.config.org_name_snakecase,
            root_path=self.root_dir,
            override=override,
            full_path=project_full_path,
            artifact_full_path=os.path.join(project_full_path, override.artifact_path),
        )

    def validate_projects(self, projects: List[ActiveRecordProjectInfo]):
        """Validate the projects"""
        self._assert_schema_files_exist(projects)

    def get_owner_team_urn_for_table(self, table: Table) -> str:
        """Get the owner team URN for a table."""

    def _get_base_generated_files(self) -> Dict[str, Dict]:
        result = {}
        for project in self.selected_projects():
            for table in project.tables:
                if table.is_allowlisted:
                    dapi_location = project.construct_dapi_location(table.table_name)
                    result[dapi_location] = {
                        "schema": OPENDAPI_SPEC_URL.format(
                            version=self.SPEC_VERSION,
                            entity="dapi",
                        ),
                        "type": "entity",
                        "urn": table.construct_urn(),
                        "owner_team_urn": table.construct_team_urn()
                        or self.get_owner_team_urn_for_table(table),
                        "description": None,
                        "datastores": table.construct_datastores(),
                        "fields": [field.for_dapi() for field in table.columns],
                        "primary_key": table.primary_keys,
                        "context": {
                            "service": table.project_name,
                            "integration": "activerecord",
                            "rel_model_path": os.path.relpath(
                                project.artifact_full_path,
                                os.path.dirname(dapi_location),
                            ),
                        },
                    }
        return result
