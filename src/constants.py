import os

# Set env variables for source and target
BASE_DIR = os.getcwd()
SRC_DIR = 'images'
DST_DIR = 'target'
try:
    os.mkdir(os.getcwd() + DST_DIR)
except FileExistsError:
    pass

SRC_FILES = os.listdir(f'{BASE_DIR}/{SRC_DIR}')
LOG_SEPARATOR = '=' * 10
LOG_DEBUG_LINE_SEPARATOR = f'{LOG_SEPARATOR} DEBUG {LOG_SEPARATOR}'
