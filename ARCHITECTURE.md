# BlenderUpdater Architecture

This document describes the architecture and design decisions of BlenderUpdater v1.0.

## Overview

BlenderUpdater has been refactored from a monolithic script into a modular, reusable Python package with multiple interfaces (UI and CLI).

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     BlenderUpdater v1.0                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐         ┌──────────────────┐        │
│  │   UI Interface   │         │  CLI Interface   │        │
│  │  (Blender Addon) │         │  (Python Module) │        │
│  └────────┬─────────┘         └────────┬─────────┘        │
│           │                            │                   │
│           │         ┌──────────────────┴───────┐          │
│           │         │                          │          │
│           └────────▶│    BlenderUpdater       │◀─────────┘
│                     │    (Core Package)       │           │
│                     └───────────┬─────────────┘           │
│                                 │                          │
│                     ┌───────────┴─────────────┐           │
│                     │                         │           │
│           ┌─────────▼─────────┐    ┌─────────▼────────┐  │
│           │ Mesh Operations   │    │     Updater      │  │
│           │  - import_and_    │    │  - Config load   │  │
│           │    rename()       │    │  - Orchestration │  │
│           │  - copy_geometry()│    │  - Batch process │  │
│           └───────────────────┘    └──────────────────┘  │
│                                                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Blender API  │
                    │     (bpy)     │
                    └───────────────┘
```

## Component Breakdown

### 1. Core Package (`blender_updater/`)

The main Python package that can be installed via pip.

#### 1.1 `updater.py`
- **Purpose**: Main orchestration logic
- **Key Class**: `BlenderUpdater`
- **Responsibilities**:
  - Load and parse configuration files
  - Coordinate mesh update operations
  - Batch processing of multiple parts
  - Handle path patterns and globbing

#### 1.2 `mesh_operations.py`
- **Purpose**: Low-level mesh manipulation
- **Key Functions**:
  - `import_and_rename()`: Import mesh and update existing object
  - `copy_geometry()`: Copy mesh while preserving UV layers
  - `which_file_format()`: Determine file format from extension
- **Responsibilities**:
  - File import (STL, GLB, GLTF)
  - Geometry copying
  - UV map preservation
  - Transform application

#### 1.3 `cli.py`
- **Purpose**: Command-line interface
- **Key Function**: `main()`
- **Responsibilities**:
  - Parse command-line arguments
  - Create updater instance
  - Invoke update operations
  - Handle Blender's argument passing

#### 1.4 `__init__.py`
- **Purpose**: Package initialization
- **Exports**: Main classes and functions
- **Version**: Defines package version

#### 1.5 `__main__.py`
- **Purpose**: Module execution entry point
- **Usage**: `python -m blender_updater`

#### 1.6 `addon.py`
- **Purpose**: Blender addon integration (optional)
- **Note**: Alternative to standalone addon

### 2. Blender Addon (`blender_addon/`)

Self-contained Blender addon with graphical interface.

#### 2.1 `__init__.py`
- **Purpose**: Complete addon implementation
- **Components**:
  - `BlenderUpdaterProperties`: Property storage
  - `BLENDERUPDATER_OT_select_config`: Config file picker operator
  - `BLENDERUPDATER_OT_update_meshes`: Update execution operator
  - `BLENDERUPDATER_PT_main_panel`: UI panel definition
- **Embedded Logic**: Contains all mesh operations inline (no dependencies)
- **Registration**: Proper Blender addon registration/unregistration

### 3. Legacy Script (`scripts/`)

#### 3.1 `do_complete_assembly.py`
- **Purpose**: Backward compatibility
- **Behavior**:
  1. Try to import `blender_updater` package
  2. If found, use package classes
  3. If not found, fall back to inline implementation
- **Maintains**: Original script interface and behavior

### 4. Packaging Files

#### 4.1 `setup.py`
- Classic Python packaging
- Defines package metadata
- Entry points for CLI commands

#### 4.2 `pyproject.toml`
- Modern Python packaging standard
- Build system requirements
- Project metadata

#### 4.3 `MANIFEST.in`
- Controls which files are included in distribution
- Ensures all necessary files are packaged

## Design Decisions

### Separation of Concerns

**Decision**: Split monolithic script into focused modules

**Rationale**:
- Easier testing and maintenance
- Reusable components
- Clear responsibilities
- Better code organization

### Dual Interface (UI + CLI)

**Decision**: Provide both graphical and command-line interfaces

**Rationale**:
- UI for designers and artists (point-and-click)
- CLI for automation and scripting
- Flexibility for different workflows
- Broader user base

### Self-Contained Addon

**Decision**: Make addon independent from pip package

**Rationale**:
- Easier installation for non-technical users
- No pip knowledge required
- Works in restricted environments
- Standard Blender addon installation

### Package Independence

**Decision**: Core logic in pip package, addon embeds logic

**Rationale**:
- Addon can work standalone
- Package can be used programmatically
- No circular dependencies
- Users can choose one or both

### Backward Compatibility

**Decision**: Keep legacy script and update it to use package

**Rationale**:
- Smooth migration for existing users
- No breaking changes
- Gradual adoption of new features
- Safety net for edge cases

## Data Flow

### UI Workflow

```
User clicks button in UI
         ↓
Operator execute() called
         ↓
Load config.json
         ↓
For each part/path in config:
    ├─ Import mesh file
    ├─ Find existing object
    ├─ Copy geometry to existing
    └─ Preserve UV/materials
         ↓
Show completion message
```

### CLI Workflow

```
User runs: blender file.blend --python -m blender_updater -- --config config.json
         ↓
CLI main() function called
         ↓
Parse arguments
         ↓
Create BlenderUpdater instance
         ↓
Call updater.update_all()
         ↓
For each part/path in config:
    ├─ Import mesh file
    ├─ Find existing object
    ├─ Copy geometry to existing
    └─ Preserve UV/materials
         ↓
Print completion message
```

## File Format Support

### STL
- Import: `bpy.ops.wm.stl_import()`
- Scale: 0.001 (automatic)
- Usage: Most common CAD export

### GLB/GLTF
- Import: `bpy.ops.import_scene.gltf()`
- Scale: 1.0 (no scaling)
- Usage: Full scene/animation support

## Configuration Schema

```json
{
  "parts": [              // Individual parts
    {
      "name": "path"      // Required: file path
    }
  ],
  "paths": [              // Glob patterns
    "pattern"             // String: path with wildcards
  ]
}
```

## Extension Points

The architecture allows for easy extension:

### Adding File Formats

1. Update `mesh_operations.which_file_format()`
2. Add import logic in `mesh_operations.import_and_rename()`

### Adding Configuration Options

1. Update config schema
2. Modify `BlenderUpdater.__init__()` to parse new options
3. Update documentation

### Adding UI Features

1. Add properties to `BlenderUpdaterProperties`
2. Create new operators for actions
3. Update panel `draw()` method

## Dependencies

### Runtime
- **Blender**: 2.80+ (provides `bpy` module)
- **Python**: 3.7+ (bundled with Blender)

### Development
- **setuptools**: For packaging
- **wheel**: For building distributions

### External
- None (fully self-contained)

## Testing Strategy

### Current
- Manual testing in Blender environment
- Python syntax validation
- Package build verification
- Security scanning (CodeQL)

### Future Considerations
- Unit tests with mock `bpy`
- Integration tests with test .blend files
- CI/CD pipeline tests
- Performance benchmarks

## Performance Considerations

- **File I/O**: Mesh import is I/O bound
- **Memory**: Temporary mesh objects created and cleaned up
- **Batch Processing**: Sequential (could parallelize in future)
- **UV Preservation**: Linear complexity with polygon count

## Security

- **Input Validation**: File paths checked for existence
- **No Network**: All operations local
- **No Arbitrary Code**: Only JSON config parsing
- **CodeQL Verified**: 0 vulnerabilities found

## Future Architecture Improvements

### Potential Enhancements

1. **Async Processing**
   - Non-blocking UI updates
   - Progress bars for large batches

2. **Undo Support**
   - Proper Blender undo stack integration
   - Rollback capability

3. **Logging System**
   - Structured logging
   - Debug/info/error levels
   - Log file output

4. **Plugin System**
   - Custom import handlers
   - Pre/post-processing hooks
   - Format converters

5. **Configuration Validation**
   - JSON schema validation
   - Better error messages
   - Auto-completion support

## Conclusion

The refactored architecture provides:
- ✅ Modularity and maintainability
- ✅ Multiple interfaces for different users
- ✅ Clean separation of concerns
- ✅ Extensibility for future features
- ✅ Professional packaging and distribution
- ✅ Backward compatibility

This design balances simplicity, usability, and professional software engineering practices.
