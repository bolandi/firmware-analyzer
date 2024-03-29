import csv
import json
import logging
import sys
import requests
from glob import glob

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

def _get_cve_description(cve_id):
    logging.debug(f'Fetching description for {cve_id}')
    uri = f'https://services.nvd.nist.gov/rest/json/cve/1.0/{cve_id}'
    response = requests.get(uri)
    json_data = json.loads(response.text)
    description = json_data['result']['CVE_Items'][0]['cve']['description']['description_data'][0]['value']
    return description

# Generate CSV file containing firmware and CVEs
def gen_cve_summary():
    image_names = _get_image_name(CVEBINTOOL_DIR)
    if (len(image_names) == 0):
        logging.info("No CVE report found. Try running cve-bin-tool first")
        return

    # Firmware, CVE1, CVE2, ...
    raw_columns = ['Firmware']
    cve_columns = ['CVE-ID', 'CVSS Score', 'Severity', 'Description']
    total_columns = ['Total Firmware Images', 'Critical', 'High', 'Medium', 'Low']
    total_stats = {'TOTAL': 0, 'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    severity_columns = ['Firmware', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    top_cve_columns = ['CVE-ID', 'Occurance', 'Affectd Firmwares']
    # Image name, number of occurances
    raw_rows = []
    cve_rows = []
    total_rows = []
    severity_rows = []
    top_cve_rows = []
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
                cve_description = ''
                try:
                    cve_description = _get_cve_description(cve_number)
                except Exception:
                    logging.error(f'Could not fetch description for {cve_number}')
                cve_rows.append([cve_number, cve_score, cve_severity, cve_description])

            # Sort descending
            raw_columns = raw_columns[0:1] + sorted(raw_columns[1:], reverse=True)

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

        raw_row = [0] * len(raw_columns)
        severity_row = [0] * len(severity_columns)
        raw_row[0] = image_name
        severity_row[0] = image_name
        for cve in json_data:
            cve_severity = cve['severity']
            if cve['cve_number'] == 'CVE-2009-3720':
            # if image_name == 'DCS-6915_REVA_FIRMWARE_1.01.00.zip' and cve_number == 'CVE-2009-3720':
                    i = 1
            occurance = cve['paths'].count(',') + 1
            raw_row[raw_columns.index(cve['cve_number'])] = raw_row[raw_columns.index(cve['cve_number'])] + occurance
            severity_row[severity_columns.index(cve_severity)] = severity_row[
                                                                     severity_columns.index(cve_severity)] + occurance
            total_stats[cve_severity] = total_stats[cve_severity] + occurance

        raw_rows.append(raw_row)
        severity_rows.append(severity_row)

    # Total
    total_rows.append([len(raw_rows), total_stats['CRITICAL'], total_stats['HIGH'],
                          total_stats['MEDIUM'], total_stats['LOW']])

    # Top CVEs
    index = 1
    for cve_id in raw_columns[1:]:
        occurance = 0
        affected_fw = 0
        for row in raw_rows:
            # try:
            if row[index] == 0:
                continue
            # except IndexError:
            #     row += [0]
            #     continue
            occurance += row[index]
            affected_fw += 1
        index += 1
        top_cve_rows.append([cve_id, occurance, affected_fw])


    with open(os.path.join(STATS_DIR, 'firmware-cve-count.csv'), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(raw_columns)
        writer.writerows(raw_rows)

    with open(os.path.join(STATS_DIR, 'firmware-cve-severity.csv'), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(severity_columns)
        writer.writerows(severity_rows)

    with open(os.path.join(STATS_DIR, 'cve-db.csv'), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(cve_columns)
        cve_rows.sort(reverse=True)
        writer.writerows(cve_rows)

    with open(os.path.join(STATS_DIR, 'cve-total.csv'), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(total_columns)
        writer.writerows(total_rows)

    with open(os.path.join(STATS_DIR, 'top-cves.csv'), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(top_cve_columns)
        writer.writerows(top_cve_rows)

    if len(empty_dirs) != 0:
        logging.debug('There was no report for the following images. Try deleting the directories and run cve-bin-tool again:')
        for image in empty_dirs:
            logging.debug(image)
