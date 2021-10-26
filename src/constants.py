import os

# Set env variables for source and target
BASE_DIR = os.getcwd()
SRC_DIR = 'images'
DST_DIR = 'target'

try:
    os.mkdir(os.getcwd() + DST_DIR)
except FileExistsError:
    pass
