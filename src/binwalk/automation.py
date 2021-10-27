#!/usr/bin/env python3
import logging

from common_helper_process import execute_shell_command_get_return_code

from src.constants import *

# COMMAND_BASE = f'docker run --user $UID:$UID -v "{BASE_DIR}:/workspace" -w /workspace sheabot/binwalk'
# COMMAND_BASE = f'docker run --group-add $(getent group docker | cut -d: -f3) -v "{BASE_DIR}:/workspace" -w /workspace sheabot/binwalk'
COMMAND_BASE = f'docker run -v "{BASE_DIR}:/workspace" -w /workspace sheabot/binwalk'


def _extract_firmware():
    # import pdb;
    # pdb.set_trace()
    for file in SRC_FILES:
        logging.info(f'Extracting {file}')
        output, return_code = execute_shell_command_get_return_code(
            f'{COMMAND_BASE} -C {DST_DIR}/binwalk -e {SRC_DIR}/{file}')
        result = 'SUCCESS' if return_code == 0 else 'FAILED'
        logging.debug(f'Status: {result}\n{LOG_DEBUG_LINE_SEPARATOR}\n{output}\n{LOG_SEPARATOR}')


def _run_custom(command):
    output, return_code = execute_shell_command_get_return_code(
        f'{COMMAND_BASE} {command}')
    if (return_code == 0):
        logging.debug(output)
    else:
        logging.error(output)


def cleanup():
    output, return_code = execute_shell_command_get_return_code(
        'rm -rf images/binwalk')
    logging.debug(output)


def run_binwalk():
    _extract_firmware()
