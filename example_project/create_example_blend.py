#!/usr/bin/env python3
"""
Script to create the example Blender project file.

This script should be run from within Blender:
    blender --background --python create_example_blend.py

It will create example_project.blend with two objects (cube and cylinder)
that match the STL files in the parts/ directory.
"""

import bpy
import os

# Clear the default scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import the cube STL
print("Importing cube.stl...")
cube_path = os.path.join(os.path.dirname(__file__), "parts", "cube.stl")
if os.path.exists(cube_path):
    bpy.ops.wm.stl_import(filepath=cube_path, global_scale=0.001)
    
    # Find the imported object and rename it
    cube_obj = bpy.context.selected_objects[0]
    cube_obj.name = "cube.stl"
    
    # Add a material to the cube
    mat_cube = bpy.data.materials.new(name="CubeMaterial")
    mat_cube.use_nodes = True
    mat_cube.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.2, 0.2, 1.0)  # Red
    cube_obj.data.materials.append(mat_cube)
    
    # Position the cube
    cube_obj.location = (-2, 0, 0)
    
    print(f"Created cube object: {cube_obj.name}")
else:
    print(f"Warning: {cube_path} not found")

# Import the cylinder STL
print("Importing cylinder.stl...")
cylinder_path = os.path.join(os.path.dirname(__file__), "parts", "cylinder.stl")
if os.path.exists(cylinder_path):
    bpy.ops.wm.stl_import(filepath=cylinder_path, global_scale=0.001)
    
    # Find the imported object and rename it
    cylinder_obj = bpy.context.selected_objects[0]
    cylinder_obj.name = "cylinder.stl"
    
    # Add a material to the cylinder
    mat_cylinder = bpy.data.materials.new(name="CylinderMaterial")
    mat_cylinder.use_nodes = True
    mat_cylinder.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.2, 0.8, 1.0)  # Blue
    cylinder_obj.data.materials.append(mat_cylinder)
    
    # Position the cylinder
    cylinder_obj.location = (2, 0, 0)
    
    print(f"Created cylinder object: {cylinder_obj.name}")
else:
    print(f"Warning: {cylinder_path} not found")

# Add a camera
bpy.ops.object.camera_add(location=(0, -10, 5))
camera = bpy.context.object
camera.rotation_euler = (1.1, 0, 0)
bpy.context.scene.camera = camera

# Add a light
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
light = bpy.context.object
light.data.energy = 2.0

# Set up the scene
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 128

# Save the file
output_path = os.path.join(os.path.dirname(__file__), "example_project.blend")
bpy.ops.wm.save_as_mainfile(filepath=output_path)

print(f"\nExample project saved to: {output_path}")
print("\nTo use this example:")
print("1. Open example_project.blend in Blender")
print("2. Install the BlenderUpdater addon or package")
print("3. Run BlenderUpdater with config.json")
print("4. The meshes will be updated while preserving materials!")
