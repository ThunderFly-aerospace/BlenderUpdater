#!/bin/bash
# Example script for updating a Blender file using BlenderUpdater
# 
# Usage:
# 1. Edit the BLEND_FILE variable below to match your .blend file
# 2. Make sure you have a config.json in the same directory
# 3. Run: ./update_blend_file.sh

BLEND_FILE="NAME_OF_FILE.blend"
CONFIG_FILE="config.json"

# Use the installed blender_updater package
blender "$BLEND_FILE" --python -m blender_updater -- --config "$CONFIG_FILE"

# Alternative: Use the legacy script directly (backward compatibility)
# blender "$BLEND_FILE" --python scripts/do_complete_assembly.py -- --config scripts/config.json
