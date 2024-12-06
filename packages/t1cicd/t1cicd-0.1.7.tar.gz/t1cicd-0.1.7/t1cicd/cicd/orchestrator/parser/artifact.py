"""
This module contains the Artifact class for handling artifact-related data.
"""

from pydantic import BaseModel, Field


class Artifact(BaseModel):
    """
    Artifact class for handling artifact-related data.
    """

    paths: list[str] = Field(..., description="The paths to the artifacts to upload")
    # expire_id: str | None = Field(None, description="The expire id for the artifacts")
