"""
Blender addon/plugin for BlenderUpdater with UI integration.

This addon provides a user interface panel in Blender to easily update meshes
using a configuration file without needing to use the command line.
"""

bl_info = {
    "name": "BlenderUpdater",
    "author": "ThunderFly-aerospace",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > BlenderUpdater",
    "description": "Update mesh models while preserving properties (textures, materials, UV maps)",
    "warning": "",
    "doc_url": "https://github.com/ThunderFly-aerospace/BlenderUpdater",
    "category": "Import-Export",
}

import bpy
from bpy.props import StringProperty
from bpy.types import Operator, Panel, PropertyGroup
import os


class BlenderUpdaterProperties(PropertyGroup):
    """Properties for BlenderUpdater addon."""
    
    config_path: StringProperty(
        name="Config File",
        description="Path to the configuration JSON file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
    )


class BLENDERUPDATER_OT_select_config(Operator):
    """Select configuration file for BlenderUpdater."""
    bl_idname = "blenderupdater.select_config"
    bl_label = "Select Config File"
    bl_description = "Select a JSON configuration file"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(subtype="FILE_PATH")
    filter_glob: StringProperty(default="*.json", options={'HIDDEN'})
    
    def execute(self, context):
        context.scene.blenderupdater_props.config_path = self.filepath
        self.report({'INFO'}, f"Selected config: {self.filepath}")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class BLENDERUPDATER_OT_update_meshes(Operator):
    """Update meshes based on configuration file."""
    bl_idname = "blenderupdater.update_meshes"
    bl_label = "Update Meshes"
    bl_description = "Update mesh models while preserving properties"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        config_path = context.scene.blenderupdater_props.config_path
        
        if not config_path:
            self.report({'ERROR'}, "Please select a configuration file first")
            return {'CANCELLED'}
        
        if not os.path.exists(config_path):
            self.report({'ERROR'}, f"Configuration file not found: {config_path}")
            return {'CANCELLED'}
        
        try:
            # Import here to ensure it's in the right context
            from .updater import BlenderUpdater
            
            # Create updater and run
            updater = BlenderUpdater(config_path)
            updater.update_all()
            
            self.report({'INFO'}, "Mesh update completed successfully")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Error during update: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}


class BLENDERUPDATER_PT_main_panel(Panel):
    """Main panel for BlenderUpdater in the 3D View sidebar."""
    bl_label = "BlenderUpdater"
    bl_idname = "BLENDERUPDATER_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BlenderUpdater'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.blenderupdater_props
        
        # Header
        box = layout.box()
        box.label(text="Mesh Model Updater", icon='MESH_DATA')
        
        # Configuration file section
        box = layout.box()
        box.label(text="Configuration:", icon='FILE')
        
        row = box.row()
        row.prop(props, "config_path", text="")
        
        row = box.row()
        row.operator("blenderupdater.select_config", icon='FILEBROWSER')
        
        # Update button
        layout.separator()
        box = layout.box()
        row = box.row()
        row.scale_y = 2.0
        row.operator("blenderupdater.update_meshes", icon='FILE_REFRESH')
        
        # Info section
        layout.separator()
        box = layout.box()
        box.label(text="Info:", icon='INFO')
        col = box.column(align=True)
        col.label(text="Updates mesh geometry while")
        col.label(text="preserving properties:")
        col.label(text="• UV maps")
        col.label(text="• Materials & Textures")
        col.label(text="• Object hierarchy")
        
        # Supported formats
        layout.separator()
        box = layout.box()
        box.label(text="Supported formats:", icon='FILE_3D')
        col = box.column(align=True)
        col.label(text="• STL")
        col.label(text="• GLB / GLTF")


# Registration
classes = (
    BlenderUpdaterProperties,
    BLENDERUPDATER_OT_select_config,
    BLENDERUPDATER_OT_update_meshes,
    BLENDERUPDATER_PT_main_panel,
)


def register():
    """Register the addon."""
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.blenderupdater_props = bpy.props.PointerProperty(
        type=BlenderUpdaterProperties
    )


def unregister():
    """Unregister the addon."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.blenderupdater_props


if __name__ == "__main__":
    register()
