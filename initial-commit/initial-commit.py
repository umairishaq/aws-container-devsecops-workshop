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
    repoConfig = event['ResourceProperties']['RepoConfig']
    masterbranch = 'master'
    devbranch = 'development'

    if event['RequestType'] == 'Create':
        print("log -- Create Event ")
        try:

            # Read in files
            buildspecPath = os.environ['LAMBDA_TASK_ROOT'] + "/buildspec-df.yml"
            buildspec = open(buildspecPath).read()
            DockerfilePath = os.environ['LAMBDA_TASK_ROOT'] + "/Dockerfile"
            Dockerfile = open(DockerfilePath).read()
            hadolintConfigPath = os.environ['LAMBDA_TASK_ROOT'] + "/hadolint.yml"
            hadolintConfig = open(hadolintConfigPath).read()

            # Add Dockerfile buildspec file to configs repo
            commit = codecommit.put_file(
                repositoryName=repoConfig,
                branchName=masterbranch,
                fileContent=buildspec,
                filePath='buildspec_dockerfile.yml',
                commitMessage='Initial Commit',
                name='Your Lambda Helper'
            )

            codecommit.put_file(
                repositoryName=repoConfig,
                branchName=masterbranch,
                parentCommitId=commit['commitId'],
                fileContent=hadolintConfig,
                filePath='hadolint.yml',
                commitMessage='Added Hadolint Configuration',
                name='Your Lambda Helper'
            )

            # Add Dockerfile to application repo
            commit2 = codecommit.put_file(
                repositoryName=repo,
                branchName=devbranch,
                fileContent=Dockerfile,
                filePath='Dockerfile',
                commitMessage='Initial Commit',
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