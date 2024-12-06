"""
This module contains the Parser class for handling parsing operations.
"""

import yaml

from t1cicd.cicd.orchestrator.parser.job import ParsedJob
from t1cicd.cicd.orchestrator.parser.keyword_parser import KeywordParserFactory
from t1cicd.cicd.orchestrator.parser.pipeline import ParsedPipeline
from t1cicd.cicd.orchestrator.parser.stage import ParsedStage
from t1cicd.cicd.orchestrator.parser.utils import is_default_keyword


class YAMLParser:
    """
    YAMLParser class for handling parsing operations.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse(self) -> ParsedPipeline:
        """
        Parse the pipeline file.

        Returns:
            ParsedPipeline: The parsed pipeline object.

        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            yaml_obj = yaml.safe_load(file)
            if yaml_obj.get("jobs") is None:
                raise ValueError("Invalid pipeline file, jobs are not defined")
            if yaml_obj.get("name") is None:
                raise ValueError("Invalid pipeline file, name is not defined")
            pipeline_name = yaml_obj.get("name")
            variables = {}
            parsed_stage = ParsedStage()
            if yaml_obj.get("default"):
                if not all(
                    is_default_keyword(k) for k in list(yaml_obj["default"].keys())
                ):
                    raise ValueError("Invalid default keyword")
                for k, v in yaml_obj.get("default").items():
                    variables[k] = KeywordParserFactory.get_parser(k).parse(v)
            if yaml_obj.get("stages"):
                stage_names = yaml_obj.get("stages")
                if len(set(stage_names)) != len(stage_names):
                    raise ValueError("Duplicate stage names")
                parsed_stage = ParsedStage(
                    stages={stage: [] for stage in yaml_obj.get("stages")}
                )

            for job_name, job_config in yaml_obj["jobs"].items():
                fields = {
                    k: KeywordParserFactory.get_parser(k).parse(v)
                    for k, v in job_config.items()
                }
                fields["name"] = job_name
                job = ParsedJob(**fields)
                # add job to stage
                stage_name = job.stage
                if stage_name not in parsed_stage.stages:
                    raise ValueError(f"Invalid stage {stage_name}")
                parsed_stage.stages[stage_name].append(job)

            pipeline = ParsedPipeline(
                pipeline_name=pipeline_name,
                parsed_stages=parsed_stage,
                variables=variables,
            )
            # print(pipeline)
            return pipeline
