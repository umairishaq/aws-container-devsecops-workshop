# Anchore Image Scanner

This directory contains a [Cloudformation template](./anchore-fargate.yml) and other assets that are required to setup the [Anchore Open Source](https://anchore.com/opensource/) Engine as a Fargate application.

The Anchore performs an analysis of a container image in ECR. This is executed as a Codebuild stage in the Codepipeline defined in the parent directory. The results of an image scan are reported to Security Hub. A lambda function defined the template recieves the results of the image scan as a payload and translates that into Amazon Finding Format payload and bulk sends the findings to Security Hub.

## Setup

### Build and Push Anchore

The [Dockerfile](./Dockerfile) defines the base image and the [config](./config.yaml) for Anchore Open Source Engine. This image first needs to be built and pushed to an ECR repo in your account.

Assuming you have an AWS profile setup with right access permissions first create the repo.

```bash
aws ecr create-repository --repository-name anchore/anchore-engine
```

Next, build the docker image for Anchore.

```bash
docker build . -t 816828077353.dkr.ecr.us-east-2.amazonaws.com/anchore/anchore-engine:v0.3.4
```

Then, login to ECR and push the image.

```bash
$(aws ecr get-login --no-include-email --region us-east-2)

docker push 816828077353.dkr.ecr.us-east-2.amazonaws.com/anchore/anchore-engine:v0.3.4
```

This should push your image out to ECR.

### Create Cloudformation Stack

Go to the Cloudformation page within AWS Console and Create Stack. Upload the anchore-fargate.yml template and provide the input parameters for `AnchoreRepo` and `AnchoreImageName` as shown in the example below.

```bash
AnchoreRepo=816828077353.dkr.ecr.us-east-2.amazonaws.com
AnchoreImageName=anchore/anchore-engine:v0.3.4
```