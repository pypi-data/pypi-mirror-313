"""
This module contains the models related to stages.
"""

from collections import defaultdict
from uuid import UUID

from t1cicd.cicd.db.db import DB
from t1cicd.cicd.db.repository.job import JobRepository
from t1cicd.cicd.db.repository.pipeline import PipelineRepository
from t1cicd.cicd.db.repository.stage import StageRepository
from t1cicd.cicd.db.transform.factory import TransformFactory


class SummaryService:
    """
    A service class for generating summaries of various entities.
    """

    def __init__(self):
        self.pipeline_repo = DB.get_repository(PipelineRepository)
        self.stage_repo = DB.get_repository(StageRepository)
        self.job_repo = DB.get_repository(JobRepository)

    async def get_pipeline_summary(self, pipeline_id: UUID | int) -> dict:
        """
        Get the summary of a pipeline

        Args:
            pipeline_id (UUID | int): The pipeline id or run id

        Returns:
            dict: The pipeline summary


        """
        if isinstance(pipeline_id, int):
            pipeline = await self.pipeline_repo.get_by_run_id(pipeline_id)
        else:
            pipeline = await self.pipeline_repo.get(pipeline_id)

        if not pipeline:
            return {}

        stage_ids = pipeline.stage_ids
        stages = []
        for stage_id in stage_ids:
            stage = await self.stage_repo.get(stage_id)
            stages.append(stage)
        return TransformFactory.create_pipeline_stage_relationship().replace_ids_with_objects(
            pipeline, stages
        )

    async def get_stage_summary(self, stage_id: UUID) -> dict:
        """

        Get the summary of a stage

        Args:
            stage_id (UUID): The stage id

        Returns:
            dict: The stage summary

        """
        stage = await self.stage_repo.get(stage_id)
        if not stage:
            return {}
        job_ids = stage.job_ids
        jobs = []
        for job_id in job_ids:
            job = await self.job_repo.get(job_id)
            jobs.append(job)
        return (
            TransformFactory.create_stage_job_relationship().replace_ids_with_objects(
                stage, jobs
            )
        )

    async def get_job_summary(self, job_id: UUID) -> dict:
        """

        Get the summary of a job

        Args:
            job_id (UUID): The job id

        Returns:
            dict: The job summary

        """
        job = await self.job_repo.get(job_id)
        if not job:
            return {}
        return job.model_dump()

    async def get_pipeline_name_ids(self, repo_url: str) -> dict[str, list[UUID]]:
        """

        Get the pipeline name and ids for a repository

        Args:
            repo_url (str): The repository url

        Returns:
            dict[str, list[UUID]]: The pipeline name and ids
        """
        pipelines = await self.pipeline_repo.get_all(repo_url)
        res = defaultdict(list)
        for pipeline in pipelines:
            res[pipeline.pipeline_name].append(pipeline.id)
        return res

    async def get_pipeline_summary_by_repo(self, repo_url: str) -> list[dict]:
        """

        Get the pipeline summary for a repository

        Args:
            repo_url (str): The repository url

        Returns:
            list[dict]: The pipeline summary
        """
        pipelines = await self.pipeline_repo.get_by_repo_url(repo_url)
        res = [pipeline.model_dump() for pipeline in pipelines]
        return res


#
#
# if __name__ == "__main__":
#
#     import json
#
#     class UUIDEncoder(json.JSONEncoder):
#         def default(self, obj):
#             if isinstance(obj, UUID) or isinstance(obj, datetime):
#                 return str(obj)
#             return super().default(obj)
#
#     async def example():
#         await DB.init(DBConfig.from_env())
#         service = SummaryService()
#         pipeline_name_ids = await service.get_pipeline_name_ids("github.com/owner/repo")
#         first_key = next(iter(pipeline_name_ids))
#         print(f"Getting summary for pipeline {first_key}")
#         pipeline_summary = await service.get_pipeline_summary(
#             pipeline_name_ids[first_key][0]
#         )
#         print(json.dumps(pipeline_summary, cls=UUIDEncoder, indent=4))
#         await DB.close()
#
#     asyncio.run(example())
