"""
This module contains the StageParser class for parsing stage-related data.
"""

from pydantic import BaseModel, Field, model_validator

from t1cicd.cicd.orchestrator.parser.constants import DEFAULT_STAGE_WORKFLOWS
from t1cicd.cicd.orchestrator.parser.job import ParsedJob
from t1cicd.cicd.orchestrator.parser.utils import (
    check_circular_dependency,
    topological_sort_for_stage,
)


class ParsedStage(BaseModel):
    """
    The parsed stage class
    """

    stages: dict[str, list[ParsedJob]] = Field(
        default_factory=lambda: {stage: [] for stage in DEFAULT_STAGE_WORKFLOWS},
        description="The stages to run",
    )

    @model_validator(mode="after")
    def check_job_dependency(self):
        """
        Check for jobs that are not defined in the stages

        :raises ValueError: If there is a job that is not defined in the stages
        """
        for stage_name, jobs in self.stages.items():
            job_names = [job.name for job in jobs]
            for job in jobs:
                for need in job.needs:
                    if need not in job_names:
                        raise ValueError(
                            f"Job {job.name} in stage {stage_name} has undefined dependency {need}"
                        )
        return self

    @model_validator(mode="after")
    def check_circular_dependency(self):
        """
        Check for circular dependencies in the stages

        :raises ValueError: If there is a circular dependency
        """
        for stage_name, jobs in self.stages.items():
            if not check_circular_dependency(jobs):
                raise ValueError(f"Stage {stage_name} has circular dependency")
        return self

    def get_jobs_in_stage(self, stage_name: str) -> list:
        """
        Get the jobs in the stage

        :param stage_name: The name of the stage
        :return: The jobs in the stage
        """
        return self.stages.get(stage_name, [])

    def get_all_stage_names(self) -> list:
        """
        Get all the stage names

        :return: All the stage names
        """
        return list(self.stages.keys())

    def get_all_jobs(self) -> list:
        """
        Get all the jobs in the stages

        :return: All the jobs in the stages
        """
        return [job for jobs in self.stages.values() for job in jobs]

    def get_all_jobs_names(self) -> list[str]:
        """
        Get all the job names in the stages

        Returns:
            list: All the job names in the stages
        """
        return [job.name for jobs in self.get_all_jobs() for job in jobs]

    def get_all_stages(self) -> list[tuple[str, list[ParsedJob]]]:
        """
        Get all the stages and their jobs

        Returns:
            list: All the stages and their jobs
        """
        return list(self.stages.items())

    def get_sorted_jobs_in_stage(self, stage_name: str) -> list[ParsedJob]:
        """
        Get the jobs in the stage sorted according to their dependencies.

        :param stage_name: The name of the stage
        :return: The sorted jobs in the stage
        """
        jobs = self.get_jobs_in_stage(stage_name)
        job_dict = {job.name: job for job in jobs}

        # Build the dependency graph
        graph = {}
        for job in jobs:
            graph[job.name] = job.needs

        # Perform topological sort
        sorted_job_names = topological_sort_for_stage(graph)

        # Return the jobs in sorted order
        return [job_dict[name] for name in sorted_job_names]
