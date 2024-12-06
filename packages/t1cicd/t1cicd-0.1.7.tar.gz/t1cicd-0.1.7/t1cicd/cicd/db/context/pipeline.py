"""
This module contains the base repository class for the database models.
"""

from pydantic import BaseModel


class PipelineCreateContext(BaseModel):
    """This is the context for creating a pipeline"""

    git_branch: str
    """git branch name"""
    git_hash: str
    """git commit hash"""
    git_comment: str
    """git commit message"""
    repo_url: str
    """git repository url"""
