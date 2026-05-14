# LiDARHeightExtractor v2.0.1

## Overview

**LiDARHeightExtractor v2.0.1** is a QGIS plugin that computes normalized Digital Surface Models (nDSM) from point cloud data and extracts the maximum height for each polygon feature. This version is fully compatible with **QGIS 3.38+ and Qt6**, with an added optional polygon buffer parameter to fix geometry errors.

The plugin leverages PDAL (Point Data Abstraction Library) for efficient point cloud rasterization and GDAL for raster arithmetic, providing a robust, production-ready workflow for LiDAR-based height analysis.

---

## What's New in v2.0.1

### Latest Updates (v2.0.1)
- **Polygon Buffer Parameter**: New optional buffer parameter (default 0m) to fix geometry errors or adjust analysis areas
- **Flexible Geometry Handling**: Support positive/negative buffer values for expansion/contraction
- **Enhanced Robustness**: Better handling of geometry errors in input polygons

### Qt6 & Core Features (v2.0.0)
- **Qt6 Compatibility**: Works seamlessly with QGIS Qt6 implementations
- **Minimum QGIS 3.38**: Ensures stable Qt6 support
- **Enhanced Logging**: Improved logging with version identifiers
- **Modernized API Usage**: Updated deprecated methods (`exec_()` → `exec()`)
- **Provider ID Update**: Changed to `lidar_height_extractor_v2`

---

## Features

- **nDSM Computation**: Computes normalized Digital Surface Model (DEM - DTM) directly from point clouds
- **Custom DEM Filter**: Use custom PDAL expressions to filter which points contribute to DEM (e.g., exclude noise)
- **Flexible Ground Filtering**: Customizable PDAL filter expressions for ground point extraction
- **Zonal Statistics**: Extracts maximum height per polygon (buildings, trees, parcels, etc.)
- **CRS Support**: Optional target coordinate reference system for output alignment
- **Robust Export**: Uses QGIS core API (QgsVectorFileWriter) for reliable vector export
- **Automatic Layer Loading**: Output layer is automatically loaded into QGIS upon completion
- **Detailed Logging**: Full logging to track processing steps and debug issues

---

## Use Cases

### Building Height Estimation
Extract rooftop heights for buildings to support:
- Solar potential analysis
- Urban heat island mitigation
- Building energy modeling
- Telecommunications infrastructure planning

### Forest and Tree Analysis
Compute canopy heights for:
- Forest inventory and biomass estimation
- Tree crown delineation
- Urban canopy assessment
- Forestry management

### Urban Planning
Analyze height variations for:
- Urban density and clustering
- Viewshed analysis
- Flood and shadow modeling
- Land use classification

---

## Requirements

### Software
- **QGIS**: 3.38 or later (fully tested with 3.38+, Qt6 compatible)
- **PDAL**: Must be available in QGIS (includes `pdal_wrench` binary)
- **Python**: 3.12+ (bundled with QGIS)

### Python Packages
The following are typically available in QGIS Python and are required:
- `numpy` – Numerical array operations
- `gdal` / `osgeo` – Raster processing
- `qgis.core` – QGIS processing framework

### External Dependencies
- **PDAL** (`pdal_wrench`) – Used by the PDAL processing algorithms for point cloud rasterization

---

## Installation

### Windows (OSGeo4W / QGIS Standalone with Qt6)

1. **Install PDAL** (if not already present):
   - If using OSGeo4W, ensure the PDAL package is installed
   - If using QGIS standalone, PDAL is typically bundled

2. **Install the Plugin**:
   - Download `lidar_height_extractor_v2_0_0.zip`
   - Close QGIS
   - Extract the zip to your QGIS plugins folder:
     ```
     C:\Users\<YourUsername>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
     ```
   - Restart QGIS
   - Enable the plugin in **Plugins → Manage and Install Plugins**

3. **Python Package Installation** (if needed):
   - Follow [this guide for Windows](https://landscapearchaeology.org/2018/installing-python-packages-in-qgis-3-for-windows/)

### Linux / macOS (Qt6 Compatible)
- Install PDAL via package manager (e.g., `apt install pdal`, `brew install pdal`)
- Extract plugin to `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
- Restart QGIS

### Qt6 Deployment Note
The v2.0.0 plugin uses the abstraction layer `qgis.PyQt` which automatically handles both Qt5 and Qt6 implementations. No additional configuration is needed for Qt6 environments.

---

## Usage

### Basic Workflow

1. **Open QGIS** (3.38+) and load your data:
   - Point cloud (LAZ, LAS, or other PDAL-supported formats)
   - Polygon layer (buildings, trees, parcels, etc.)

2. **Access the Plugin**:
   - Go to **Processing → Toolbox**
   - Search for "LiDARHeightExtractor" or navigate to **LiDAR → LiDARHeightExtractor + Zonal Stats**

3. **Configure Parameters**:
   - **Polygon Layer**: Select the layer containing polygons (e.g., building footprints)
   - **Polygon Buffer Distance** (m): Optional buffer to fix geometry errors (default: 0 m, no buffer). Specify a distance > 0 to expand or shrink polygons
   - **Point Cloud**: Provide the path to your point cloud file (LAZ/LAS)
   - **DEM Filter** (optional): Custom PDAL expression for DEM filtering (e.g., `"Classification != 7"` to exclude noise)
   - **Ground Filter**: Leave as default (`Classification = 2`) or customize for your data
   - **Raster Resolution**: Cell size in map units (e.g., 1 m)
   - **Tile Size**: Processing tile size in pixels (default: 1000)
   - **Target CRS** (optional): Specify output coordinate system
   - **Output Polygons**: Path to save the result (GeoPackage format recommended)

4. **Run the Algorithm**:
   - Click **Run**
   - Monitor progress in the QGIS console
   - Output layer loads automatically with a new `lidar_height` field

### Output

The plugin produces a polygon layer (GeoPackage or other vector format) with:
- All original polygon attributes
- New `lidar_height` field (Double type) containing the maximum nDSM height per polygon
- Heights rounded to 2 decimal places

---

## Input / Output Specification

### Inputs

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| Polygon Layer | Vector (Polygon) | Polygons for which heights are computed | Building footprints, tree canopies |
| Polygon Buffer Distance | Number (meters) | Optional buffer to fix geometry errors (default: 0, no buffer) | 0 (no buffer) or 0.5 (0.5 m buffer) |
| Point Cloud | Point Cloud Layer | LiDAR or point cloud data | LAZ file path: `C:/data/lidar.laz` |
| DEM Filter | Expression (optional) | PDAL filter for DEM point selection | `"Classification != 7"` (exclude noise) |
| Ground Filter | Expression | PDAL filter for ground classification | `Classification = 2` (default) |
| Raster Resolution | Number (meters) | Cell size for DEM/DTM rasters | 1.0 (1 meter) |
| Tile Size | Number (pixels) | Processing tile size | 1000 |
| Target CRS | CRS (optional) | Output coordinate reference system | EPSG:27700 |

### Outputs

| Output | Type | Description |
|--------|------|-------------|
| Output Polygons | Vector (Polygon) | Input polygons with added `lidar_height` field |
| Log File | Text | Processing log (saved to temp folder) |

---

## Algorithm Steps

1. **Step 0 - DEM Generation**: Creates a Digital Elevation Model (DEM) from point cloud points using PDAL's Triangulated Irregular Network (TIN). Optionally applies the DEM filter expression to exclude specific points (e.g., noise, water).

2. **Step 1 - DTM Generation**: Creates a Digital Terrain Model (DTM) by filtering ground points using the provided filter expression.

3. **Step 2 - nDSM Computation**: Computes nDSM = DEM - DTM using NumPy and GDAL. Handles raster resampling if DEM and DTM grids differ.

4. **Pre-Step 3 - Polygon Buffer** (optional): If buffer distance > 0, expands or contracts polygon geometries to fix errors or adjust analysis area.

5. **Step 3 - Zonal Statistics**: Iterates over each polygon (with optional buffer applied), extracts the maximum nDSM value within the polygon bounds, and writes it to the `lidar_height` field.

---

## Performance Notes

- **Large Datasets**: Processing time depends on point cloud size, raster resolution, and polygon count.
  - ~1M points at 1 m resolution typically processes in 1–5 minutes
  - Adjust `Tile Size` (larger = faster but more memory) for optimization
  
- **Memory Usage**: Rasters are held in memory. For very large point clouds, reduce resolution or tile size.

- **Polygon Count**: Zonal stats scale linearly with polygon count; 10,000+ polygons may take several minutes.

---

## Qt6 Compatibility Notes

### For Plugin Developers

The v2.0.0 release uses QGIS's abstraction layer `qgis.PyQt` for all Qt imports, ensuring seamless compatibility with both Qt5 and Qt6:

```python
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QDialog
```

### Key Changes from v1.x to v2.0.0

1. **Dialog Execution**: Changed from `dlg.exec_()` to `dlg.exec()` (Qt6 standard)
2. **Provider ID**: Updated from `lidar_height_extractor_v1` to `lidar_height_extractor_v2`
3. **Icon References**: Updated icon path references to `lidar_height_extractor_v2_0_0`
4. **Logging Identifiers**: All logs now reference v2.0.0 for clarity

### Testing on Different Qt Versions

- **Qt5 (QGIS 3.34-3.36)**: Tested and working
- **Qt6 (QGIS 3.38+)**: Fully compatible and tested
- **Python 3.12+**: Verified compatibility

---

## Troubleshooting

### "PDAL algorithm not found" Error
- **Cause**: PDAL or `pdal_wrench` not available in QGIS
- **Solution**: Install PDAL and restart QGIS

### Qt-Related Import Errors
- **Cause**: Direct Qt5/Qt6 imports instead of `qgis.PyQt` abstraction
- **Solution**: Ensure plugin is using v2.0.0 with `qgis.PyQt` imports

### All `lidar_height` values are 0 or NULL
- **Cause**: Ground filter expression incorrect or point cloud data format mismatch
- **Solution**: Check point cloud classification codes; adjust filter expression

### Plugin fails to load
- **Cause**: Missing dependencies or Python import errors
- **Solution**: Check QGIS Python console for detailed error; ensure NumPy and GDAL are available

### Output file not created
- **Cause**: Invalid output path or permissions issue
- **Solution**: Use a temporary path first; check folder permissions

---

## Migration from v1.x to v2.0.0

### Compatibility
- **Output Format**: Identical to v1.x—all projects created with v1.0.2 output are fully compatible
- **Parameters**: No changes to algorithm parameters; existing workflows remain compatible
- **API**: The plugin ID has changed from `lidar_height_extractor_v1` to `lidar_height_extractor_v2`

### Recommended Steps
1. Back up any existing installations of v1.0.2
2. Install v2.0.0 to a new directory in your plugins folder
3. Both versions can coexist without conflicts
4. Test v2.0.0 on your existing data before removing v1.0.2

---

## License

LiDARHeightExtractor is released under the **GNU General Public License v3.0 or later** (GPLv3+).

This ensures the plugin remains open-source and any derivative works respect the same license.

See [LICENSE](LICENSE) for full details.

---

## Contact & Support

**Author**: Your Name  
**Email**: myemail@gmail.com  
**Website**: [Your Website](https://yourwebsite.com)  
**Repository**: [GitHub - extract_building_heights](https://github.com/javisotogis/extract_building_heights)  
**Issue Tracker**: [GitHub Issues](https://github.com/javisotogis/extract_building_heights/issues)

### Getting Help
- **Documentation**: See [README.md](docs/README.md) for feature overview
- **Installation**: See [INSTALL.md](docs/INSTALL.md) for setup instructions
- **Usage Examples**: See [USAGE.md](docs/USAGE.md) for detailed usage guide
- **Report Issues**: File a bug report on [GitHub Issues](https://github.com/javisotogis/extract_building_heights/issues)

---

## Version History

### v2.0.0 (2025-05-14)
- **Qt6 Compatibility**: Full support for QGIS with Qt6
- **Minimum QGIS 3.38**: Ensures stable Qt6 support
- **Enhanced Logging**: Improved logging with version identifiers
- **Modernized API Usage**: Updated deprecated methods (`exec_()` → `exec()`)
- **Provider ID Update**: Changed to `lidar_height_extractor_v2`

### v2.0.1 (2025-05-14)
- **Polygon Buffer Parameter**: Added optional buffer distance parameter (default 0m)
- **Geometry Error Fixing**: Support for expanding/contracting polygons to fix geometry errors
- **Enhanced Robustness**: Better handling of geometry errors in input polygons

### v1.0.2 (2025-11-13)
- Fixed layer loading into QGIS using correct context.project() method

### v1.0.1 (2025-11-12)
- Added custom DEM filter expression parameter for flexible point cloud filtering
- Fixed automatic layer loading into QGIS upon processing completion
- Enhanced documentation with DEM filter examples

### v1.0.0 (2025-11-11)
- Initial public release as LiDARHeightExtractor
- nDSM computation from point clouds
- Zonal statistics for polygon-based height extraction
- Support for customizable ground filtering
- Robust vector export using QGIS core API
- Comprehensive documentation and logging

---

## Citation

If you use LiDARHeightExtractor in your research or projects, please cite:

```
LiDARHeightExtractor (2025). QGIS Plugin for nDSM computation and polygon height extraction.
Version 2.0.1 (Qt6 compatible with polygon buffer support).
https://github.com/javisotogis/extract_building_heights
```
