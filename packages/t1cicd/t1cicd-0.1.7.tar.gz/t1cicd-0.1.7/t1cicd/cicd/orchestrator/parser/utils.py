"""
Utility functions for the parser module.
"""

from collections import defaultdict

from t1cicd.cicd.orchestrator.parser.constants import (
    DEFAULT_GLOBAL_KEYWORDS,
    JOB_KEYWORDS,
)
from t1cicd.cicd.orchestrator.parser.job import ParsedJob


def is_default_keyword(keyword: str) -> bool:
    """
    Check if the keyword is a default global keyword.

    Args:
        keyword (str): The keyword to check

    Returns:
        bool: True if the keyword is a default global keyword, False otherwise

    """
    return keyword in DEFAULT_GLOBAL_KEYWORDS


def topological_sort(jobs: list[ParsedJob]):
    """

    Perform a topological sort on the dependency graph.

    Args:
        jobs (list[ParsedJob]): The list of parsed jobs

    Returns:
        list: A list of job names in execution order

    """
    # Create a graph representation
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    for job in jobs:
        for dependency in job.needs:
            graph[dependency].append(job.name)
            in_degree[job.name] += 1

    # Initialize queue with jobs that have no dependencies
    queue = [job.name for job in jobs if in_degree[job.name] == 0]

    result = []
    while queue:
        # Jobs at the same level can be executed simultaneously
        level = []
        for _ in range(len(queue)):
            job_name = queue.pop(0)
            level.append(job_name)

            # Reduce in-degree for dependent jobs
            for dependent in graph[job_name]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        result.append(level)

    # Check for cycles
    if len([job for level in result for job in level]) != len(jobs):
        raise ValueError("Cyclic dependency detected")

    return result


def get_dry_run_order(stages: dict[str, list[ParsedJob]]) -> list:
    """
    Get the order of execution for the stages.

    Args:

        stages (dict[str, list[ParsedJob]]): The stages and their jobs

    Returns:
        list: The order of execution for the stages
    """
    result = []
    for _, jobs in stages.items():
        execution_order = topological_sort(jobs)
        result.append(execution_order)
    return result


def check_circular_dependency(jobs: list[ParsedJob]) -> bool:
    """
    Check for circular dependencies in the jobs.

    Args:
        jobs (list[ParsedJob]): The list of parsed jobs

    Returns:
        bool: True if there are no circular dependencies, False otherwise
    """
    try:
        topological_sort(jobs)
    except ValueError:
        return False
    return True


def is_valid_override(override):
    """
    Check if the override format is valid.

    Args:
        override (list[str]): The list of overrides

    Returns:
        bool: True if the override format is valid, False otherwise
    """
    if override:
        for ovr in override:
            if "=" not in ovr:
                print(f"Invalid override format: {override}")
                continue
            key_path, value = ovr.split("=", 1)
            if not key_path or not value:
                print(f"Invalid override format: {override}")
                continue
            # check key_path format valid
            keys = key_path.split(".")
            if keys[0] == "default":
                if keys[1] not in DEFAULT_GLOBAL_KEYWORDS or len(keys) != 2:
                    print(f"Invalid override format: {override}")
                    continue
            elif keys[0] == "name" or keys[0] == "stages":
                if len(keys) != 1:
                    print(f"Invalid override format: {override}")
                    continue
            elif keys[0] == "jobs":
                if keys[2] not in JOB_KEYWORDS or len(keys) != 3:
                    print(f"Invalid override format: {override}")
                    continue
            else:
                print(f"Invalid override format: {override}")
                continue

    return True


def apply_override(config, override):
    """
    Recursively navigate through the config dictionary using the key path
    and set the value at the appropriate location.
    """
    for ovr in override:
        key_path, value = ovr.split("=", 1)
        keys = key_path.split(".")
        if keys[0] == "name":
            config.pipeline_name = value
            continue
        if keys[0] == "default" and keys[1] in DEFAULT_GLOBAL_KEYWORDS:
            config.variables[keys[1]] = value
            continue
        if keys[0] == "jobs":
            if keys[2] in JOB_KEYWORDS:
                stage_jobs = config.get_all_jobs()
                cur_stage = None
                for stage, jobs in stage_jobs.items():
                    if keys[1] in [job.name for job in jobs]:
                        cur_stage = stage
                        break
                if not cur_stage:
                    raise ValueError(f"Job {keys[1]} not found in any stage")
                for job in stage_jobs[cur_stage]:
                    if job.name == keys[1]:
                        setattr(job, keys[2], value)
                        break
                if keys[2] == "stage":
                    # update the stage for the job in the stage
                    for stage, jobs in stage_jobs.items():
                        for job in jobs:
                            if job.name == keys[1]:
                                stage_jobs[stage].remove(job)
                                stage_jobs[value].append(job)
                                break
            continue
        if keys[0] == "stages":
            # value is a list of stage names like: ["build", "pre-tests", "tests", "deploy"]
            # check if value contains all the stages in the pipeline while it can have extra stages
            value = value[1:-1].split(", ")
            if not set(config.get_all_stage_names()).issubset(set(value)):
                raise ValueError(f"Invalid override format: {ovr}")

            # create ParsedStage object with the stages in the override that is not in the pipeline
            # and add it to the config
            print(value)
            new_stages = {stage: [] for stage in value}
            for stage, jobs in config.parsed_stages.stages.items():
                new_stages[stage] = jobs
            config.parsed_stages.stages = new_stages
            continue

        raise ValueError(f"Invalid override format: {ovr}")


def topological_sort_for_stage(graph: dict[str, list[str]]) -> list[str]:
    """
    Perform a topological sort on the dependency graph.

    :param graph: A dictionary representing the dependency graph
    :return: A list of job names in execution order
    """
    visited = set()
    temp_mark = set()
    result = []

    def visit(node):
        if node in temp_mark:
            raise ValueError(f"Circular dependency detected: {node}")
        if node not in visited:
            temp_mark.add(node)
            for neighbor in graph.get(node, []):
                visit(neighbor)
            temp_mark.remove(node)
            visited.add(node)
            result.append(node)

    for node in graph:
        visit(node)

    return result[::-1]  # Reverse the result to get the correct order
