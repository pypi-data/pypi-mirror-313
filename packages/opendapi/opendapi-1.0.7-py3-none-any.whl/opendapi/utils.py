"""Utility functions for the OpenDAPI client."""

# pylint: disable=unnecessary-lambda-assignment

import base64
import importlib
import inspect
import io
import json
import os
import re
from copy import deepcopy
from typing import Any, Dict, List, Optional, TextIO, Tuple

import jsonref
import requests
import requests_cache
from jsonschema import validators
from jsonschema.validators import validator_for
from ruamel.yaml import YAML as _YAML
from ruamel.yaml import CommentedMap

from opendapi.defs import OPENDAPI_URL, HTTPMethod
from opendapi.logging import logger

session = requests_cache.CachedSession(
    "opendapi_schema_cache", expire_after=300, backend="memory"
)


class YAML(_YAML):
    """YAML class for OpenDAPI"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable aliasing
        self.representer.ignore_aliases = lambda *_: True


def get_root_dir_fullpath(current_filepath: str, root_dir_name: str):
    """Get the full path of the root directory"""
    return os.path.join(
        f"/{root_dir_name}".join(
            os.path.dirname(os.path.abspath(current_filepath)).split(root_dir_name)[:-1]
        ),
        root_dir_name,
    )


def find_subclasses_in_directory(
    root_dir: str, base_class, exclude_dirs: List[str] = None
):
    """Find subclasses of a base class in modules in a root_dir"""
    subclasses = []
    filenames = find_files_with_suffix(root_dir, [".py"], exclude_dirs=exclude_dirs)
    for py_file in filenames:
        rel_py_file = py_file.split(f"{root_dir}/")[1]
        module_name = rel_py_file.replace("/", ".").replace(".py", "")
        try:
            module = importlib.import_module(module_name)
            for _, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, base_class)
                    and obj != base_class
                    and obj not in subclasses
                ):
                    subclasses.append(obj)
        except Exception as exc:  # pylint: disable=broad-except
            logger.warning("Could not import module %s with %s", module_name, str(exc))
    return subclasses


def find_files_with_suffix(
    root_dir: str, suffixes: List[str], exclude_dirs: List[str] = None
):
    """Find files with a suffix in a root directory"""
    files = []
    default_exclude_dirs = [
        "__pycache__",
        ".git",
        "node_modules",
        ".git",
        ".venv",
        "virtualenv",
        ".virtualenv",
        "venv",
        "env",
        "dist",
        "migrations",
        "tmp",
        "temp",
        "cache",
        "dbt_packages",
        "packages",
        "Test",
        "test",
        "Tests",
        "tests",
        "e2e",
    ]
    all_exclude_dirs = (
        exclude_dirs + default_exclude_dirs if exclude_dirs else default_exclude_dirs
    )
    exclude_dirs_pattern = re.compile(r"^(?:" + "|".join(all_exclude_dirs) + r")$")
    for root, dirs, filenames in os.walk(root_dir, topdown=True):
        dirs[:] = [d for d in dirs if not exclude_dirs_pattern.match(d)]
        for filename in filenames:
            full_filepath = os.path.join(root, filename)
            if full_filepath.endswith(tuple(suffixes)):
                files.append(full_filepath)
    return files


def deep_get_dict(dct, path=None):
    """Get a value from a nested dict"""
    if not path:
        path = []
    for key in path:
        if key in dct:
            dct = dct[key]
        else:
            return None
    return dct


def make_snake_case(string: str) -> str:
    """Convert a string to snake case"""
    return re.sub(r"[\s\-\.]+", "_", string).lower()


def read_yaml_or_json(filepath: str, yaml: YAML = None) -> dict:
    """Read a yaml or json file"""
    yaml = yaml or YAML()
    with open(filepath, "r", encoding="utf-8") as filepath_handle:
        if filepath.endswith(".yaml") or filepath.endswith(".yml"):
            return yaml.load(filepath_handle.read())
        if filepath.endswith(".json"):
            return json.load(filepath_handle)
    raise ValueError(f"Unsupported filepath type for {filepath}")


def _write_to_io(
    filepath: str, data: dict, io_: TextIO, yaml: YAML, json_spec: Optional[dict] = None
) -> None:
    """Write a dict as yaml or json file format to the io object"""
    if filepath.endswith(".yaml") or filepath.endswith(".yml"):
        # this mutates the data, so we deepcopy it
        sorted_yaml_dump(deepcopy(data), io_, json_spec=json_spec, yaml=yaml)
    elif filepath.endswith(".json"):
        json.dump(data, io_, indent=4)
    else:
        raise ValueError(f"Unsupported filepath type for {filepath}")


def write_to_yaml_or_json_string(
    filepath: str,
    data: dict,
    yaml: YAML = None,
    json_spec: Optional[dict] = None,
) -> str:
    """Write a dict to a yaml or json - formatted string"""
    yaml = yaml or YAML()
    sio = io.StringIO()
    _write_to_io(filepath, data, sio, yaml, json_spec)
    return sio.getvalue()


def write_to_yaml_or_json(
    filepath: str,
    data: dict,
    yaml: YAML = None,
    json_spec: Optional[dict] = None,
) -> None:
    """Write a dict to a yaml or json file"""
    yaml = yaml or YAML()
    with open(filepath, "w", encoding="utf-8") as filepath_handle:
        _write_to_io(filepath, data, filepath_handle, yaml, json_spec=json_spec)


def get_repo_name_from_root_dir(root_dir: str) -> str:
    """Get the repo name from the root directory"""
    return os.path.basename(root_dir.rstrip("/"))


def fetch_schema(schema_url: str) -> dict:
    """Fetch a schema from a URL and cache it in the requests cache"""
    if not schema_url.startswith(OPENDAPI_URL):
        raise ValueError(
            f"Unsupported schema found at {schema_url} for "
            f"- not hosted on {OPENDAPI_URL}"
        )
    return session.get(schema_url, timeout=2).json()


def sort_dict_by_keys(dct: dict) -> dict:
    """Sort a dict by its keys"""
    return dict(sorted(dct.items(), key=lambda x: x[0]))


def sorted_yaml_dump(
    content: dict,
    stream: TextIO,
    json_spec: Optional[dict] = None,
    yaml: YAML = None,
):
    """Dump a yaml file with sorted keys, as indicated by the json schema (or alphabetically)"""
    yaml = yaml or YAML()

    if not json_spec:
        jsonschema_ref = content.get("schema")
        json_spec = fetch_schema(jsonschema_ref) if jsonschema_ref else {}

    def _rec_sort(item, schema):
        """Helper function to recursively sort a dict"""

        # We will use the priority in the schema to sort the keys.
        # If priority is not present, we will use a high number to sort it at the end.
        # If priority is the same, we will sort the keys alphabetically.
        sorter = lambda x: (schema.get(x, {}).get("order", 99999), x)

        if isinstance(item, dict):
            # could use dict in newer python versions
            res = CommentedMap()
            schema = schema.get("properties", {})
            for k in sorted(item.keys(), key=sorter):
                res[k] = _rec_sort(item[k], schema.get(k, {}))
            return res

        if isinstance(item, list):
            schema = schema.get("items", {})
            for idx, elem in enumerate(item):
                item[idx] = _rec_sort(elem, schema)

        return item

    json_spec = jsonref.JsonRef.replace_refs(json_spec)
    sorted_content = _rec_sort(content, json_spec)
    yaml.dump(sorted_content, stream)


def make_api_request(
    url: str,
    headers: Dict,
    json_payload: Optional[Dict],
    method: HTTPMethod,
    timeout: int = 30,
    req_session: Optional[requests.Session] = None,
) -> Tuple[requests.Response, Optional[requests.Session]]:
    """Make API calls to github, returning entire response"""
    if method is HTTPMethod.POST:
        return make_api_w_query_and_body(
            url=url,
            headers=headers,
            query_params=None,
            body_json=json_payload,
            method=HTTPMethod.POST,
            timeout=timeout,
            req_session=req_session,
        )
    return make_api_w_query_and_body(
        url=url,
        headers=headers,
        query_params=json_payload,
        body_json=None,
        method=method,
        timeout=timeout,
        req_session=req_session,
    )


def make_api_w_query_and_body(
    url: str,
    headers: Dict,
    query_params: Optional[Dict],
    body_json: Optional[Dict],
    method: HTTPMethod,
    timeout: int = 30,
    req_session: Optional[requests.Session] = None,
) -> Tuple[requests.Response, Optional[requests.Session]]:
    """Make API calls to github, returning entire response"""
    request_maker = req_session or requests

    if method is HTTPMethod.POST:
        response = request_maker.post(
            url,
            headers=headers,
            params=query_params,
            json=body_json,
            timeout=timeout,
        )
    elif method is HTTPMethod.GET:
        if body_json:
            raise ValueError("GET requests cannot have a body")
        response = request_maker.get(
            url,
            params=query_params,
            headers=headers,
            timeout=timeout,
        )
    else:
        if body_json:
            raise ValueError("DELETE requests cannot have a body")
        response = request_maker.delete(
            url,
            params=query_params,
            headers=headers,
            timeout=timeout,
        )

    return response, req_session


def _remove_additional_properties_validator(base_validator_cls):
    """
    Extend a validator to remove additional properties not found in the schema.
    Edited from
    https://stackoverflow.com/questions/44694835/remove-properties-from-json-object-not-present-in-schema

    NOTE: Does not work with separate-schema polymorphism,
    since we do not fetch the other schema
    """

    original_properties_validator = base_validator_cls.VALIDATORS["properties"]

    def remove_additional_properties(validator, properties, instance, schema):
        """
        Callback invoked by jsonschema to validate a properties present in an instance
        against the expected properties [properties] defined in the schema.

        This callback removes any additional properties found in the instance
        that are not found in the schema.
        """
        if not validator.is_type(instance, "object"):
            return

        for prop in list(instance.keys()):
            if prop not in properties:
                del instance[prop]

        yield from original_properties_validator(
            validator, properties, instance, schema
        )

    return validators.extend(
        base_validator_cls,
        {
            **base_validator_cls.VALIDATORS,
            "properties": remove_additional_properties,
        },
    )


def prune_additional_properties(inst: dict, schema: dict) -> dict:
    """
    Trim the inst of additional properties not found in the schema

    NOTE: This does not validate the instance, only prunes it, and does not
          work with separate-schema polymorphism, since we do not fetch the other schema
    """
    inst = deepcopy(inst)
    validator_for_schema = validator_for(schema)
    remove_additional_cls = _remove_additional_properties_validator(
        validator_for_schema
    )
    # iterates through all of the errors - meaning that the entire schema is traversed,
    # allowing us to prune nested objects as well
    # Note that we never raise the error, since this does not validate, only prunes
    for _ in remove_additional_cls(schema).iter_errors(inst):
        pass
    return inst


def encode_json_to_base64(json_data: Any) -> str:
    """Encode json to a base64 string"""
    return base64.b64encode(json.dumps(json_data).encode("utf-8")).decode("utf-8")


def decode_base64_to_json(base64_str: str) -> Any:
    """Decode a base64 string to json"""
    return json.loads(base64.b64decode(base64_str.encode("utf-8")).decode("utf-8"))


_ORM_EXTRACTED_FIELDS_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$defs": {
        "field": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                },
                "data_type": {
                    "type": "string",
                },
                "is_nullable": {
                    "type": "boolean",
                },
            },
            "required": ["name", "data_type"],
        }
    },
    "type": "object",
    "properties": {
        "schema": {
            "type": "string",
            "format": "uri",
        },
        "urn": {
            "type": "string",
            "pattern": "^([\\w-]+\\.)+[\\w-]+$",
        },
        "fields": {
            "type": "array",
            "items": {"$ref": "#/$defs/field"},
            "minItems": 1,
        },
        "primary_key": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
    },
    "required": ["schema", "urn", "fields", "primary_key"],
}


def has_underlying_model_changed(
    dapi_one: Optional[Dict], dapi_two: Optional[Dict]
) -> bool:
    """
    Check if the underlying model has changed.

    This is done by pruning all non-ORM-derived portions from the Dapis and comparing them.
    """
    return prune_additional_properties(
        dapi_one or {}, _ORM_EXTRACTED_FIELDS_SCHEMA
    ) != prune_additional_properties(dapi_two or {}, _ORM_EXTRACTED_FIELDS_SCHEMA)
