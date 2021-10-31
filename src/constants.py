import os

# Docker images
BINWALK_DOCKER_IMAGE = 'farbo/binwalk'

# Set env variables for source and target
BASE_DIR = os.getcwd()
SRC_DIR = 'images'
DST_DIR = 'target'
try:
    os.mkdir(f'{BASE_DIR}/{DST_DIR}')
except FileExistsError:
    pass

SRC_PATH = f'{BASE_DIR}/{SRC_DIR}'
DST_PATH = f'{BASE_DIR}/{DST_DIR}'
SRC_FILES = os.listdir(SRC_PATH)
LOG_SEPARATOR = '=' * 10
LOG_DEBUG_LINE_SEPARATOR = f'{LOG_SEPARATOR} DEBUG {LOG_SEPARATOR}'
