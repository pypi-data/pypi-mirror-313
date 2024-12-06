"""
CICD Client
===========

This script defines the `CICDClient` class, which provides methods to interact with a CICD server. It includes
functionality to send HTTP requests, handle responses, and display results using a rich console for better visualization.

Modules:
    - click: For command-line interaction.
    - requests: To make HTTP requests.
    - rich.console.Console: Provides a rich console for output.
    - rich.pretty.Pretty: Enables pretty printing of complex data structures.

Classes:
    - CICDClient: A client for interacting with local or remote CICD servers.

Functions:
    - print_response(response): Prints a formatted response using the rich console.
"""

import click
import requests
from rich.console import Console
from rich.pretty import Pretty

console = Console()


def print_response(response):
    """
    Prints a formatted response using the rich console.

    Args:
        response (Any): The response object or data to be printed.
    """
    console.print(Pretty(response))


class CICDClient:
    """
    A client for interacting with local or remote CICD servers.

    Attributes:
        local_base_url (str): Base URL for the local CICD server.
        remote_base_url (str): Base URL for the remote CICD server.
        headers (dict): HTTP headers to be sent with each request.
    """

    def __init__(
        self,
        local_base_url="http://127.0.0.1:5000",
        remote_base_url="https://remote-server.com",
    ):
        """
        Initializes the CICDClient with base URLs and default headers.

        Args:
            local_base_url (str, optional): Base URL for the local server. Defaults to "http://127.0.0.1:5000".
            remote_base_url (str, optional): Base URL for the remote server. Defaults to "https://remote-server.com".
        """
        self.local_base_url = local_base_url
        self.remote_base_url = remote_base_url
        self.headers = {
            "Content-Type": "application/json",
            # Add authentication headers here if needed
        }

    def request(self, method, endpoint, data=None, local=False):
        """
        Sends an HTTP request to the specified endpoint.

        Args:
            method (str): HTTP method (e.g., "GET", "POST").
            endpoint (str): API endpoint to which the request is sent.
            data (dict, optional): Data to be sent in the request body. Defaults to None.
            local (bool, optional): Whether to use the local or remote base URL. Defaults to False.

        Returns:
            requests.Response: The HTTP response object.

        Examples:
            response = client.request("POST", "/api/v1/run", data={"key": "value"}, local=True)
        """
        base_url = self.local_base_url if local else self.remote_base_url
        url = f"{base_url}{endpoint}"
        response = requests.request(
            method=method, url=url, timeout=3600, headers=self.headers, json=data
        )
        return response

    def handle_response(self, response=None, verbose=False):
        """
        Handles and processes the response from the CICD server.

        Depending on the HTTP status code, it prints the response message or error details. If verbose
        mode is enabled, additional data is displayed.

        Args:
            response (requests.Response, optional): The HTTP response object. Defaults to None.
            verbose (bool, optional): Whether to display verbose output. Defaults to False.

        Examples:
            client.handle_response(response, verbose=True)
        """
        if response is not None:
            status_code = response.status_code
            message = response.json().get("message")
            verbose_data = response.json().get("verbose_data")

            if status_code == 200:
                print_response(message)
                if verbose:
                    click.echo(verbose_data)
            elif status_code == 400:
                click.echo(f"Error message: {message}")
                if verbose:
                    click.echo(f"Verbose data: {verbose_data}")
            else:
                click.echo(f"Error message: {message}")
                if verbose:
                    click.echo(f"Verbose data: {verbose_data}")
        else:
            click.echo("No data returned from the backend or the request failed")
