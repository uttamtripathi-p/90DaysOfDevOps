# Think about a team of 5 developers all pushing code to the same repo manually deploying to production.
## What can go wrong?
Maybe the code from one developer fails and the whole project collapses or the push conflict might occur.

## What does "it works on my machine" mean and why is it a real problem?
Because one can have different dependencies which might not be installed in others.So, this is a real problem.

## How many times a day can a team safely deploy manually?
At max, 2-3 times.

# Pipeline Anatomy
A pipeline has these parts —

## Trigger — It tells the pipeline when to start (like; someone pushes code, someone creates a pull req,etc..)
## Stage — This is just a logical phase where build,test and deployment happens
## Job — The task/work to be executed
## Step — a single command or action inside a job 
## Runner — the machine that executes the job (like; virtual/local machine)
## Artifact - output produced by a job


## CI/CD/CD refers to three related but distinct practices in modern software development:
Continuous Integration (CI) is the practice of frequently merging developer code changes into a shared repository — often multiple times a day. Each merge triggers an automated build and test pipeline to catch integration bugs early. The goal is to detect problems as soon as they're introduced rather than at the end of a long development cycle
.
## Continuous Delivery (CD) extends CI by automatically preparing every passing build for release to a staging or production-like environment. The code is always in a deployable state, but an actual deployment to production requires a manual approval step. This gives teams control over when to release while ensuring the software is ready to release at any time.

## Continuous Deployment (CD) goes one step further — every change that passes all automated tests is deployed to production automatically, with no human intervention. This is the most advanced practice and requires a very mature test suite and high confidence in automation.
