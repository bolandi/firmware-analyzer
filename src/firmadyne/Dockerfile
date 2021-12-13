FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN echo "dash dash/sh boolean false" | debconf-set-selections && dpkg-reconfigure dash

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    git-core \
    ca-certificates \
    busybox-static \
    fakeroot \
    dmsetup \
    kpartx \
    netcat-openbsd \
    nmap \
    python3-pip \
    python3-psycopg2 \
    snmp \
    uml-utilities \
    util-linux \
    vlan \
    qemu-system-arm \
    qemu-system-mips \
    qemu-system-x86 \
    qemu-utils \
    lsb-core \
    wget \
    tar \
    sudo \
    # expect can be used to interact with qemu shell
    expect \
    eslint && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN git clone --recursive https://github.com/firmadyne/firmadyne.git /home/firmadyne/firmadyne

RUN useradd -d /home/firmadyne -m -s /bin/bash firmadyne && echo \
    "firmadyne:firmadyne" | chpasswd && adduser firmadyne sudo

# Add user as sudoer
RUN echo "firmadyne ALL=NOPASSWD:ALL">>/etc/sudoers

RUN chown -R firmadyne:firmadyne /home/firmadyne

# Switch to your new user in the docker image
USER firmadyne
WORKDIR /home/firmadyne/firmadyne

RUN source ./download.sh

# Set FIRMWARE_DIR in firmadyne.config
RUN sed -i "/FIRMWARE_DIR=/c\FIRMWARE_DIR=$PWD" firmadyne.config
# Comment out psql -d firmware ... in getArch.sh
RUN sed -i 's/psql/#psql/' ./scripts/getArch.sh
# Change interpreter to python3
RUN sed -i 's/env python/env python3/' ./sources/extractor/extractor.py ./scripts/makeNetwork.py

COPY run.sh .
# Replace makeImage with the modified version
COPY makeImage.sh ./scripts/makeImage.sh

# Download linpeas to search for possible paths to escalate privileges
RUN wget -N https://raw.githubusercontent.com/carlospolop/privilege-escalation-awesome-scripts-suite/master/linPEAS/linpeas.sh -P ./scripts
RUN chmod +x ./scripts/linpeas.sh

# Fix "USER: unbound variable" when executing final run
ENV USER firmadyne

# Call run.sh without arguments
ENTRYPOINT [ "/home/firmadyne/firmadyne/run.sh" ]

