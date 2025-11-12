"""
Command-line interface for BlenderUpdater.

This module provides the CLI entry point for running BlenderUpdater from Blender.
"""

import sys
import argparse


def main():
    """
    Main entry point for the BlenderUpdater CLI.
    
    This should be called from within Blender's Python environment:
    blender file.blend --python -m blender_updater.cli -- --config config.json
    """
    # Parse arguments - Blender passes args after "--"
    parser = argparse.ArgumentParser(
        description="Update mesh models in Blender while preserving properties"
    )
    parser.add_argument(
        "-c", "--config",
        help="Configuration file path",
        default="./config.json"
    )
    
    # Handle both direct calls and calls through Blender
    if "--" in sys.argv:
        args = parser.parse_known_args(sys.argv[sys.argv.index("--")+1:])[0]
    else:
        args = parser.parse_args()
    
    # Import here to ensure we're in Blender context
    from .updater import BlenderUpdater
    
    # Create updater and run
    updater = BlenderUpdater(args.config)
    updater.update_all()


if __name__ == "__main__":
    main()
