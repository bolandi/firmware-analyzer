import json
import logging

from common_helper_process import execute_shell_command_get_return_code

from src.constants import *
from src.utils import get_carved_elf_offsets

# -j=json and -q=quiet i.e. output json without debug logs
CWE_CHECKER_COMMAND_BASE = 'docker run --rm -v "{ELF_PATH}":/input {DOCKER_IMAGE} -jq  /input'
FILE_COMMAND_BASE = 'docker run --entrypoint /usr/bin/file --rm -v "{ELF_PATH}":/input {DOCKER_IMAGE} /input'
BLACK_LIST = ['vmlinux.64', 'vmlinux.32']

try:
    os.mkdir(CWE_CHECKER_DIR)
except FileExistsError:
    pass


def _scan_binwalk_carved_elfs():
    carved_elfs = (get_carved_elf_offsets())

    cwd = os.getcwd() + '/'
    # Output from the scan is a single JSON with mapping from ELF paths to an array of CWE findings for that ELF
    log_file = {}
    for elf in carved_elfs:
        include = True
        # Exclude known or time consuming files using black list
        for item in BLACK_LIST:
            if elf.endswith(item):
                include = False
                break
        if include:
            # Filter out ELFs with missing section headers to speed up the scan
            cmd = FILE_COMMAND_BASE.format(ELF_PATH=cwd + elf, DOCKER_IMAGE=BINWALK_DOCKER_IMAGE)
            output, return_code = execute_shell_command_get_return_code(cmd)
            if return_code == 0 and 'missing section headers' in output:
                logging.info(f'Skipping scan for {elf} due to missing section headers')
                continue
            # File is eligible for scanning
            logging.info(f'Running cwe-checker on {cwd}{elf}')
            cmd = CWE_CHECKER_COMMAND_BASE.format(ELF_PATH=cwd + elf, DOCKER_IMAGE=CWE_CHECKER_DOCKER_IMAGE)
            output, return_code = execute_shell_command_get_return_code(cmd)
            if return_code != 0:
                logging.info('FAILED')
                # logging.debug(f'Return code = {return_code} - Output= {output}')
            else:
                logging.info('SUCCESS')
                logging.debug(f'Return code = {return_code} - Output= {output}')
                log_file[f'{cwd}{elf}'] = json.loads(output)

    if len(log_file) == 0:
        logging.info('No results found')
        return

    with open(f'{BASE_DIR}/{CWE_CHECKER_DIR}/results_for_binwalk_artifacts.json', 'w') as file:
        json.dump(log_file, file)


def run_cwe_checker():
    _scan_binwalk_carved_elfs()
