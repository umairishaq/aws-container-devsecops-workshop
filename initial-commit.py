from __future__ import print_function
from urllib2 import build_opener, HTTPHandler, Request
from botocore.exceptions import ClientError
import boto3
import json
import httplib
import os

def handler(event, context):
    print("log -- Event: %s " % json.dumps(event))
    codecommit = boto3.client('codecommit')
    # Variables
    repo = event['ResourceProperties']['Repo']
    masterbranch = 'master'
    devbranch = 'development'
    buildspec = '''
version: 0.2

phases:
    pre_build:
        commands:
        - echo Logging in to Amazon ECR...
        - $(aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION)
    build:
        commands:
        - echo Build started on `date`
        - echo Building the Docker image...          
        - docker build -t $IMAGE_REPO_NAME:$CODEBUILD_RESOLVED_SOURCE_VERSION .
        - docker tag $IMAGE_REPO_NAME:$CODEBUILD_RESOLVED_SOURCE_VERSION $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$CODEBUILD_RESOLVED_SOURCE_VERSION     
    post_build:
        commands:
        - echo Build completed on `date`
        - echo Pushing the Docker image...
        - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$CODEBUILD_RESOLVED_SOURCE_VERSION'''
    Dockerfile = '''
FROM ubuntu:12.04

MAINTAINER Kimbro Staken version: 0.1

RUN apt-get update && apt-get install -y apache2 && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2

EXPOSE 80

CMD ["/usr/sbin/apache2", "-D", "FOREGROUND"]'''

    if event['RequestType'] == 'Create':
        print("log -- Create Event ")
        try:
            commit = codecommit.put_file(
                repositoryName=repo,
                branchName=devbranch,
                fileContent=buildspec,
                filePath='buildspec.yml',
                commitMessage='Initial Commit',
                name='Your Lambda Helper'
            )
            commit2 = codecommit.put_file(
                repositoryName=repo,
                branchName=devbranch,
                fileContent=Dockerfile,
                filePath='Dockerfile',
                parentCommitId=commit['commitId'],
                commitMessage='Second Commit',
                name='Your Lambda Helper'
            )

            codecommit.create_branch(
                repositoryName=repo,
                branchName=masterbranch,
                commitId=commit2['commitId']
            )

            codecommit.update_default_branch(
                repositoryName=repo,
                defaultBranchName=devbranch
            )
            response = sendResponse(event, context, "SUCCESS", { "Message": "Initial commits - Success" })
        except ClientError as e:
            print(e)
        response = sendResponse(event, context, "SUCCESS", { "Message": "Initial commits - Error" })
    elif event['RequestType'] == 'Update':
        print("log -- Update Event")
        try:
            response = sendResponse(event, context, "SUCCESS", { "Message": "Initial commits - Success" })
        except ClientError as e:
            print(e)
            response = sendResponse(event, context, "SUCCESS", { "Message": "Initial commits - Error" })
    elif event['RequestType'] == 'Delete':
        print("log -- Delete Event")
        response = sendResponse(event, context, "SUCCESS", { "Message": "Deletion successful!" })
    else:
        print("log -- FAILED")
        response = sendResponse(event, context, "FAILED", { "Message": "Unexpected event received from CloudFormation" })
    return response

def sendResponse(event, context, responseStatus, responseData):
    responseBody = json.dumps({
        "Status": responseStatus,
        "Reason": "See the details in CloudWatch Log Stream: " + context.log_stream_name,
        "PhysicalResourceId": context.log_stream_name,
        "StackId": event['StackId'],
        "RequestId": event['RequestId'],
        "LogicalResourceId": event['LogicalResourceId'],
        "Data": responseData
    })
    opener = build_opener(HTTPHandler)
    request = Request(event['ResponseURL'], data=responseBody)
    request.add_header('Content-Type', '')
    request.add_header('Content-Length', len(responseBody))
    request.get_method = lambda: 'PUT'
    response = opener.open(request)
    print("Status code: {}".format(response.getcode()))
    print("Status message: {}".format(response.msg))
    return responseBody