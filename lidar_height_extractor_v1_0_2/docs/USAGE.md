# LiDARHeightExtractor Usage

- Polygon layer: the polygons for which you want the maximum height. Examples:
  - Building footprints -> rooftop height
  - Tree canopy polygons -> maximum canopy height
  - Parcels or blocks -> max elevation within each polygon

- When running, the plugin will:
  1. Generate a DEM from the point cloud using PDAL `to_raster_tin`.
  2. Generate a DTM by filtering ground points (default filter: `Classification = 2`).
  3. Compute nDSM = DEM - DTM using NumPy/GDAL.
  4. For each polygon, compute the maximum nDSM value and write it to the `lidar_height` field.

Examples:
- Buildings: use building footprints. Useful for estimating rooftop-mounted solar potential or clearance.
- Trees: use canopy polygons to compute max tree heights for forestry or urban canopy analysis.

