# What is a reusable workflow?
## A workflow that can be called and reused by other workflows instead of repeating the same steps in every workflow file.

# What is the workflow_call trigger?
## It's the trigger that marks a workflow as reusable — meaning it can be called by another workflow instead of running on its own like push or pull request.

# How is calling a reusable workflow different from using a regular action (uses:)?
## A regular action runs a single step — like login, build, checkout. A reusable workflow runs an entire job with multiple steps inside it. Think of action as one task and reusable workflow as a full pipeline.

# Where must a reusable workflow file live?
## It must be inside the .github/workflows/ folder. And the repository must be either public or in the same organization to be called from another workflow.

