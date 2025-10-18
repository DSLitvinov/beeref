#!/bin/bash

# BeeRef Development Runner Script
# This script runs BeeRef in development mode using PDM

# Add PDM to PATH if not already there
export PATH="/Users/dmitry/Library/Python/3.13/bin:$PATH"

echo "Starting BeeRef in development mode..."
echo "Python version: $(pdm run python --version)"
echo "Working directory: $(pwd)"
echo ""

# Run BeeRef with PDM
pdm run python -m beeref "$@"
