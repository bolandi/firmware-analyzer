import os

# Docker images
BINWALK_DOCKER_IMAGE = 'farbo/binwalk:latest'
CWE_CHECKER_DOCKER_IMAGE = 'fkiecad/cwe_checker:latest'
FIRMWALKER_DOCKER_IMAGE = 'farbo/firmwalker:latest'
FIRMADYNE_DOCKER_IMAGE = 'farbo/firmadyne:latest'
FIRMADYNE_EXTRACTOR_DOCKER_IMAGE = 'ddcc/firmadyne-extractor:latest'
BYTESWEEP_DOCKER_IMAGE = 'farbo/bytesweep:latest'
BANG_DOCKER_IMAGE = 'farbo/bang:latest'
CVEBINTOOL_DOCKER_IMAGE = 'farbo/cve_bin_tool:latest'

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
BINWALK_PATH_PREFIX = '/workspace/target/binwalk/'
CWE_CHECKER_DIR = f'{DST_DIR}/cwe-checker'
FIRMWALKER_DIR = f'{DST_DIR}/firmwalker'
FIRMADYNE_DIR = f'{DST_DIR}/firmadyne'
BYTESWEEP_DIR = f'{DST_DIR}/bytesweep'
BANG_DIR = f'{DST_DIR}/bang'
CVEBINTOOL_DIR = f'{DST_DIR}/cvebintool'
STATS_DIR = f'{DST_DIR}/stats'
CVE_STATS_FILE = f'{STATS_DIR}/cve-stats.csv'

# Log
LOG_SEPARATOR = '=' * 10
LOG_DEBUG_LINE_SEPARATOR = f'{LOG_SEPARATOR} DEBUG {LOG_SEPARATOR}'

# Misc
DATE_TIME_FORMAT = '%Y%m%d-%H%M%S'
