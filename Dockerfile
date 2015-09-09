############################################################
# Dockerfile to build Dim Wit Application Containers
############################################################

# Set the base image to Ubuntu
FROM ubuntu:14.10

# File Author / Maintainer
MAINTAINER James Lindsay <james@jimb.io>

# Update the sources list
RUN apt-get update && apt-get install -y \
    tar \
    git \
    curl \
    nano \
    wget \
    dialog \
    net-tools \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    libffi-dev \
    libssl-dev \
    openjdk-8-jre

# create volume.
VOLUME /tmp

# set new working directory
RUN mkdir /dimwit-src
WORKDIR /dimwit-src

# Expose ports
EXPOSE 8080

# Create non-root user.
RUN useradd ubuntu -m -s /bin/bash

# set the entry point.
ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-jar", "gs-accessing-mongodb-data-rest-0.1.0.jar"]

