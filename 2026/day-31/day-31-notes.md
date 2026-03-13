# CMD vs ENTRYPOINT

## Use CMD when:

The container can reasonably run different commands depending on context
You want a helpful default but full flexibility
Example: a base Ubuntu/Python image where users might run bash, python, or anything else

## Use ENTRYPOINT when:

Your container has one clear, dedicated purpose
You're shipping a tool and the container is that tool
Example: a container that wraps ffmpeg, curl, or your own app — users only pass flags/args, not a whole new command

## Use both together when:

You have a fixed executable but want sensible default arguments that are easy to swap
Example: ENTRYPOINT ["python", "app.py"] + CMD ["--port", "8080"] — the app always runs, but the port is overridable


