FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN echo "dash dash/sh boolean false" | debconf-set-selections && dpkg-reconfigure dash

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    git-core \
    ca-certificates \
    radare2 \
    python3 \
    python3-pip \
    nano \
    sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://gitlab.com/bytesweep/bytesweep.git /home/bytesweep/bytesweep

RUN useradd -d /home/bytesweep -m -s /bin/bash bytesweep && echo \
    "bytesweep:bytesweep" | chpasswd && adduser bytesweep sudo

# Add user as sudoer
RUN echo "bytesweep ALL=NOPASSWD:ALL">>/etc/sudoers

RUN chown -R bytesweep:bytesweep /home/bytesweep

# Switch to your new user in the docker image
USER bytesweep
WORKDIR /home/bytesweep/bytesweep

RUN pip3 install -r requirements.txt
RUN pip3 install .

# Symlink python to python3
RUN sudo ln -s /usr/bin/python3 /usr/bin/python

# Replace bytesweep script with modified version
COPY bytesweep ./scripts/bytesweep

ENTRYPOINT [ "/home/bytesweep/bytesweep/scripts/bytesweep" ]