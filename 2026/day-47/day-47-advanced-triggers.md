# Why GitHub says scheduled workflows may be delayed or skipped on inactive repos?

## Becasue GitHub runs scheduled workflows on shared infrastructure — millions of repos use it.
## So GitHub prioritizes active repos over inactive ones.

# When would you use paths vs paths-ignore?
## Use paths when want to run on a file/folder with specific pattern, use paths-ignore when want to ignre file/folder of a pattern.

# When would an external system (like a Slack bot or monitoring tool) trigger a pipeline?

## If it hits the repo's API
## A Slack bot has a /deploy command → someone types it → bot hits GitHub API → workflow runs
## A monitoring tool detects server is down → automatically hits GitHub API → workflow runs to restart server

# Explanation of workflow_run vs workflow_call
## workflow_run runs a workflow when the desired state or conditions are fulfilled.
## workflow_call it makes a workflow reusable like a function.

# The cron expression for: every weekday at 9 AM IST
## '30 3 * * 1-5'

# The cron expression for: first day of every month at midnight
## 0 0 1 * *
