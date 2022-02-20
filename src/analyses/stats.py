import json
import logging
import sys
from glob import glob
import csv

from src.constants import *

try:
    os.mkdir(STATS_DIR)
except FileExistsError:
    pass


def _get_image_name(path):
    paths = glob(os.path.join(BASE_DIR, path, '*/'))
    image_names = []
    for dir in paths:
        image_names.append(dir.split(os.path.sep)[-2])
    return image_names


# Generate CSV file containing firmware and CVEs
def gen_cve_summary():
    image_names = _get_image_name(CVEBINTOOL_DIR)
    if (len(image_names) == 0):
        logging.info("No CVE report found. Try running cve-bin-tool first")
        sys.exit(0)

    # CSV columns: Firmware, CVE1, CVE2, ...
    columns = ['Firmware']
    # CSV rows: Image name, number of occurances
    rows = []
    empty_dirs=[]
    for image_name in image_names:
        path = os.path.join(BASE_DIR, CVEBINTOOL_DIR, image_name)
        report = [f for f in os.listdir(path) if f.endswith('.json')]
        if len(report) == 0:
            empty_dirs.append(image_name)
            continue
        f = open(os.path.join(path, report[0]), 'r')
        # List of dicts
        json_data = json.loads(f.read())

        if (len(json_data) == 0):
            continue

        for cve in json_data:
            cve_number = cve['cve_number']
            if cve_number not in columns:
                columns.append(cve_number)

        row = [''] * len(columns)
        row[0] = image_name
        for cve in json_data:
            occurance = cve['paths'].count(',') + 1
            row[columns.index(cve['cve_number'])] = occurance
        rows.append(row)

    with open(os.path.join(STATS_DIR, 'cve-stats.csv'), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

    if len(empty_dirs) != 0:
        logging.debug('There was no report for the following images. Try deleting the directories and run cve-bin-tool again:')
        for image in empty_dirs:
            logging.debug(image)
