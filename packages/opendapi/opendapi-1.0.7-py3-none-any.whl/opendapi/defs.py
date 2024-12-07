"""Constants and reusable definitions for the OpenDAPI Python client."""

from enum import Enum

TEAMS_SUFFIX = [".teams.yaml", ".teams.yml", ".teams.json"]
DATASTORES_SUFFIX = [".datastores.yaml", ".datastores.yml", ".datastores.json"]
PURPOSES_SUFFIX = [".purposes.yaml", ".purposes.yml", ".purposes.json"]
DAPI_SUFFIX = [".dapi.yaml", ".dapi.yml", ".dapi.json"]
SUBJECTS_SUFFIX = [".subjects.yaml", ".subjects.yml", ".subjects.json"]
CATEGORIES_SUFFIX = [".categories.yaml", ".categories.yml", ".categories.json"]
OPENDAPI_CONFIG_SUFFIX = [
    "opendapi.config.yaml",
    "opendapi.config.yml",
    "opendapi.config.json",
]
GITHUB_ACTIONS_SUFFIX = [".github/workflows/opendapi_ci.yml"]

ALL_OPENDAPI_SUFFIXES = (
    TEAMS_SUFFIX
    + DATASTORES_SUFFIX
    + PURPOSES_SUFFIX
    + DAPI_SUFFIX
    + OPENDAPI_CONFIG_SUFFIX
    + GITHUB_ACTIONS_SUFFIX
)

OPENDAPI_URL = "https://opendapi.org/"
OPENDAPI_SPEC_URL = OPENDAPI_URL + "spec/{version}/{entity}.json"

PLACEHOLDER_TEXT = "placeholder text"

CONFIG_FILEPATH_FROM_ROOT_DIR = "opendapi.config.yaml"
DEFAULT_DAPIS_DIR = "dapis"
GITHUB_ACTIONS_FILEPATH_FROM_ROOT_DIR = ".github/workflows/opendapi_ci.yml"
DEFAULT_DAPI_SERVER_HOSTNAME = "https://api.wovencollab.com"


class HTTPMethod(Enum):
    """HTTP methods."""

    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"


class OpenDAPIEntity(Enum):
    """The various opendapi entities"""

    CATEGORIES = "categories"
    DAPI = "dapi"
    DATASTORES = "datastores"
    PURPOSES = "purposes"
    SUBJECTS = "subjects"
    TEAMS = "teams"

    # legacy ones we need to remove after we are certain no
    # old PREs are in use
    SINGULAR_DATASTORE = "datastore"
    SINGULAR_PURPOSE = "purpose"
    SINGULAR_TEAM = "team"
