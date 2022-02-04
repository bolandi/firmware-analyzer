FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN echo "dash dash/sh boolean false" | debconf-set-selections && dpkg-reconfigure dash

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    git-core \
    ca-certificates \
    # BANG requires 3.9+
#    python3.9 \
#    python3-pip \
    nano \
    cabextract \
    default-jdk \
    e2tools \
    liblz4-tool \
    lzop \
    ncompress \
    p7zip-full \
    python3-psycopg2 \
    python3-elasticsearch \
    python3-defusedxml \
    python3-lz4 \
    python3-pil \
    python3-icalendar \
    python3-snappy \
    python3-tlsh \
    python3.9-dev \
    qemu-utils \
    rzip \
    squashfs-tools \
    zstd \
    binutils-common \
    liblzo2-dev \
    curl \
    build-essential \
    wget \
    liblzma-dev \
    lzma \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src

# BANG requires 3.9+ but doesn't run on the default 3.9.5 ppa hence installing 3.9.6
#RUN sudo wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz && sudo tar xzf Python-3.9.6.tgz
#RUN cd Python-3.9.6 && sudo ./configure && sudo make altinstall

# Clone BANG repository
RUN git clone https://github.com/armijnhemel/binaryanalysis-ng.git /home/bang/bang

RUN useradd -d /home/bang -m -s /bin/bash bang && echo \
    "bang:bang" | chpasswd && adduser bang sudo

# Add user as sudoer
RUN echo "bang ALL=NOPASSWD:ALL">>/etc/sudoers

RUN chown -R bang:bang /home/bang

# Switch to your new user in the docker image
USER bang
WORKDIR /home/bang/bang

# Install kaitai-struct-compiler
RUN curl -LO https://github.com/kaitai-io/kaitai_struct_compiler/releases/download/0.9/kaitai-struct-compiler_0.9_all.deb
RUN sudo apt-get install -y ./kaitai-struct-compiler_0.9_all.deb

# Fix import errors for kaitai struct files. May be fixed in later versions
RUN sed -i "s#/archive/zip#zip#g" src/parsers/browser/crx/crx.ksy
RUN sed -i "s#/common/bytes_with_io#/font/pcf/bytes_with_io#g" src/parsers/image/apple_icon/icns.ksy
COPY network/* src/parsers/network/
# Set custom configuration
COPY bang.config ./src

# Compile *.ksy files
RUN cd src && make

# BANG doesn't run on 3.8.10 and 3.9.5 which ironically are the default versions in Ubuntu repository as of the
# date of writing this comment. Installing python 3.9.6 from source was a pain specially with issues running pip
# hence using Pyenv which is a life saver.
# Set-up necessary Env vars for PyEnv
ENV PYENV_ROOT /home/bang/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
ENV PYTHON_VERSION 3.9.6

# Install pyenv
RUN set -ex \
    && curl https://pyenv.run | bash \
    && pyenv update \
    && pyenv install $PYTHON_VERSION \
    && pyenv global $PYTHON_VERSION \
    && pyenv rehash

# Install python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN chmod +x ./src/bang-scanner
RUN mkdir /home/bang/tmp

ENTRYPOINT [ "/home/bang/bang/src/bang-scanner" ]
