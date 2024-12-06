"""
This module contains the transaction class for handling pipeline transactions.
"""

from uuid import UUID

from psycopg_pool import AsyncConnectionPool

from t1cicd.cicd.db.context.pipeline import PipelineCreateContext
from t1cicd.cicd.db.db import DB
from t1cicd.cicd.db.model.job import Job, JobCreate, JobStatus
from t1cicd.cicd.db.model.pipeline import PipelineCreate, PipelineStatus
from t1cicd.cicd.db.model.stage import Stage, StageCreate, StageStatus
from t1cicd.cicd.db.repository.job import JobRepository
from t1cicd.cicd.db.repository.pipeline import PipelineRepository
from t1cicd.cicd.db.repository.stage import StageRepository
from t1cicd.cicd.db.transaction.base import BaseTransaction
from t1cicd.cicd.orchestrator.parser.pipeline import ParsedPipeline


class PipelineTransaction(BaseTransaction):
    """
    Transaction class for handling pipeline transactions.

    Provides methods to create, retrieve, update, and delete pipelines with associated stages and jobs in the database.
    """

    def __init__(self, pool: AsyncConnectionPool):
        super().__init__(pool)
        self.pipeline_repo = DB.get_repository(PipelineRepository)
        """The pipeline repository"""
        self.stage_repo = DB.get_repository(StageRepository)
        """The stage repository"""
        self.job_repo = DB.get_repository(JobRepository)
        """The job repository"""

    async def create_new_pipeline(
        self, parsed_pipeline: ParsedPipeline, context: PipelineCreateContext
    ) -> tuple[UUID, int]:
        """
        Create a new pipeline with stages and jobs

        Args:
            parsed_pipeline (ParsedPipeline): The parsed pipeline
            context (PipelineCreateContext): The pipeline create context

        Returns:
            tuple[UUID, int]: The pipeline id and run id
        """
        async with self.get_transaction():

            pipeline = await self.pipeline_repo.create(
                PipelineCreate(
                    git_branch=context.git_branch,
                    git_hash=context.git_hash,
                    git_comment=context.git_comment,
                    repo_url=context.repo_url,
                    pipeline_name=parsed_pipeline.pipeline_name,
                )
            )
            for stage_order, (stage_name, parsed_jobs) in enumerate(
                parsed_pipeline.get_all_stages()
            ):
                stage = await self.stage_repo.create(
                    StageCreate(
                        stage_name=stage_name,
                        pipeline_id=pipeline.id,
                        stage_order=stage_order,
                    )
                )
                for job_order, job in enumerate(parsed_jobs):
                    await self.job_repo.create(
                        JobCreate(
                            stage_id=stage.id,
                            job_name=job.name,
                            job_order=job_order,
                            allow_failure=job.allow_failure,
                        )
                    )

            return pipeline.id, pipeline.run_id

    async def get_all_jobs(self, pipeline_id: UUID) -> dict[str, Job]:
        """

        Get all the jobs in the pipeline

        Args:
            pipeline_id (UUID): The pipeline id

        Returns:
            dict[str, Job]: The jobs in the pipeline

        """
        async with self.get_transaction():
            pipeline = await self.pipeline_repo.get(pipeline_id)
            stage_ids = pipeline.stage_ids
            jobs: dict[str, Job] = {}
            for stage_id in stage_ids:
                stage = await self.stage_repo.get(stage_id)
                for job_id in stage.job_ids:
                    job = await self.job_repo.get(job_id)
                    jobs[job.job_name] = job
            return jobs

    async def get_all_stages(self, pipeline_id: UUID) -> dict[str, Stage]:
        """

        Get all the stages in the pipeline

        Args:
            pipeline_id (UUID): The pipeline id

        Returns:
            dict[str, Stage]: The stages in the pipeline

        """
        async with self.get_transaction():
            pipeline = await self.pipeline_repo.get(pipeline_id)
            stage_ids = pipeline.stage_ids
            stages: dict[str, Stage] = {}
            for stage_id in stage_ids:
                stage = await self.stage_repo.get(stage_id)
                stages[stage.stage_name] = stage
            return stages

    async def cancel_pipeline_by_run_id(self, run_id: int):
        """

        Cancel a pipeline by its run id

        Args:
            run_id (int): The run id


        """
        async with self.get_transaction():
            pipeline = await self.pipeline_repo.get_by_run_id(run_id)
            if not pipeline:
                return
            for stage_id in pipeline.stage_ids:
                stage = await self.stage_repo.get(stage_id)
                if stage.status in (StageStatus.RUNNING, StageStatus.PENDING):
                    stage.status = StageStatus.CANCELED
                    await self.stage_repo.update(stage)
                for job_id in stage.job_ids:
                    job = await self.job_repo.get(job_id)
                    if job.status in (JobStatus.RUNNING, JobStatus.PENDING):
                        job.status = JobStatus.CANCELLED
                        await self.job_repo.update(job)
            pipeline.status = PipelineStatus.CANCELED
            await self.pipeline_repo.update(pipeline)
