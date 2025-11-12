# BlenderUpdater

Script for updating mesh models in Blender projects while preserving their properties (textures, colors, materials, etc.).

## Features

- Updates mesh geometry while preserving UV maps, materials, and other properties
- Supports multiple file formats: STL, GLB, GLTF
- Configuration-based batch updating
- Preserves object hierarchy and transformations

## Usage

1. Place `update_blend_file.sh` in the same folder as your main Blender file
2. Edit `update_blend_file.sh` and fill in the name of your blend file
3. Configure `scripts/config.json` to define which parts to update
4. Run: `./update_blend_file.sh`

## Configuration

Edit `scripts/config.json` to specify:
- Individual parts by exact path
- Path patterns using wildcards

Example:
```json
{
  "parts": [
    {
      "name": "./parts_in_use/part.stl"
    }
  ],
  "paths": [
    "./parts_in_use/*.stl"
  ]
}
```

## Supported File Formats

- STL (imported with 0.001 scale)
- GLB
- GLTF

## How It Works

The script:
1. Imports new mesh geometry from specified files
2. Matches them with existing objects in the Blender scene by name
3. Replaces only the geometry while preserving:
   - UV maps
   - Materials
   - Textures
   - Object properties
   - Hierarchy and parenting

## Requirements

- Blender (command-line accessible)
- Python (included with Blender)
