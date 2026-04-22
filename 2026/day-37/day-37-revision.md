## Container commands

run= starts a container from a dockerfile
ps= lists all running containers
stop= stops the instructed container
rm= removes the container
exec= with this you can enter inside a container
logs= shows logs of the instructed container(docker logs <cont_id>)

## Image commands —

build= use to build an image from a Dockerfile
pull= used to pull an image from docker-hub
push= used to push image from your local to docker-hub
tag= gives tag to an image before pushing it to docker-hub
ls= shows available images at your local
rmi= ued to remove marked image(docker rmi <image_id>)

## Volume commands —

create= used to create a new volume
ls= shows all volumes
inspect= inspects a volume , shows info like created-on, mountpoint etc..
rm= removes an existing volume
## Network commands —
create= creates a new network
ls= shows all available networks
inspect= inspects a network, shows info like attached-containers, created-on and config info.
connect= connects a container to instructed container

## Compose commands —

up= build images and runs container for assigned services in compose file
down= stops and removes all compose running containers and networks
ps= shows all running containers started from compose file
logs= shows logs of file and its services
build= only builds images for services and doesn't start the container

## Cleanup commands —

prune= removes all unsused objects whether it is image,container,network,volume  eg(docker image prune; removes all system images) a single command to remove all unused objects is (docker system prune)
system df=  display information regarding the amount of disk space consumed by the Docker daemon

## Dockerfile instructions —

FROM= tells our dockerfile which base image to use
RUN= the command to be executed while image build process
WORKDIR= sets the working directory(which opens first when you open a container)
EXPOSE= tells the user which port to expose(it didn't do anything)
COPY= copies files from local system to  the image
CMD=sets the default command that runs when the container starts, and it can be overridden at runtime (command is written in pieces)
ENTRYPOINT= you can write the full command, but the key difference from CMD is that ENTRYPOINT is harder to override at runtime, making it better for defining the main executable of a container
