"""
Mock Configuration for --override
==================

This module provides a mock configuration for testing and development purposes, based on the system design.

Classes:
    - MockConfiguration: Creates an example configuration using parsed pipeline, stages, and jobs.
"""

# A mock configuration based on the system design


from t1cicd.cicd.orchestrator.parser.job import ParsedJob
from t1cicd.cicd.orchestrator.parser.pipeline import ParsedPipeline
from t1cicd.cicd.orchestrator.parser.stage import ParsedStage


class MockConfiguration:
    """
    Creates a mock configuration for testing CI/CD pipelines.

    Attributes:
        example_pipeline (ParsedPipeline): An example parsed pipeline configuration.
    """

    example_pipeline: ParsedPipeline

    def __init__(self):
        """
        Initializes the mock configuration with a predefined example pipeline.

        The pipeline includes:
        - A "build" stage with two jobs.
        - A "test" stage with one job.
        - A "deploy" stage with one job.
        """
        example_job1 = ParsedJob(
            name="test_job1",
            stage="build",
            image="python:3.8",
            script="python test.py",
        )
        example_job2 = ParsedJob(
            name="test_job2",
            stage="build",
            image="python:3.8",
            script="python test.py",
        )
        example_job3 = ParsedJob(
            name="test_job3",
            stage="test",
            image="python:3.8",
            script="python test.py",
        )
        example_job4 = ParsedJob(
            name="test_job4",
            stage="deploy",
            image="python:3.8",
            script="python test.py",
        )
        example_stages = ParsedStage(
            stages={
                "build": [example_job1, example_job2],
                "test": [example_job3],
                "deploy": [example_job4],
            }
        )

        self.example_pipeline = ParsedPipeline(
            pipeline_name="test_pipeline",
            parsed_stages=example_stages,
            variables={},
        )

    def load_config(self):
        """
        Loads the mock configuration.

        Returns:
            ParsedPipeline: The example parsed pipeline configuration.
        """
        return self.example_pipeline
