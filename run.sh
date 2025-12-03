#!/bin/bash

echo "🚀 Starting SwipeNest Subtitle Engine"
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"

# Detect input and output folders
INPUT_DIR="/app/input"
OUTPUT_DIR="/app/output"

# Create output folder if missing
mkdir -p "$OUTPUT_DIR"

# Check if input folder exists and has videos
if [ ! -d "$INPUT_DIR" ] || [ -z "$(ls -A $INPUT_DIR)" ]; then
  echo "❌ No videos found in $INPUT_DIR folder."
  exit 1
fi

# Run main.py with progress logs
python main.py --input_dir "$INPUT_DIR" --output_dir "$OUTPUT_DIR"

echo "🚀 SwipeNest finished at $(date '+%Y-%m-%d %H:%M:%S')"
