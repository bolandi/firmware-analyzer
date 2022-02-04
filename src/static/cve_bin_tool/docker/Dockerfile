FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN echo "dash dash/sh boolean false" | debconf-set-selections && dpkg-reconfigure dash

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    git-core \
    ca-certificates \
    python3 \
    python3-pip \
    nano \
    file \
    binutils \
    tar \
    unzip \
    rpm2cpio \
    cpio \
    cabextract \
    sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -d /home/cvebintool -m -s /bin/bash cvebintool && echo \
    "cvebintool:cvebintool" | chpasswd && adduser cvebintool sudo

# Install latest cve-bin-tool from PyPI
RUN pip3 install cve-bin-tool

# Add user as sudoer
RUN echo "cvebintool ALL=NOPASSWD:ALL">>/etc/sudoers

RUN chown -R cvebintool:cvebintool /home/cvebintool

# Switch to your new user in the docker image
USER cvebintool
WORKDIR /home/cvebintool

# Symlink python to python3
RUN sudo ln -s /usr/bin/python3 /usr/bin/python

# todo: cve_bin_tool_config sample in this directory can be used to run the tool with dafault config

# Run cve-bin-tool on an empty directory to download CVEs
RUN mkdir tmp && cve-bin-tool tmp

# Add custom script to run cve-bin-tool
COPY run.sh ./

ENTRYPOINT [ "/home/cvebintool/run.sh" ]
