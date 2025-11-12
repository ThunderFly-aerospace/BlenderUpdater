# BlenderUpdater Example Project

This example demonstrates how to use BlenderUpdater to update mesh models in a Blender project.

## Contents

- `example_project.blend` - Basic Blender project with two objects
- `config.json` - Configuration file for BlenderUpdater
- `parts/` - Directory containing mesh files
  - `cube.stl` - A simple cube mesh
  - `cylinder.stl` - A simple cylinder mesh

## Setup

### 1. Open the Blender Project

Open `example_project.blend` in Blender. You should see two objects:
- A cube object named `cube.stl`
- A cylinder object named `cylinder.stl`

These objects have materials and properties applied to them.

### 2. Modify the Mesh Files

You can modify the STL files in the `parts/` directory using any 3D modeling software (CAD, Blender, etc.).

For this example, the files are already present and ready to use.

## Usage

### Method 1: Using the UI Addon

1. Install the BlenderUpdater addon (see main [INSTALL.md](../INSTALL.md))
2. Open `example_project.blend` in Blender
3. Press `N` to open the sidebar
4. Go to the `BlenderUpdater` tab
5. Click "Select Config File" and choose `config.json` from this directory
6. Click "Update Meshes"

The meshes will be updated while preserving their materials and properties!

### Method 2: Using the CLI

```bash
# From the repository root, install the package
cd ..
/path/to/blender/python -m pip install .

# Run the updater
cd example_project
blender example_project.blend --python -m blender_updater -- --config config.json
```

### Method 3: Using the Legacy Script

```bash
# From the example_project directory
blender example_project.blend --python ../scripts/do_complete_assembly.py -- --config config.json
```

## What to Expect

After running BlenderUpdater:

1. The geometry of the cube and cylinder will be updated from the STL files
2. **Materials** will be preserved - colors and textures remain intact
3. **UV maps** will be preserved (if they exist)
4. **Object properties** will be preserved
5. **Transformations** (position, rotation, scale) will be preserved

## Try It Yourself

1. Apply a material to the cube in Blender (e.g., make it red)
2. Move or rotate the objects
3. Export new versions of the STL files with different geometry
4. Run BlenderUpdater
5. Notice that your materials and transformations are still there, but the geometry is updated!

## Configuration Explanation

The `config.json` file tells BlenderUpdater which meshes to update:

```json
{
  "parts": [
    {
      "name": "./parts/cube.stl"
    },
    {
      "name": "./parts/cylinder.stl"
    }
  ],
  "paths": [
    "./parts/*.stl"
  ]
}
```

- `parts`: List of specific files to import
- `paths`: Glob patterns to match multiple files (e.g., all STL files in parts/)

## Notes

- Make sure the object names in Blender match the filenames
- STL files are automatically scaled by 0.001 (millimeters to meters)
- You can use STL, GLB, or GLTF formats

## Troubleshooting

If objects don't update:
- Check that object names in Blender match the filenames (e.g., `cube.stl`)
- Verify the paths in `config.json` are correct relative to the Blender file
- Check the console output for error messages

## Learn More

- See [QUICKSTART.md](../QUICKSTART.md) for general usage
- See [README.md](../README.md) for full documentation
