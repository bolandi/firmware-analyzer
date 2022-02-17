import os.path

import subprocess

import csv
import logging
from glob import glob
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired

from src.constants import *


def create_target_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_carved_elf_offsets(type=None):
    os.chdir(BINWALK_DIR)
    carved_elfs = {}
    for log_file in os.listdir(os.getcwd()):
        if log_file.endswith('.log'):
            with open(log_file) as csv_log:
                csv_reader = csv.reader(csv_log, delimiter=',')
                for row in csv_reader:
                    if row[0].startswith('FILE'):
                        row = next(csv_reader)
                        # strip path prefix to provide relative path from $pwd
                        path = row[0][len(BINWALK_PATH_PREFIX):] if row[0].startswith(BINWALK_PATH_PREFIX) else row[0]
                    if row[2].startswith('ELF'):
                        carved_elfs[path] = row[2]

    return carved_elfs


def get_binwalk_artifacts(dir_only=True):
    paths = glob(os.path.join(BASE_DIR, BINWALK_DIR, '*/'))
    artifacts = {}
    for path in paths:
        dir_name = path.split('/')[-2]  # First and last token are empty strings
        # Rename to orignal image name
        prefix = '_'
        suffix = '.extracted'
        dir_name = dir_name[dir_name.startswith(prefix) and len(prefix):]
        dir_name = dir_name[dir_name.endswith(suffix) and 0:-len(suffix)]
        artifacts[dir_name] = path

    # Include binary images that are not extractable i.e. not a directory
    if dir_only == False:
        for image in SRC_FILES:
            if image not in artifacts:
                artifacts[image] = os.path.join(BASE_DIR ,BINWALK_DIR, image)

    return artifacts

def get_bang_extracted_dirs():
    paths = glob(f'{BASE_DIR}/{BANG_DIR}/*/')
    dirs = {}
    for path in paths:
        dir_name = path.split('/')[-2]  # First and last token are empty strings
        dirs[dir_name] = path
    return dirs
