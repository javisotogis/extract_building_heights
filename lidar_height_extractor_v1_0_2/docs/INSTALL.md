# Installation Guide - LiDARHeightExtractor v2.0.0

## Prerequisites

Before installing the plugin, ensure you have:

1. **QGIS 3.38 or later** (with Qt6 support)
2. **PDAL** installed (includes `pdal_wrench` binary)
3. **Python 3.12+** (bundled with QGIS)
4. **NumPy and GDAL** (typically available in QGIS Python environment)

---

## Windows Installation (OSGeo4W / QGIS Standalone)

### Step 1: Install PDAL

#### Option A: Using OSGeo4W
If you're using QGIS via OSGeo4W:

```bash
osgeo4w-setup.exe
```

During installation, select the **PDAL** package.

#### Option B: QGIS Standalone
PDAL is typically bundled with QGIS standalone installations. Verify by checking:
- **Processing → Options → Providers → PDAL**

If PDAL is not available, download from [PDAL Releases](https://github.com/PDAL/PDAL/releases).

### Step 2: Install the Plugin

1. **Download** the plugin:
   - Download `lidar_height_extractor_v2_0_0.zip` from [GitHub Releases](https://github.com/javisotogis/extract_building_heights/releases)

2. **Locate your QGIS plugins folder**:
   - Open QGIS
   - Go to **Settings → User Profiles → Open Active Profile Folder**
   - Navigate to `python/plugins/`
   - This is typically: `C:\Users\<YourUsername>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`

3. **Extract the plugin**:
   - Extract `lidar_height_extractor_v2_0_0.zip` into the `plugins` folder
   - You should have: `plugins/lidar_height_extractor_v2_0_0/`

4. **Restart QGIS**:
   - Close and reopen QGIS

5. **Enable the plugin**:
   - Go to **Plugins → Manage and Install Plugins**
   - Search for "LiDARHeightExtractor"
   - Check the box to enable it
   - The plugin should now appear in your Processing Toolbox

### Step 3: Verify Installation

1. Open **Processing → Toolbox**
2. Search for "LiDARHeightExtractor"
3. You should see: **LiDARHeightExtractor + Zonal Stats**
4. If found, the installation is successful!

---

## Linux Installation

### Prerequisites

```bash
# Install PDAL
sudo apt install pdal

# Install Python dependencies (if needed)
sudo apt install python3-numpy python3-gdal
```

### Plugin Installation

1. **Locate your QGIS plugins folder**:
   ```bash
   ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
   ```

2. **Extract the plugin**:
   ```bash
   unzip lidar_height_extractor_v2_0_0.zip -d ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
   ```

3. **Restart QGIS**:
   ```bash
   qgis
   ```

4. **Enable in QGIS**:
   - **Plugins → Manage and Install Plugins**
   - Search for "LiDARHeightExtractor"
   - Enable the plugin

---

## macOS Installation

### Prerequisites

```bash
# Install PDAL using Homebrew
brew install pdal

# Verify PDAL is installed
which pdal_wrench
```

### Plugin Installation

1. **Locate your QGIS plugins folder**:
   ```bash
   ~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/
   ```

2. **Extract the plugin**:
   ```bash
   unzip lidar_height_extractor_v2_0_0.zip -d ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/
   ```

3. **Restart QGIS**

4. **Enable the plugin**:
   - **Plugins → Manage and Install Plugins**
   - Search for "LiDARHeightExtractor"
   - Enable it

---

## Installing Python Packages (if needed)

### Windows

If NumPy or GDAL are missing from your QGIS Python environment:

1. **Open OSGeo4W Shell** (or PowerShell for standalone QGIS)

2. **Activate QGIS Python**:
   ```bash
   # For OSGeo4W
   set PYTHONPATH=%OSGEO4W_ROOT%\apps\Python312
   
   # For standalone QGIS
   set PYTHONPATH=C:\Program Files\QGIS\apps\Python312
   ```

3. **Install packages**:
   ```bash
   pip install numpy gdal
   ```

### Linux

```bash
# Install system packages
sudo apt install python3-numpy python3-gdal

# Or via pip
pip3 install numpy gdal
```

### macOS

```bash
# Using Homebrew
brew install gdal numpy

# Or via pip
pip3 install numpy gdal
```

---

## Qt6 Compatibility

### For QGIS 3.38+

LiDARHeightExtractor v2.0.0 is fully compatible with QGIS 3.38+ deployments using Qt6:

- ✅ All `qgis.PyQt` imports are Qt6-compatible
- ✅ No additional configuration needed
- ✅ Works seamlessly alongside Qt5-based QGIS 3.34-3.36

### Checking Your QGIS Qt Version

In QGIS Python console:
```python
from qgis.PyQt.QtCore import QT_VERSION_STR
print(f"Qt Version: {QT_VERSION_STR}")
```

---

## Troubleshooting Installation

### Plugin Not Appearing in Processing Toolbox

**Solution 1: Check if plugin is enabled**
- **Plugins → Manage and Install Plugins**
- Search "LiDARHeightExtractor"
- Ensure checkbox is ✓ enabled

**Solution 2: Restart QGIS**
- Close QGIS completely
- Wait 5 seconds
- Reopen QGIS

**Solution 3: Verify folder structure**
- Check: `plugins/lidar_height_extractor_v2_0_0/`
- Ensure `__init__.py`, `metadata.txt`, and `lidar_height_extractor_plugin.py` are present

### "PDAL algorithm not found" Error

- **Cause**: PDAL not installed or not in QGIS PATH
- **Solution**: 
  1. Install PDAL via your system package manager
  2. Verify in QGIS: **Processing → Options → Providers → PDAL** is enabled
  3. Restart QGIS

### Python Import Error

**Check QGIS Python Console**:
1. Go to **Plugins → Python Console**
2. Try importing:
   ```python
   import numpy
   from osgeo import gdal
   from qgis.PyQt.QtCore import QCoreApplication
   ```

If any import fails, install the missing package (see "Installing Python Packages" above).

---

## Upgrading from v1.0.2 to v2.0.0

### Compatibility
- ✅ All outputs from v1.0.2 are compatible with v2.0.0
- ✅ Parameter formats are unchanged
- ✅ Both versions can coexist

### Migration Steps

1. **Back up v1.0.2** (optional):
   ```bash
   # Rename old installation
   mv lidar_height_extractor_v1_0_2 lidar_height_extractor_v1_0_2.bak
   ```

2. **Install v2.0.0** as described above

3. **Test on sample data** before removing v1.0.2

4. **Remove v1.0.2** when satisfied (optional)

---

## Support

For installation issues:
- **Python Console Error**: Copy the full error and post on [GitHub Issues](https://github.com/javisotogis/extract_building_heights/issues)
- **PDAL Issues**: Check [PDAL Documentation](https://pdal.io/)
- **QGIS Configuration**: See [QGIS Documentation](https://docs.qgis.org/)

---

## Next Steps

Once installed, see [USAGE.md](USAGE.md) for workflow instructions.
