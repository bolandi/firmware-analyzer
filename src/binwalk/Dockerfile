FROM sheabot/binwalk:latest

# Set shell to bash instead of dash
ARG DEBIAN_FRONTEND=noninteractive

# Required lib for generating the entropy plot
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-matplotlib

# Create a non-root user named binwalk,
# give them the password "binwalk" put them in the sudo group
RUN useradd -d /home/binwalk -m -s /bin/bash binwalk && echo \
    "binwalk:binwalk" | chpasswd && adduser binwalk sudo

# Create target directory inside workspace
RUN mkdir -p /workspace/target

# Make biwnalk owner of workspace used by the volume
RUN chown -R binwalk:binwalk /workspace

# Switch to your new user in the docker image
USER binwalk
