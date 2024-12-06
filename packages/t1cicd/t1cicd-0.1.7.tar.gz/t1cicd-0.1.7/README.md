# T1-CICD

## High-Level Design

![High-Level Design](./images/system_diagram_highlevel.jpg)

## Sequence Diagram

### Pipeline Run

![sequence_diagram_pipeline_run](./images/sequence_diagram_pipeline_run.png)

### Pipeline Cancel

![sequence_diagram_pipeline_run](./images/sequence_diagram_pipeline_cancel.png)

### Pipeline Report

![sequence_diagram_pipeline_run](./images/sequence_diagram_pipeline_report.png)

## Components

| Components | README |
| :-------: | :----: | 
| CLI   | [Design Doc](t1cicd/cicd/cli/README.md)   |
| Rest API  | [Design Doc](t1cicd/cicd/api/README.md)   |
| Orchestrator | [Design Doc](t1cicd/cicd/orchestrator/README.md)   | 
| PostgreSQL | [Design Doc](t1cicd/cicd/db/README.md)   | 
| Docker Server | [Design Doc](t1cicd/cicd/docker/README.md)   | 


### CLI
CLI provides the interface to use our CICD system. It supports users to upload a custom pipeline yaml file, to run the pipeline, cancel the pipeline and get pipeline reports.

CLI runs on user's host. CLI only communicates with RestAPI. CLI send requests and receives responses through flask apis.

### Rest API
Rest API receives CLI's request and process the data for function calls to let the orchestrator run pipelines or get reports from the database.

RestAPI can run on user's host for local run, or run on a remote server. RestAPI communicates with CLI, Orchestrator and PostgreSQL. 
- For communication with CLI, RestAPI receives requests and sends requests through flask apis. 
- For communication with Orchestrator, for now we implement them in one host, so RestAPI will use function calls to execute functions in Orchestrator; While RestAPI and Orchestrator can also be in different hosts, and in this case they can communicate via a message queue, and RestAPI will push the processed request from CLI to the message queue, and Orchestrator will get the processed request from the queue. 
- For communication with PostgreSQL, RestAPI will GET reports from the database. We have implemented apis to call DB functions.

### Orchestrator
Orchestrator is the main part for CICD RUN. It parses user's pipeline config files, stores all processed data to the database, controls the order of running pipelines, and creates Docker containers to run jobs. For now it supports running multiple pipelines in serial. In one pipeline, stages run in serial, and jobs without dependencies run in parallel.

Orchestrator can run on user's host for local run, or run on the same remote server as Rest API, or run on another server. Orchestrator communicates with PostgreSQL and Docker Server.
- For communication with PostgreSQL, the orchestrator POST parsed pipelines and update all status to the Database.
- For communication with Docker Server, the orchestrator use Docker APIs to create and run containers.

### PostgreSQL
We use PostgreSQL for data storage.

PostgreSQL Server can run on user's host for local run, or run on a remote server.

### Docker Server
We use Docker to run containers.

Docker Server can run on user's host for local run, or run on a remote server. Docker communicates with Orchestrator that returns logs and run responses back to Orchestrator.

## Getting Started

If you want to use our CICD system, follow this [User Guide](dev-docs/client_guide.md). 
<!-- (For now, all the components are deployed locally. In t1cicd package, only the CLI part can be directly used without any configuration. Users needs to setup the config of Database and run server using poetry manually. In future improvement with running on cloud, we expect users only have CLI on their end, and the server and DB will be pre-deployed on the other host.) -->

If you want to build and develop on our CICD system, follow this [Developer Guide](dev-docs/developer_guide.md).
