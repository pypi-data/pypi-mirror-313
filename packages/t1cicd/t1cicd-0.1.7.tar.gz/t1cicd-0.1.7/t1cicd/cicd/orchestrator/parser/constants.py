"""
This module contains constants used in the CICD parser.
"""

DEFAULT_GLOBAL_KEYWORDS = {
    "image",
}

JOB_KEYWORDS = {"stage", "needs", "script", "artifacts", "rules", "image"}


DEFAULT_STAGE_WORKFLOWS = {"build", "test", "doc", "deploy"}
