# Database Schema Documentation

## Table: pipelines

### Description

The `pipelines` table stores information about CI/CD pipelines.

### Columns

| Column Name    | Data Type                | Constraints                                                  | Description                                   |
|----------------|--------------------------| ------------------------------------------------------------ |-----------------------------------------------|
| id             | UUID                     | `PRIMARY KEY`, `DEFAULT uuid_generate_v4()`                  | Unique identifier for each pipeline.          |
| run_id         | BIGSERIAL                |                                                              | Sequential ID for pipeline runs.              |
| repo_url       | VARCHAR(255)             | `NOT NULL`                                                   | URL of the repository associated with the pipeline. |
| status         | VARCHAR(20)              | `NOT NULL`, `CHECK (status IN ('pending', 'running', 'success', 'failed', 'canceled'))` | Current status of the pipeline execution.     |
| pipeline_name  | VARCHAR(255)             |                                                              | Name of the pipeline, if applicable.          |
| running_time   | FLOAT                    |                                                              | Total running time of the pipeline, in seconds. |
| start_time     | TIMESTAMP WITH TIME ZONE |                                                              | The timestamp indicating when the pipeline started. |
| end_time       | TIMESTAMP WITH TIME ZONE |                                                              | The timestamp indicating when the pipeline ended. |
| git_branch     | VARCHAR(255)             | `NOT NULL`                                                   | Git branch associated with the pipeline.      |
| git_hash       | VARCHAR(40)              | `NOT NULL`                                                   | Git commit hash associated with the pipeline. |
| git_comment    | TEXT                     |                                                              | Commit message or description associated with the pipeline. |
| created_at     | TIMESTAMP WITH TIME ZONE | `DEFAULT CURRENT_TIMESTAMP`                                  | Timestamp of when the pipeline record was created. |
| updated_at     | TIMESTAMP WITH TIME ZONE | `DEFAULT CURRENT_TIMESTAMP`                                  | Timestamp of when the pipeline record was last updated. |


### Additional Information

- **indexes**

  - **idx_pipelines_status**: Index on `status` for faster lookups.

  - **idx_pipelines_git_branch**: Index on `git_branch` for faster lookups.

  - **idx_pipelines_created_at**: Index on `created_at` for faster lookups.


## Table: stages

### Description

The `stages` table stores information about stages within a pipeline.

### Columns

| Column Name | Data Type      | Constraints                                                  | Description                                                  |
|-------------|----------------| ------------------------------------------------------------ | ------------------------------------------------------------ |
| id          | UUID           | Primary Key, Default `uuid_generate_v4()`                    | Unique identifier for each stage record.                     |
| pipeline_id | UUID           | Foreign Key, NOT NULL                                        | References `pipelines(id)`; associates the stage with a specific pipeline. |
| stage_name  | VARCHAR(100)   | NOT NULL                                                     | Descriptive name of the stage.                               |
| status      | VARCHAR(20)    | NOT NULL, Default `'pending'`, CHECK (`status` IN `('pending', 'running', 'success', 'failed')`) | Current status of the stage. Possible values: `pending`, `running`, `success`, `failed`. |
| start_time  | TIMESTAMPTZ    |                                                              | Timestamp marking when the stage began.                      |
| end_time    | TIMESTAMPTZ    |                                                              | Timestamp marking when the stage ended.                      |
| stage_order | INTEGER        | NOT NULL, UNIQUE with `pipeline_id`                          | Defines the order of this stage within its pipeline, unique per pipeline. |
| created_at  | TIMESTAMPTZ    | NOT NULL, Default `CURRENT_TIMESTAMP`                        | Timestamp when this stage record was created.                |
| updated_at  | TIMESTAMPTZ    | NOT NULL, Default `CURRENT_TIMESTAMP`                        | Timestamp when this stage record was last updated.           |



### Additional Information

- **Indexes**:

  - idx_stages_pipeline_id: Index on `pipeline_id` for faster lookups.

  - idx_stages_stage_order: Index on `stage_order` for faster lookups.




## Table: jobs

### Description

This table tracks individual job records associated with specific stages in a process. Each job has a status, start and end times, and can be retried a specified number of times.

### Columns

| Column Name  | Data Type      | Constraints                                                                                 | Description                                                  |
|--------------|----------------|---------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| id           | UUID           | Primary Key, Default `uuid_generate_v4()`                                                  | Unique identifier for each job record.                       |
| stage_id     | UUID           | Foreign Key, NOT NULL                                                                       | References `stages(id)`; identifies the stage associated with this job. |
| job_name     | VARCHAR(100)   | NOT NULL                                                                                    | Descriptive name of the job.                                 |
| job_order    | INTEGER        | NOT NULL                                                                                    | Indicates the execution order of this job within a stage.    |
| status       | VARCHAR(20)    | NOT NULL, Default `'pending'`, CHECK (`status` IN `('pending', 'running', 'success', 'failed', 'cancelled', 'skipped')`) | Current status of the job. Possible values: `pending`, `running`, `success`, `failed`, `cancelled`, `skipped`. |
| start_time   | TIMESTAMPTZ    |                                                                                             | Timestamp indicating when the job started.                   |
| end_time     | TIMESTAMPTZ    |                                                                                             | Timestamp indicating when the job ended.                     |
| retry_count  | INTEGER        | NOT NULL, Default `0`                                                                       | Number of times this job has been retried.                   |
| created_at   | TIMESTAMPTZ    | NOT NULL, Default `CURRENT_TIMESTAMP`                                                       | Timestamp when this job record was created.                  |
| updated_at   | TIMESTAMPTZ    | NOT NULL, Default `CURRENT_TIMESTAMP`                                                       | Timestamp when this job record was last updated.             |


### Additional Information

- **Foreign Keys**: `stage_id` references `stages(id)`, with `ON DELETE CASCADE` ensuring that if a related stage is deleted, associated jobs are also removed.

- **Status Enum**: The `status` column is restricted to specific values (`pending`, `running`, `success`, `failed`, `cancelled`, `skipped`) to standardize job states across the system.
- **Automatic Timestamps**:
  - `created_at` and `updated_at` columns have default values to automatically log creation and update events.
- **Indexes**:
  - Primary key on `id`.
- **Notes**:
  - The `retry_count` field can help in tracking resilience by monitoring retry attempts for each job.

## Table: artifacts

### Description

The `artifacts` table stores information about artifacts related to jobs in the CI/CD pipeline.

### Columns

| Column Name | Data Type                | Constraints                                     | Description                               |
| ----------- | ------------------------ | ----------------------------------------------- | ----------------------------------------- |
| id          | UUID                     | PRIMARY KEY, DEFAULT uuid_generate_v4()         | Unique identifier for each artifact.      |
| job_id      | UUID                     | REFERENCES jobs(id) ON DELETE CASCADE, NOT NULL | Foreign key referencing the `jobs` table. |
| file_path   | VARCHAR(255)             | NOT NULL                                        | Path to the artifact file.                |
| file_size   | BIGINT                   | NOT NULL                                        | Size of the artifact file in bytes.       |
| created_at  | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP                       | Timestamp when the artifact was created.  |
| expiry_date | TIMESTAMP WITH TIME ZONE |                                                 | Optional expiry date for the artifact.    |

### Additional Information

- **Indexes**

  - idx_artifacts_job_id: Index on `job_id` for faster lookups.

  - idx_artifacts_expiry_date: Index on `expiry_date` for cleanup operations.

