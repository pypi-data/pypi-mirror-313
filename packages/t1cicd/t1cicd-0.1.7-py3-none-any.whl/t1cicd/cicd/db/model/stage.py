"""
This module contains the models related to stages.
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class StageStatus(str, Enum):
    """
    Enum representing the status of a stage.

    Attributes:
        PENDING (str): The stage is pending.
        RUNNING (str): The stage is running.
        SUCCESS (str): The stage completed successfully.
        FAILED (str): The stage failed.
        CANCELED (str): The stage was canceled.
    """

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"


class Stage(BaseModel):
    """This is the model for a stage"""

    id: UUID
    """The unique identifier for the stage"""
    pipeline_id: UUID
    """The unique identifier for the pipeline"""
    stage_name: str
    """The name of the stage"""
    status: StageStatus
    """The status of the stage"""
    start_time: datetime | None
    """The time the stage started"""
    end_time: datetime | None
    """The time the stage ended"""
    stage_order: int
    """The order of the stage in the pipeline"""
    created_at: datetime | None
    """The time the stage was created"""
    updated_at: datetime | None
    """The time the stage was updated"""
    job_ids: list[UUID] = []


class StageCreate(BaseModel):
    """
    Model for creating a new stage.

    Attributes:
        pipeline_id (UUID): The unique identifier for the pipeline.
        stage_name (str): The name of the stage.
        stage_order (int): The order of the stage in the pipeline.
    """

    pipeline_id: UUID
    stage_name: str
    stage_order: int
