"""
This module contains the factory for creating relationships between different models.
"""

from t1cicd.cicd.db.model.job import Job
from t1cicd.cicd.db.model.pipeline import Pipeline
from t1cicd.cicd.db.model.stage import Stage
from t1cicd.cicd.db.transform.base import ModelRelationship


class TransformFactory:
    """
    A factory class for creating relationships between different models.

    This class provides static methods to create relationships between
    Pipeline, Stage, and Job models.
    """

    @staticmethod
    def create_pipeline_stage_relationship() -> ModelRelationship[Pipeline, Stage]:
        """
        Create a relationship between a pipeline and its stages

        Returns:
            ModelRelationship[Pipeline, Stage]: The relationship between a pipeline and its stages

        """
        return ModelRelationship(
            parent_model=Pipeline, related_model=Stage, related_ids_field="stage_ids"
        )

    @staticmethod
    def create_stage_job_relationship() -> ModelRelationship[Stage, Job]:
        """

        Create a relationship between a stage and its jobs

        Returns:
            ModelRelationship[Stage, Job]: The relationship between a stage and its jobs


        """
        return ModelRelationship(
            parent_model=Stage, related_model=Job, related_ids_field="job_ids"
        )

    @staticmethod
    def create_pipeline_stage_job_relationship() -> ModelRelationship[Pipeline, Stage]:
        """
        Create a relationship between a pipeline and its stages and jobs

        Returns:
            ModelRelationship[Pipeline, Stage]: The relationship between a pipeline and its stages and jobs


        """
        stage_job_summary = TransformFactory.create_stage_job_relationship()
        return ModelRelationship(
            parent_model=Pipeline,
            related_model=Stage,
            related_ids_field="stage_ids",
            nested_relationship=stage_job_summary,
        )
