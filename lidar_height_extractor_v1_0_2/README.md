# LiDARHeightExtractor v1.0.2

## Overview

**LiDARHeightExtractor** is a QGIS plugin that computes normalized Digital Surface Models (nDSM) from point cloud data and extracts the maximum height for each polygon feature. This is useful for analyzing building rooftop heights, tree canopy heights, or any polygon-based height extraction analysis.

The plugin leverages PDAL (Point Data Abstraction Library) for efficient point cloud rasterization and GDAL for raster arithmetic, providing a robust, production-ready workflow for LiDAR-based height analysis.

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
- **QGIS**: 3.34 or later (tested on 3.40.0-Bratislava)
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

### Windows (OSGeo4W / QGIS Standalone)

1. **Install PDAL** (if not already present):
   - If using OSGeo4W, ensure the PDAL package is installed
   - If using QGIS standalone, PDAL is typically bundled

2. **Install the Plugin**:
   - Download `lidar_height_extractor_v1_0_0.zip`
   - Close QGIS
   - Extract the zip to your QGIS plugins folder:
     ```
     C:\Users\<YourUsername>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
     ```
   - Restart QGIS
   - Enable the plugin in **Plugins → Manage and Install Plugins**

3. **Python Package Installation** (if needed):
   - Follow [this guide for Windows](https://landscapearchaeology.org/2018/installing-python-packages-in-qgis-3-for-windows/)

### Linux / macOS
- Install PDAL via package manager (e.g., `apt install pdal`, `brew install pdal`)
- Extract plugin to `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
- Restart QGIS

---

## Usage

### Basic Workflow

1. **Open QGIS** and load your data:
   - Point cloud (LAZ, LAS, or other PDAL-supported formats)
   - Polygon layer (buildings, trees, parcels, etc.)

2. **Access the Plugin**:
   - Go to **Processing → Toolbox**
   - Search for "LiDARHeightExtractor" or navigate to **LiDAR → LiDARHeightExtractor + Zonal Stats**

3. **Configure Parameters**:
   - **Polygon Layer**: Select the layer containing polygons (e.g., building footprints)
   - **Point Cloud**: Provide the path to your point cloud file (LAZ/LAS)
   - **Polygon Layer**: Your input polygon layer (buildings, trees, etc.)
   - **Point Cloud**: Your LiDAR data
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

4. **Step 3 - Zonal Statistics**: Iterates over each polygon, extracts the maximum nDSM value within the polygon bounds, and writes it to the `lidar_height` field.

---

## Performance Notes

- **Large Datasets**: Processing time depends on point cloud size, raster resolution, and polygon count.
  - ~1M points at 1 m resolution typically processes in 1–5 minutes
  - Adjust `Tile Size` (larger = faster but more memory) for optimization
  
- **Memory Usage**: Rasters are held in memory. For very large point clouds, reduce resolution or tile size.

- **Polygon Count**: Zonal stats scale linearly with polygon count; 10,000+ polygons may take several minutes.

---

## Troubleshooting

### "PDAL algorithm not found" Error
- **Cause**: PDAL or `pdal_wrench` not available in QGIS
- **Solution**: Install PDAL and restart QGIS

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

### v1.0.1 (2025-11-13)
- Added custom DEM filter expression parameter for flexible point cloud filtering
- Fixed automatic layer loading into QGIS upon processing completion
- Enhanced documentation with DEM filter examples

### v1.0.0 (2025-11-12)
- Initial public release
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
https://github.com/javisotogis/extract_building_heights
```

---

## Acknowledgments

LiDARHeightExtractor relies on:
- **QGIS** and its processing framework
- **PDAL** for efficient point cloud processing
- **GDAL** for raster operations
- **NumPy** for numerical computations

---

## Contributing

Contributions, bug reports, and feature requests are welcome!

1. Fork the [repository](https://github.com/javisotogis/extract_building_heights)
2. Create a feature branch
3. Submit a pull request with a clear description of your changes

---

## Disclaimer

This plugin is provided "as-is" without warranty. Users are responsible for validating results and ensuring data quality. Always backup your data before processing.

---

**Last Updated**: November 13, 2025  
**Status**: Stable (v1.0.2)
