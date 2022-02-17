import os.path
import sys
from os import path

import logging
from common_helper_process import execute_shell_command_get_return_code

from src.constants import *
from src.utils import get_bang_extracted_dirs, get_binwalk_artifacts

CVEBINTOOL_COMMAND_BASE = 'docker run --rm -v "{INPUT_DIR}":"/{IMG_NAME}" ' \
                    '-v "{OUTPUT_DIR}":/output {DOCKER_IMAGE} ' \
                    '"/{IMG_NAME}" /output'

try:
    os.mkdir(CVEBINTOOL_DIR)
except FileExistsError:
    pass

def run_cve_bin_tool():
    artifacts = get_binwalk_artifacts(dir_only=False)
    if len(artifacts) == 0:
        logging.info(f'No extracted image found under {BINWALK_DIR}.\nTry running binwalk first')
        sys.exit(0)

    for img_name, extracted_path in artifacts.items():
        logging.info(f'Running cve-bin-tool analysis on {extracted_path}')
        target_dir = os.path.join(BASE_DIR, CVEBINTOOL_DIR, img_name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        else:
            logging.info(f'The target directory already exists, skipping analysis for {target_dir}')
            continue

        cmd = CVEBINTOOL_COMMAND_BASE.format(INPUT_DIR=extracted_path, OUTPUT_DIR=target_dir,
                                        DOCKER_IMAGE=CVEBINTOOL_DOCKER_IMAGE, IMG_NAME=img_name)

        output, return_code = execute_shell_command_get_return_code(cmd)
        if return_code != 0:
            logging.info('FAILED')
            logging.debug(output)
            os.rmdir(target_dir)
        else:
            logging.info(f'SUCCESS: Results written to {target_dir}')

# todo: consider committing docker container for smoother re-run on images
