# Changelog

All notable changes to BlenderUpdater will be documented in this file.

## [1.0.0] - 2024-11-12

### Added

- **Python Package Structure**: Transformed into a pip-installable package
  - `blender_updater` module with modular architecture
  - Separate modules for mesh operations, updater logic, and CLI
  - Installation via pip from source or GitHub
  - Entry point for command-line usage: `blender-updater`

- **Blender Addon with UI**: New graphical interface for interactive use
  - Panel in 3D View sidebar (press N > BlenderUpdater tab)
  - File browser to select configuration files
  - Update button with visual feedback
  - Self-contained addon in `blender_addon/` folder
  - All mesh updating logic embedded (no external dependencies)

- **Multiple Usage Modes**:
  - **UI Addon**: For interactive design work in Blender
  - **CLI Package**: For automation, scripts, and CI/CD pipelines
  - **Legacy Script**: Backward compatibility with original script

- **Comprehensive Documentation**:
  - `INSTALL.md`: Detailed installation guide with platform-specific instructions
  - `blender_addon/README.md`: Addon-specific documentation
  - Updated main README with quick start guides
  - Example configuration files
  - Troubleshooting guides

- **Configuration Files**:
  - `config.json`: Example configuration in root
  - `config.example.json`: Template for new projects
  - Same format works across all usage modes

### Changed

- **Modular Architecture**: Separated monolithic script into focused modules
  - `mesh_operations.py`: Mesh import and geometry copying functions
  - `updater.py`: Main updater class and orchestration
  - `cli.py`: Command-line interface
  - `addon.py`: Blender addon UI components

- **Updated Legacy Script**: `scripts/do_complete_assembly.py`
  - Now tries to use installed package first
  - Falls back to inline implementation if package not installed
  - Maintains backward compatibility

- **Updated Shell Script**: `update_blend_file.sh`
  - Shows how to use installed package
  - Includes comment with legacy script usage

- **Updated `.gitignore`**: Added build artifacts and distribution files

### Features Preserved

- Updates mesh geometry while preserving:
  - UV maps
  - Materials and textures
  - Object properties
  - Hierarchy and parenting
  
- Supports multiple file formats:
  - STL (with 0.001 scale)
  - GLB
  - GLTF

- Configuration-based batch updating with:
  - Individual part paths
  - Glob patterns for multiple files

### Technical Details

- Minimum Blender version: 2.80
- Python version: 3.7+
- Package name: `blender-updater`
- Module name: `blender_updater`
- Addon category: Import-Export

### Security

- CodeQL security scan: ✅ No vulnerabilities found
- Safe file operations with proper error handling
- No external network dependencies

### Distribution

- Available installation methods:
  - From source: `pip install .`
  - From GitHub: `pip install git+https://github.com/...`
  - As Blender addon: Install through Blender UI
  - Legacy script: Direct execution (backward compatible)

## [Previous Versions]

Previous versions were single-script implementations without package structure.
