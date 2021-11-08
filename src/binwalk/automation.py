#!/usr/bin/env python3
import logging
import shutil
from shutil import copyfile
from os import path

from common_helper_process import execute_shell_command_get_return_code

from src.constants import *

COMMAND_BASE = f'cd images && docker run --rm -v "{BASE_DIR}:/workspace" -w /workspace {BINWALK_DOCKER_IMAGE}'
BINWALK_DIR = f'{DST_DIR}/binwalk'

try:
    os.mkdir(BINWALK_DIR)
except FileExistsError:
    pass


def _extract():
    """ Combines recursive extraction with signature analysis. Also deletes carved files after extraction

    Artifacts:
    - Extracted carved files at target/binwalk/_{file}
    - Signature analysis in CSV foramt: {file}.log
    """
    for file in SRC_FILES:
        if path.exists(f'{BINWALK_DIR}/{file}.log'):
            logging.info(f'{file} already extracted.')
            continue
        # todo: skip over directories in source folder
        logging.info(f'Extracting {file}')
        # todo: fix hex in csv (needs a PR to binwalk repo) and target permission
        cmd = f'{COMMAND_BASE} -C {DST_DIR}/binwalk -eMr {SRC_DIR}/{file} --log={BINWALK_DIR}/{file}.log -c'
        output, return_code = execute_shell_command_get_return_code(cmd)

        result = 'SUCCESS' if return_code == 0 else 'FAILED'
        logging.debug(f'Status: {result}\n{LOG_DEBUG_LINE_SEPARATOR}\n{output}\n{LOG_SEPARATOR}')


# To be used by other tools
# todo: fix paths
def extract(file, target_dir):
    logging.info(f'Extracting {file}')
    output, return_code = execute_shell_command_get_return_code(
        f'{COMMAND_BASE} -C {DST_DIR}/{target_dir} -erE {file}')
    if return_code != 0:
        # Archive or image not recognized but still eligible for analysis
        copyfile(f'{file}, {DST_PATH}/{target_dir}/{file}')
    result = 'SUCCESS' if return_code == 0 else 'FAILED'
    logging.debug(f'Status: {result}\n{LOG_DEBUG_LINE_SEPARATOR}\n{output}\n{LOG_SEPARATOR}')
    return return_code


def _move_artifacts(src, dst):
    shutil.move(src, dst)


def entropy(file=None, target_dir=None):
    """ Calculate entropy. If no specific file is specified in the source directory then it runs for all of them

    Artifacts:
    - {file}.entropy: Entropy log details in csv including the offset of edges
    - {file}.png: The entropy plot. Requires python3-matplotlib
    """
    if file:
        logging.info(f'Calculating entropy for {file}')
        cmd = f'{COMMAND_BASE} -EJ {SRC_DIR}/{file} --log={BINWALK_DIR}/{file}.entropy -c'
        output, return_code = execute_shell_command_get_return_code(
            cmd)
        if return_code == 0:
            _move_artifacts(f'{file}.png', f'{DST_PATH}/{target_dir}' if target_dir else BINWALK_DIR)
        else:
            logging.error('Status: FAILED')
        return return_code

    for file in SRC_FILES:
        if path.exists(f'{BINWALK_DIR}/{file}.entropy'):
            logging.info(f'Entropy for {file} already calculated.')
            continue
        cmd = f'{COMMAND_BASE} -EJ {SRC_DIR}/{file} --log={BINWALK_DIR}/{file}.entropy --csv'
        logging.info(f'Calculating entropy for {file}')
        output, return_code = execute_shell_command_get_return_code(
            cmd)
        if return_code == 0:
            _move_artifacts(f'{file}.png', BINWALK_DIR)
        else:
            logging.error('Status: FAILED')
            logging.debug(output)


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
    entropy()
    _extract()
