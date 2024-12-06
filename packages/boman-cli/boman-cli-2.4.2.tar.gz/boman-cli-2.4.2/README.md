# Introduction 
Boman CLI is a Orchestration script written in python to run security scans on the local or CI/CD environment and upload the results to Boman.ai SaaS server.


# Installation

` pip install boman-cli`

# Getting Started

###  For help

` boman-cli -h` 

### Authentication of project has been moved from boman.yaml to boman-cli

`boman-cli -a run -at <project token> -ct <customer token>`

To obtain `project token` and `customer token`. Go to SaaS platform. Click on Apps -> app menu of the particular app -> Get Scan Token 


### To test the boman cli server

` boman-cli -a test-saas`


### To test the boman configuration written in boman.yaml file

` boman-cli -a test-yaml`

### To run the scan 

` boman-cli -a run`

### To run the scan on specific Boman SaaS URL (On prem)

` boman-cli -a run -u {URL}`


### To fail build on high/medium/low finding is detected

`boman-cli -a run -fb {severity}`

Severity can be high, medium or low.

Example: boman-cli -a run -fb high


### To custom change the boman.yaml file, pass the custom file name as input for -config argument

`boman-cli -a run -config <custom_boman_yaml_file_name_here>`

Example: boman-cli -a run -config ./customboman.yaml


### To inject custom zap auth session script file, pass the custom file name as input for -zap_session_script argument

`boman-cli -a run -zap_session_script <custom_session_script_file_name_here>`

Example: boman-cli -a run -zap_session_script ./session.js


# Error codes

0  : Successfull scan
1  : Server/SaaS error
2  : Auth error
3  : Docker/System error
4  : Misconfig error




### Release Note:

### V2.3.0
- **New:** The pipeline configuration has been relocated from `boman.yaml` to the SaaS platform. Navigate to **Apps -> App menu -> Configure pipeline** to set it up. The current `boman.yaml` configuration will remain functional until it is officially deprecated.


### V2.2.0
    - New scan added: IaC.

### V2.1.1
    - Ignore files or directory for SAST and SCA

### V2.1
    - New scan added: SBOM.

### V2.0

    - New scan added: Container scan.
    - New Tool added for SCA scan type.


### V1.9:

    - [Bug fix] Updated the Upload Logs success message

Released on: 21 June 2024




### V1.8:

    - Adapted to our new Boman SaaS platform

Released on: 20 June 2024




### V1.7:

    - Fixed docker-request libraries issue
    - Zap Authenticated scan 
    - Fetch Git details
    - custom boman.yaml and zap session script load option

Released on: 21 May 2024




