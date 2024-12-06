"""
Docker Job Runner
=================

This module provides the `DockerJobRunner` class for running CI/CD pipeline jobs inside Docker containers.

Classes:
    - DockerJobRunner: Manages the execution of pipeline jobs using Docker.
"""

import os

import docker
from docker.errors import DockerException, ImageNotFound


class DockerJobRunner:
    """
    A class to manage the execution of CI/CD pipeline jobs inside Docker containers.

    Attributes:
        client (docker.DockerClient): Docker client for interacting with Docker.
        doc_path (str): Path to the directory where logs are stored.
        volumes (dict): Dictionary of volume mappings for the Docker container.
        work_dir (str): Working directory inside the Docker container.
        pipeline_name (str): Name of the pipeline for which the job is executed.
    """

    def __init__(self, pipeline_name=None, absolute_path=None):
        """
        Initializes the DockerJobRunner.

        Args:
            pipeline_name (str, optional): Name of the pipeline. Defaults to None.
            absolute_path (str, optional): Path to the host directory to be mounted in the container. Defaults to None.
        """
        self.client = docker.from_env()
        base_directory = os.path.abspath(os.path.join(os.getcwd(), ".."))
        self.doc_path = f"{base_directory}/logs/{pipeline_name}"
        volumes = {
            absolute_path: {
                "bind": "/app",
                "mode": "rw",
            },
            self.doc_path: {
                "bind": "/app/docs",
                "mode": "rw",
            },
        }
        self.volumes = volumes
        self.work_dir = "/app"
        self.pipeline_name = pipeline_name

    def get_doc_path(self):
        """
        Returns the path to the directory where logs are stored.

        Returns:
            str: The log directory path.
        """
        return self.doc_path

    def execute_job(self, job, environment=None, auto_clean=False):
        """
        Executes a job inside a Docker container.

        This method:
        - Checks if the Docker image is available locally; pulls it if not.
        - Runs the container and executes the job's script.
        - Waits for the container to finish execution.
        - Writes the container's logs to a file.
        - Cleans up the container if `auto_clean` is True.

        Args:
            job (object): A parsed job containing the image name, script commands, etc.
            environment (dict, optional): Environment variables for the container. Defaults to None.
            auto_clean (bool, optional): Whether to clean up the container after execution. Defaults to False.

        Raises:
            RuntimeError: If any error occurs during image pull, container run, execution, or cleanup.
        """
        # 1, Check if the image is already present, if not pull it
        image_name = job.image
        try:
            # Check if the image is already available locally
            self.client.images.get(image_name)
        except ImageNotFound:
            # Pull the image if it doesn't exist locally
            try:
                self.client.images.pull(image_name)
            except DockerException as e:
                error_message = f"Docker error during image pull: {e}"
                raise RuntimeError(error_message)

        # 2, Run the container
        try:
            container = self.client.containers.run(
                image=image_name,
                command=f"/bin/sh -c '{' && '.join(job.script)}'",  # run the script one by one
                tty=True,  # Keep the terminal open
                working_dir=self.work_dir,
                volumes=self.volumes,
                environment=environment,
                name=f"{job.name}_container",
                detach=True,
            )
        except DockerException as e:
            error_message = f"Docker error during container run: {e}"
            raise RuntimeError(error_message)

        # 3, Wait for container to finish
        try:
            container.wait()
        except DockerException as e:
            error_message = f"Error waiting for container: {e}"
            raise RuntimeError(error_message)

        # 4, Write container logs to file
        try:
            self.write_container_logs_to_file(container)
        except RuntimeError as e:
            error_message = f"Error detected in logs: {e}"
            raise RuntimeError(error_message)
        except Exception as e:
            error_message = f"Error writing container logs to file: {e}"
            raise RuntimeError(error_message)

        # 5, Clean up the container
        finally:
            if auto_clean:
                try:
                    container.stop()
                    container.remove()
                except DockerException as e:
                    error_message = f"Failed to clean up container: {e}"
                    raise RuntimeError(error_message)

    def write_container_logs_to_file(self, container):
        """
        Writes logs from the Docker container to a file.

        Logs are stored in the directory corresponding to the pipeline name, and the file is named
        after the container.

        Args:
            container (docker.models.containers.Container): The Docker container object.

        Raises:
            RuntimeError: If writing logs or accessing container status fails.
        """
        try:
            # Add timestamps=True to get logs containing timestamps
            logs = container.logs(stdout=True, stderr=True, timestamps=True)

            # Move up one level from the current working directory
            base_directory = os.path.abspath(os.path.join(os.getcwd(), ".."))

            # Build the full log file path, including the container name
            directory_path = os.path.join(
                base_directory, "logs", f"{self.pipeline_name}"
            )

            # Ensure the directory exists
            os.makedirs(directory_path, exist_ok=True)

            container_file_path = os.path.join(
                directory_path, f"{container.name}_output.log"
            )

            # Write logs to file
            with open(container_file_path, "w", encoding="utf-8") as file:
                file.write(logs.decode("utf-8"))

            # Catch log error
            exit_code = container.wait().get("StatusCode")
            logs_decoded = logs.decode("utf-8")
            if exit_code != 0:
                raise RuntimeError(
                    f"Container exited with error status {exit_code}: {logs_decoded}"
                )

        except Exception as e:
            error_message = f"Error writing container logs to file: {e}"
            raise RuntimeError(error_message)
