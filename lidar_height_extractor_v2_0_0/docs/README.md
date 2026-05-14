# LiDARHeightExtractor v2.0.0 Documentation

Welcome to the LiDARHeightExtractor documentation! This directory contains comprehensive guides to help you install, configure, and use the plugin effectively.

---

## Documentation Structure

### 📖 [README.md](README.md) — Start Here
Overview of the plugin, key features, requirements, and quick start information. If you're new to LiDARHeightExtractor, start here!

### 🛠️ [INSTALL.md](INSTALL.md) — Installation Guide
Step-by-step installation instructions for:
- **Windows** (OSGeo4W / QGIS Standalone)
- **Linux** (Ubuntu, Debian, etc.)
- **macOS**
- **Qt6 Compatibility Notes**
- Troubleshooting common installation issues

### 📚 [USAGE.md](USAGE.md) — Usage Guide
Comprehensive guide covering:
- Basic workflow
- Parameter configuration and explanation
- Practical examples (buildings, trees, flood analysis)
- Performance tuning and best practices
- Troubleshooting and logging
- FAQs

---

## Quick Links

| Task | Document | Section |
|------|----------|---------|
| Install plugin | [INSTALL.md](INSTALL.md) | Windows / Linux / macOS |
| Get started | [USAGE.md](USAGE.md) | Basic Workflow |
| Configure parameters | [USAGE.md](USAGE.md) | Parameter Guide |
| Example workflows | [USAGE.md](USAGE.md) | Example Workflows |
| Troubleshoot problems | [INSTALL.md](INSTALL.md) or [USAGE.md](USAGE.md) | Troubleshooting sections |
| Learn about Qt6 | [INSTALL.md](INSTALL.md) | Qt6 Compatibility |

---

## What is LiDARHeightExtractor?

**LiDARHeightExtractor** is a QGIS plugin that:

1. **Computes nDSM** (Normalized Digital Surface Model) from LiDAR point cloud data
2. **Extracts maximum heights** for each polygon feature (buildings, trees, parcels, etc.)
3. **Provides precise height analysis** for urban planning, forestry, solar analysis, and more

### Key Capabilities

✅ **nDSM Computation** from point clouds  
✅ **Custom filtering** for DEM and ground classification  
✅ **Zonal statistics** (max height per polygon)  
✅ **Qt6 Compatible** (QGIS 3.38+)  
✅ **Robust logging** and error reporting  
✅ **Multiple CRS support** including optional reprojection  

---

## System Requirements

- **QGIS**: 3.38 or later (Qt6 compatible)
- **Python**: 3.12+ (included with QGIS)
- **PDAL**: Point Data Abstraction Library (required external dependency)
- **Dependencies**: NumPy, GDAL (typically available in QGIS)

---

## Installation Overview

### Quick Install (Windows)

1. Download `lidar_height_extractor_v2_0_0.zip`
2. Extract to: `C:\Users\<YourUsername>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
3. Restart QGIS
4. Enable in **Plugins → Manage and Install Plugins**

For detailed instructions, see [INSTALL.md](INSTALL.md).

---

## Basic Workflow

```
1. Prepare polygon layer (buildings, trees, etc.)
2. Provide LiDAR point cloud file (LAZ/LAS)
3. Configure parameters (resolution, filters, etc.)
4. Run algorithm in Processing Toolbox
5. View results with height values per polygon
```

For step-by-step guide, see [USAGE.md](USAGE.md).

---

## Common Use Cases

### 🏢 Building Height Estimation
Extract rooftop heights for:
- Solar potential analysis
- Urban planning
- Telecommunications planning

### 🌳 Tree Canopy Analysis
Compute tree heights for:
- Forest inventory
- Urban canopy assessment
- Tree risk management

### 🌊 Flood & Elevation Analysis
Analyze heights for:
- Flood risk assessment
- Shadow modeling
- Urban density analysis

---

## Version Information

**Current Version**: 2.0.1  
**Release Date**: May 14, 2025  
**Qt Version Support**: Qt5 (via abstraction) and Qt6 (primary)

### What's New in v2.0.1

- ✨ Optional polygon buffer parameter (default 0m)
- 🔧 Support for geometry error fixing via expansion/contraction
- 📊 Enhanced robustness for problematic polygon datasets

### Previous: What's New in v2.0.0

- ✨ Full Qt6 compatibility
- 📈 Minimum QGIS 3.38 for stable Qt6 support
- 🔍 Enhanced logging with version identifiers
- ⚡ Modernized API usage (`exec()` instead of `exec_()`)
- 📝 Improved error messages and handling

For details, see the main [README.md](../README.md#whats-new-in-v200).

---

## Getting Help

### Documentation
- 📖 [Installation Guide](INSTALL.md)
- 📚 [Usage Guide](USAGE.md)
- 📄 [Main README](../README.md)

### Support Channels
- **GitHub Issues**: [Report bugs or ask questions](https://github.com/javisotogis/extract_building_heights/issues)
- **Python Console**: Check **Plugins → Python Console** for error details
- **Log Files**: Processing logs saved to temp folder for debugging

### Common Issues

| Issue | Solution |
|-------|----------|
| Plugin not showing | See [INSTALL.md → Troubleshooting](INSTALL.md#troubleshooting-installation) |
| PDAL not found | See [INSTALL.md → PDAL Errors](INSTALL.md#pdal-algorithm-not-found-error) |
| All heights are 0 | See [USAGE.md → Troubleshooting](USAGE.md#practical-tips--best-practices) |
| Memory errors | See [USAGE.md → Performance Optimization](USAGE.md#5-performance-optimization) |

---

## Citation

If you use LiDARHeightExtractor in your research or projects, please cite:

```
LiDARHeightExtractor (2025). QGIS Plugin for nDSM computation and polygon height extraction.
Version 2.0.0 (Qt6 compatible).
https://github.com/javisotogis/extract_building_heights
```

---

## License

LiDARHeightExtractor is released under the **GNU General Public License v3.0 or later** (GPLv3+).

See [LICENSE](../LICENSE) for full details.

---

## Support the Project

If you find LiDARHeightExtractor helpful:
- ⭐ Star the [GitHub repository](https://github.com/javisotogis/extract_building_heights)
- 🐛 Report bugs on [GitHub Issues](https://github.com/javisotogis/extract_building_heights/issues)
- 💡 Suggest improvements
- 📢 Share your work and use cases!

---

## Navigation

- **← Back**: [Main README](../README.md)
- **→ Install**: [INSTALL.md](INSTALL.md)
- **→ Usage**: [USAGE.md](USAGE.md)

---

**Last Updated**: May 14, 2025  
**Maintained by**: Your Name  
**Repository**: [extract_building_heights](https://github.com/javisotogis/extract_building_heights)
