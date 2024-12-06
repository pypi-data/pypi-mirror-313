from __future__ import annotations

from enum import Enum


class RuntimeEnvVar(Enum):
    """
    Environment variables.
    """

    PROJECT = "PROJECT_NAME"
    RUN_ID = "RUN_ID"
