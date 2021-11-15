import os

# Docker images
BINWALK_DOCKER_IMAGE = 'farbo/binwalk'
CWE_CHECKER_DOCKER_IMAGE = 'fkiecad/cwe_checker'

# Set env variables for source and target
BASE_DIR = os.getcwd()
SRC_DIR = 'images'
DST_DIR = 'target'
try:
    os.mkdir(f'{BASE_DIR}/{DST_DIR}')
except FileExistsError:
    pass

# Paths
SRC_PATH = f'{BASE_DIR}/{SRC_DIR}'
DST_PATH = f'{BASE_DIR}/{DST_DIR}'
SRC_FILES = os.listdir(SRC_PATH)
BINWALK_DIR = f'{DST_DIR}/binwalk'
CWE_CHECKER_DIR = f'{DST_DIR}/cwe-checker'
BINWALK_PATH_PREFIX = '/workspace/target/binwalk/'

# Log
LOG_SEPARATOR = '=' * 10
LOG_DEBUG_LINE_SEPARATOR = f'{LOG_SEPARATOR} DEBUG {LOG_SEPARATOR}'
