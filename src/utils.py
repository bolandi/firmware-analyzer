import csv
from glob import glob
from pathlib import Path

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


def get_binwalk_extracted_dirs(level=0):
    paths = glob(f'{BASE_DIR}/{BINWALK_DIR}/*/')
    dirs = {}
    for path in paths:
        dir_name = path.split('/')[-2]  # First and last token are empty strings
        dirs[dir_name] = path
    return dirs