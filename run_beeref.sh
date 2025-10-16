#!/bin/bash
# Script to run BeeRef with the virtual environment

cd "$(dirname "$0")"
source venv/bin/activate
python -m beeref "$@"
