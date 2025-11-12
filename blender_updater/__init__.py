"""
BlenderUpdater - A Python package for updating mesh models in Blender while preserving properties.

This package allows you to update mesh geometry in Blender scenes while preserving:
- UV maps
- Materials
- Textures
- Object properties
- Hierarchy and parenting
"""

__version__ = "1.0.0"
__author__ = "ThunderFly-aerospace"

from .updater import BlenderUpdater
from .mesh_operations import copy_geometry, import_and_rename

__all__ = ['BlenderUpdater', 'copy_geometry', 'import_and_rename']
