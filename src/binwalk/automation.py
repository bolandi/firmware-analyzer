#!/usr/bin/env python3
import logging
import os
from common_helper_process import execute_shell_command_get_return_code
from src.constants import *

COMMAND_BASE = f'docker run --user $UID:$UID -v "{BASE_DIR}:/workspace" -w /workspace sheabot/binwalk'


def _extract_firmware():

    output, return_code = execute_shell_command_get_return_code(f'{COMMAND_BASE} -C {DST_DIR}/binwalk -eM {SRC_DIR}/*')
    logging.info(f'out={output}\nreturn={return_code}')


def _run_custom(command):
    output, return_code = execute_shell_command_get_return_code(
        f'docker run -v "$(pwd):/workspace" -w /workspace  sheabot/binwalk {command}')
    if (return_code == 0):
        logging.debug(output)
    else:
        logging.error(output)


def cleanup():
    output, return_code = execute_shell_command_get_return_code(
        'rm -rf images/binwalk')
    logging.debug(output)


def run():
    _extract_firmware()
