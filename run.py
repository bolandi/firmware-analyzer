#!/usr/bin/env python3
import logging
import sys
from argparse import ArgumentParser

from src.constants import *
from src.dynamic.firmadyne.automation import run_firmadyne
from src.static.binwalk.automation import run_binwalk
from src.static.bytesweep.automation import run_bytesweep
from src.static.cwe_checker.automation import run_cwe_checker
from src.static.firmwalker.automation import run_firmwalker
from src.static.binaryanalysis_ng.automation import run_bang

try:
    from common_helper_process import execute_shell_command_get_return_code
except ImportError:
    os.system('pip3 install -r requirements.txt')


def print_usage():
    print('usage: run.py [build|custom|clean]')


def main():
    logging.basicConfig(format='%(asctime)-15s %(module)s: %(message)s', stream=sys.stdout, level=logging.DEBUG)
    parser = ArgumentParser()
    parser.add_argument('-b', '--binwalk', action='store_true', help='Runs binwalk on the firmware images')
    parser.add_argument('-cc', '--cwe_checker', action='store_true', help='Runs cwe-checker on the firmware images')
    parser.add_argument('-fw', '--firmwalker', action='store_true', help='Runs firmwalker on the firmware images')
    parser.add_argument('-fd', '--firmadyne', action='store_true',
                        help='Runs dynamic analysis using firmadyne on the firmware images')
    parser.add_argument('-bs', '--bytesweep', action='store_true', help='Runs bytesweep analysis on extracted images')
    parser.add_argument('-bang', action='store_true', help='Run Binary Analysis Next Gen on the firmware images')
    parser.add_argument('-a', '--all', action='store_true', help='Runs all supported tools on the firmware images')

    if (len(sys.argv) == 1):
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if args.binwalk:
        run_binwalk()
    if args.cwe_checker:
        run_cwe_checker()
    if args.firmwalker:
        run_firmwalker()
    if args.firmadyne:
        # todo: add optional parameter to pass a single image using full path
        run_firmadyne()
    if args.bytesweep:
        run_bytesweep()
    if args.bang:
        run_bang()
    if args.all:
        # todo: run all analysis tools in proper order
        logging.error("Not implemented")

if __name__ == '__main__':
    main()
