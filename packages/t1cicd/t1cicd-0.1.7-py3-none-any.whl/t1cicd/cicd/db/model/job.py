"""
This module contains the models related to artifacts.
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class JobStatus(str, Enum):
    """
    Enum representing the status of a job.

    Attributes:
        PENDING (str): The job is pending.
        RUNNING (str): The job is running.
        SUCCESS (str): The job completed successfully.
        FAILED (str): The job failed.
        CANCELLED (str): The job was cancelled.
        SKIPPED (str): The job was skipped.
    """

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"


class Job(BaseModel):
    """This is the model for a job"""

    id: UUID
    stage_id: UUID
    job_name: str
    job_order: int
    status: JobStatus = JobStatus.PENDING
    start_time: datetime | None
    end_time: datetime | None
    retry_count: int = 0
    created_at: datetime
    updated_at: datetime
    artifact_ids: list[UUID] = []
    allow_failure: bool = False


class JobCreate(BaseModel):
    """
    Model for creating a new job.

    Attributes:
        stage_id (UUID): The unique identifier for the stage.
        job_name (str): The name of the job.
        job_order (int): The order of the job in the stage.
        allow_failure (bool): Whether the job is allowed to fail without failing the stage.
    """

    stage_id: UUID
    job_name: str
    job_order: int
    allow_failure: bool = False
