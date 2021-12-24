#Requirements

For running Firmadyne, devicemapper is required using of the following host os:
devicemapper is supported on Docker Engine - Community running on CentOS, Fedora, SLES 15, Ubuntu, Debian, or RHEL.
More details:
https://docs.docker.com/storage/storagedriver/device-mapper-driver/

#todo: details on how to customize execution

todo: proper instructions with details. for a quick debug try running a docker in interactive mode and also disabling the 5 minutes termiantion signal in run.sh. sample docker command:
# the input is the tarball of the carved root filesystem  
docker run --rm -it --privileged=true -v /home/farrokh/kth/thesis/2021/workspace/firmware-analyzer/target/firmadyne/DES-1210-52_REVC_FIRMWARE_4.10.004.zip/DES-1210-52_REVC_FIRMWARE_4.10.004.zip_ec08f6f2b5ffdfb4094d0215d0c8aee0.tar.gz:/input -v /home/farrokh/kth/thesis/2021/workspace/firmware-analyzer/target/firmadyne/tmp:/output farbo/firmadyne:latest /input /output