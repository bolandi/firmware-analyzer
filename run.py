#!/usr/bin/env python3
import logging
import sys
from argparse import ArgumentParser

from src.binwalk.automation import run_binwalk
from src.constants import *
from src.cwe_checker.automation import run_cwe_checker
from src.firmwalker.automation import run_firmwalker

try:
    from common_helper_process import execute_shell_command_get_return_code
except ImportError:
    os.system('pip3 install -r requirements.txt')
from common_helper_process import execute_shell_command_get_return_code


def _pull_docker_images(images=None):
    for image in images:
        cmd = f'docker pull {image}'
        logging.info(f'Pulling {image} docker image: {cmd}')
        output, return_code = execute_shell_command_get_return_code(cmd)
    if return_code != 0:
        logging.error(f'Failed to pull {image} docker image:\n{output}')


def print_usage():
    print('usage: run.py [build|custom|clean]')


def main():
    logging.basicConfig(format='%(asctime)-15s %(module)s: %(message)s', stream=sys.stdout, level=logging.DEBUG)
    parser = ArgumentParser()
    parser.add_argument('-b', '--binwalk', action='store_true', help='Runs binwalk on the firmware images')
    parser.add_argument('-cc', '--cwe_checker', action='store_true', help='Runs cwe-checker on the firmware images')
    parser.add_argument('-fw', '--firmwalker', action='store_true', help='Runs firmwalker on the firmware images')
    parser.add_argument('-a', '--all', action='store_true', help='Runs all supported tools on the firmware images')

    if (len(sys.argv) == 1):
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if args.binwalk:
        _pull_docker_images((BINWALK_DOCKER_IMAGE,))
        run_binwalk
    if args.cwe_checker:
        _pull_docker_images((CWE_CHECKER_DOCKER_IMAGE,))
        run_cwe_checker
    if args.firmwalker:
        _pull_docker_images((FIRMWALKER_DOCKER_IMAGE,))
        run_firmwalker
    if args.all:
        docker_images = list((BINWALK_DOCKER_IMAGE, CWE_CHECKER_DOCKER_IMAGE, FIRMWALKER_DOCKER_IMAGE))
        _pull_docker_images(docker_images)


if __name__ == '__main__':
    main()
