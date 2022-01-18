import os.path

import logging
import shutil
from common_helper_process import execute_shell_command_get_return_code
from src.constants import *

# Input already extracted image, write reports in specified output directory
from src.utils import get_binwalk_extracted_dirs

BYTESWEEP_CMD_BASE = 'docker run --rm -v "{INPUT_DIR}":/input '\
                     '-v "{OUTPUT_DIR}":/output {DOCKER_IMAGE} -v '\
                     '-D /input DummyImgFile /output'

try:
    os.mkdir(BYTESWEEP_DIR)
except FileExistsError:
    pass


def run_bytesweep(extraction_dir=None):
    dirs = get_binwalk_extracted_dirs(format=True)
    if len(dirs) == 0:
        logging.info(f'No extracted directory found. Try running binwalk first')

    for img_name, extracted_path in dirs.items():
        logging.info(f'Running bytesweep analysis on {extracted_path}')
        target_dir = os.path.join(BASE_DIR, BYTESWEEP_DIR, img_name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        else:
            logging.info(f'The target directory already exists, skipping analysis for {target_dir}')
            continue

        # # Source image file is used for final report, it's not re-extracted
        # img_file = os.path.join(SRC_PATH, img_name)
        cmd = BYTESWEEP_CMD_BASE.format(INPUT_DIR=extracted_path, OUTPUT_DIR=target_dir,
                                        DOCKER_IMAGE=BYTESWEEP_DOCKER_IMAGE)
        output, return_code = execute_shell_command_get_return_code(cmd)
        if return_code != 0:
            logging.info('FAILED')
            logging.debug(output)
        else:
            logging.info(f'SUCCESS: Results written to {target_dir}')

