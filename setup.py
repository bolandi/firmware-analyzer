#!/usr/bin/env python3
import logging
import os
import sys
from src.binwalk.automation import _extract_firmware

try:
    from common_helper_process import execute_shell_command_get_return_code
except ImportError:
    os.system('pip3 install -r requirements.txt')
from common_helper_process import execute_shell_command_get_return_code

def _pull_docker_images():
    logging.info('Pulling binwalk docker image')
    output, return_code = execute_shell_command_get_return_code('docker pull sheabot/binwalk')
    if return_code != 0:
        logging.error(f'Failed to pull binwalk docker image:\n{output}')
    else:
        logging.debug(output)


def print_usage():
    print('usage: setup.py [build|custom|clean]')


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    command = ''
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'build':
            _pull_docker_images()
        elif command == 'custom':
            # _run_custom(command)
            pass
        elif command == 'clean':
            # cleanup()
            pass
        else:
            print_usage()
    else:
        _pull_docker_images()
        _extract_firmware()
    # TODO: run analysis

'''
Run all the tools and combine functionality between them e.g. extractions by binwalk, analysis by cwe-checker, et
'''
