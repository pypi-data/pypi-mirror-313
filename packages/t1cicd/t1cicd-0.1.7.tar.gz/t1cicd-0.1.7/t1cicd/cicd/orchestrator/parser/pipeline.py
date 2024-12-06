"""
The pipeline module contains the ParsedPipeline class which is used to represent the parsed pipeline
"""

from typing import List

from pydantic import BaseModel, Field, model_validator

from t1cicd.cicd.orchestrator.parser.constants import DEFAULT_GLOBAL_KEYWORDS
from t1cicd.cicd.orchestrator.parser.job import ParsedJob
from t1cicd.cicd.orchestrator.parser.stage import ParsedStage
from t1cicd.cicd.orchestrator.parser.utils import get_dry_run_order


class ParsedPipeline(BaseModel):
    """
    The parsed pipeline corresponds to the content of YAML file

    """

    pipeline_name: str = Field(..., description="The name of the pipeline")
    parsed_stages: ParsedStage = Field(..., description="The stages to run")
    variables: dict = Field(..., description="The variables to use in the pipeline")

    @model_validator(mode="before")
    def populate_variables(cls, values):
        """
        Populate the job fields with variables if they are None

        Args:
            values: The values to populate

        Returns:
            The values with the populated job fields
        """
        # Check each field and populate from variables if None
        parsed_stages = values.get("parsed_stages")
        variables = values.get("variables")

        # Populate job fields with variables if they are None
        for _, jobs in parsed_stages.stages.items():
            for job in jobs:
                for keyword in DEFAULT_GLOBAL_KEYWORDS:
                    if (getattr(job, keyword, None) is None) and (keyword in variables):
                        setattr(job, keyword, variables[keyword])

        return values

    def get_jobs_in_stage(self, stage_name: str) -> list:
        """
        Get the jobs in the stage

        Args:
            stage_name (str): The name of the stage

        Returns:
            list: The jobs in the stage
        """
        return self.parsed_stages.get_jobs_in_stage(stage_name)

    def get_all_stage_names(self) -> list:
        """
        Get all the stage names

        Returns:
            list: All the stage names


        """
        return self.parsed_stages.get_all_stage_names()

    def get_all_jobs(self) -> dict[str, List[ParsedJob]]:
        """
        Get all the jobs


        Returns:
            dict: All the jobs

        """
        return self.parsed_stages.stages

    def get_all_stages(self) -> list[tuple[str, List[ParsedJob]]]:
        """
        Get all the stages

        Returns:
            list: All the stages

        """
        return self.parsed_stages.get_all_stages()

    def dry_run(self):
        """
        Print the order of execution

        """
        dry_run_order = get_dry_run_order(self.parsed_stages.stages)
        order = 0
        for stage in dry_run_order:
            for jobs in stage:
                print(f"{order}: {jobs}")
                order += 1

    # Execute the pipeline for now. This will be discarded and replaced by the actual execution in the future
    def execute_pipeline(self):
        """

        Execute the pipeline
        """
        for stage_name in self.get_all_stage_names():
            print(f"Executing Stage: {stage_name}")
            sorted_jobs = self.parsed_stages.get_sorted_jobs_in_stage(stage_name)
            for job in sorted_jobs:
                self.execute_job(job)

    def execute_job(self, job: ParsedJob):
        """
        Execute the job

        Args:
            job (ParsedJob): The job

        """
        print(f"Executing Job: {job.name}")

        if isinstance(job.script, list):
            for command in job.script:
                print(f"Running command: {command}")
        else:
            print(f"Running command: {job.script}")
        print(f"Job {job.name} completed.\n")
