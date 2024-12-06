"""
This module contains the Job class for handling job-related data.
"""

from pydantic import BaseModel, Field

from t1cicd.cicd.orchestrator.parser.artifact import Artifact


class ParsedJob(BaseModel):
    """
    Job class for handling job-related data.
    """

    name: str = Field(..., description="The name of the job")
    image: str = Field(None, description="The image to use for the job")
    stage: str = Field(..., description="The stage to run the job in")
    needs: list[str] = Field(
        default_factory=list, description="The jobs that this job depends on"
    )
    script: list[str] | str = Field(..., description="The script to run in the job")
    artifacts: Artifact | None = Field(None, description="The artifacts to upload")
    allow_failure: bool = Field(False, description="Whether the job is allowed to fail")
