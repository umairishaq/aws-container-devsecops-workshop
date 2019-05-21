# Anchore Image Scanner

## Create Cloudformation Stack

```bash
aws cloudformation create-stack \
    --stack-name anchore-stack \
    --template-body file://anchore-fargate.yml \
    --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
    --region us-east-2
```