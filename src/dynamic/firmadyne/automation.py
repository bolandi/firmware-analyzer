import os.path

import sys

import logging
import shutil
from common_helper_process import execute_shell_command_get_return_code

from src.constants import *

EXTRACTION_CMD_BASE = 'docker run --rm -v "{INPUT_DIR}":/firmware-in:ro '\
                      '-v "{OUTPUT_DIR}":/firmware-out {DOCKER_IMAGE} ' \
                      'fakeroot /home/extractor/extractor/extractor.py -np '\
                      '/firmware-in/"{IMG_BASE_NAME}" /firmware-out'
FIRMADYNE_CMD_BASE = 'docker run --rm --privileged=true -v "{INPUT_DIR}":/input '\
                     '-v "{OUTPUT_DIR}":/output {DOCKER_IMAGE} /input /output'

try:
    os.mkdir(FIRMADYNE_DIR)
except FileExistsError:
    pass


def _extract(image_path):
    base_name = os.path.basename(image_path)
    working_dir = os.path.join(BASE_DIR, FIRMADYNE_DIR, base_name)
    try:
        os.mkdir(working_dir)
    except FileExistsError:
        pass

    # Check if extracted root filesystem already extracted
    for file in os.listdir(working_dir):
        if file.endswith('.tar.gz'):
            logging.info(f"Skipping extraction, root file system already exists at {image_path}. ")
            return working_dir, file

    logging.info(f"Extracting root file system for {image_path}")
    cmd = EXTRACTION_CMD_BASE.format(INPUT_DIR=os.path.dirname(image_path), OUTPUT_DIR=working_dir,
                                     DOCKER_IMAGE=FIRMADYNE_EXTRACTOR_DOCKER_IMAGE,
                                     IMG_BASE_NAME=base_name
                                     )
    output, return_code = execute_shell_command_get_return_code(cmd)

    for file in os.listdir(working_dir):
        if file.endswith('.tar.gz'):
            return working_dir, file

    logging.error('Failed to extract root file system, probably the image does not include a file system.')
    logging.debug(f'More details: \n{output}')
    shutil.rmtree(working_dir)
    return '', ''


def _run_emulation(working_dir, rootfs):
    logging.info(f'Running emulation for {os.path.join(working_dir, rootfs)}.\nThis may take several minutes ...')
    cmd = FIRMADYNE_CMD_BASE.format(INPUT_DIR=os.path.join(working_dir, rootfs), OUTPUT_DIR=working_dir,
                                    DOCKER_IMAGE=FIRMADYNE_DOCKER_IMAGE)
    # For some reason, kpartx cannot mount the loopback device after a successful previous mount but scceeeds in the
    # next retry. Retrying this (exit code == 9) for 3 times
    for retry in range(3):
        # todo: add option for verbose when running firmadyne, if absent then set stdout to pipe
        output, return_code = execute_shell_command_get_return_code(cmd)
        if return_code == 9:
            continue
        else:
            break

    if return_code == 0:
        logging.info(f'SUCCESS: Emulation log is written as {os.path.join(working_dir, "emulation.log")}')
        return 0
    else:
        logging.debug(f'FAILED: {output}')
        return 1


def run_firmadyne(image_path=None):
    if image_path != None:
        working_dir, rootfs = _extract(image_path)
        if len(working_dir) != 0 or len(rootfs) != 0:
            return _run_emulation(working_dir, rootfs)
        else:
            return 1

    # Run emulation for all the images found in images directory
    if len(SRC_FILES) == 0:
        logging.info(f"No images found under {SRC_PATH}")
        sys.exit(0)

    for file in SRC_FILES:
        target_dir = os.path.join(BASE_DIR, FIRMADYNE_DIR, file)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        elif len(os.listdir(target_dir)) != 0:
            logging.info(f'The target directory already exists, skipping analysis for {target_dir}')
            continue

        working_dir, rootfs = _extract(os.path.join(SRC_PATH, file))
        if len(working_dir) == 0 or len(rootfs) == 0:
            continue
        _run_emulation(working_dir, rootfs)

