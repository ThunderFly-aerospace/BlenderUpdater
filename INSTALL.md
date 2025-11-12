# Installation Guide for BlenderUpdater

This guide covers installation for both the UI addon and the CLI package.

## Choose Your Installation Method

### For Interactive Use → Install the Blender Addon

Best for designers and artists who want to use a graphical interface.

### For Automation → Install the Python Package

Best for CI/CD pipelines, scripts, and automated workflows.

---

## Installing the Blender Addon (UI)

### Method 1: Download Pre-built ZIP (Easiest)

1. **Download the addon**:
   - Go to the [Releases page](https://github.com/ThunderFly-aerospace/BlenderUpdater/releases)
   - Download `blender_updater_addon-*.zip`

2. **Install in Blender**:
   - Open Blender
   - Go to `Edit` > `Preferences` > `Add-ons`
   - Click the `Install...` button
   - Select the downloaded zip file
   - Click `Install Add-on`

3. **Enable the addon**:
   - In the Add-ons preferences, search for "BlenderUpdater"
   - Check the box next to "Import-Export: BlenderUpdater"

### Method 2: From Source

1. **Download the addon**:
   - Clone this repository or download it as a ZIP
   - Locate the `blender_addon` folder

2. **Install in Blender**:
   - Open Blender
   - Go to `Edit` > `Preferences` > `Add-ons`
   - Click the `Install...` button
   - Navigate to the `blender_addon` folder
   - Select it (or zip it first and select the zip file)
   - Click `Install Add-on`

3. **Enable the addon**:
   - In the Add-ons preferences, search for "BlenderUpdater"
   - Check the box next to "Import-Export: BlenderUpdater"

4. **Access the addon**:
   - Open the 3D View
   - Press `N` to show the sidebar
   - Click on the `BlenderUpdater` tab

### Method 2: Manual Installation

1. **Locate Blender's addons directory**:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\{version}\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/{version}/scripts/addons/`
   - **Linux**: `~/.config/blender/{version}/scripts/addons/`

2. **Copy the addon**:
   - Copy the entire `blender_addon` folder to the addons directory
   - The folder structure should be: `.../addons/blender_addon/__init__.py`

3. **Enable in Blender**:
   - Open Blender
   - Go to `Edit` > `Preferences` > `Add-ons`
   - Search for "BlenderUpdater" and enable it

---

## Installing the Python Package (CLI)

### Prerequisites

You need to find your Blender's Python executable. Common locations:

- **Linux**: 
  - `/usr/share/blender/3.x/python/bin/python3.x`
  - Or run: `which blender` then look in that directory
  
- **macOS**: 
  - `/Applications/Blender.app/Contents/Resources/3.x/python/bin/python3.x`
  
- **Windows**: 
  - `C:\Program Files\Blender Foundation\Blender 3.x\3.x\python\bin\python.exe`

### Method 1: Install from Local Source

```bash
# Clone the repository
git clone https://github.com/ThunderFly-aerospace/BlenderUpdater.git
cd BlenderUpdater

# Install using Blender's Python
/path/to/blender/python -m pip install .

# Or install in development mode for easier updates
/path/to/blender/python -m pip install -e .
```

### Method 2: Install from GitHub

```bash
# Install directly from GitHub
/path/to/blender/python -m pip install git+https://github.com/ThunderFly-aerospace/BlenderUpdater.git
```

### Method 3: Install from Source Distribution

```bash
# If you have the .tar.gz file
/path/to/blender/python -m pip install blender-updater-1.0.0.tar.gz
```

### Verify Installation

```bash
# Check if the package is installed
/path/to/blender/python -m pip list | grep blender-updater

# Test the CLI
/path/to/blender/python -m blender_updater.cli --help
```

---

## Using Both Methods Together

You can install both the addon and the package:

- **Use the addon** for interactive design work
- **Use the CLI** for automated builds and scripts

They use the same core logic and configuration format, so you can switch between them seamlessly.

---

## Upgrading

### Upgrade the Addon

1. Uninstall the old version in Blender Preferences > Add-ons
2. Download the new version
3. Follow the installation steps again

### Upgrade the Package

```bash
# Upgrade to the latest version
/path/to/blender/python -m pip install --upgrade blender-updater

# Or if installed from Git
/path/to/blender/python -m pip install --upgrade git+https://github.com/ThunderFly-aerospace/BlenderUpdater.git
```

---

## Uninstallation

### Uninstall the Addon

1. Open Blender
2. Go to `Edit` > `Preferences` > `Add-ons`
3. Search for "BlenderUpdater"
4. Expand the addon and click `Remove`

Or manually delete the `blender_addon` folder from Blender's addons directory.

### Uninstall the Package

```bash
/path/to/blender/python -m pip uninstall blender-updater
```

---

## Troubleshooting

### "Module not found" error

- Make sure you're using Blender's Python, not your system Python
- Verify the installation: `/path/to/blender/python -m pip list | grep blender-updater`

### Addon doesn't appear in Blender

- Check that you enabled it in Preferences > Add-ons
- Look for errors in Blender's console (Window > Toggle System Console on Windows)
- Verify the folder structure is correct

### Permission errors during installation

- On Linux/macOS, you might need to run with appropriate permissions
- Or install to user directory: `--user` flag with pip

### Import errors when using the package

- The package requires `bpy` (Blender Python API), which is only available when running inside Blender
- Make sure you're running scripts through Blender's Python interpreter

---

## Need Help?

- Check the [README.md](README.md) for usage examples
- Visit the [GitHub Issues](https://github.com/ThunderFly-aerospace/BlenderUpdater/issues) page
- See [blender_addon/README.md](blender_addon/README.md) for addon-specific help
