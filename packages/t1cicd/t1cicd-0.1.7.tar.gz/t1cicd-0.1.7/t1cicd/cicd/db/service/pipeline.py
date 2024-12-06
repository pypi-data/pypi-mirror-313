# t1cicd/cicd/db/service/pipeline_service.py

"""
This module contains the service class for handling pipeline-related operations.
"""

from uuid import UUID

from t1cicd.cicd.db.context.pipeline import PipelineCreateContext
from t1cicd.cicd.db.db import DB
from t1cicd.cicd.db.transaction.pipeline import PipelineTransaction
from t1cicd.cicd.orchestrator.parser.pipeline import ParsedPipeline


class PipelineService:
    """
    Service class for handling pipeline-related operations.
    """

    @staticmethod
    async def create_pipeline(
        parsed_pipeline: ParsedPipeline,
        git_branch: str,
        git_hash: str,
        git_comment: str = "",
        repo_url: str = "",
    ) -> tuple[UUID, int]:
        """

        Create a new pipeline in the database.

        Args:
            parsed_pipeline (ParsedPipeline): The parsed pipeline object.
            git_branch (str): The branch name.
            git_hash (str): The commit hash.
            git_comment (str, optional): The commit comment. Defaults to "".
            repo_url (str, optional): The repository URL. Defaults to "".

        Returns:
            tuple[UUID, int]: The pipeline ID and run ID
        """
        context = PipelineCreateContext(
            git_branch=git_branch,
            git_hash=git_hash,
            git_comment=git_comment,
            repo_url=repo_url,
        )
        pipeline_transaction = DB.get_transaction(PipelineTransaction)
        pipeline_id, run_id = await pipeline_transaction.create_new_pipeline(
            parsed_pipeline, context
        )
        print(f"Created pipeline: {pipeline_id}")
        return pipeline_id, run_id
