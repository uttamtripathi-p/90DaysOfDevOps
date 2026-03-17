# When would you use each restart policy?

### restart: no
Use during development when you want to debug why a container crashed — you don't want it auto restarting before you can see the error.
### restart: always
Use for critical production services like databases, web servers — anything that must keep running 24/7 even after a system reboot.

### restart: on-failure
Use for background jobs or scripts that might fail due to an error but shouldn't restart if you manually stop them.

### unless-stopped
Use when you want always behavior but with one exception — if YOU manually stopped it, don't restart it. Good for services you sometimes need to temporarily turn off.
