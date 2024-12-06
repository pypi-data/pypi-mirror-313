"""
Utilities
=========

This module provides utility functions for working with YAML configuration files and validating remote Git repositories.

Functions:
    - find_yaml_config(): Searches for a YAML configuration file in the current directory.
    - is_valid_remote_repo(repo_url): Checks if a remote Git repository is valid.
"""

import git
import requests


def is_valid_remote_repo(repo_url):
    """
    Checks if a remote Git repository is valid.

    This function attempts to validate the repository by:
    1. Checking if the URL is accessible via an HTTP(S) request for HTTP(S) URLs.
    2. Handling Git exceptions for non-HTTP(S) repository URLs.

    Args:
        repo_url (str): The URL of the remote Git repository.

    Returns:
        bool: True if the repository is valid, False otherwise.

    Example:
        >>> is_valid_remote_repo("https://github.com/example/repo.git")
        True
    """
    try:
        # Check if it's an HTTP(S) repository
        if repo_url.startswith("http"):
            # Make a simple request to check if the URL exists
            response = requests.get(repo_url, timeout=10)
            return response.status_code == 200
    except git.exc.GitCommandError:
        return False
    except requests.exceptions.RequestException:
        return False
    return False
