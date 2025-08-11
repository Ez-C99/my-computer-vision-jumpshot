#!/usr/bin/env bash
set -euo pipefail
source .venv/bin/activate

python -m my_computer_vision_jumpshot.cli \
  --video examples/sample_video.mp4 \
  --out   examples/sample_output
