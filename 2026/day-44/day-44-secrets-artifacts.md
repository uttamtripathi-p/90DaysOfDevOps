#  Why should you never print secrets in CI logs?
## Secret information like passwords, API keys, tokens, etc. can get leaked if printed in logs.

# When would you use artifacts in a real pipeline?
## In a real pipeline, artifacts are used to pass build outputs between jobs — for example, compiling code in a build job and passing the binary to a test or deploy job without rebuilding it. They're also useful for storing reports like test results, code coverage, or security scan outputs so you can download and review them after the pipeline finishes.
#  What are Secrets?
## Secrets are sensitive values like passwords, API keys, tokens etc. that should never be hardcoded directly in your code or workflow files.
