import rasterio
from rasterio.plot import show
import numpy as np
from matplotlib.colors import ListedColormap

# Open the slope raster
with rasterio.open("./sloped/mount_st_helens_USGS_1m_dem_8bit_gray_slope.tif") as src:
    slope_data = src.read(1)

# Define custom colormap
colors = [
    (1.0, 1.0, 1.0, 0.0),  # Transparent
    (1.0, 1.0, 0.7, 1.0),  # Light yellow
    (1.0, 0.85, 0.46, 1.0),  # Yellow-orange
    (0.99, 0.7, 0.3, 1.0),  # Orange
    (0.99, 0.55, 0.24, 1.0),  # Dark orange
    (0.94, 0.23, 0.13, 1.0),  # Red
]
cmap = ListedColormap(colors)

# Apply a mask for transparency below 25 degrees
slope_data = np.ma.masked_where(slope_data < 25, slope_data)

# Plot with Rasterio
show(slope_data, cmap=cmap)
