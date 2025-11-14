#!/bin/bash
set -eo pipefail

echo "🚀 Starting Swipenest Subtitle Generator..."

python -m src.main

echo "✅ Subtitle generation completed."
