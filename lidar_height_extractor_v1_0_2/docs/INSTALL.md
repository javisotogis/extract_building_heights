# Installation notes

LiDARHeightExtractor relies on PDAL's `pdal_wrench` to produce rasters from point clouds. On Windows, PDAL is usually included with QGIS or can be installed separately.

Windows recommendations:
- If using OSGeo4W, ensure the PDAL package is installed.
- See guide: https://landscapearchaeology.org/2018/installing-python-packages-in-qgis-3-for-windows/ (for Python packages)

Python packages inside QGIS:
- NumPy and GDAL are typically available in QGIS Python. If your QGIS lacks required modules, install them into the QGIS python environment.

