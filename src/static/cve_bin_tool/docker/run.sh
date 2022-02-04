#!/bin/bash
set -u

IN_DIR=${1}
OUT_DIR=${2}

# Default report name is output.cve-bin-tool.$date.*
DATE=`date +%d-%m-%y`

cve-bin-tool -f json -o $OUT_DIR/report-$DATE.json --report $IN_DIR
# The tool returns 0 if no CVE found, 1 if any CVE found and more than 1 if something went wrong
if [ $? -gt 1 ]; then
  exit 1
fi

# Generate html report for UI as well. Due to cache on previous run, it will be fast
cve-bin-tool -f html -o $OUT_DIR/report-$DATE.html --report $IN_DIR
if [ $? -gt 1 ]; then
  exit 1
fi

exit 0
