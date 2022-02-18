#!/usr/bin/env python3
import logging
import sys
from argparse import ArgumentParser
from src.constants import *

try:
    from src.dynamic.firmadyne.automation import run_firmadyne
    from src.static.binwalk.automation import run_binwalk
    from src.static.bytesweep.automation import run_bytesweep
    from src.static.cve_bin_tool.automation import run_cve_bin_tool
    from src.static.cwe_checker.automation import run_cwe_checker
    from src.static.firmwalker.automation import run_firmwalker
    from src.static.binaryanalysis_ng.automation import run_bang
    from common_helper_process import execute_shell_command_get_return_code
except ImportError:
    os.system('pip3 install -r requirements.txt')


def print_usage():
    print('usage: run.py [build|custom|clean]')


def main():
    logging.basicConfig(format='%(asctime)-15s:%(levelname)s %(funcName)s: %(message)s', stream=sys.stdout, level=logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('-bw', '--binwalk', action='store_true', help='Runs binwalk on the firmware images')
    parser.add_argument('-cc', '--cwe_checker', action='store_true', help='Runs cwe-checker on the firmware images')
    parser.add_argument('-fw', '--firmwalker', action='store_true', help='Runs firmwalker on the firmware images')
    parser.add_argument('-fd', '--firmadyne', action='store_true',
                        help='Runs dynamic analysis using firmadyne on the firmware images')
    parser.add_argument('-bs', '--bytesweep', action='store_true', help='Runs bytesweep analysis on extracted images')
    parser.add_argument('-bang', action='store_true', help='Run Binary Analysis Next Gen on the firmware images')
    parser.add_argument('-cbt', action='store_true', help='Run cv-bin-tool on extracted images')
    parser.add_argument('-a', '--all', action='store_true', help='Runs all supported tools on the firmware images')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print debug logs')

    if (len(sys.argv) == 1):
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
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
    if args.cbt:
        run_cve_bin_tool()
    if args.all:
        run_binwalk()
        run_firmwalker()
        run_cwe_checker()
        run_bytesweep()
        run_cve_bin_tool()
        run_firmadyne()

if __name__ == '__main__':
    main()
