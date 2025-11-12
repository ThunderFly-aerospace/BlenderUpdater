# BlenderUpdater

A Python package for updating mesh models in Blender projects while preserving their properties (textures, colors, materials, etc.).

> 🚀 **New to BlenderUpdater?** Check out the [Quick Start Guide](QUICKSTART.md) to get up and running in 5 minutes!

> 📦 **Want to try it out?** See the [Example Project](example_project/) with sample meshes and a ready-to-use Blender file!

## Features

- Updates mesh geometry while preserving UV maps, materials, and other properties
- Supports multiple file formats: STL, GLB, GLTF
- Configuration-based batch updating
- Preserves object hierarchy and transformations
- **Two usage modes:**
  - **UI Addon**: Graphical interface within Blender for interactive use
  - **CLI Package**: Command-line tool for automation and CI/CD pipelines
- Pip-installable package for easy reuse across projects

## Use Cases

- **Interactive Design Work**: Use the Blender addon UI to quickly update meshes during design iterations
- **Automated Builds**: Use the CLI in scripts and automation workflows
- **Version Control**: Keep only configuration files in your repo, install BlenderUpdater as a dependency
- **Multiple Projects**: Install once, use across all your Blender projects

## Installation

There are two ways to use BlenderUpdater:

### Option 1: Blender Addon with UI (Recommended for most users)

Install the addon for a graphical user interface directly in Blender:

**From Release (Easiest):**
1. Download `blender_updater_addon-*.zip` from the [Releases page](https://github.com/ThunderFly-aerospace/BlenderUpdater/releases)
2. In Blender: `Edit > Preferences > Add-ons > Install`
3. Select the downloaded zip file
4. Enable "Import-Export: BlenderUpdater"

**From Source:**
1. In Blender: `Edit > Preferences > Add-ons > Install`
2. Select the `blender_addon` folder from this repository
3. Enable "Import-Export: BlenderUpdater"
4. Access from 3D View sidebar (press `N`) > BlenderUpdater tab

### Option 2: Python Package for CLI (For automation and scripts)

Install as a pip package for command-line usage:

```bash
# Install from source
/path/to/blender/python -m pip install .

# Or install from GitHub
/path/to/blender/python -m pip install git+https://github.com/ThunderFly-aerospace/BlenderUpdater.git
```

**📖 See [INSTALL.md](INSTALL.md) for detailed installation instructions, including platform-specific paths and troubleshooting.**

## Usage

### Using the Blender Addon (UI)

After installing the addon:

1. Open your Blender project
2. Press `N` to show the sidebar in 3D View
3. Go to the `BlenderUpdater` tab
4. Click `Select Config File` and choose your `config.json`
5. Click `Update Meshes`

The addon provides visual feedback and error messages directly in Blender's interface.

### Using the CLI (Command Line)

Once installed as a Python package, you can use BlenderUpdater from the command line:

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

### Programmatic Usage

You can also use BlenderUpdater programmatically within Blender scripts:

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
