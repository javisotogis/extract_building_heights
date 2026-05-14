# LiDARHeightExtractor v2.0.0 - Deployment Guide

## Project Summary

**LiDARHeightExtractor v2.0.0** is a production-ready QGIS plugin for extracting building/tree heights from LiDAR point clouds. This version is **fully compatible with Qt6** and QGIS 3.38+.

---

## What's New in v2.0.0

### Major Updates
- ✨ **Qt6 Compatibility**: Works seamlessly with QGIS Qt6 implementations
- 📈 **QGIS 3.38+ Minimum**: Ensures stable Qt6 support
- 🔍 **Enhanced Logging**: v2.0.0 identifiers in all logs for clarity
- ⚡ **Modernized API**: Uses `exec()` instead of deprecated `exec_()`
- 📝 **Improved Documentation**: Comprehensive Qt6 compatibility guide

### Backward Compatibility
- ✅ **Output identical to v1.0.2**: All generated data is compatible
- ✅ **Parameter structure unchanged**: Existing workflows migrate seamlessly
- ✅ **Side-by-side installation**: v1.0.2 and v2.0.0 can coexist

---

## Directory Structure

```
lidar_height_extractor_v2_0_0/
├── __init__.py                          # Plugin initialization
├── metadata.txt                         # QGIS plugin metadata
├── lidar_height_extractor_plugin.py     # Main plugin class (Qt6 updated)
├── provider.py                          # QGIS processing provider
├── requirements.txt                     # External dependencies
├── LICENSE                              # GPL 3.0 license
├── README.md                            # Main documentation
├── QT6_COMPATIBILITY.md                 # Qt6 compatibility details
│
├── algorithms/
│   └── extract_building_height.py       # Core algorithm (Qt6 ready)
│
├── ui/
│   └── extract_building_height_dialog.py # Dialog handler (Qt6 ready)
│
├── forms/
│   └── extract_building_height_dialog_base.ui # Qt Designer UI file
│
└── docs/
    ├── README.md                        # Documentation overview
    ├── INSTALL.md                       # Installation guide (Qt6 section)
    └── USAGE.md                         # Detailed usage guide
```

---

## Installation for End Users

### Quick Install (Windows)

1. Download: `lidar_height_extractor_v2_0_0.zip`
2. Extract to: `C:\Users\<YourUsername>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
3. Restart QGIS
4. Enable in: **Plugins → Manage and Install Plugins** → Search "LiDARHeightExtractor"

### Quick Install (Linux)

```bash
unzip lidar_height_extractor_v2_0_0.zip -d ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
```

For detailed instructions, see [docs/INSTALL.md](docs/INSTALL.md).

---

## Qt6 Compatibility Summary

### Key Technical Changes

| Component | v1.0.2 | v2.0.0 | Qt6 Safe |
|-----------|--------|--------|----------|
| Dialog execution | `exec_()` | `exec()` | ✅ Yes |
| Qt imports | `qgis.PyQt` | `qgis.PyQt` | ✅ Yes |
| Provider ID | `lidar_height_extractor_v1` | `lidar_height_extractor_v2` | ✅ Yes |
| Icon reference | `v1_0_0` | `v2_0_0` | ✅ Yes |
| Python version | 3.10+ | 3.12+ | ✅ Yes |
| QGIS minimum | 3.34 | 3.38 | ✅ Yes |

### What This Means

- **No breaking changes** for users—output remains identical
- **Seamless Qt6 support** through QGIS PyQt abstraction layer
- **Modern API usage** follows QGIS best practices
- **Ready for future QGIS versions**

For detailed technical information, see [QT6_COMPATIBILITY.md](QT6_COMPATIBILITY.md).

---

## Feature Overview

### Core Capabilities

1. **DEM Generation**: Creates Digital Elevation Model from point clouds
2. **DTM Generation**: Creates Digital Terrain Model with ground filtering
3. **nDSM Computation**: Calculates Normalized Digital Surface Model (DEM - DTM)
4. **Zonal Statistics**: Extracts maximum height per polygon
5. **Custom Filtering**: PDAL expressions for flexible data processing
6. **CRS Support**: Optional reprojection to target coordinate system
7. **Automatic Loading**: Results load directly into QGIS
8. **Detailed Logging**: Full processing logs for debugging

### Use Cases

- 🏢 **Building Height**: Extract rooftop heights for solar/urban analysis
- 🌳 **Tree Heights**: Compute canopy heights for forestry/urban canopy
- 🌊 **Flood Risk**: Analyze elevation for flood modeling
- 📊 **Urban Planning**: Height analysis for density, zoning, visibility

---

## System Requirements

### Required

- **QGIS**: 3.38 or later (with Qt6 support)
- **Python**: 3.12+ (bundled with QGIS)
- **PDAL**: Point Data Abstraction Library (external dependency)

### Included

- **NumPy**: Numerical computing (typically available in QGIS)
- **GDAL**: Raster processing (typically available in QGIS)

### Installation Notes

- **Windows**: Use OSGeo4W or QGIS standalone; PDAL often bundled
- **Linux**: Install PDAL via package manager (`apt install pdal`)
- **macOS**: Install PDAL via Homebrew (`brew install pdal`)

---

## Testing Checklist

### Pre-Deployment Tests

- [ ] Plugin loads without errors in QGIS 3.38+
- [ ] Dialog opens correctly with modern `exec()` method
- [ ] Processing algorithm appears in Processing Toolbox
- [ ] Test run on sample data completes successfully
- [ ] Output layer loads into QGIS with `lidar_height` field
- [ ] Log file contains v2.0.0 identifiers

### Compatibility Tests

- [ ] Provider ID shows as `lidar_height_extractor_v2`
- [ ] Icon displays correctly (if included)
- [ ] No Qt6 import errors in Python console
- [ ] Version string shows "LiDARHeightExtractor — v2.0.0"

---

## User Migration from v1.0.2

### For Existing Users

1. **Backup** (optional): Rename old version to `lidar_height_extractor_v1_0_2.bak`
2. **Install**: Extract v2.0.0 to plugins folder
3. **Restart**: Reopen QGIS
4. **Test**: Run on sample data
5. **Verify**: Output layer loads successfully

### Compatibility

- ✅ All v1.0.2 output data works with v2.0.0
- ✅ Both versions can coexist without conflicts
- ✅ Parameter formats unchanged
- ✅ Output format identical

---

## Development & Customization

### Plugin Structure

```
Main Entry Point:
├── __init__.py (classFactory) → LiDARHeightExtractorPlugin

Plugin Class:
├── initGui() → Register provider and UI
├── unload() → Clean up resources
└── open_dialog() → Launch dialog (Qt6: exec())

Processing Provider:
├── provider.py → LidarProvider
└── algorithms/extract_building_height.py → Algorithm

UI Components:
├── forms/extract_building_height_dialog_base.ui → Designer file
└── ui/extract_building_height_dialog.py → Dialog handler
```

### Qt6 Code Pattern (Reference)

```python
# ✅ Correct Qt6-safe pattern used in v2.0.0
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QDialog

# Dialog execution (Qt6 compliant)
dlg = ExtractBuildingHeightDialog(self.iface)
dlg.exec()  # Modern method, works in Qt5 & Qt6
```

---

## Deployment Checklist

### Before Release

- [ ] All files created in v2.0.0 directory
- [ ] Metadata version updated to 2.0.0
- [ ] All references to v1 updated to v2
- [ ] Documentation complete and reviewed
- [ ] Qt6 compatibility verified
- [ ] Testing completed
- [ ] License included
- [ ] Requirements documented

### Release Steps

1. **Package**: Create `lidar_height_extractor_v2_0_0.zip`
2. **Test**: Extract and test in clean QGIS 3.38+ installation
3. **Document**: Include README, INSTALL.md, USAGE.md
4. **Release**: Upload to GitHub releases
5. **Announce**: Notify users about new Qt6-compatible version

### Post-Release

- [ ] Monitor GitHub issues for bug reports
- [ ] Provide user support for installation/usage
- [ ] Plan next feature updates
- [ ] Track QGIS version compatibility

---

## Documentation Files

### For Users
- [README.md](README.md) – Plugin overview and features
- [docs/INSTALL.md](docs/INSTALL.md) – Installation instructions
- [docs/USAGE.md](docs/USAGE.md) – Complete usage guide
- [docs/README.md](docs/README.md) – Documentation index

### For Developers
- [QT6_COMPATIBILITY.md](QT6_COMPATIBILITY.md) – Technical Qt6 changes
- Python source code with comments

---

## Support & Resources

### User Support
- **GitHub Issues**: [Report bugs](https://github.com/javisotogis/extract_building_heights/issues)
- **QGIS Documentation**: [QGIS User Manual](https://docs.qgis.org/)
- **PDAL Documentation**: [PDAL Docs](https://pdal.io/)

### Developer Resources
- **QGIS PyQGIS API**: [PyQGIS Reference](https://qgis.org/pyqgis/latest/)
- **Qt6 Documentation**: [Qt6 Docs](https://doc.qt.io/qt-6/)
- **QGIS Plugin Guide**: [Plugin Development](https://docs.qgis.org/latest/en/docs/pyqgis_developer_guide/)

---

## FAQ

**Q: Can I use v2.0.0 with QGIS 3.34?**  
A: Not officially. v2.0.0 requires QGIS 3.38+ for Qt6 support. Use v1.0.2 for QGIS 3.34-3.36.

**Q: Are v1.0.2 and v2.0.0 outputs compatible?**  
A: Yes! Outputs are identical. Both versions can be used interchangeably.

**Q: Do I need to reinstall PDAL?**  
A: No. PDAL installation is unchanged from v1.0.2.

**Q: Is there a GUI for the dialog?**  
A: A minimal Qt dialog is included. The primary interface is the Processing Toolbox.

**Q: Can both v1.0.2 and v2.0.0 run simultaneously?**  
A: Yes, they use different provider IDs and won't conflict.

---

## Contact

**Plugin Repository**: [extract_building_heights](https://github.com/javisotogis/extract_building_heights)  
**Issue Tracker**: [GitHub Issues](https://github.com/javisotogis/extract_building_heights/issues)  
**License**: GNU General Public License v3.0+

---

## Version History

**v2.0.0** (2025-05-14)
- Qt6 compatibility
- QGIS 3.38+ minimum
- Enhanced logging
- Modernized API usage

**v1.0.2** (2025-11-13)
- Fixed layer loading

**v1.0.1** (2025-11-12)
- Added custom DEM filter

**v1.0.0** (2025-11-11)
- Initial release

---

**Document Date**: May 14, 2025  
**Plugin Version**: 2.0.0  
**Qt Support**: Qt5 (3.34-3.36) and Qt6 (3.38+)  
**Status**: Ready for deployment
