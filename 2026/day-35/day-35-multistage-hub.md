# Why is the multi-stage image so much smaller?

Stage 1 (build) → has everything needed to build the app — Node.js, npm, package files, build tools. This is heavy!
Stage 2 (deployer) → only copies the final built app — no npm, no build tools, no unnecessary files

So the final image only contains what's needed to run the app, not what was needed to build it!
