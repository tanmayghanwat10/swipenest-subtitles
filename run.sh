#!/bin/bash
set -euo pipefail

IMAGE_NAME="swipenest"
TAG="latest"

# Build image if missing or rebuild on demand
docker build -t "${IMAGE_NAME}:${TAG}" .

# Check for arguments
if [ $# -gt 0 ]; then
    case "$1" in
        "local")
            echo "Running in local video mode..."
            docker run --rm \
              -v "$(pwd)/input:/app/input" \
              -v "$(pwd)/output:/app/output" \
              -v "$(pwd)/Config.txt:/app/Config.txt" \
              "${IMAGE_NAME}:${TAG}" local
            ;;
        "youtube")
            if [ $# -gt 1 ]; then
                echo "Running in YouTube mode with URL: $2"
                docker run --rm \
                  -v "$(pwd)/input:/app/input" \
                  -v "$(pwd)/output:/app/output" \
                  -v "$(pwd)/Config.txt:/app/Config.txt" \
                  "${IMAGE_NAME}:${TAG}" youtube "$2"
            else
                echo "Error: YouTube URL required for youtube mode"
                echo "Usage: $0 {local|youtube <url>}"
                exit 1
            fi
            ;;
        "interactive")
            echo "Running in interactive mode..."
            docker run --rm -it \
              -v "$(pwd)/input:/app/input" \
              -v "$(pwd)/output:/app/output" \
              -v "$(pwd)/Config.txt:/app/Config.txt" \
              "${IMAGE_NAME}:${TAG}"
            ;;
        *)
            echo "Usage: $0 {local|youtube <url>|interactive}"
            exit 1
            ;;
    esac
else
    # Default to interactive mode
    echo "Running in interactive mode (default)..."
    docker run --rm -it \
      -v "$(pwd)/input:/app/input" \
      -v "$(pwd)/output:/app/output" \
      -v "$(pwd)/Config.txt:/app/Config.txt" \
      "${IMAGE_NAME}:${TAG}"
fi
