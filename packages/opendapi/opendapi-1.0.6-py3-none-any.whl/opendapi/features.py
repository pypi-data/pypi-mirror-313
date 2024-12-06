"""Feature defs for the OpenDAPI client."""

import os
from enum import Enum
from typing import Dict, Optional

########## Enums ##########


class Feature(Enum):
    """Features for the OpenDAPI client."""

    DATA_CLASSIFICATION_V1 = "data_classification_v1"
    IMPACT_ANALYSIS_V1 = "impact_analysis_v1"
    MODEL_OWNERSHIP_V1 = "model_ownership_v1"

    @property
    def env_var(self):
        """Get the environment variable for the feature."""
        return f"__WOVEN_FEATURE_{self.name}__"

    @staticmethod
    def is_feature(val: str) -> bool:
        """Check if the value is a feature."""
        return val in Feature._value2member_map_


class FeatureStatus(Enum):
    """Statuses for the features."""

    DISABLED = "disabled"
    ENABLED = "enabled"
    PILOT = "pilot"

    @property
    def is_on(self):
        """Check if the feature is enabled or piloted."""
        return self in (FeatureStatus.ENABLED, FeatureStatus.PILOT)


########## feature state helpers ##########


def load_from_raw_dict(
    raw_feature_to_status: Dict[str, str]
) -> Dict[Feature, FeatureStatus]:
    """
    Load the feature flags from the encoded string.
    """
    return {
        Feature(feature): FeatureStatus(status)
        for feature, status in raw_feature_to_status.items()
        # in case server launches feature first, this need not fail
        if Feature.is_feature(feature)
    }


def set_feature_to_status(
    feature_to_status: Optional[Dict[Feature, FeatureStatus]],
):
    """
    Set the feature flags for the OpenDAPI client.
    """
    feature_to_status = feature_to_status or {}
    for feature, status in feature_to_status.items():
        os.environ[feature.env_var] = status.value


def get_feature_status(feature: Feature) -> FeatureStatus:
    """
    Get the status of a feature.
    """

    return FeatureStatus(os.environ.get(feature.env_var, FeatureStatus.DISABLED.value))


def is_feature_on(feature: Feature) -> bool:
    """
    Check if a feature is enabled or piloted.
    """

    return get_feature_status(feature).is_on


def feature_to_status_dict() -> Dict[Feature, FeatureStatus]:
    """
    Get a dictionary of features to status.
    """

    return {feature: get_feature_status(feature) for feature in Feature}
