#!/bin/bash
set -e
set -u

INFILE=${1}
OUT_DIR=${2}

# Get Architecture
ARCH=""
set +e
ARCH=$(source ./scripts/getArch.sh $INFILE|awk -F' *:? *' '{print $2}')
if [ $? != 0 ]; then
  echo "Failed to get architecture"
  exit 1
fi
set -e

# Rename and copy image into images directory
cp $INFILE ./images/1.tar.gz

# Make image as root
sudo -su root source ./scripts/makeImage.sh 1 $ARCH
<<'###'
set +e
# Retry doesn't work in the same container. Should be retried on the automation script using a new container
if [ $? -eq 9 ]; then
  echo "----Image mount failed. Retrying after 5 seconds..."
  sleep 5
  sudo -su root source ./scripts/makeImage.sh 1 $ARCH
  if [ $? != 0 ]; then
    echo "----Failed to create image"
    exit 1
  fi
fi
set -e
###

# Infer network
echo "----Inferring network, please wait..."
INTERFACES=$(source ./scripts/inferNetwork.sh 1 $ARCH|awk -F'[][]' '{print $2}')
echo "Interfaces: ${INTERFACES}"

echo "Running firmware : Terminating after 5 minutes..."
set +e
# Wait 5 minutes for firmware to boot and run analysis.
# Alternatives: named pipe or expect command to interact with qemu
timeout --preserve-status --signal SIGINT 300 "./scratch/1/run.sh"
set -e
sleep 1

# Copy execution log to output directory
echo "Writing emulation log to disc"
cp ./scratch/1/qemu.final.serial.log "${OUT_DIR}/emulation.log"

# todo: run exploits toward running firmware.
#source runExploits.py $ARCH $INTERFACES $OUT_DIR

