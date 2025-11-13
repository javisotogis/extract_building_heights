# LiDARHeightExtractor v1.0.0

LiDARHeightExtractor computes an nDSM (DEM - DTM) from a point cloud (via PDAL's to_raster_tin) and calculates the maximum height per input polygon. Use cases: building rooftop heights, tree canopy heights, or any polygon-based height extraction.

Requirements
- QGIS 3.34+ (tested on 3.40)
- PDAL + pdal_wrench available in QGIS (used by processing algorithms `pdal:exportrastertin`)
- GDAL, NumPy (available in QGIS Python)

Installation
1. Install PDAL and ensure QGIS processing has the PDAL provider and `pdal_wrench` binary available.
2. Copy the `lidar_height_extractor_v1_0_0` folder to your QGIS plugins folder or install the supplied zip.

Usage
- Input polygon layer (called "polygon layer") must contain the polygons you wish to compute heights for. Examples: buildings (for rooftop heights), tree polygons (for canopy height), urban blocks, etc.
- Point cloud: provide a LAZ/LAZ path via the PDAL URI (e.g. `pdal:///C:/path/to/points.laz`).
- Resolution: raster cell size in same units as CRS.
- Output polygon: GeoPackage path or temporary.

Notes
- The plugin does NOT include PDAL binaries. Install PDAL separately.
- If you have external Python dependencies, list them in `requirements.txt` and follow INSTALL.md (Windows instructions linked).

