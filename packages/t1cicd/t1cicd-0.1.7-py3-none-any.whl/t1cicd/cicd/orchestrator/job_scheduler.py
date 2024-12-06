"""
Job Scheduler
=============

This module defines the `ScheduledJob` and `JobScheduler` classes for managing and running jobs
within a pipeline stage. Jobs are executed based on their dependencies and can handle failures.

Classes:
    - ScheduledJob: Represents a job with its dependencies and metadata.
    - JobScheduler: Manages and executes jobs within a pipeline stage, ensuring dependency constraints.
"""

import asyncio
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from t1cicd.cicd.api.custom_logger import CustomLogger
from t1cicd.cicd.db.db import DB
from t1cicd.cicd.db.model.job import Job, JobStatus
from t1cicd.cicd.db.repository.job import JobRepository
from t1cicd.cicd.db.transaction.pipeline import PipelineTransaction


class ScheduledJob:
    """
    Represents a job with its dependencies, metadata, and execution state.

    Attributes:
        name (str): The name of the job.
        needs (list): A list of job names that this job depends on.
        in_degree (int): The number of dependencies this job has.
        image (str): The Docker image used to run the job.
        script (list | None): The commands to be executed in the job.
        artifacts (Any): Artifacts produced by the job.
        allow_failure (bool): Whether the job is allowed to fail without affecting the pipeline.
        future (concurrent.futures.Future): The future object representing the job's execution.
    """

    def __init__(
        self,
        name: str,
        needs: list,
        image: str,
        script: list | None,
        artifacts,
        allow_failure=False,
    ):
        self.name = name
        self.needs = needs
        self.in_degree = len(needs)
        self.image = image
        self.script = script
        self.artifacts = artifacts
        self.allow_failure = allow_failure
        self.future = None


class JobScheduler:
    """
    Manages and executes jobs within a pipeline stage, ensuring dependency constraints.

    Attributes:
        job_dict (dict[str, Job]): A dictionary mapping job names to job objects.
        pipeline_id (str): The ID of the pipeline the jobs belong to.
        max_jobs (int): Maximum number of jobs to run concurrently.
        docker_runner (DockerJobRunner): The Docker runner used to execute jobs.
        total_jobs (int): Total number of jobs to be executed.
        completed_jobs (int): Number of jobs that have been completed.
        job_failed (bool): Indicates if a non-allow-failure job has failed.
        dependency_graph (defaultdict): Graph mapping jobs to their dependent jobs.
        executor (ThreadPoolExecutor): Thread pool executor for running jobs.
        lock (threading.RLock): Lock for thread-safe operations.
        condition (threading.Condition): Condition for synchronization of job completion.
    """

    def __init__(
        self, job_dict: dict[str, Job], pipeline_id, max_jobs=10, docker_runner=None
    ):
        """
        Initializes the JobScheduler.

        Args:
            job_dict (dict[str, Job]): A dictionary of job objects.
            pipeline_id (str): The ID of the pipeline.
            max_jobs (int, optional): Maximum number of jobs to run concurrently. Defaults to 10.
            docker_runner (DockerJobRunner, optional): Docker runner for executing jobs. Defaults to None.
        """
        self.job_dict = job_dict
        self.jobs = {}  # {job_name: ScheduledJob}
        self.dependency_graph = defaultdict(list)  # {job_name: [dependent_job_name]}
        self.lock = threading.RLock()
        self.executor = ThreadPoolExecutor(max_workers=max_jobs)
        self.docker_runner = docker_runner
        self.total_jobs = 0
        self.completed_jobs = 0
        self.condition = threading.Condition()
        self.job_failed = (
            False  # Flag to indicate if a non-allow-failure job has failed
        )
        self.pipeline_id = pipeline_id

    def add_job(self, job):
        """
        Adds a job to the scheduler.

        Args:
            job (Job): The job to add.
        """
        self.jobs[job.name] = ScheduledJob(
            job.name, job.needs, job.image, job.script, job.artifacts, job.allow_failure
        )
        self.total_jobs += 1
        for dep_job in job.needs:
            self.dependency_graph[dep_job].append(job.name)

    def run_jobs(self):
        """
        Executes all jobs, respecting their dependency constraints.

        Blocks until all jobs are completed.
        """
        ready_jobs = [
            job_name for job_name, job in self.jobs.items() if job.in_degree == 0
        ]
        with self.lock:
            for job_name in ready_jobs:
                self._start_job(job_name)

        # Wait for all jobs to complete
        with self.condition:
            while self.completed_jobs < self.total_jobs:
                self.condition.wait()

        self.executor.shutdown(wait=True)

    def _start_job(self, job_name):
        """
        Starts the execution of a job.

        Args:
            job_name (str): The name of the job to start.
        """
        job = self.jobs[job_name]
        with self.lock:
            should_cancel = self.job_failed
            db_job = self.job_dict[job_name]
            needs_update = False
            if should_cancel:
                if db_job.status not in [
                    JobStatus.CANCELLED,
                    JobStatus.FAILED,
                    JobStatus.SUCCESS,
                ]:
                    db_job.status = JobStatus.CANCELLED
                    self.completed_jobs += 1
                    needs_update = True
                with self.condition:
                    self.condition.notify_all()

        if should_cancel:
            if needs_update:
                asyncio.run(DB.get_repository(JobRepository).update(db_job))
            return

        print(f"Starting job {job_name}")
        CustomLogger.add(f"Starting job {job_name}")
        future = self.executor.submit(self._run_job, job)
        job.future = future

    def _run_job(self, job):
        """
        Executes a job in a separate thread.

        Args:
            job (ScheduledJob): The job to execute.
        """
        try:
            self.job_dict = asyncio.run(
                DB.get_transaction(PipelineTransaction).get_all_jobs(self.pipeline_id)
            )
            if self.job_dict[job.name].status == JobStatus.CANCELLED:
                return
            db_job = self.job_dict[job.name]
            db_job.start_time = datetime.now()
            db_job.status = JobStatus.RUNNING
            asyncio.run(DB.get_repository(JobRepository).update(db_job))

            print(f"Running job {job.name}")
            CustomLogger.add(f"Running job {job.name}")
            self.docker_runner.execute_job(job, auto_clean=True)
            print(f"Job {job.name} completed")
            CustomLogger.add(f"Job {job.name} completed")

            db_job.status = JobStatus.SUCCESS
            db_job.end_time = datetime.now()
            asyncio.run(DB.get_repository(JobRepository).update(db_job))
        except Exception as e:
            print(f"Job {job.name} failed with error: {e}")
            CustomLogger.add(f"Job {job.name} failed with error: {e}")
            db_job.status = JobStatus.FAILED
            db_job.end_time = datetime.now()
            asyncio.run(DB.get_repository(JobRepository).update(db_job))

            if not job.allow_failure:
                with self.lock:
                    self.job_failed = True
        finally:
            with self.lock:
                self.completed_jobs += 1
                with self.condition:
                    self.condition.notify_all()

                dep_jobs_to_start = []
                for dep_job_name in self.dependency_graph.get(job.name, []):
                    dep_job = self.jobs[dep_job_name]
                    dep_job.in_degree -= 1
                    if dep_job.in_degree == 0:
                        dep_jobs_to_start.append(dep_job_name)

            for dep_job_name in dep_jobs_to_start:
                self._start_job(dep_job_name)
