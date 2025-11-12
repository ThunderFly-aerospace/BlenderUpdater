# BlenderUpdater

A Python package for updating mesh models in Blender projects while preserving their properties (textures, colors, materials, etc.).

## Features

- Updates mesh geometry while preserving UV maps, materials, and other properties
- Supports multiple file formats: STL, GLB, GLTF
- Configuration-based batch updating
- Preserves object hierarchy and transformations
- Pip-installable package for easy reuse across projects

## Installation

### Install from local source

```bash
# Navigate to the repository
cd BlenderUpdater

# Install using Blender's pip
/path/to/blender/python/bin/python -m pip install .
```

### Install from GitHub

```bash
# Install directly from GitHub using Blender's pip
/path/to/blender/python/bin/python -m pip install git+https://github.com/ThunderFly-aerospace/BlenderUpdater.git
```

**Note**: The exact path to Blender's Python varies by platform:
- **Linux**: `/usr/share/blender/3.x/python/bin/python3.x`
- **macOS**: `/Applications/Blender.app/Contents/Resources/3.x/python/bin/python3.x`
- **Windows**: `C:\Program Files\Blender Foundation\Blender 3.x\3.x\python\bin\python.exe`

## Usage

### As a Python Module (Recommended)

Once installed, you can use BlenderUpdater from any Blender project:

```bash
blender your_file.blend --python -m blender_updater -- --config config.json
```

Or using Blender's Python directly:

```bash
/path/to/blender/python/bin/python -m blender_updater.cli --config config.json
```

### Using the Legacy Script (Backward Compatibility)

For backward compatibility, the original script is still available in the `scripts/` directory:

```bash
blender your_file.blend --python scripts/do_complete_assembly.py -- --config scripts/config.json
```

### In Your Python Code

You can also use BlenderUpdater programmatically within Blender:

```python
from blender_updater import BlenderUpdater

# Create updater with config file
updater = BlenderUpdater("config.json")

# Update all meshes
updater.update_all()

# Optionally save the file
updater.save_blend_file("output.blend")
```

## Configuration

Create a `config.json` file in your project directory to specify which meshes to update:

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

### Configuration Options

- `parts`: Array of individual part definitions
  - `name`: Path to the mesh file to import
- `paths`: Array of glob patterns for batch importing
  - Supports wildcards like `*.stl` to match multiple files

## Supported File Formats

- **STL** (imported with 0.001 scale)
- **GLB**
- **GLTF**

## How It Works

The package:
1. Imports new mesh geometry from specified files
2. Matches them with existing objects in the Blender scene by name
3. Replaces only the geometry while preserving:
   - UV maps
   - Materials
   - Textures
   - Object properties
   - Hierarchy and parenting

## Project Structure

After installation, your Blender project only needs:
- `config.json` - Configuration file specifying which meshes to update
- Your `.blend` file
- The mesh files referenced in the configuration

The BlenderUpdater logic is installed in Blender's Python environment and can be reused across multiple projects.

## Requirements

- Blender 2.8+ (with Python 3.7+)
- Python packages are managed by Blender's bundled Python

## Development

To contribute or modify the package:

```bash
# Clone the repository
git clone https://github.com/ThunderFly-aerospace/BlenderUpdater.git
cd BlenderUpdater

# Install in development mode
/path/to/blender/python/bin/python -m pip install -e .
```

## License

MIT License - see LICENSE file for details
