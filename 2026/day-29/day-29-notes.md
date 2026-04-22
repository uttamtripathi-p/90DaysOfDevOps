# Task:1 What is Docker?

## What is a Container?
A container packages your app + its dependencies into one isolated unit. It runs the same everywhere — no more "works on my machine" issues.

## Containers vs Virtual Machines
ContainerVMOSShares host kernelOwn full OSSizeMBsGBsStartupMillisecondsMinutesIsolationProcess-levelHardware-level
Key point: VMs virtualize hardware. Containers virtualize the OS. Containers are faster and lighter.

## Docker Architecture

Client — Your CLI (docker run, docker build), sends commands to the daemon
Daemon (dockerd) — Background engine that builds and runs containers
Image — Read-only blueprint, built from a Dockerfile
Container — A running instance of an image
Registry — Image storage hub (e.g. Docker Hub)
