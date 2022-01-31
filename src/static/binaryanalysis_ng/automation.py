import os.path
from os import path

import logging
from common_helper_process import execute_shell_command_get_return_code

from src.constants import *

BANG_COMMAND_BASE = 'docker run --rm -v "{INPUT_IMG}":"/{IMG_NAME}" ' \
                    '-v "{OUTPUT_DIR}":/output {DOCKER_IMAGE} ' \
                    '-f "/{IMG_NAME}" -u /output'

try:
    os.mkdir(BANG_DIR)
except FileExistsError:
    pass


def run_bang():
    for file in SRC_FILES:
        src_img = path.join(SRC_PATH, file)
        target_dir = path.join(BASE_DIR, BANG_DIR, file)
        if path.exists(target_dir):
            logging.info(f'{file} has already been scanned.')
            continue
        else:
            os.makedirs(target_dir)
        logging.info(f'Scanning {file} using binary analysis ng')
        cmd = BANG_COMMAND_BASE.format(INPUT_IMG=src_img, OUTPUT_DIR=target_dir,
                                       IMG_NAME=file, DOCKER_IMAGE=BANG_DOCKER_IMAGE)

        output, return_code = execute_shell_command_get_return_code(cmd)

        if return_code != 0:
            logging.info('FAILED')
            logging.debug(output)
        else:
            logging.info(f'SUCCESS: Results written to {target_dir}')