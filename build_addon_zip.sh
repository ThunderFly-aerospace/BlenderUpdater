#!/bin/bash
# Script to create a zip file of the Blender addon
# This is useful for manual distribution or local testing

set -e

# Get version from git tag or use 'dev'
if git describe --tags --exact-match 2>/dev/null; then
    VERSION=$(git describe --tags --exact-match | sed 's/^v//')
else
    VERSION="dev-$(git rev-parse --short HEAD)"
fi

OUTPUT_FILE="blender_updater_addon-${VERSION}.zip"

echo "Building addon zip: ${OUTPUT_FILE}"
echo "Version: ${VERSION}"

# Create zip from blender_addon directory
cd blender_addon
zip -r "../${OUTPUT_FILE}" . -x "*.pyc" -x "__pycache__/*" -x ".DS_Store" -x "*.git*"
cd ..

echo ""
echo "✅ Successfully created: ${OUTPUT_FILE}"
echo ""
echo "To install in Blender:"
echo "1. Open Blender"
echo "2. Go to Edit > Preferences > Add-ons"
echo "3. Click Install and select ${OUTPUT_FILE}"
echo "4. Enable 'Import-Export: BlenderUpdater'"
