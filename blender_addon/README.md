# BlenderUpdater Addon

This is the Blender addon version of BlenderUpdater that provides a graphical user interface (UI) directly within Blender.

## Installation Methods

### Method 1: Install from Blender UI (Recommended)

1. Download or copy the `blender_addon` folder
2. Open Blender
3. Go to `Edit > Preferences > Add-ons`
4. Click `Install...` button
5. Navigate to and select the `blender_addon` folder (or zip it first and select the zip)
6. Enable the addon by checking the box next to "Import-Export: BlenderUpdater"

### Method 2: Manual Installation

Copy the entire `blender_addon` folder to your Blender addons directory:

- **Windows**: `%APPDATA%\Blender Foundation\Blender\{version}\scripts\addons\`
- **macOS**: `~/Library/Application Support/Blender/{version}/scripts/addons/`
- **Linux**: `~/.config/blender/{version}/scripts/addons/`

Then enable it in Blender Preferences > Add-ons.

## Usage

After installation and enabling the addon:

1. Open your Blender project
2. Press `N` to open the sidebar in the 3D View
3. Click on the `BlenderUpdater` tab
4. Click `Select Config File` and choose your `config.json`
5. Click `Update Meshes` to update all meshes defined in the configuration

## Configuration File

The addon uses the same configuration format as the CLI version. Create a `config.json` file:

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

## Features

- **Easy UI access**: No need to use command line
- **Visual feedback**: Progress and errors shown in Blender's UI
- **File browser**: Built-in file picker for selecting configuration
- **Same functionality**: Uses the same core logic as the CLI version
- **Format support**: STL, GLB, GLTF
- **Property preservation**: Maintains UV maps, materials, textures, hierarchy

## Notes

- The addon works independently and doesn't require pip installation
- All the mesh updating logic is self-contained within the addon
- The CLI functionality remains available through the `blender_updater` package
- Both can be used in the same project

## Troubleshooting

If the addon doesn't appear after installation:
1. Make sure you enabled it in Preferences > Add-ons
2. Search for "BlenderUpdater" in the add-ons list
3. Check the Blender console for any error messages (Window > Toggle System Console on Windows)

## Compatibility

- Blender 2.80 and newer
- Python 3.7+ (included with Blender)
