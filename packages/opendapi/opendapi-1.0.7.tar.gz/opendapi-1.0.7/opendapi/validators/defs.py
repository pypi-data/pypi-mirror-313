"""Defs for Validators"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from opendapi.defs import OpenDAPIEntity


class ValidationError(Exception):
    """Exception raised for validation errors"""


class MultiValidationError(ValidationError):
    """Exception raised for multiple validation errors"""

    def __init__(self, errors: List[str], prefix_message: str = None):
        self.errors = errors
        self.prefix_message = prefix_message

    def __str__(self):
        return (
            f"\n\n{self.prefix_message}\n\n"
            + f"Found {len(self.errors)} errors:\n\n"
            + "\n\n".join(self.errors)
        )


class FileSet(Enum):
    """Enum for the file set"""

    ORIGINAL = "original"
    GENERATED = "generated"
    MERGED = "merged"


@dataclass
class CollectedFile:
    """class for the collect result"""

    original: Optional[Dict]
    generated: Optional[Dict]
    merged: Dict
    filepath: str
    commit_sha: Optional[str]
    entity: OpenDAPIEntity
