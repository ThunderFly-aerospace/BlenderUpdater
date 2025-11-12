"""
Main updater class for BlenderUpdater.

Handles configuration loading and orchestration of mesh updates.
"""

import json
import os
import glob
from .mesh_operations import import_and_rename


class BlenderUpdater:
    """
    Main class for updating mesh models in Blender scenes.
    
    Loads configuration and orchestrates mesh updates while preserving properties.
    """
    
    def __init__(self, config_file):
        """
        Initialize the BlenderUpdater with a configuration file.
        
        Args:
            config_file: Path to the JSON configuration file
        """
        self.config_file = config_file
        self.config_folder = os.path.dirname(os.path.abspath(config_file))
        self.config_name = os.path.basename(config_file).split('.')[0]
        
        with open(config_file, 'r') as file:
            self.config_data = json.load(file)
        
        print("Configuration file:", config_file)
        if 'parts' in self.config_data:
            for parts in self.config_data['parts']:
                print("Parts:", parts)
        if 'paths' in self.config_data:
            for paths in self.config_data['paths']:
                print("Paths:", paths)
    
    def update_all(self):
        """
        Update all mesh models defined in the configuration.
        
        Processes both individual parts and path patterns.
        """
        print("############################")
        print("############################")
        print("##                        ##")
        print("##    Generating model    ##")  
        print("##                        ##")
        print("############################")
        print("############################")
        
        # Import parts defined in config file
        if "parts" in self.config_data:
            for part in self.config_data['parts']:
                file = part['name']
                filename = file.rpartition('/')[2]
                import_and_rename(file, filename)
        
        # Import parts in paths defined in config file
        if "paths" in self.config_data:
            for paths in self.config_data['paths']:
                for file in glob.glob(paths):
                    filename = os.path.basename(file)
                    import_and_rename(file, filename)
        
        print("############################")
        print("############################")
        print("##                        ##")
        print("##          DONE          ##")  
        print("##                        ##")
        print("############################")
        print("############################")
    
    def save_blend_file(self, filename):
        """
        Save the Blender file.
        
        Args:
            filename: Path where to save the .blend file
        """
        import bpy
        bpy.ops.wm.save_as_mainfile(filepath=filename)
