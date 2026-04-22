# Why would you pass outputs between jobs?
## Because jobs run in isolated environments — they cannot directly share variables or data with each other.
## So if Job A calculates something (e.g., version number, date, build status), and Job B needs that value — you must explicitly pass it via outputs.

# A step with continue-on-error: true — what does this do?
## By default, if a step fails → workflow stops.
## With continue-on-error: true → step can fail but workflow keeps running normally.