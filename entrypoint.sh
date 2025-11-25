#!/bin/bash
set -eo pipefail

echo "🚀 Starting Swipenest Subtitle Generator..."

if [ "$1" = "local" ]; then
  echo "Running local video processing mode..."
  python -m src.main_local
elif [ "$1" = "youtube" ]; then
  if [ -z "$2" ]; then
    echo "Error: YouTube URL required for youtube mode"
    exit 1
  fi
  echo "Running YouTube video processing mode with URL: $2"
  python -m src.main_youtube "$2"
else
  echo "Running interactive mode..."
  python -m src.main
fi

echo "✅ Subtitle generation completed."
