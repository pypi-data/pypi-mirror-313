
# CLI

## Get Started

You can install CLI via pypi:

```
pip install t1cicd
```

To see the helper for CLI commands:

```
cicd --help
```

## Commands

### cicd

- Usage: cicd [OPTIONS] COMMAND [ARGS]...

  Entry point for the CICD CLI.

  This command is used to interact with the CICD server. If no subcommand is
  specified, it will check the configuration file or perform a dry run based
  on the provided options.

  Args:     ctx (click.Context): Click context object.     check (bool): Flag
  to indicate if the config file should be checked.     dryrun (bool): Flag to
  indicate if a dry run should be performed.     config_file (str): Path to
  the pipeline configuration file.

  Raises:     click.UsageError: If both --check and --dryrun flags are
  specified.

  Examples:     $ cicd --check     $ cicd --dryrun --config-file
  /path/to/config.yml

- Options:
  - -c, --check              Check config file.
  - -dr, --dryrun            Dry run.
  - -cf, --config-file TEXT  Path to config file.
  - -h, --help               Show this message and exit.

- Commands:
  - cancel  Cancel a specific pipeline in a repository.
  - report  Show a report of a pipeline or its components.
  - run     Run a specific pipeline or override the config file in a repo
  - stop    Stop a specific pipeline in a repository.

## Sub-Commands

### cicd report

- Usage: cicd report [OPTIONS]

 	 Show a report of a pipeline.
 	
  Use cases:

  1. no options are specified, show a report of all pipelines.

  2. --pipeline is specified, show a report of all runs for the pipeline.

  3. --pipeline and --run are specified, show a report of the run for the
  pipeline.

  4. --pipeline and --stage are specified, show a report of all runs in the
  stage.

  5. --pipeline, --run, and --stage are specified, show a report of the run in
  the stage.

  6. --pipeline, --stage, and --job are specified, show a report of all runs
  in the job.

  7. --pipeline, --run, --stage, and --job are specified, show a report of the
  run in the job.

  8. otherwise, no report is shown.

- Options:
  - -r, --repo TEXT      Repository path.  [required]
  - -l, --local          Run locally.
  - -p, --pipeline TEXT  Pipeline name.
  - -rn, --run TEXT      Run number.
  - -s, --stage TEXT     Stage name.
  - -j, --job TEXT       Job name.
  - -h, --help           Show help message and exit.

### cicd run

- Usage: cicd run [OPTIONS]

  Run a specific pipeline or override the config file in a repository.
  
    If --override is specified, override the config file with the new config.
  
    if either --pipeline or --file is specified, run the specific pipeline.
  
    Otherwise, run all pipelines in the repository.
  
- Options:

  - -r, --repo TEXT      Repository path.  [default: (current local directory)]
  - -l, --local          Run locally.
  - -b, --branch TEXT    Branch name.  [default: (main branch)]
  - -c, --commit TEXT    Commit hash.  [default: (the latest commit)]
  - -p, --pipeline TEXT  Pipeline name.
  - -f, --file TEXT      Path to config file.
  - -o, --override TEXT  Override config file.
  - -v, --verbose        Verbose output.
  - -h, --help           Show this message and exit.

### cicd cancel

- Usage: cicd cancel [OPTIONS]

  Cancel a specific pipeline in a repository.

  If the specified pipeline is running, it will be canceled.

  If the specified pipeline is not running, nothing will happen.

- Options:
  - -r, --repo TEXT      Repository path.  [default: (current local directory)]
  - -l, --local          Run locally.
  - -b, --branch TEXT    Branch name.  [default: (main branch)]
  - -c, --commit TEXT    Commit hash.  [default: (the latest commit)]
  - -p, --pipeline TEXT  Pipeline name.
  - -rn, --run TEXT      Run number.
  - -v, --verbose        Verbose output.
  - -h, --help           Show this message and exit.


### cicd stop [Not Fully Implemented]

- Usage: cicd stop [OPTIONS]

  	Stop a specific pipeline in a repository.
    if either --pipeline or --file is specified, stop the specific pipeline.
    Otherwise, stop all pipelines in the repository.

- Options:
  - -r, --repo TEXT    Repository path.  [default: (current local directory)]
  - -l, --local        Run locally.
  - -b, --branch TEXT  Branch name.  [default: (main branch)]
  - -c, --commit TEXT  Commit hash.  [default: (the latest commit)]
  - -p, --pipeline TEXT  Pipeline name.
  - -f, --file TEXT      Path to config file.
  - -h, --help         Show help message and exit.