# Module 5: Cleanup

In order to prevent charges to your account we recommend cleaning up the infrastructure that was created. If you plan to keep things running so you can examine the workshop a bit more please remember to do the cleanup when you are done. It is very easy to leave things running in an AWS account, forgot about it, and then accrue charges.

!!! info "You will need to manually delete some resources before you delete the CloudFormation stacks so please do the following steps in order."

1.  Open your Cloud9 IDE
2.  Run the following:

```
# Get Account #
account=`aws sts get-caller-identity --query [Account] --output text`

# Delete S3 Bucket
aws s3 rm s3://container-devsecops-wksp-$account-us-east-2-artifacts --recursive
aws s3api delete-bucket --bucket container-devsecops-wksp-$account-us-east-2-artifacts
aws logs delete-log-group --log-group-name /aws/codebuild/container-devsecops-wksp-build-dockerfile
aws logs delete-log-group --log-group-name /aws/codebuild/container-devsecops-wksp-build-secrets
aws logs delete-log-group --log-group-name /aws/codebuild/container-devsecops-wksp-scan-image
aws logs delete-log-group --log-group-name /aws/codebuild/container-devsecops-wksp-publish
aws logs delete-log-group --log-group-name /aws/codebuild/container-devsecops-wksp-anchore-build
aws logs delete-log-group --log-group-name /aws/lambda/container-devsecops-wksp-initial-commit
aws logs delete-log-group --log-group-name /aws/lambda/container-devsecops-wksp-pr
aws logs delete-log-group --log-group-name /aws/lambda/container-devsecops-wksp-codebuild-dockerfile
aws logs delete-log-group --log-group-name /aws/lambda/container-devsecops-wksp-codebuild-secrets
aws logs delete-log-group --log-group-name /aws/lambda/container-devsecops-wksp-codebuild-vulnerability
aws logs delete-log-group --log-group-name /aws/lambda/container-devsecops-wksp-codebuild-publish
aws logs delete-log-group --log-group-name /aws/ecs/taskcontainer-devsecops-wksp-anchore-engine

# Delete ECR Repositories
aws ecr delete-repository --repository-name container-devsecops-wksp-sample --force
aws ecr delete-repository --repository-name container-devsecops-wksp-anchore --force

# Delete CloudFormation Stacks
aws cloudformation delete-stack --stack-name container-dso-wksp-pipeline-stack
aws cloudformation delete-stack --stack-name container-dso-wksp-anchore-stack

echo 'Completed cleanup.'

```