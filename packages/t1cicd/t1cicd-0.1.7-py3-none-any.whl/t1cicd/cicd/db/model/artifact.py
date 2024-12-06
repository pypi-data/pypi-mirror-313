"""
This module contains the models related to artifacts.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Artifact(BaseModel):
    """This is the model for an artifact"""

    id: UUID
    """The unique identifier for the artifact"""
    job_id: UUID
    """The unique identifier for the job that created the artifact"""
    file_path: str
    """The path to the artifact file"""
    file_size: int
    """The size of the artifact file"""
    created_at: datetime
    """The date and time the artifact was created"""
    expiry_date: datetime | None
    """The date and time the artifact expires"""


class ArtifactCreate(BaseModel):
    """
    Model for creating a new artifact.

    Attributes:
        job_id (UUID): The unique identifier for the job that created the artifact.
        file_path (str): The path to the artifact file.
        file_size (int): The size of the artifact file.
        expiry_date (datetime | None): The date and time the artifact expires.
    """

    job_id: UUID
    file_path: str
    file_size: int
    expiry_date: datetime | None = None
