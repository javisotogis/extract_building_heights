# Usage Guide - LiDARHeightExtractor v2.0.0

## Overview

LiDARHeightExtractor computes a normalized Digital Surface Model (nDSM) from LiDAR point cloud data and extracts the maximum nDSM height within each polygon feature. This guide covers basic workflow, parameter configuration, and practical examples.

---

## Basic Workflow

### 1. Prepare Your Data

**Polygon Layer**: A vector layer containing polygons for which you want height values
- Examples: building footprints, tree canopy polygons, parcels, urban blocks
- Format: Shapefile, GeoPackage, GeoJSON, etc.
- CRS: Should match or be compatible with your point cloud CRS

**Point Cloud**: LiDAR data in a format supported by PDAL
- Formats: LAZ, LAS, other PDAL-supported formats (E57, XYZ, etc.)
- Format: Full file path (e.g., `C:/data/lidar.laz`)
- CRS: Should match or be compatible with polygon layer CRS

### 2. Open Processing Toolbox

1. In QGIS, go to **Processing → Toolbox**
2. Search for "LiDARHeightExtractor"
3. Double-click: **LiDARHeightExtractor + Zonal Stats**

### 3. Configure Parameters

The algorithm dialog will show the following parameters:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **Polygon layer** | Vector Layer | ✓ | Your input polygons (buildings, trees, etc.) |
| **Polygon buffer distance** | Number (m) | ✓ | Optional buffer to fix geometry errors (default: 0 m, no buffer). Use positive values to expand, negative to contract |
| **Point Cloud** | Point Cloud | ✓ | Path to LAZ/LAS file |
| **DEM filter expression** | Expression | ✗ | Optional PDAL filter for DEM points (e.g., exclude noise) |
| **Ground filter for DTM** | Expression | ✓ | PDAL filter for ground points (default: `Classification = 2`) |
| **Raster resolution** | Number | ✓ | Cell size in map units (default: 1 m) |
| **Tile size** | Integer | ✓ | Processing tile size in pixels (default: 1000) |
| **Target CRS** | CRS | ✗ | Optional output coordinate system |
| **Output polygons** | File Path | ✓ | Path to save result (GeoPackage recommended) |

---

## Parameter Guide

### Polygon Layer
- **What**: The vector layer containing your analysis polygons
- **Examples**:
  - Building footprints (OSM buildings)
  - Tree canopy outlines
  - Parcel boundaries
  - Urban blocks
- **Notes**: Ensure polygons are in the same or compatible CRS as point cloud

### Polygon Buffer Distance (New!)
- **Purpose**: Optionally expand or contract polygons to fix geometry errors or adjust analysis area
- **Default**: 0 m (no buffer applied)
- **Examples**:
  - `0` m – No buffer (standard, recommended)
  - `0.5` m – Expand polygons by 0.5 meters (fixes small geometry errors)
  - `1.0` m – Expand by 1 meter (useful for small gaps between adjacent buildings)
  - `-0.5` m – Contract by 0.5 meters (shrink polygons inward)
- **Use Cases**:
  - Fix small slivers or gaps in polygon coverage
  - Account for positional uncertainty in digitized boundaries
  - Adjust analysis footprint for adjacent features
- **Notes**: 
  - Positive values expand polygons outward
  - Negative values contract polygons inward
  - Buffer is applied before height extraction
  - Segments=4 used for smooth buffer (computational efficiency)

### Point Cloud
- **What**: Path to your LiDAR data file
- **Format**: Full absolute path
- **Example**: `C:/data/Harrogate_LiDAR.copc.laz`
- **Supported Formats**: LAZ, LAS, and other PDAL-supported formats

### DEM Filter Expression (Optional)
- **Purpose**: Filter which points contribute to the DEM (Digital Elevation Model)
- **Default**: Empty (uses all points)
- **Examples**:
  - `"Classification != 7"` – Exclude noise points
  - `"Classification != 18"` – Exclude water
  - `"Classification in (2, 6)"` – Only ground and structures
  - `"ReturnNumber = 1"` – Only first returns
- **Notes**: Leave empty to use all points

### Ground Filter for DTM (Required)
- **Purpose**: Filter for ground points to create the DTM (Digital Terrain Model)
- **Default**: `Classification = 2` (ASPRS classification for ground)
- **Examples**:
  - `"Classification = 2"` – Standard ground (default)
  - `"Classification in (2, 26)"` – Ground and classified medium vegetation
  - `"Classification = 9"` – Water (if analyzing flood risk)
- **Notes**: Choose based on your point cloud classification scheme

### Raster Resolution
- **Purpose**: Cell size for DEM and DTM rasters
- **Units**: Map units (e.g., meters if CRS is in meters)
- **Typical Values**:
  - `0.5 m` – Fine detail, high memory usage, slower
  - `1.0 m` – Balanced (recommended)
  - `2.0 m` – Coarse, faster, lower detail
  - `5.0 m` – Very coarse, fastest
- **Notes**: Finer resolution = more detail but slower processing

### Tile Size
- **Purpose**: Processing tile size in pixels for PDAL algorithm
- **Default**: `1000` pixels
- **Typical Values**:
  - `500` – Smaller tiles, lower memory, slower
  - `1000` – Balanced (default, recommended)
  - `2000` – Larger tiles, higher memory, faster
- **Notes**: Adjust if you run out of memory; increase if processing is slow

### Target CRS (Optional)
- **Purpose**: Reproject output polygons to a specific coordinate reference system
- **Default**: Empty (uses source CRS)
- **Example**: EPSG:27700 (British National Grid)
- **Notes**: Leave empty to keep source CRS

### Output Polygons
- **Purpose**: Path where the result polygon layer will be saved
- **Format**: GeoPackage (.gpkg) recommended; also supports Shapefile, GeoJSON
- **Example**: `C:/results/harrogate_building_heights.gpkg`
- **Notes**: Plugin will create this file; ensure write permissions to folder

---

## Example Workflows

### Example 1: Building Height Extraction (Rooftop Heights)

**Goal**: Extract rooftop heights for all buildings

**Setup**:
- **Polygon layer**: Building footprints (e.g., from OSM)
- **Point Cloud**: LiDAR survey data (LAZ file)
- **DEM Filter**: `"Classification != 7"` (exclude noise)
- **Ground Filter**: `"Classification = 2"` (standard ground)
- **Resolution**: 1.0 m
- **Output**: `buildings_with_heights.gpkg`

**Output**: Each building polygon will have a `lidar_height` field with rooftop height in meters

**Use Cases**:
- Solar potential analysis (taller buildings = more solar potential)
- Urban heat island modeling
- Building energy consumption estimates
- Telecom tower clearance analysis

---

### Example 2: Tree Canopy Height Analysis

**Goal**: Compute maximum tree canopy heights

**Setup**:
- **Polygon layer**: Tree canopy outlines (from manual delineation or other classification)
- **Point Cloud**: LiDAR survey with vegetation classification
- **DEM Filter**: Empty (use all points)
- **Ground Filter**: `"Classification = 6"` (if low vegetation is classified as 6)
- **Resolution**: 0.5 m (finer detail for small trees)
- **Output**: `trees_with_heights.gpkg`

**Output**: Each tree polygon will have a `lidar_height` field with maximum canopy height

**Use Cases**:
- Forest inventory and biomass estimation
- Urban canopy assessment
- Tree risk assessment
- Forestry management planning

---

### Example 3: Flood Risk & Shadow Analysis

**Goal**: Analyze elevation for flood modeling

**Setup**:
- **Polygon layer**: Building or land parcels
- **Point Cloud**: DEM-quality LiDAR
- **DEM Filter**: `"Classification != 7"` (exclude noise)
- **Ground Filter**: `"Classification = 2"` (ground only, for DTM)
- **Resolution**: 2.0 m (coarse for large areas)
- **Output**: `parcels_with_elevation.gpkg`

**Output**: Each parcel's maximum elevation for flood risk analysis

---

## Running the Algorithm

### Step 1: Input All Parameters
- Fill in all required fields (marked with ✓)
- Configure optional filters as needed
- Double-check file paths

### Step 2: Click "Run"
- Algorithm begins processing
- Progress shows in the QGIS interface
- Processing may take 1–5 minutes depending on data size

### Step 3: Monitor Progress
- Watch the **Log** at the bottom of QGIS
- You'll see steps: DEM generation → DTM generation → nDSM computation → Zonal statistics
- Processing displays feature count and polygon progress

### Step 4: Check Results
- The output layer automatically loads into QGIS
- Zoom to output layer
- Open **Attribute Table** to view `lidar_height` values

---

## Output Interpretation

### Output Layer Structure

The output polygon layer contains:

1. **All original attributes** from input polygon layer
2. **New `lidar_height` field** (type: Double)
   - Values: Maximum nDSM height per polygon in meters
   - Precision: Rounded to 2 decimal places
   - Null/0: Polygon has no points above ground

### Example Attribute Table

| ID | Name | Geometry | lidar_height |
|----|------|----------|--------------|
| 1 | Building A | POLYGON(...) | 12.45 |
| 2 | Building B | POLYGON(...) | 0.0 |
| 3 | Building C | POLYGON(...) | 8.67 |

- **12.45 m**: Building A has max height of 12.45 meters
- **0.0 m**: Building B has no points above ground (possibly error in ground classification)
- **8.67 m**: Building C has max height of 8.67 meters

---

## Practical Tips & Best Practices

### 1. Data Preparation
- **Verify CRS**: Ensure polygons and point cloud are in same or compatible CRS
- **Check Classification**: Review point cloud classification scheme (ASPRS standard by default)
- **Clean Polygons**: Remove invalid/degenerate polygons before processing

### 2. Parameter Tuning
- **Start with defaults**: Use default ground filter (`Classification = 2`)
- **Adjust resolution** based on point cloud density and detail needed
- **Test on subset** before processing entire dataset

### 3. Ground Filter Selection
| Scenario | Ground Filter | Notes |
|----------|---------------|-------|
| Standard LiDAR | `Classification = 2` | Most common, ASPRS standard |
| Dense Urban | `Classification in (2, 26)` | Include classified medium vegetation |
| Vegetation Area | `Classification = 6` | For low vegetation / shrub |
| Water Analysis | `Classification = 9` | For water surface |

### 4. Troubleshooting Issues
- **All heights are 0**: Check ground filter (may be too restrictive)
- **Processing is slow**: Increase tile size or resolution
- **Memory errors**: Reduce tile size or use coarser resolution
- **Missing output layer**: Check output file path permissions

### 5. Performance Optimization
- **Large datasets**: Use coarser resolution (2-5 m) initially
- **Many polygons**: Process in batches or use larger tiles
- **Memory constraints**: Reduce tile size (512-750 px)

---

## Logging & Debugging

### Access the Log File

After processing completes:
1. Check the Processing results panel
2. Look for "Log File" path (typically in `C:/Users/<name>/AppData/Local/Temp/`)
3. Open in text editor to review processing steps

### Common Log Messages

| Message | Meaning |
|---------|---------|
| `DEM generated: /path/to/dem.tif` | DEM raster successfully created |
| `DTM generated: /path/to/dtm.tif` | DTM raster successfully created |
| `Rasters with different size/transform — resampling DTM to DEM grid` | DTM was resampled to match DEM; normal operation |
| `Step 3: Computing zonal statistics` | Starting polygon height extraction |
| `Feature 100 has bounds outside raster` | Polygon extends beyond raster bounds (warning, normal) |

---

## Performance Benchmarks

Example timings for various dataset sizes:

| Scenario | Points | Polygons | Tile Size | Resolution | Duration |
|----------|--------|----------|-----------|------------|----------|
| Small buildings | 100K | 50 | 1000 | 1 m | ~30 sec |
| Medium city | 1M | 500 | 1000 | 1 m | ~2 min |
| Large city | 5M | 2000 | 1500 | 2 m | ~5 min |
| Very large | 10M+ | 5000+ | 2000 | 5 m | ~10 min |

**Note**: Timings depend on CPU, RAM, disk speed, and data complexity.

---

## Next Steps

- **Visualize Results**: Style the `lidar_height` field using color ramps
- **Statistical Analysis**: Use QGIS statistics tools on height values
- **Export Results**: Save to various formats (Shapefile, GeoJSON, etc.)
- **Further Processing**: Use in models for solar analysis, flood risk, etc.

---

## Support & Resources

- **Documentation**: See [README.md](../README.md) for features and technical details
- **Installation**: See [INSTALL.md](INSTALL.md) for setup instructions
- **GitHub**: [extract_building_heights](https://github.com/javisotogis/extract_building_heights)
- **Issues**: Report bugs on [GitHub Issues](https://github.com/javisotogis/extract_building_heights/issues)

---

## FAQs

**Q: Can I use a Shapefile instead of LAZ?**  
A: LiDARHeightExtractor expects point cloud data. Shapefiles are vector data. Use LAZ/LAS files only.

**Q: What if my polygons are in a different CRS than the point cloud?**  
A: QGIS handles on-the-fly CRS transformation, but ensure both are set correctly.

**Q: How do I handle negative heights?**  
A: Negative heights indicate points below the ground surface. The algorithm filters these out (ignores values ≤ 0).

**Q: Can I process multiple point clouds at once?**  
A: Run the algorithm separately for each point cloud, or merge point clouds before processing.

**Q: Why are some polygons showing 0 height?**  
A: No points above ground detected. Check: ground filter is too strict, polygon is outside point cloud bounds, or no points exist there.
