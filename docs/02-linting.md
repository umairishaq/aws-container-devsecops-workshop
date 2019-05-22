# Module 2 <small>Dockerfile Linting</small>

## Create the buildspec file

```yaml
version: 0.2

phases:
pre_build:
    commands:
    - echo Copying hadolint.yml to the application directory
    - cp hadolint.yml $CODEBUILD_SRC_DIR_AppSource/hadolint.yml
    - echo Switching to the application directory
    - cd $CODEBUILD_SRC_DIR_AppSource
    - echo Pulling the hadolint docker image
    - docker pull hadolint/hadolint:v1.16.2
build:
    commands:
    - echo Build started on `date`
    - echo Scanning with Hadolint...          
    - result=`docker run --rm -i -v ${PWD}/hadolint.yml:/.hadolint.yaml hadolint/hadolint:v1.16.2 hadolint -f json - < Dockerfile`
post_build:
    commands:
    - echo $result
    - aws ssm put-parameter --name "codebuild-dockerfile-results" --type "String" --value "$result" --overwrite
    - echo Build completed on `date`
```

## Add a Dockerlinting Stage

## Test Pipeline

## Fix issues

FROM python:alpine3.7

FROM python:latest

USER root change to guest


  - docker.io


  "AWS API Key": "AKIA[0-9A-Z]{16}",


---

## Stage Architecture

After you have successfully added the Dockerfile linting stage to your CodePipeline and successfully remediated any issues, you can proceed to the next module.