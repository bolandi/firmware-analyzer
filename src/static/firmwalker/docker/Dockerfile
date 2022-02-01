FROM ubuntu:20.04

# Set shell to bash instead of dash
ARG DEBIAN_FRONTEND=noninteractive
RUN echo "dash dash/sh boolean false" | debconf-set-selections && dpkg-reconfigure dash

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    git-core \
    ca-certificates \
    eslint && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone latest firmwalker from github repository
RUN git clone https://github.com/craigz28/firmwalker /home/firmwalker/firmwalker

# Create a non-root user named firmwalker
RUN useradd -d /home/firmwalker -m -s /bin/bash firmwalker && echo \
    "firmwalker:firmwalker" | chpasswd && adduser firmwalker sudo

RUN chown -R firmwalker:firmwalker /home/firmwalker

# Switch to your new user in the docker image
USER firmwalker

WORKDIR /home/firmwalker/firmwalker

# Call firmwalker executable without arguments
ENTRYPOINT [ "/home/firmwalker/firmwalker/firmwalker.sh" ]
