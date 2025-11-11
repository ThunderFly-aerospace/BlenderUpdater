import math
import os
import bpy
C = bpy.context
D = bpy.data
import sys
import argparse
import json
import glob

print("############################")
print("############################")
print("##                        ##")
print("##    Generating model    ##")  
print("##                        ##")
print("############################")
print("############################")


## Nacteni konfiguraci a konfiguracnich souboru
parser = argparse.ArgumentParser()

parser.add_argument("-c", "--config", help="Configuration file", default="./scripts/config.json")

args = parser.parse_known_args(sys.argv[sys.argv.index("--")+1:])[0]

config_file = args.config
config_folder = os.path.dirname(os.path.abspath(config_file))
config_name = os.path.basename(config_file).split('.')[0]
with open(config_file, 'r') as file:
    config_data = json.load(file)

print("Configuration file ", config_file)
for parts in config_data['parts']:
    print("Parts: ", parts)
for paths in config_data['paths']:
    print("Paths: ", paths)


def deselect():
    for ob in bpy.context.selected_objects:
        bpy.data.objects[ob.name].select_set(False)
        #ob.select_set(False)

def import_and_rename(file, name = None, merge = True):

    print("-----------------------------------------------")
    print(f"Importing file '{file}' with name '{name}'.")

    before = set(bpy.data.objects)
    
    # load new model
    format_type = which_file_format(name)  
    if format_type == "stl":
    	bpy.ops.wm.stl_import(filepath=file, global_scale=0.001)
    elif format_type in {"gltf", "glb"}:
    	bpy.ops.import_scene.gltf(filepath=file, filter_glob='*.glb;*.gltf')
    else:
        print(f"Unsupported file format: {format_type}")
        return
    	
    after = set(bpy.data.objects) - before
    imported_objs = list(after)

    if not imported_objs:
        print("Nothing imported.")
        return
    
    original_obj = bpy.data.objects.get(name) 
    if not original_obj:
        print(f"No existing object named '{name}' to replace.")
        return

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


def copy_geometry(target_obj, source_obj):
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
  

def save_blender_file(filename):
	bpy.ops.wm.save_as_mainfile(filepath=filename)
	
def which_file_format(filename):
	file_format = filename.rpartition('.')[2]
	return file_format


# imports parts defined in config file
if "parts" in config_data:
	for part in config_data['parts']:
		file = part['name']
		filename = file.rpartition('/')[2]
		#print("file = ", file, " filename = ", filename)
		import_and_rename(file, filename)

# imports parts in paths defined in config file
if "paths" in config_data:
	for paths in config_data['paths']:
		for file in glob.glob(paths):
		    filename = os.path.basename(file)
		    #print("file = ", file, " filename = ", filename)
		    import_and_rename(file, filename)


print("############################")
print("############################")
print("##                        ##")
print("##          DONE          ##")  
print("##                        ##")
print("############################")
print("############################")

#sys.exit()
#save_blender_file("Thundermill_automatic.blend")
#if config.get('save_blend', False):
#save_blender_file(os.path.abspath(config_file.split('.')[0]+'.blend'))
