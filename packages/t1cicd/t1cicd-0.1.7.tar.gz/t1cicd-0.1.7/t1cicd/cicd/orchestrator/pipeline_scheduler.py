"""
Pipeline Scheduler
==================

This module defines the `PipelineScheduler` class, which handles scheduling and execution of CI/CD pipelines.
It clones repositories, parses pipeline configurations, and orchestrates the execution of pipeline stages
and jobs using Docker containers.

Classes:
    - PipelineScheduler: Manages the end-to-end execution of pipelines.
"""

import asyncio
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from t1cicd.cicd.api.custom_logger import CustomLogger
from t1cicd.cicd.db.db import DB
from t1cicd.cicd.db.model.job import JobStatus
from t1cicd.cicd.db.model.pipeline import PipelineStatus
from t1cicd.cicd.db.model.stage import StageStatus
from t1cicd.cicd.db.repository.job import JobRepository
from t1cicd.cicd.db.repository.pipeline import PipelineRepository
from t1cicd.cicd.db.repository.stage import StageRepository
from t1cicd.cicd.db.service.pipeline import PipelineService
from t1cicd.cicd.db.transaction.pipeline import PipelineTransaction
from t1cicd.cicd.docker.docker_runner import DockerJobRunner
from t1cicd.cicd.orchestrator.job_scheduler import JobScheduler
from t1cicd.cicd.orchestrator.parser.parser import YAMLParser


class PipelineScheduler:
    """
    Schedules and runs CI/CD pipelines based on a provided repository, branch, and commit.
    Allows running pipelines based on a config file or a pipeline name.
    """

    def __init__(
        self,
        repo,
        branch,
        commit,
        config_file=None,
        pipeline_name=None,
        temp_dir=None,
        pipelines_dir=None,
        git_handler=None,
        docker_runner=None,
    ):
        """
        Initialize the PipelineScheduler with the given parameters.

        Args:
            repo (str): URL of the repository.
            branch (str): Name of the branch.
            commit (str): Commit hash to use.
            config_file (str, optional): Path to the configuration file for the pipeline.
            pipeline_name (str, optional): Name of the pipeline to run.
            temp_dir (str, optional): Directory to clone the repository and perform temporary operations.
            pipelines_dir (str, optional): Directory containing pipeline configuration files.
            git_handler (object, optional): An instance of a Git handler for cloning and checkout.
            docker_runner (object, optional): An instance of a Docker runner for executing jobs.
        """
        self.repo = repo
        self.branch = branch
        self.commit = commit
        self.config_file = config_file
        self.pipeline_name = pipeline_name
        self.parsed_pipelines = []
        self.temp_dir = temp_dir
        self.pipeline_dir = pipelines_dir
        self.git_handler = git_handler
        self.docker_runner = docker_runner
        self.commit_message = ""

    def clone_and_prepare_repo(self):
        """
        Clones the repository and checks out the specified branch and commit.

        This method uses the git_handler to clone the repository and checkout the branch/commit
        in the temporary directory specified by temp_dir.

        Raises:
            RuntimeError: If cloning or checkout fails.
        """
        try:
            # Git clone and checkout
            self.commit, self.commit_message = self.git_handler.clone_and_checkout(
                self.repo, self.branch, self.commit, self.temp_dir
            )
        except Exception as e:
            raise RuntimeError(f"Failed to clone and checkout the repo: {e}")

    def parse_pipelines(self):
        """
        Parses the pipelines either from a config file or by looking for a specific pipeline name.

        - If a config_file is provided, the pipeline is parsed from that file.
        - If a pipeline_name is provided, it looks for the corresponding pipeline configuration file in the pipeline_dir.
        - If neither config_file nor pipeline_name is provided, all pipeline files in the directory are parsed.

        Raises:
            FileNotFoundError: If a config file is not found.
            ValueError: If the specified pipeline name is not found.
            RuntimeError: If there is an error while parsing the pipeline configuration.
        """
        try:
            # Situation 1: Config file is provided
            if self.config_file:
                print(f"Config file found: {self.config_file}")
                CustomLogger.add(f"Config file found: {self.config_file}")
                parser = YAMLParser(self.config_file)
                parsed_pipeline = parser.parse()
                self.parsed_pipelines.append(parsed_pipeline)
            # Situation 2: Pipeline name is provided
            elif self.pipeline_name:
                print("Pipeline name is provided and is: ", self.pipeline_name)
                CustomLogger.add(
                    f"Pipeline name is provided and is: {self.pipeline_name}"
                )

                # Flag to track if the pipeline is found
                pipeline_found = False

                # Go through all files in the pipelines directory and parse them
                for file in os.listdir(self.pipeline_dir):
                    if file.endswith(".yml") or file.endswith(".yaml"):
                        file_path = os.path.join(self.pipeline_dir, file)
                        parser = YAMLParser(file_path)
                        parsed_pipeline = parser.parse()

                        # Check if the parsed pipeline matches the provided name
                        if parsed_pipeline.pipeline_name == self.pipeline_name:
                            self.parsed_pipelines.append(parsed_pipeline)
                            pipeline_found = (
                                True  # Set the flag if the pipeline is found
                            )
                            break  # Exit loop once the pipeline is found

                # If no matching pipeline is found, raise an error
                if not pipeline_found:
                    raise ValueError(
                        f"Pipeline '{self.pipeline_name}' not found in the directory: {self.pipeline_dir}"
                    )
            # Situation 3: Neither config_file nor pipeline_name is provided
            else:
                # Add all pipelines in the .cicd_pipelines folder
                for file in os.listdir(self.pipeline_dir):
                    if file.endswith(".yml") or file.endswith(".yaml"):
                        file_path = os.path.join(self.pipeline_dir, file)
                        parser = YAMLParser(file_path)
                        parsed_pipeline = parser.parse()
                        self.parsed_pipelines.append(parsed_pipeline)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Config file not found: {e}")
        except Exception as e:
            raise RuntimeError(f"Error parsing the pipeline config: {e}")

    def run(self):
        """
        Clones the repository, parses pipelines, and runs the stages of each pipeline sequentially.

        - Clones the repository based on the provided repo, branch, and commit.
        - Parses pipelines based on the config file or pipeline name.
        - Executes the stages of the parsed pipelines in sequence, running each job in a Docker container.

        Returns:
            str: A message indicating the result of the pipeline execution.

        Raises:
            RuntimeError: If an error occurs during the execution of a job.
        """
        self.clone_and_prepare_repo()
        self.parse_pipelines()

        print("finish parsing pipelines")
        CustomLogger.add("finish parsing pipelines")
        p_status_dict = {}
        # Loop over each parsed pipeline and run the stages sequentially
        for pipeline in self.parsed_pipelines:
            print(f"Running pipeline: {pipeline.pipeline_name}")
            CustomLogger.add(f"Running pipeline: {pipeline.pipeline_name}")
            # init pipeline metadata
            pipeline_id, run_id = asyncio.run(
                PipelineService.create_pipeline(
                    pipeline,
                    git_branch=self.branch,
                    git_hash=self.commit,
                    git_comment=self.commit_message,
                    repo_url=self.repo,
                )
            )
            p_status_dict[pipeline.pipeline_name] = [run_id]
            # p_status_dict[pipeline.pipeline_name].append(run_id)
            print(f"Created pipeline: {pipeline_id}")
            CustomLogger.add(f"Created pipeline: {pipeline_id}")
            # update start time
            p = asyncio.run(DB.get_repository(PipelineRepository).get(pipeline_id))

            if p.status == PipelineStatus.CANCELED:
                print(f"Pipeline {pipeline.pipeline_name} is already cancelled")
                CustomLogger.add(
                    f"Pipeline {pipeline.pipeline_name} is already cancelled"
                )
                continue

            p.start_time = datetime.now()
            p.status = PipelineStatus.RUNNING
            asyncio.run(DB.get_repository(PipelineRepository).update(p))
            job_dict = asyncio.run(
                DB.get_transaction(PipelineTransaction).get_all_jobs(pipeline_id)
            )

            continue_pipeline = True
            all_successful = True
            cancelled_stages = []
            stage_dict = asyncio.run(
                DB.get_transaction(PipelineTransaction).get_all_stages(pipeline_id)
            )
            for stage_name in pipeline.get_all_stage_names():
                if not continue_pipeline:
                    # Mark remaining stages and jobs as CANCELLED
                    cancelled_stages.append(stage_name)
                    print(
                        f"Pipeline stopped due to critical failure. Canceling stage: {stage_name}"
                    )
                    CustomLogger.add(
                        f"Pipeline stopped due to critical failure. Canceling stage: {stage_name}"
                    )
                    asyncio.run(
                        self._cancel_stage_jobs(
                            pipeline.parsed_stages.get_sorted_jobs_in_stage(stage_name),
                            job_dict,
                        )
                    )
                    continue

                print(f"Executing stage: {stage_name}")
                CustomLogger.add(f"Executing stage: {stage_name}")

                stage = stage_dict[stage_name]

                s = asyncio.run(DB.get_repository(StageRepository).get(stage.id))
                if s.status == StageStatus.CANCELED:
                    print(f"Stage {stage_name} is already cancelled")
                    CustomLogger.add(f"Stage {stage_name} is already cancelled")
                    continue

                # Update stage start time and status
                stage.start_time = datetime.now()
                stage.status = StageStatus.RUNNING
                asyncio.run(DB.get_repository(StageRepository).update(stage))

                # Get all jobs in the current stage
                jobs = pipeline.parsed_stages.get_sorted_jobs_in_stage(stage_name)

                # Execute each job in the current stage
                absolute_path = self.temp_dir
                # volumes = {absolute_path: {"bind": "/app", "mode": "rw"}}
                # work_dir = "/app"
                docker_runner = DockerJobRunner(pipeline.pipeline_name, absolute_path)

                job_scheduler = JobScheduler(job_dict, pipeline_id, 10, docker_runner)
                for job in jobs:
                    job_scheduler.add_job(job)
                job_scheduler.run_jobs()

                # Get the latest status of the stage
                s = asyncio.run(DB.get_repository(StageRepository).get(stage.id))
                if s.status == StageStatus.CANCELED:
                    print(f"Stage {stage_name} is already cancelled")
                    CustomLogger.add(f"Stage {stage_name} is already cancelled")
                    continue
                job_dict = asyncio.run(
                    DB.get_transaction(PipelineTransaction).get_all_jobs(pipeline_id)
                )
                # After the stage is executed, check if any non-allow-failure jobs failed
                critical_failure = self._check_critical_failures(jobs, job_dict)
                allow_failure_failure = self._check_allow_failure_failures(
                    jobs, job_dict
                )
                if critical_failure or allow_failure_failure:
                    print(f"Critical failure detected in stage: {stage_name}")
                    CustomLogger.add(
                        f"Critical failure detected in stage: {stage_name}"
                    )
                    # update stage end time and status
                    stage = stage_dict[stage_name]
                    stage.end_time = datetime.now()
                    stage.status = StageStatus.FAILED
                    asyncio.run(DB.get_repository(StageRepository).update(stage))
                    all_successful = False
                    if critical_failure:
                        continue_pipeline = False
                else:
                    print(f"Stage {stage_name} executed successfully")
                    # update stage end time and status
                    stage = stage_dict[stage_name]
                    stage.end_time = datetime.now()
                    stage.status = StageStatus.SUCCESS
                    asyncio.run(DB.get_repository(StageRepository).update(stage))

            # Update stage end time and status for cancelled stages
            for stage_name in cancelled_stages:
                stage = stage_dict[stage_name]
                stage.status = StageStatus.CANCELED
                asyncio.run(DB.get_repository(StageRepository).update(stage))

            # Get latest pipeline status
            p = asyncio.run(DB.get_repository(PipelineRepository).get(pipeline_id))
            if p.status == PipelineStatus.CANCELED:
                print(f"Pipeline {pipeline.pipeline_name} is already cancelled")
                CustomLogger.add(
                    f"Pipeline {pipeline.pipeline_name} is already cancelled"
                )
                continue

            p.end_time = datetime.now()
            # if p.start_time.tzinfo is None:  # If offset-naive
            p.start_time = p.start_time.replace(tzinfo=ZoneInfo("America/Los_Angeles"))
            # if p.end_time.tzinfo is None:  # If offset-naive
            p.end_time = p.end_time.replace(tzinfo=ZoneInfo("America/Los_Angeles"))
            p.running_time = (p.end_time - p.start_time).total_seconds()
            print(f"Continue: {continue_pipeline}, All successful: {all_successful}")
            p.status = (
                PipelineStatus.SUCCESS
                if (continue_pipeline and all_successful)
                else PipelineStatus.FAILED
            )
            p_status_dict[pipeline.pipeline_name].append(p.status)
            asyncio.run(DB.get_repository(PipelineRepository).update(p))
        return self.get_pipeline_result(p_status_dict)

    def execute_job(self, job):
        """
        Executes a job inside a Docker container.

        Args:
            job (object): A job object containing details about the job to be executed.

        Raises:
            RuntimeError: If there is an error during the execution of the job.
        """
        try:
            absolute_path = self.temp_dir
            volumes = {absolute_path: {"bind": "/app", "mode": "rw"}}
            work_dir = "/app"

            self.docker_runner.execute_job(job, work_dir, volumes, auto_clean=True)
        except Exception as e:
            raise RuntimeError(f"Error executing job: {e}")

    def _check_critical_failures(self, stage_jobs: list, job_dict):
        """
        Checks if there are any jobs in the given stage that failed and have allow_failure=False.

        Args:
            stage_name (str): The name of the stage to check.
            job_dict (dict): Dictionary of all jobs in the pipeline.

        Returns:
            bool: True if a critical failure is found, False otherwise.
        """
        for _, db_job in job_dict.items():
            for job in stage_jobs:
                if db_job.job_name == job.name:
                    if db_job.status == JobStatus.FAILED and not db_job.allow_failure:
                        return True
        return False

    def _check_allow_failure_failures(self, stage_jobs: list, job_dict):
        """
        Checks if there are any jobs in the given stage that failed and have allow_failure=True.

        Args:
            stage_name (str): The name of the stage to check.
            job_dict (dict): Dictionary of all jobs in the pipeline.

        Returns:
            bool: True if a job with allow_failure=True failed, False otherwise.
        """
        for _, db_job in job_dict.items():
            for job in stage_jobs:
                if db_job.job_name == job.name:
                    if db_job.status == JobStatus.FAILED and db_job.allow_failure:
                        return True
        return False

    async def _cancel_stage_jobs(self, stage_jobs, job_dict):
        """
        Marks all jobs in the given stage as CANCELLED.

        Args:
            stage_name (str): The name of the stage to cancel.
            job_dict (dict): Dictionary of all jobs in the pipeline.
        """
        for _, db_job in job_dict.items():
            for job in stage_jobs:
                if db_job.job_name == job.name:
                    if db_job.status in [JobStatus.PENDING, JobStatus.RUNNING]:
                        db_job.status = JobStatus.CANCELLED
                        await DB.get_repository(JobRepository).update(db_job)

    def get_pipeline_result(self, p_status_dict):
        """
        Retrieves a summary of the pipeline execution result.

        Returns:
            str: A message summarizing the triggered pipeline run, depending on whether a config file or pipeline name was provided.
        """
        summary_list = []
        # get pipeline result status
        for pipeline_name, info in p_status_dict.items():
            run_id = info[0]
            status = info[1] if len(info) > 1 else "CANCELED"
            summary_list.append(
                f"Pipeline '{pipeline_name}' (Run ID: {run_id}) status: {status.upper()}"
            )
        return "\n ".join(summary_list)
