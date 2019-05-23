# Module 5: Cleanup

In order to prevent charges to your account we recommend cleaning up the infrastructure that was created. If you plan to keep things running so you can examine the workshop a bit more please remember to do the cleanup when you are done. It is very easy to leave things running in an AWS account, forgot about it, and then accrue charges.

!!! info "You will need to manually delete some resources before you delete the CloudFormation stacks so please do the following steps in order."

## Retrieve your AWS Account #

1.  Open your Cloud9 IDE
2.  Retrieve and copy your AWS Account #

```
aws sts get-caller-identity
```

## Delete the artifact S3 bucket

* Delete all objects in the bucket (Replace <Account#>):
```
aws s3 rm s3://container-devsecops-wksp-<ACCOUNT#>-us-east-2-artifacts --recursive
```
* Delete bucket (Replace <Account #>):
```
aws s3api delete-bucket --bucket container-devsecops-wksp-<ACCOUNT#>-us-east-2-artifacts
```

## Delete the AWS CloudWatch Log Groups

```
aws logs delete-log-group --log-group-name /aws/codebuild/container-devsecops-wksp-build-dockerfile
aws logs delete-log-group --log-group-name /aws/lambda/container-devsecops-wksp-codebuild-dockerfile
aws logs delete-log-group --log-group-name /aws/lambda/container-devsecops-wksp-initial-commit
```

## Delete the AWS ECR repositories

```
aws ecr delete-repository --repository-name container-devsecops-wksp-sample
aws ecr delete-repository --repository-name container-devsecops-wksp-anchore
```

## Delete CloudFormation templates

* Delete the pipeline stack:
```
aws cloudformation delete-stack --stack-name container-dso-wksp-pipeline-stack
```

* Delete the Anchore service:
```
aws cloudformation delete-stack --stack-name container-dso-wksp-pipeline-stack
```

