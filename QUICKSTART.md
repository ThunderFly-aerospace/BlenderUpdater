# BlenderUpdater Quick Start Guide

Get started with BlenderUpdater in 5 minutes!

## Choose Your Path

### 🎨 I want a graphical interface → [Use the Addon](#using-the-addon)
### ⌨️ I want command-line automation → [Use the CLI](#using-the-cli)

---

## Using the Addon

### 1. Install the Addon

In Blender:
1. Go to `Edit` > `Preferences` > `Add-ons`
2. Click `Install...`
3. Navigate to and select the `blender_addon` folder from this repository
4. Enable "Import-Export: BlenderUpdater"

### 2. Create a Configuration File

Create a file named `config.json` in your project:

```json
{
  "parts": [
    {
      "name": "./parts/my_part.stl"
    }
  ],
  "paths": [
    "./parts/*.stl"
  ]
}
```

### 3. Use the Addon

1. Open your Blender project
2. Press `N` to show the sidebar
3. Click the `BlenderUpdater` tab
4. Click `Select Config File` and choose your `config.json`
5. Click `Update Meshes` 🎉

---

## Using the CLI

### 1. Install the Package

```bash
# Find Blender's Python (see INSTALL.md for your platform)
BLENDER_PYTHON=/path/to/blender/python

# Install from source
cd BlenderUpdater
$BLENDER_PYTHON -m pip install .

# OR install from GitHub
$BLENDER_PYTHON -m pip install git+https://github.com/ThunderFly-aerospace/BlenderUpdater.git
```

### 2. Create a Configuration File

Create `config.json` in your project (same format as above).

### 3. Run from Command Line

```bash
# Method 1: Using blender
blender your_file.blend --python -m blender_updater -- --config config.json

# Method 2: Using blender-updater command (if added to PATH)
blender your_file.blend --python -m blender_updater.cli -- --config config.json
```

---

## Configuration Format

The configuration file (`config.json`) supports two ways to specify meshes:

### Individual Parts

```json
{
  "parts": [
    {
      "name": "./path/to/part1.stl"
    },
    {
      "name": "./path/to/part2.glb"
    }
  ]
}
```

### Path Patterns (Wildcards)

```json
{
  "paths": [
    "./parts/*.stl",
    "./models/*.glb",
    "./components/**/*.gltf"
  ]
}
```

### Combined

```json
{
  "parts": [
    {
      "name": "./special/part.stl"
    }
  ],
  "paths": [
    "./regular_parts/*.stl"
  ]
}
```

---

## Supported File Formats

- **STL** - Automatically scaled by 0.001
- **GLB** - Blender binary GLTF
- **GLTF** - Blender text GLTF

---

## What Gets Preserved?

When updating meshes, BlenderUpdater preserves:

- ✅ UV maps
- ✅ Materials
- ✅ Textures
- ✅ Object properties
- ✅ Object hierarchy
- ✅ Parent-child relationships
- ✅ Transformations (location, rotation, scale)

Only the mesh geometry is updated!

---

## Troubleshooting

### "Object not found" error
- Make sure the object name in Blender matches the filename (without path)
- Example: `part.stl` should have an object named `part.stl` in your scene

### "Nothing imported" error
- Check that the file path in config.json is correct
- Use paths relative to your Blender file or absolute paths

### Addon doesn't appear
- Make sure you enabled it in Preferences > Add-ons
- Search for "BlenderUpdater" in the add-ons list
- Check Window > Toggle System Console for errors

### Module not found error (CLI)
- Verify installation: `/path/to/blender/python -m pip list | grep blender-updater`
- Make sure you're using Blender's Python, not system Python

---

## Next Steps

- 📖 Read [INSTALL.md](INSTALL.md) for detailed installation instructions
- 📚 See [README.md](README.md) for complete documentation
- 🔧 Check [CHANGELOG.md](CHANGELOG.md) for version history
- 🐛 Report issues on [GitHub](https://github.com/ThunderFly-aerospace/BlenderUpdater/issues)

---

## Example Workflow

### 1. Initial Setup

```bash
# Your project structure
my_blender_project/
├── project.blend
├── config.json
└── parts/
    ├── part1.stl
    └── part2.stl
```

### 2. Create config.json

```json
{
  "paths": ["./parts/*.stl"]
}
```

### 3. Update Meshes

**Via UI**: Open Blender → N panel → BlenderUpdater → Select config.json → Update Meshes

**Via CLI**: `blender project.blend --python -m blender_updater -- --config config.json`

### 4. Keep Working

- Update your STL files externally (CAD, 3D software, etc.)
- Run BlenderUpdater again to refresh the meshes in Blender
- All your materials, textures, and properties remain intact! 🎉

---

## Tips & Tricks

💡 **Tip 1**: Use path patterns (`*.stl`) to automatically update all parts in a folder

💡 **Tip 2**: Keep your CAD files organized in a separate `parts/` folder

💡 **Tip 3**: Use version control (git) for your config.json, not for .blend files

💡 **Tip 4**: Use the UI for interactive work, CLI for automation

💡 **Tip 5**: Both UI and CLI can coexist - use what fits your workflow!

---

Happy Blending! 🚀
