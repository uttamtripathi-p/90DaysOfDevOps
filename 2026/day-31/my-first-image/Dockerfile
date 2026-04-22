
# Base image
#FROM ubuntu:latest AS builder

# Installing curl

#RUN apt-get update -y && apt-get install curl -y

# Default command

#CMD echo "Hello from my custom image!"


# First we tell the file which base image we want to use

#FROM ubuntu:latest AS builder

# Executing command during build

#RUN apt-get update -y

# To set working directory

#WORKDIR /app

# To copy files from host to image

#COPY . .

# Any port we want to tell the user to expose

#EXPOSE 80 

# Default command that will run during running container
#ENTRYPOINT echo "You're getting better"


# Dockerfile to run , port and access through browser

# Base image

FROM nginx:alpine AS builder

# Setting workdirectory
WORKDIR /home

# Copying my file

COPY . /usr/share/nginx/html

# The port to expose 

EXPOSE 80

# Command to run

CMD ["nginx", "-g" , "daemon off;"]

