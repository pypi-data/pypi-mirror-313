
# Orchestrator

This is the Orchestrator that automates the execution of pipeline stages and jobs defined in a configuration file. The orchestrator uses Docker containers to run jobs, ensuring isolated, reproducible environments.
It needs the API server to be running and also the setup of the database.

## Overview
The orchestrator consists of three main components:

#### 1. Pipeline Scheduler (pipeline_scheduler.py)
Responsible for cloning Git repositories, parsing pipeline configuration files, and orchestrating the execution of pipeline stages.

#### 2. Job Scheduler (job_scheduler.py)
Executes jobs within a pipeline stage. Jobs in the same stage run in parallel if they have no dependencies.
The job scheduler also manages job failures.

#### 3. Git Handler (git_handler.py)
Handles Git operations such as cloning repositories and checkout branches and commits.

### Features
#### 1. Repository Cloning:
Clones the specified Git repository and retrieves the pipeline configuration file (pipeline.yml).

#### 2. Pipeline Configuration Parsing:
Parses the pipeline configuration to identify stages, jobs, and dependencies.

#### 3. Stage-Oriented Execution:
Executes pipeline stages in the defined order. Jobs within a stage are executed concurrently if no dependencies are specified.

#### 4. Job Dependency Management:
Ensures that dependent jobs are executed in the correct order. Jobs can only run after their dependencies have completed successfully.

#### 5. Docker-Based Execution:
Each job runs inside a Docker container for isolation and reproducibility. It will interact with the docker runner module to run the jobs.

#### 6. Failure Handling:
Monitors job execution, handles failures. If allow failure is set to true, the pipeline continues execution even if a job fails.
The status of the pipeline is failed after the completion of the pipeline. If allow failure is set to false, the pipeline stops execution after a job failure.


## Git Handler Design

This document outlines the design of the Git Handler module, which is used to clone Git repositories and manage branches or commits.

### Workflow
1. Validate the Repository
   - Check if the repository is valid (remote or local).

2. Checkout Branch and Commit
   1. Switch to the specified branch.
   2. Check out the commit (or the latest commit if none is specified).

3. Clone the Repository
   - Clone the repository into the temporary directory.

### Behavior of Temporary Directory
- Path: `/t1-cicd/tmp`

- Automatic Creation:

    If the t1-cicd/tmp directory does not exist, it will be automatically created during the cloning process.
- Overwriting:
  
  Every time the module is invoked, the contents of `/t1-cicd/tmp` are cleared and replaced with the newly cloned repository.

### Error Handling
- Invalid Repository:
Ensures that the repository exists and is accessible.

### Purpose of Return Values

- Returned Values:

`self.commit`: The commit hash of the checked-out commit.

`commit_message`: The message associated with the checked-out commit.

- After cloning and checking out a repository, the pipeline use these values to update the database with the version of the code it executed