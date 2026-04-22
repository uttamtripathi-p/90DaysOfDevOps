# What is the difference between a named volume and a bind mount?

### A Named Volume is fully managed by Docker — you just give it a name, Docker decides where to store it on the host, and it handles all the internals. You don't need to know or care about the actual folder path. It's safe, portable, and ideal for persistent data like databases.


### A Bind Mount, on the other hand, maps a specific folder from your host machine directly into the container. You're in full control of the path, and any changes on either side reflect instantly. It's perfect for development when you want to edit code on your host and see changes live inside the container.

# Why does custom networking allow name-based communication but the default bridge doesn't?

### When we use default bridge, docker just connects container on a network,and doesn't assign any DNS server.So, it just understands another container by IP not by name.

### But when we create custom bridge, docker automatically spins up an internal DNS server for the network.S, when we ping it understands not only ip but also name.
