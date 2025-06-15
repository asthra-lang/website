#!/bin/bash

# Script to sync versioned documentation from local asthra repository
# Assumes asthra repo is located at ../asthra relative to this script

set -e  # Exit on any error

echo "Starting versioned documentation sync..."

# Check if asthra repository exists
if [ ! -d "../asthra" ]; then
    echo "Error: asthra repository not found at ../asthra"
    echo "Please ensure the asthra repository is cloned one level up from this directory"
    exit 1
fi

# Check if it's a git repository
if [ ! -d "../asthra/.git" ]; then
    echo "Error: ../asthra is not a git repository"
    echo "Please ensure the asthra repository is properly cloned"
    exit 1
fi

# Use shared Python sync script (now handles versioned docs)
python3 sync-docs.py ../asthra

echo "Versioned documentation sync completed!"
echo "You can now run 'bundle exec jekyll serve' to preview the site locally" 