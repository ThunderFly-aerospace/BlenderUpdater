r"""
BlenderUpdater Addon - Install this folder as a Blender addon.

This addon provides a UI panel in Blender for updating mesh models
while preserving their properties.

Installation:
1. Copy the entire 'blender_addon' folder to Blender's addons directory:
   - Windows: %APPDATA%\Blender Foundation\Blender\{version}\scripts\addons\
   - macOS: ~/Library/Application Support/Blender/{version}/scripts/addons/
   - Linux: ~/.config/blender/{version}/scripts/addons/

2. Or use Blender's UI: Edit > Preferences > Add-ons > Install
   (Select the blender_addon folder as a zip or directly)

3. Enable the addon in Preferences > Add-ons by checking the box next to "BlenderUpdater"

4. Find the panel in 3D View > Sidebar (press N) > BlenderUpdater tab
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
import json
import glob


class BlenderUpdaterProperties(PropertyGroup):
    """Properties for BlenderUpdater addon."""
    
    config_path: StringProperty(
        name="Config File",
        description="Path to the configuration JSON file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
    )


def which_file_format(filename):
    """Determine the file format from filename extension."""
    file_format = filename.rpartition('.')[2]
    return file_format


def copy_geometry(target_obj, source_obj):
    """Copy geometry from source mesh to target mesh while preserving UV layers."""
    source_mesh = source_obj.data
    target_mesh = target_obj.data
    
    # Backup all UV layers from TARGET
    uv_backup = []
    for layer in target_mesh.uv_layers:
        uv_backup.append({
            "name": layer.name,
            "data": [loop.uv.copy() for loop in layer.data]
        })

    # Remove existing UV layers
    while target_mesh.uv_layers:
        target_mesh.uv_layers.remove(target_mesh.uv_layers[0])

    # Clear and rebuild geometry
    target_mesh.clear_geometry()
    target_mesh.from_pydata(
        [v.co for v in source_mesh.vertices],
        [],
        [[v for v in p.vertices] for p in source_mesh.polygons]
    )

    # Restore UV layers
    for layer_info in uv_backup:
        uv_layer = target_mesh.uv_layers.new(name=layer_info["name"])
        data = layer_info["data"]
        if len(data) == len(uv_layer.data):
            for i in range(len(data)):
                uv_layer.data[i].uv = data[i]

    # Smooth shading
    for poly in target_mesh.polygons:
        poly.use_smooth = True

    # Finalize
    target_mesh.update()
    target_mesh.validate()


def import_and_rename(file, name=None):
    """Import a mesh file and update an existing object with the same name."""
    print("-----------------------------------------------")
    print(f"Importing file '{file}' with name '{name}'.")

    before = set(bpy.data.objects)
    
    # Load new model
    format_type = which_file_format(name)  
    if format_type == "stl":
        bpy.ops.wm.stl_import(filepath=file, global_scale=0.001)
    elif format_type in {"gltf", "glb"}:
        bpy.ops.import_scene.gltf(filepath=file, filter_glob='*.glb;*.gltf')
    else:
        print(f"Unsupported file format: {format_type}")
        return None
        
    after = set(bpy.data.objects) - before
    imported_objs = list(after)

    if not imported_objs:
        print("Nothing imported.")
        return None
    
    original_obj = bpy.data.objects.get(name) 
    if not original_obj:
        print(f"No existing object named '{name}' to replace.")
        return None

    if original_obj.type == 'MESH':
        imported_mesh = next((o for o in imported_objs if o.type == 'MESH'), None)
        if imported_mesh:            
            bpy.ops.object.select_all(action='DESELECT')
            imported_mesh.select_set(True)
            bpy.context.view_layer.objects.active = imported_mesh
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            copy_geometry(original_obj, imported_mesh)
            # Cleanup
            bpy.data.objects.remove(imported_mesh, do_unlink=True)
        else:
            print("No imported mesh found to replace the original mesh.")
    elif original_obj.type == 'EMPTY':
        # Find the imported EMPTY (if multiple imported meshes, find matching EMPTY)
        imported_empty = next((o for o in imported_objs if o.type == 'EMPTY'), None)
    
        # Copy geometry of EMPTY itself if it has mesh data
        if original_obj.data and original_obj.data.type == 'MESH' and imported_empty and imported_empty.data and imported_empty.data.type == 'MESH':
            copy_geometry(original_obj, imported_empty)
    
        orig_children = [o for o in original_obj.children if o.type == 'MESH']
        imp_children = [o for o in imported_objs if o.type == 'MESH']
    
        # Apply transforms to imported children
        bpy.ops.object.select_all(action='DESELECT')
        for imp_child in imp_children:
            imp_child.select_set(True)
            bpy.context.view_layer.objects.active = imp_child
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
        # Copy geometry for each child mesh, matching by name base
        for orig in orig_children:
            base = orig.name.split('.')[0]
            match = next((imp for imp in imp_children if imp.name.startswith(base)), None)
            if match:
                copy_geometry(orig, match)
    
        # Cleanup imported objects
        for obj in imported_objs:
            bpy.data.objects.remove(obj, do_unlink=True)

    else:
        print(f"Object type '{original_obj.type}' not supported for merging.")
        # Rename the first imported object if any
        if imported_objs:
            obj = imported_objs[0]
            obj.data.name = name
            obj.name = name
        else:
            print("No imported object to rename.")
    
    print("-----------------------------------------------")
    
    return name


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
            print("############################")
            print("############################")
            print("##                        ##")
            print("##    Generating model    ##")  
            print("##                        ##")
            print("############################")
            print("############################")
            
            # Load configuration
            with open(config_path, 'r') as file:
                config_data = json.load(file)
            
            print("Configuration file:", config_path)
            if 'parts' in config_data:
                for parts in config_data['parts']:
                    print("Parts:", parts)
            if 'paths' in config_data:
                for paths in config_data['paths']:
                    print("Paths:", paths)
            
            # Import parts defined in config file
            if "parts" in config_data:
                for part in config_data['parts']:
                    file = part['name']
                    filename = file.rpartition('/')[2]
                    import_and_rename(file, filename)
            
            # Import parts in paths defined in config file
            if "paths" in config_data:
                for paths in config_data['paths']:
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
