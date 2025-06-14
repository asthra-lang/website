#!/bin/bash

# Script to sync documentation from local asthra repository
# Assumes asthra repo is located at ../asthra relative to this script

set -e  # Exit on any error

echo "Starting documentation sync..."

# Check if asthra repository exists
if [ ! -d "../asthra" ]; then
    echo "Error: asthra repository not found at ../asthra"
    echo "Please ensure the asthra repository is cloned one level up from this directory"
    exit 1
fi

# Check if asthra/docs directory exists
if [ ! -d "../asthra/docs" ]; then
    echo "Error: docs directory not found in ../asthra/docs"
    echo "Please ensure the asthra repository has a docs directory"
    exit 1
fi

# Create _docs directory if it doesn't exist
mkdir -p _docs

echo "Removing existing docs directories..."
# Remove existing docs directories
rm -rf _docs/contributor _docs/spec _docs/stdlib _docs/user-manual

echo "Copying documentation directories from ../asthra/docs..."

# Copy documentation directories if they exist
if [ -d "../asthra/docs/contributor" ]; then
    cp -r ../asthra/docs/contributor _docs/
    echo "✓ Copied contributor docs"
else
    echo "⚠ Warning: contributor docs not found in ../asthra/docs/"
fi

if [ -d "../asthra/docs/spec" ]; then
    cp -r ../asthra/docs/spec _docs/
    echo "✓ Copied spec docs"
else
    echo "⚠ Warning: spec docs not found in ../asthra/docs/"
fi

if [ -d "../asthra/docs/stdlib" ]; then
    cp -r ../asthra/docs/stdlib _docs/
    echo "✓ Copied stdlib docs"
else
    echo "⚠ Warning: stdlib docs not found in ../asthra/docs/"
fi

if [ -d "../asthra/docs/user-manual" ]; then
    cp -r ../asthra/docs/user-manual _docs/
    echo "✓ Copied user-manual docs"
else
    echo "⚠ Warning: user-manual docs not found in ../asthra/docs/"
fi

echo "Documentation synced successfully!"
echo "You can now run 'bundle exec jekyll serve' to preview the site locally" 