# Module 2 <small>Add a Dockerfile linting stage</small>

Attendees will learn about the security considerations around building container images and then apply those learnings by embedding security testing into a CI/CD pipeline that's used for building, shipping, and deploying a container based application. They will get hands-on experience integrating security testing such as static analysis of Dockerfiles and application code, vulnerability assessments of images, and signing of images using a variety of open source projects. At the end of the workshop they'll have a fully automated CI/CD pipeline with embedded security testing that they can use to deploy an application.

* **Level**: Intermediate
* **Duration**: 2 - 3 hours
* **<a href="https://www.nist.gov/cyberframework/online-learning/components-framework" target="_blank">CSF Functions</a>**: Prevent
* **<a href="https://d0.awsstatic.com/whitepapers/AWS_CAF_Security_Perspective.pdf" target="_blank">CAF Components</a>**: Preventative
* **<a href="https://awssecworkshops.com/getting-started/" target="_blank">Prerequisites</a href>**: AWS Account, Admin IAM User

## Create the CodeBuild Project

```
aws codebuild create-project \
    --name "my-demo-project" \
    --source "{\"type\": \"S3\",\"location\": \"codebuild-us-west-2-123456789012-input-bucket/my-source.zip\"}" \
    --artifacts {"\"type\": \"S3\",\"location\": \"codebuild-us-west-2-123456789012-output-bucket\""} \
    --environment "{\"type\": \"LINUX_CONTAINER\",\"image\": \"aws/codebuild/standard:1.0\",\"computeType\": \"BUILD_GENERAL1_SMALL\"}" \
    --service-role "arn:aws:iam::123456789012:role/service-role/my-codebuild-service-role"
```

## Add a Stage to CodePipeline

## Integrate the feedback loop

## Test the Pipeline


---

## Stage Architecture

After you have successfully added the Dockerfile linting stage to your CodePipeline and successfully remediated any issues, you can proceed to the next module.