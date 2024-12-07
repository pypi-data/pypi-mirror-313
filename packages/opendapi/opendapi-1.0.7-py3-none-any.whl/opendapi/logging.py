"""Debugging utilities for OpenDAPI"""

import logging
import os
import sys
import time
from enum import Enum
from importlib.metadata import version

import sentry_sdk
from deepmerge import always_merger

DAPI_API_KEY_HEADER = "X-DAPI-Server-API-Key"
WOVEN_DENY_LIST = sentry_sdk.scrubber.DEFAULT_DENYLIST + [DAPI_API_KEY_HEADER]


class LogDistKey(Enum):
    """Set of Dist keys for logging"""

    ASK_DAPI_SERVER = "ask_dapi_server"
    CLI_INIT = "cli_init"
    CLI_GENERATE = "cli_generate"
    CLI_ENRICH = "cli_enrich"
    CLI_REGISTER = "cli_register"


class LogCounterKey(Enum):
    """Set of Counter keys for logging"""

    ASK_DAPI_SERVER_PAYLOAD_ITEMS = "ask_dapi_server_payload_items"
    VALIDATOR_ERRORS = "validator_errors"
    VALIDATOR_ITEMS = "validator_items"
    USER_PR_CREATED = "user_pr_created"
    SUGGESTIONS_PR_CREATED = "suggestions_pr_created"
    SUGGESTIONS_FILE_COUNT = "suggestions_file_count"


class Timer:
    """A context manager to measure the time taken for a block of code and publish to sentry."""

    def __init__(self, dist_key: LogDistKey, tags=None) -> None:
        """Initialize the timer"""
        self.dist_key = dist_key
        self.tags = tags
        self.start = None

    def __enter__(self):
        """Start the timer"""
        self.start = time.time()
        return self

    def set_tags(self, tags):
        """Set tags for the timer"""
        self.tags = always_merger.merge(self.tags, tags)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """End the timer and log the distribution metric to sentry."""
        _end = time.time()
        _elapsed = _end - self.start
        key_name = (
            self.dist_key.value
            if isinstance(self.dist_key, LogDistKey)
            else self.dist_key
        )
        sentry_sdk.metrics.distribution(
            key=f"opendapi.{key_name}",
            value=_elapsed * 1000,
            unit="milliseconds",
            tags=self.tags,
        )

        return False


def increment_counter(key: LogCounterKey, value: int = 1, tags: dict = None):
    """Increment a counter metric in sentry."""
    key_name = key.value if isinstance(key, LogCounterKey) else key
    sentry_sdk.metrics.incr(
        key=f"opendapi.{key_name}",
        value=value,
        tags=tags,
    )


def sentry_init(
    sentry_config: dict,
    tags: dict = None,
):
    """Initialize sentry, but silently fail in case of errors"""
    # Silently return if we don't have the required information
    sentry_config["release"] = version("opendapi")
    sentry_config["event_scrubber"] = sentry_sdk.scrubber.EventScrubber(
        denylist=WOVEN_DENY_LIST,
        recursive=True,
    )
    sentry_config["_experiments"] = {
        # Turns on the metrics module
        "enable_metrics": True,
        # Enables sending of code locations for metrics
        "metric_code_locations": True,
    }
    sentry_sdk.init(**sentry_config)

    # Set sentry tags
    sentry_tags = tags or {}
    for tag, value in sentry_tags.items():
        sentry_sdk.set_tag(tag, value)


class OpenDAPILogger(logging.Logger):
    """Custom logger class for OpenDAPI."""

    # Add specific things here later such as timers


def setup_logger(name="opendapi", level=None) -> OpenDAPILogger:
    """Setup the logger for the application."""

    # Default to ERROR if not set
    level_env = (
        getattr(logging, os.environ["LOG_LEVEL"].upper(), None)
        if os.environ.get("LOG_LEVEL")
        else None
    )

    # Fallback if LOG_LEVEL is not set
    fallback_level = logging.CRITICAL
    level = level or level_env or fallback_level

    logging.setLoggerClass(OpenDAPILogger)
    _logger = logging.getLogger(name)
    _logger.setLevel(level)
    # Do not propagate to the root logger
    _logger.propagate = False

    if _logger.hasHandlers():
        _logger.handlers = []  # pragma: no cover

    _logger.addHandler(logging.StreamHandler(sys.stdout))

    for handler in _logger.handlers:
        handler.setLevel(level)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s"
            )
        )

    return _logger


logger: OpenDAPILogger = setup_logger()
