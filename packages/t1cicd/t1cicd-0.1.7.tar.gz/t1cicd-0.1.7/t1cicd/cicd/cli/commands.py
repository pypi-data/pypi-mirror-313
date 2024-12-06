"""
CICD Commands
=============

This script defines the `CicdCommands` class, which provides various methods for interacting with CICD pipelines. 
It uses the `CICDClient` to send HTTP requests to the CICD server for operations like configuration checks, dry runs, 
report generation, pipeline execution, stopping, and canceling pipelines.

Classes:
    - CicdCommands: A collection of methods to manage and interact with CICD pipelines.
"""


class CicdCommands:
    """
    A collection of methods to manage and interact with CICD pipelines.

    Attributes:
        client (CICDClient): An instance of the CICD client for handling HTTP requests.
    """

    def __init__(self, client):
        """
        Initializes the CicdCommands with a CICD client.

        Args:
            client (CICDClient): An instance of the CICD client.
        """
        self.client = client

    def check_config(self, yaml_path):
        """
        Checks the validity of a pipeline configuration file.

        Args:
            yaml_path (str): Path to the YAML configuration file.

        Sends a POST request to the `/api/check-config` endpoint to validate the configuration.
        """
        payload = {"yaml_path": yaml_path}
        endpoint = "/api/check-config"
        response = self.client.request("POST", endpoint, payload, local=True)
        self.client.handle_response(response)

    def perform_dry_run(self, yaml_path):
        """
        Performs a dry run of the pipeline configuration.

        Args:
            yaml_path (str): Path to the YAML configuration file.

        Sends a POST request to the `/api/dry-run` endpoint to simulate the pipeline execution.
        """
        payload = {"yaml_path": yaml_path}
        endpoint = "/api/dry-run"
        response = self.client.request("POST", endpoint, payload, local=True)
        self.client.handle_response(response)

    def show_report(self, repo, local, pipeline, run, stage, job):
        """
        Displays a report of pipelines, runs, stages, or jobs.

        Args:
            repo (str): Repository path.
            local (bool): Whether to run the command locally.
            pipeline (str, optional): Pipeline name. Defaults to None.
            run (str, optional): Run number. Defaults to None.
            stage (str, optional): Stage name. Defaults to None.
            job (str, optional): Job name. Defaults to None.

        Depending on the provided arguments, sends a GET request to the appropriate `/api/report` endpoint.
        """
        payload = {"repo": repo}
        local = True  # Only for now
        if not pipeline and not run and not stage and not job:
            endpoint = "/api/report"
        elif pipeline and not run and not stage and not job:
            endpoint = f"/api/report/pipeline/{pipeline}"
        elif pipeline and run and not stage and not job:
            endpoint = f"/api/report/pipeline/{pipeline}/{run}"
        elif pipeline and not run and stage and not job:
            endpoint = f"/api/report/stage/{pipeline}/{stage}"
        elif pipeline and run and stage and not job:
            endpoint = f"/api/report/stage/{pipeline}/{stage}/{run}"
        elif pipeline and not run and stage and job:
            endpoint = f"/api/report/job/{pipeline}/{stage}/{job}"
        elif pipeline and run and stage and job:
            endpoint = f"/api/report/job/{pipeline}/{stage}/{job}/{run}"
        else:
            response = None
            self.client.handle_response(response)
            return

        response = self.client.request("GET", endpoint, payload, local)
        self.client.handle_response(response)

    def override_config(self, repo, local, override):
        """
        Overrides the configuration file for a repository.

        Args:
            repo (str): Repository path.
            local (bool): Whether to run the command locally.
            override (list): List of overrides for the configuration.

        Sends a POST request to the `/api/override-config` endpoint.
        """
        payload = {"repo": repo, "local": local, "override": override}
        endpoint = "/api/override-config"
        local = True  # Only for now
        response = self.client.request("POST", endpoint, payload, local)
        self.client.handle_response(response)

    def run_pipeline(self, repo, local, branch, commit, pipeline, file, verbose):
        """
        Executes a specific pipeline.

        Args:
            repo (str): Repository path.
            local (bool): Whether to run the command locally.
            branch (str): Branch name.
            commit (str): Commit hash.
            pipeline (str): Pipeline name.
            file (str): Path to the pipeline configuration file.
            verbose (bool): Whether to display verbose output.

        Sends a POST request to the `/api/run-pipeline` endpoint.
        """
        payload = {
            "repo": repo,
            "commit": commit,
            "branch_name": branch,
            "pipeline": pipeline,
            "file": file,
        }
        endpoint = "/api/run-pipeline"
        local = True  # Only for now
        response = self.client.request("POST", endpoint, payload, local)
        self.client.handle_response(response, verbose)

    def stop_pipeline(self, repo, local, branch, commit, pipeline, file):
        """
        Stops a specific pipeline in a repository.

        Args:
            repo (str): Repository path.
            local (bool): Whether to run the command locally.
            branch (str): Branch name.
            commit (str): Commit hash.
            pipeline (str): Pipeline name.
            file (str): Path to the pipeline configuration file.

        Sends a POST request to the `/api/stop-pipeline` endpoint.
        """
        payload = {
            "repo": repo,
            "commit": commit,
            "branch_name": branch,
            "pipeline": pipeline,
            "file": file,
        }
        endpoint = "/api/stop-pipeline"
        local = True  # Only for now
        response = self.client.request("POST", endpoint, payload, local)
        self.client.handle_response(response)

    def cancel_pipeline(self, repo, local, branch, commit, pipeline, run, verbose):
        """
        Cancels a running pipeline in a repository.

        Args:
            repo (str): Repository path.
            local (bool): Whether to run the command locally.
            branch (str): Branch name.
            commit (str): Commit hash.
            pipeline (str): Pipeline name.
            run (str): Run number.
            verbose (bool): Whether to display verbose output.

        Sends a POST request to the `/api/cancel-pipeline` endpoint.
        """
        payload = {
            "repo": repo,
            "commit": commit,
            "branch_name": branch,
            "pipeline": pipeline,
            "run_number": run,
        }
        endpoint = "/api/cancel-pipeline"
        local = True  # Only for now
        response = self.client.request("POST", endpoint, payload, local)
        self.client.handle_response(response, verbose)
