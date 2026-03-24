# Why a pipeline fails
## A pipeline fails when any step returns a non-zero exit code. Linux/bash convention is simple:

## 0 = success
## anything else = failure
## When a step fails, GitHub Actions stops that job immediately and marks everything after it as skipped

# How do you read the error?
## The mental order — always read bottom to top
## The last line tells you what failed, but the lines above tell you why. 
## Most people stare at the bottom and miss the actual reason sitting a few lines up.
