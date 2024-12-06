"""
CICD CLI
========

This script provides a command-line interface (CLI) for interacting with a CICD server. It includes commands to 
check configurations, perform dry runs, generate reports, run pipelines, stop pipelines, and cancel pipelines.

Modules:
    - click: CLI framework for creating commands.
    - CICDClient: Client for communicating with the CICD server.
    - CicdCommands: Wrapper for executing CICD-related operations.
    - is_git_repo: Utility function to check if the path is a valid Git repository.

Commands:
    cicd: Entry point for the CLI. Allows checking configurations and performing dry runs.
    report: Displays a report of a pipeline or its components.
    run: Executes a pipeline or overrides configuration files.
    stop: Stops a pipeline in a repository.
    cancel: Cancels a running pipeline.
"""

import click

from t1cicd.cicd.cli.client import CICDClient
from t1cicd.cicd.cli.commands import CicdCommands

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option("--check", "-c", is_flag=True, help="Check config file.")
@click.option("--dryrun", "-dr", is_flag=True, help="Dry run.")
@click.option(
    "--config-file",
    "-cf",
    default="./.cicd-pipelines/pipeline.yml",
    help="Path to config file.",
)
@click.pass_context
def cicd(ctx, check, dryrun, config_file):
    """
    Entry point for the CICD CLI.

    This command is used to interact with the CICD server. If no subcommand is specified, it will check
    the configuration file or perform a dry run based on the provided options.

    Args:
        ctx (click.Context): Click context object.
        check (bool): Flag to indicate if the config file should be checked.
        dryrun (bool): Flag to indicate if a dry run should be performed.
        config_file (str): Path to the pipeline configuration file.

    Raises:
        click.UsageError: If both --check and --dryrun flags are specified.

    Examples:
        $ cicd --check
        $ cicd --dryrun --config-file /path/to/config.yml
    """
    ctx.ensure_object(dict)
    ctx.obj["client"] = CICDClient()
    cicd_cmds = CicdCommands(ctx.obj["client"])

    if ctx.invoked_subcommand is None:
        if check and dryrun:
            raise click.UsageError("Cannot specify both --check and --dryrun")
        if dryrun:
            cicd_cmds.perform_dry_run(config_file)
            print(f"Performing dry run with config file: {config_file}")
        else:
            cicd_cmds.check_config(config_file)
            print(f"Checking config file: {config_file}")
    else:
        pass


@cicd.command()
@click.option("--repo", "-r", required=True, help="Repository path.")
@click.option("--local", "-l", is_flag=True, help="Run locally.")
@click.option("--pipeline", "-p", help="Pipeline name.")
@click.option("--run", "-rn", "run_number", help="Run number.")
@click.option("--stage", "-s", help="Stage name.")
@click.option("--job", "-j", help="Job name.")
@click.pass_context
def report(ctx, repo, local, pipeline, run_number, stage, job):
    """
    Show a report of a pipeline or its components.

    The report provides detailed information about pipelines, runs, stages, or jobs depending
    on the specified options.

    Args:
        ctx (click.Context): Click context object.
        repo (str): Path to the repository.
        local (bool): Whether to run the command locally.
        pipeline (str, optional): Name of the pipeline.
        run_number (str, optional): Run number.
        stage (str, optional): Name of the stage.
        job (str, optional): Name of the job.

    Examples:
        $ cicd report --repo /path/to/repo --pipeline my_pipeline
        $ cicd report --repo /path/to/repo --local
    """

    cicd_cmds = CicdCommands(ctx.obj["client"])
    cicd_cmds.show_report(repo, local, pipeline, run_number, stage, job)


@cicd.command()
@click.option(
    "--repo",
    "-r",
    default="./",
    show_default="current local directory",
    help="Repository path.",
)
@click.option("--local", "-l", is_flag=True, help="Run locally.")
@click.option("--branch", "-b", show_default="main branch", help="Branch name.")
@click.option("--commit", "-c", show_default="the latest commit", help="Commit hash.")
@click.option("--pipeline", "-p", help="Pipeline name.")
@click.option("--file", "-f", help="Path to config file.")
@click.option("--override", "-o", multiple=True, help="Override config file.")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output.")
@click.pass_context
def run(ctx, repo, local, branch, commit, pipeline, file, override, verbose):
    """
    Run a specific pipeline or override the config file in a repository.

    If --override is specified, override the config file with the new config.

    Args:
        ctx (click.Context): Click context object.
        repo (str): Path to the repository.
        local (bool): Whether to run the command locally.
        branch (str, optional): Branch name. Defaults to "main".
        commit (str, optional): Commit hash. Defaults to "HEAD".
        pipeline (str, optional): Pipeline name.
        file (str, optional): Path to the configuration file.
        override (list, optional): List of overrides for the configuration file.
        verbose (bool): Verbose output flag.

    Raises:
        click.UsageError: If invalid combinations of flags are specified.

    Examples:
        $ cicd run --repo /path/to/repo --pipeline my_pipeline
        $ cicd run --repo /path/to/repo --override key=value
    """

    if override and (branch or commit):
        raise click.UsageError("Cannot specify both --branch/--commit and --override")

    if pipeline and file:
        raise click.UsageError("Cannot specify both --pipeline and --file")

    if override:
        cicd_cmds = CicdCommands(ctx.obj["client"])
        cicd_cmds.override_config(repo, local, override)
        print(f"Overriding config file with: {override}")
        return

    cicd_cmds = CicdCommands(ctx.obj["client"])
    cicd_cmds.run_pipeline(repo, local, branch, commit, pipeline, file, verbose)


@cicd.command()
@click.option(
    "--repo",
    "-r",
    default="./",
    show_default="current local directory",
    help="Repository path.",
)
@click.option("--local", "-l", is_flag=True, help="Run locally.")
@click.option(
    "--branch",
    "-b",
    default="main",
    show_default="main branch",
    help="Branch name.",
)
@click.option(
    "--commit",
    "-c",
    default="HEAD",
    show_default="the latest commit",
    help="Commit hash.",
)
@click.option("--pipeline", "-p", help="Pipeline name.")
@click.option("--file", "-f", help="Path to config file.")
@click.pass_context
def stop(ctx, repo, local, branch, commit, pipeline, file):
    """
    Stop a specific pipeline in a repository.

    Args:
        ctx (click.Context): Click context object.
        repo (str): Path to the repository.
        local (bool): Whether to run the command locally.
        branch (str, optional): Branch name. Defaults to "main".
        commit (str, optional): Commit hash. Defaults to "HEAD".
        pipeline (str, optional): Pipeline name.
        file (str, optional): Path to the configuration file.

    Examples:
        $ cicd stop --repo /path/to/repo --pipeline my_pipeline
    """

    cicd_cmds = CicdCommands(ctx.obj["client"])
    cicd_cmds.stop_pipeline(repo, local, branch, commit, pipeline, file)
    print(f"Stopping pipeline in repo: {repo}")


@cicd.command()
@click.option(
    "--repo",
    "-r",
    default="./",
    show_default="current local directory",
    help="Repository path.",
)
@click.option("--local", "-l", is_flag=True, help="Run locally.")
@click.option("--branch", "-b", show_default="main branch", help="Branch name.")
@click.option("--commit", "-c", show_default="the latest commit", help="Commit hash.")
@click.option("--pipeline", "-p", help="Pipeline name.")
@click.option("--run", "-rn", "run_number", help="Run number.")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output.")
@click.pass_context
def cancel(ctx, repo, local, branch, commit, pipeline, run_number, verbose):
    """
    Cancel a specific pipeline in a repository.

    If the specified pipeline is running, it will be canceled.
    Otherwise, no action will be taken.

    Args:
        ctx (click.Context): Click context object.
        repo (str): Path to the repository.
        local (bool): Whether to run the command locally.
        branch (str, optional): Branch name.
        commit (str, optional): Commit hash.
        pipeline (str, optional): Pipeline name.
        run_number (str, optional): Run number.
        verbose (bool): Verbose output flag.

    Examples:
        $ cicd cancel --repo /path/to/repo --pipeline my_pipeline
    """

    cicd_cmds = CicdCommands(ctx.obj["client"])
    cicd_cmds.cancel_pipeline(
        repo, local, branch, commit, pipeline, run_number, verbose
    )


def main():
    """
    Main entry point for the CICD CLI.
    """
    cicd()


if __name__ == "__main__":
    cicd()
