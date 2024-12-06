"""
This module contains the models related to artifacts.
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class PipelineStatus(str, Enum):
    """
    Enum representing the status of a pipeline.

    Attributes:
        PENDING (str): The pipeline is pending.
        RUNNING (str): The pipeline is running.
        SUCCESS (str): The pipeline completed successfully.
        FAILED (str): The pipeline failed.
        CANCELED (str): The pipeline was canceled.
    """

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"


class PipelineCreate(BaseModel):
    """
    Model for creating a new pipeline.

    Attributes:
        git_branch (str): The git branch name.
        git_hash (str): The git commit hash.
        git_comment (str): The git commit message.
        pipeline_name (str): The name of the pipeline.
        repo_url (str): The git repository URL.
        status (PipelineStatus): The status of the pipeline.
    """

    git_branch: str
    git_hash: str
    git_comment: str
    pipeline_name: str
    repo_url: str
    status: PipelineStatus = PipelineStatus.PENDING
    # user_id: UUID


class Pipeline(BaseModel):
    """This is the model for a pipeline"""

    id: UUID
    """The unique identifier for the pipeline"""
    run_id: int
    """The unique identifier for the pipeline run"""
    pipeline_name: str
    """The name of the pipeline"""
    repo_url: str
    """The git repository url"""
    git_branch: str
    """The git branch name"""
    git_hash: str
    """The git commit hash"""
    git_comment: str
    """The git commit message"""
    status: PipelineStatus
    """The status of the pipeline"""
    running_time: float | None
    """The time the pipeline has been running   """
    start_time: datetime | None
    """The time the pipeline started"""
    end_time: datetime | None
    """The time the pipeline ended"""
    created_at: datetime
    """The time the pipeline was created"""
    stage_ids: list[UUID] = []
    """The unique identifiers for the stages in the pipeline"""
    # user_id: UUID
