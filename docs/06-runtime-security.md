# Module 5 <small>Add runtime security scanning</small>

**Time**: 15 minutes

In this stage you will be setting up a runtime security engine to monitor your running containers. In this stage you’ll be leveraging <a href="https://falco.org/docs/" target="_blank">Falco</a>, an open source project that can monitor containers running in production and report anomalous activity based on sets of default and custom rules.


## Setup Slack Webhook

The alerts from our runtime security engine will need a way to reach us in a fast manner. For this workshop, we will be displaying our alerts from Falco in a slack channel that Falco can connect to through a slack channel. 

If you don’t already have a slack workspace, follow <a href="https://slack.com/help/articles/206845317" target="_blank">this tutorial</a> to create one.

Then, configure your webook with this guide: 
<a href="https://api.slack.com/messaging/webhooks" target="_blank">Create an incoming Webhook.</a>

## Setup Falco Image

Now let’s customize our Falco image for our slack channel and push it onto ECR. 

In your cloud 9 workspace, perform the following terminal commands:

```
docker pull falcosecurity/falco
sudo yum -y install kernel-devel-$(uname -r)
docker run --name falco --privileged -v /var/run/docker.sock:/host/var/run/docker.sock -v /dev:/host/dev -v /proc:/host/proc:ro -v /boot:/host/boot:ro -v /lib/modules:/host/lib/modules:ro -v /usr:/host/usr:ro falcosecurity/falco & 
sleep 10 && docker exec -it falco /bin/bash
 sed -i 's/XXX/YOUR_SLACK_WEBHOOK_SUFFIX/g' /etc/falco/falco.yaml
 sed -i 's/json_output:[ ]false/json_output: true/g' /etc/falco/falco.yaml
 sed -ri '/./{H;$!d} ; x ; s/(program_output:\n[ ].enabled:[ ])false/\1true/' /etc/falco/falco.yaml 
exit
```

**NOTE**: If the prompt is stuck, press the return key to get back to the prompt.

Example of SLACK_WEBHOOK_SUFFIX is the portion of url in red: 
https://hooks.slack.com/services/<span style="color:red">TLZLLH2LD/BM03Y783E/r5fA22YDWW3awUNG5hMBJBft</span>

**IMPORTANT**: For the value of your SLACK_WEBHOOK_SUFFIX, add a ‘\’ in front of every ‘/’ in the suffix.

For example, 

TLZLLH2LD<span style="color:red">/</span>BM03Y783E<span style="color:red">/</span>r5fA22YDWW3awUNG5hMBJBft

becomes

TLZLLH2LD<span style="color:red">\\/</span>BM03Y783E<span style="color:red">\\/</span>r5fA22YDWW3awUNG5hMBJBft


Now, check the created docker image into the repo, **after substituting** your account number in the following commands

```
docker commit falco AWS_ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com/container-devsecops-wksp-falco:slack
$(aws ecr get-login --region us-east-2 --no-include-email)
docker push AWS_ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com/container-devsecops-wksp-falco:slack 
```


The above commands pulls a generic Falco image, runs it as a container, and replaces the Falco configuration with our slack webhook. The running container is then committed to an image and pushed onto ECR. 

## Test Runtime Security

In this final stage, we will test the runtime security engine we have added to our cluster. At this point, we have pushed our runtime security image onto ECR, but it has not yet been deployed into our cluster.

1.  Click on your Cloud9 IDE tab.

2.  Create a new pull request using the following command:

```
aws codecommit create-pull-request \
    --title "Updated ECR Images" \
    --description "Please review these changes." \
    --targets repositoryName=container-devsecops-wksp-app,sourceReference=development,destinationReference=master
```

3.  Navigate to Codepipeline in your AWS console and select the workshop pipeline.
4.	In the top right, select Release Change.

After pushing onto ECR and running through the pipeline another time, the ECS deploy stage in the pipeline will have created a new task definition and updated our service in the ECS cluster.

Now, let’s try and launch an attack against our sample-app running as a container. 

1.	Click on your Cloud9 IDE tab.
2.	Open a new tab and navigate to EC2 in the AWS console. 
3.	Find the EC2 instance tagged as container-devsecops-wksp-ecs-instance with the tag name. 
4.	Note the Public IP address of this instance
5.	Enter the following commands
```
nc <Public IP Address of EC2 Instance> 8080 
```
6.	Now, run the following.
```
/bin/ash 2>&1
cd .
touch ~/.bash_profile 
```
7.	Check your slack channel. You should see the warning “ Warning a shell configuration file has been modified...” along with a timestamp.

What the above commands did was initiate a connection with our sample-app running as a container. Then, a reverse shell was opened and creation of a sensitive configuration file was attempted. 

Congratulations! You’ve completed integrating runtime monitoring into your container cluster! You now have a way to protect your containers not just before deployment but at runtime as well. 
