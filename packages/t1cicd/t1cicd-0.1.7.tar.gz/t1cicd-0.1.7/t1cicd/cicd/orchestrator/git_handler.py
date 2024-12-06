"""
Git Handler
===========

This module provides the `HandleGit` class to manage Git repository operations such as cloning and checking out
branches and commits.

Classes:
    - HandleGit: Handles Git operations for CI/CD pipelines.

Functions:
    - clone_and_checkout: Clones a Git repository and checks out a specific branch and commit.
"""

import os
import subprocess

import git

from t1cicd.cicd.api.custom_logger import CustomLogger

from .utils import is_valid_remote_repo


class HandleGit:
    """
    A class to handle Git operations such as cloning and checking out branches or commits.

    Attributes:
        cur_dir (str): The current working directory.
        temp_dir (str): Directory for temporary Git operations.
        commit (str): The latest commit hash checked out.
    """

    def __init__(self):
        """
        Initializes the HandleGit object.

        Sets the current working directory and a temporary directory for Git operations.
        """
        self.cur_dir = os.getcwd()
        self.temp_dir = os.path.join(os.path.dirname(self.cur_dir), "temp")
        self.commit = None
        print(os.getcwd())

    def clone_and_checkout(self, repo=None, branch="main", commit=None, temp_dir=None):
        """
        Clones a Git repository and checks out a specific branch and commit.

        Args:
            repo (str, optional): URL or path of the Git repository. Defaults to None.
            branch (str, optional): Name of the branch to check out. Defaults to "main".
            commit (str, optional): Commit hash to check out. Defaults to None.
            temp_dir (str, optional): Temporary directory for cloning the repository. Defaults to None.

        Returns:
            str: The commit hash of the checked-out commit.

        Raises:
            ValueError: If no repository is provided, the repository is invalid, or Git operations fail.
        """
        temp_dir = temp_dir or self.temp_dir

        if not repo:
            try:
                local_repo = git.Repo(os.getcwd(), search_parent_directories=False)
                repo = local_repo.working_dir
                print(f"Using local repository at: {repo}")
                CustomLogger.add(f"Using local repository at: {repo}")
            except git.exc.InvalidGitRepositoryError:
                raise ValueError(
                    "No --repo provided and the current directory is not a Git repository"
                )

        if repo.startswith("http"):
            if not is_valid_remote_repo(repo):
                raise ValueError(
                    f"Remote repository '{repo}' does not exist or is not accessible."
                )
        elif not os.path.exists(repo) or not os.path.isdir(os.path.join(repo, ".git")):
            raise ValueError(
                f"Local repository '{repo}' does not exist or is not a valid Git repository."
            )

        if os.path.exists(temp_dir):
            subprocess.run(["rm", "-rf", temp_dir], check=True)

        try:
            git.Repo.clone_from(repo, temp_dir)
            print(f"Cloned repository from {repo} to {temp_dir}")
            CustomLogger.add(f"Cloned repository from {repo} to {temp_dir}")

            os.chdir(temp_dir)
            repo_clone = git.Repo(temp_dir)

            repo_clone.git.checkout(branch)
            if commit:
                self.commit = commit
                repo_clone.git.checkout(commit)
            else:
                latest_commit = repo_clone.head.commit.hexsha
                self.commit = latest_commit
                print(f"No commit specified, using latest commit: {latest_commit}")
                CustomLogger.add(
                    f"No commit specified, using latest commit: {latest_commit}"
                )
                repo_clone.git.checkout(latest_commit)
            commit_message = repo_clone.commit(self.commit).message.strip()
            return self.commit, commit_message

        except git.exc.GitCommandError as e:
            print(f"Error: Failed to clone repository '{repo}': {e}")
            raise ValueError(f"Failed to clone repository: {e}")


if __name__ == "__main__":
    git_handler = HandleGit()
    git_handler.clone_and_checkout(repo="~/Desktop/repo_example", branch="main")
