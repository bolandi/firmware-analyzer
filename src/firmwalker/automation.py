import logging
from pathlib import Path

from common_helper_process import execute_shell_command_get_return_code

from src.constants import *
from src.utils import get_binwalk_extracted_dirs

# Run firmwalker on the parent extracted folder (immediate directory)
FIRMWALKER_COMMAND_BASE = 'docker run --rm -v {INPUT_DIR}:/input -v {OUTPUT_DIR}:/output {DOCKER_IMAGE} /input /output/{REPORT}'

try:
    os.mkdir(FIRMWALKER_DIR)
except FileExistsError:
    pass


def _scan_binwalk_extracted_filesystems():
    # For each dir in dirs dictionary: Key= Directory name - Value= Directory path
    dirs = get_binwalk_extracted_dirs()

    for name, path in dirs.items():
        logging.info(f'Running firmwalker on {path}')
        p = Path(f'{BASE_DIR}/{FIRMWALKER_DIR}')
        cmd = FIRMWALKER_COMMAND_BASE.format(INPUT_DIR=path, DOCKER_IMAGE=FIRMWALKER_DOCKER_IMAGE,
                                             REPORT=name + '.txt', OUTPUT_DIR=Path(f'{BASE_DIR}/{FIRMWALKER_DIR}'))
        output, return_code = execute_shell_command_get_return_code(cmd)
        if return_code == 0:
            logging.info(f'SUCCESS: Scan report is written as {name}.txt')
        else:
            logging.debug(f'FAILED: {output}')


def run_firmwalker():
    _scan_binwalk_extracted_filesystems()
