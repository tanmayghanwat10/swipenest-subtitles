#!/bin/bash
set -euo pipefail

IMAGE_NAME="swipenest-subtitles"
TAG="latest"

# Build image if missing or rebuild on demand
docker build -t "${IMAGE_NAME}:${TAG}" .

# Run with mounted input/output
docker run --rm \
  -v "$(pwd)/input:/app/input" \
  -v "$(pwd)/output:/app/output" \
  -v "$(pwd)/Config.txt:/app/Config.txt" \
  "${IMAGE_NAME}:${TAG}"
