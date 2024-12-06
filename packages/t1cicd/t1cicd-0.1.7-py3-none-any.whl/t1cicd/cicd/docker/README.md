# Docker design
This document outlines the use of Docker for containerized job execution and the organization of logs.

## Design Overview
- Pipeline-Level Isolation
  - Each pipeline is assigned its own independent Docker client instance.

- Job-Level Isolation
  - Each job within a pipeline is executed in its own dedicated Docker container.

- Log Management
  - Each job’s logs are saved directly in the corresponding container’s mounted directory.
  
- Thread-Safety
  - To avoid potential issues with concurrent modifications, jobs within the same pipeline are not allowed to modify the same section of code simultaneously.

## Design Diagram
```
+---------------------------------------------------------------------------+
|                  Docker Engine                                            |
|                                                                           |
|   +-------------------------------+   +-------------------------------+   |
|   |       PipelineInstance1       |   |       PipelineInstance2       |   |
|   |   (Independent Docker Client) |   |   (Independent Docker Client) |   |
|   |                               |   |                               |   |
|   |   +-------------------+       |   |   +-------------------+       |   |
|   |   |   Container 1     |       |   |   |   Container N     |       |   |
|   |   |  (Executes Job 1) |       |   |   |  (Executes Job N) |       |   |
|   |   |  Volumes:         |       |   |   +-------------------+       |   |
|   |   |  - absolute_path  |       |   +-------------------------------+   |        
|   |   |    -> /app        |       |                                       |
|   |   |  - doc_path       |       |                                       |
|   |   |    -> /app/docs   |       |                                       |   
|   |   +-------------------+       |                                       |          
|   |                               |                                       |
|   |   +-------------------+       |                                       |
|   |   |   Container 2     |       |                                       |
|   |   |  (Executes Job 2) |       |                                       |
|   |   |  Volumes:         |       |                                       | 
|   |   |  - absolute_path  |       |                                       |          
|   |   |    -> /app        |       |                                       |
|   |   |  - doc_path       |       |                                       |
|   |   |    -> /app/docs   |       |                                       |
|   |   +-------------------+       |                                       |
|   |                               |                                       |
|   |   +-------------------+       |                                       |
|   |   |   Container n     |       |                                       |
|   |   |  (Executes Job n) |       |                                       |              
|   |   +-------------------+       |                                       |      
|   +-------------------------------+                                       |
|                                                                           |           
+---------------------------------------------------------------------------+
```
## Log Organization
Logs are stored in a hierarchical structure under the `t1-cicd/logs/` directory. 
This organization ensures that logs are easy to locate, per pipeline and per job.

### Unique Naming and Overwriting
- **Pipeline Names**: 
  - Each pipeline has a unique name, which forms the top-level directory for its logs.
- **Job Names**: 
  - Each job within a pipeline also has a unique name.
- **Overwriting Behavior**: 
  - If the same pipeline is run multiple times, the logs for the previous run will be overwritten. 
  - This ensures that the latest execution logs are always available and prevents unnecessary duplication.

## Example Log Directory Structure:
```
t1-cicd/logs/ 
├── pipeline_1/ 
│ ├── job_1/ 
│ │  └── job.log
| |  └── dummy.txt
│ └── job_2/ 
│       └── job.log 
├── pipeline_2/ 
│  ├── job_1/ 
│  │   └── job.log 
│  └── job_2/ 
│         └── job.log
```
