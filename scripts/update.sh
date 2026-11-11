#!/bin/bash
set -e

# Navigate to repo directory
cd internal-docs/

# Pull latest changes
echo "Pulling latest changes from GitHub..."
git pull

# Update dependencies
echo "Updating dependencies..."
source .venv/bin/activate
uv pip install -e .

echo "✅ notebooklm-py updated successfully!"
