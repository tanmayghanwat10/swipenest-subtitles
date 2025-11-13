#!/bin/bash
set -euo pipefail

echo "🚀 Starting Swipenest Subtitle Generator..."

START_STR=$(date +"%d/%m/%Y %H:%M:%S")
START_TS=$(date +%s)

python3 src/main.py

END_STR=$(date +"%d/%m/%Y %H:%M:%S")
END_TS=$(date +%s)
ELAPSED=$((END_TS - START_TS))
MINUTES=$((ELAPSED / 60))
SECONDS=$((ELAPSED % 60))

mkdir -p output
echo "$START_STR" > output/output.txt
echo "$END_STR" >> output/output.txt

echo "⏱️ Total execution time: ${ELAPSED} seconds (${MINUTES} min ${SECONDS} sec)"
