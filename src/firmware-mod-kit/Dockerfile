# todo:
# [x] from binwalk image
# [x] apt get pre-req
# [] clone mod-kit repo from release or tag
# [] simlink fmk -> workspac/target
# [] add single extrac method using kwargs: if no param then run on all in /images else extract specific
# [] extract both binwalk and modkit into target, use {tool_name} dir for only logs and tool specific artifacts

FROM farbo/binwalk:latest

# Set shell to bash instead of dash
ARG DEBIAN_FRONTEND=noninteractive

# Required lib for generating the entropy plot
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    zlib1g-dev \
    liblzma-dev \
    python-magic


