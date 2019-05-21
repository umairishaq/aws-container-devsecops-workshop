# Module 1 <small>Environment Setup</small>

In the first module you will be configuring the initial pipeline and setting up the Anchore service which you will be integrating the pipeline with later on in this workshop.  This module requires you to run two separate <a href="https://aws.amazon.com/cloudformation/" target="_blank">AWS CloudFormation</a> templates which will automate the creation of the pipeline and Anchore service.  You will then walk through each stage and manually configure the security testing.

## Deploy the Anchore service

The first CloudFormation you run will create the Anchore vulnerability scanning service.  Before you deploy the CloudFormation template feel free to view it <a href="https://github.com/aws-samples/aws-container-devsecops-workshop/blob/master/anchore/anchore-fargate.yml" target="_blank">here</a href>.

Region| Deploy
------|-----
US East 2 (Ohio) | <a href="https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=container-dso-wksp-anchore-stack&templateURL=https://s3.us-east-2.amazonaws.com/sa-security-specialist-workshops-us-east-2/devsecops/containers/anchore-fargate.yml" target="_blank">![Deploy Module 1 in us-west-2](./images/deploy-to-aws.png)</a>

1. Click the **Deploy to AWS** button above.  This will automatically take you to the console to run the template.  

2. On the **Specify Details** click **Next**. 
	
3. Once you have entered your parameters click **Next**, then **Next** again \(leave everything on this page at the default\).

4. Finally, acknowledge that the template will create IAM roles and CAPABILITY_AUTO_EXPAND and click **Create**.

This will bring you back to the CloudFormation console. You can refresh the page to see the stack starting to create.

!!! warning "Before moving on, make sure the stack is in a **CREATE_COMPLETE** status."

## Deploy your pipeline

The second CloudFormation you run will create the initial pipeline.  Before you deploy the CloudFormation template feel free to view it <a href="https://github.com/aws-samples/aws-container-devsecops-workshop/blob/master/initial-pipeline/pipeline-setup.yml" target="_blank">here</a href>.

Region| Deploy
------|-----
US East 2 (Ohio) | <a href="https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=container-dso-wksp-pipeline-stack&templateURL=https://s3.us-east-2.amazonaws.com/sa-security-specialist-workshops-us-east-2/devsecops/containers/pipeline-setup.yml" target="_blank">![Deploy Module 1 in us-west-2](./images/deploy-to-aws.png)</a>

1. Click the **Deploy to AWS** button above.  This will automatically take you to the console to run the template.  

2. On the **Specify Details** section enter the necessary parameters as shown below. 

	| Parameter | Value  |
	|---|---|
	| Stack name | container-devsecops-wksp  |
	| Fail When | Select a threshold  |
	
3. Once you have entered your parameters click **Next**, then **Next** again \(leave everything on this page at the default\).

4. Finally, acknowledge that the template will create IAM roles and click **Create**.

This will bring you back to the CloudFormation console. You can refresh the page to see the stack starting to create. 

!!! warning "Before moving on, make sure the stack is in a **CREATE_COMPLETE** status."

## Browse to your Cloud9 IDE

You will be doing the majority of the workshop using the <a href="https://aws.amazon.com/cli/" target="_blank">AWS Command Line Interface (CLI)</a> within <a href="https://aws.amazon.com/cloud9/" target="_blank">AWS Cloud9</a>, a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a browser.

1.	Open the <a href="https://us-east-2.console.aws.amazon.com/cloud9/home?region=us-east-2" target="_blank">AWS Cloud9 console</a> (us-east-2)
2.	Click **Open IDE** in the **container-devsecops-wksp-ide** environment.  This will take you to your IDE in a new tab.  Always keep this tab open  

!!! info "To make life easier on yourself, always keep your IDE tab open and use a different tab for all other activities."

## Test your pipeline

Now you can test your pipeline to see how your Pull Requests result with an image being built and pushed to <a href="https://aws.amazon.com/ecr/" target="_blank">AWS ECR</a>.

1.	Within your Cloud9 IDE expand your **sample application** on the left side.
2.  Open the **Dockerfile**.
3.  Add a name to the maintainer line.
4.  Push your commit and create a Pull Request.

```
    cd sample-application/
    git add Dockerfile
    git commit -m "Modified Maintainer in Dockerfile"
    git push -u origin development
    aws codecommit create-pull-request --title "Updated Maintainer" --description "Please review these changes." --targets repositoryName=container-devsecops-wksp-app,sourceReference=development,destinationReference=master
```

You can browse to <a href="https://us-east-2.console.aws.amazon.com/codesuite/codepipeline/pipelines/container-devsecops-wksp-pipeline/view" target="_blank">AWS CodePipeline</a> to view your code progress through the pipeline.  You can see that there are currently only two stages in the pipeline; one for pulling the source code and one for building and pushing the image to ECR.

---

After you have successfully setup your environment, you can proceed to the next module.