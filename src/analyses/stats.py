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

    # Firmware, CVE1, CVE2, ...
    raw_columns = ['Firmware']
    cve_columns = ['CVE-ID', 'CVSS Score', 'Severity']
    total_columns = ['Total Firmware Images', 'Critical', 'High', 'Medium', 'Low']
    total_stats = {'TOTAL': 0, 'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    # Image name, number of occurances
    raw_rows = []
    cve_rows = []
    total_rows = []
    empty_dirs=[]

    total=0
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
            cve_score = cve['score']
            cve_severity = cve['severity']
            if cve_number not in raw_columns:
                raw_columns.append(cve_number)
                cve_rows.append([cve_number, cve_score, cve_severity])

        row = [0] * len(raw_columns)
        row[0] = image_name
        for cve in json_data:
            cve_severity = cve['severity']
            occurance = cve['paths'].count(',') + 1
            row[raw_columns.index(cve['cve_number'])] = row[raw_columns.index(cve['cve_number'])] + occurance
            total_stats[cve_severity] = total_stats[cve_severity] + occurance

        raw_rows.append(row)

    # Total
    total_rows.append([len(raw_rows), total_stats['CRITICAL'], total_stats['HIGH'],
                          total_stats['MEDIUM'], total_stats['LOW']])

    with open(os.path.join(STATS_DIR, 'firmware-cve-count.csv'), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(raw_columns)
        writer.writerows(raw_rows)

    with open(os.path.join(STATS_DIR, 'cve-score-severity.csv'), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(cve_columns)
        writer.writerows(cve_rows)

    with open(os.path.join(STATS_DIR, 'cve-total.csv'), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(total_columns)
        writer.writerows(total_rows)

    if len(empty_dirs) != 0:
        logging.debug('There was no report for the following images. Try deleting the directories and run cve-bin-tool again:')
        for image in empty_dirs:
            logging.debug(image)
