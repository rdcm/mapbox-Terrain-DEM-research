import os
import numpy as np
from osgeo import gdal, osr
from PIL import Image

# Disable GDAL exceptions warning
gdal.UseExceptions()

# Step 1: Decode Terrain-RGB to Elevation


# mapbox-terrain-dem-v1: height = -10000 + ((R * 256 * 256 + G * 256 + B) * 0.1)
# mapbox-terrain-rgb-v1: height = -10000 + ((R * 256 * 256 + G * 256 + B) * 0.1)
def rgb_to_elevation(r, g, b):
    return -10000 + ((r * 256 * 256 + g * 256 + b) * 0.1)


# Step 2: Scale elevation data
def scale_to_8bit(data, min_value, max_value):
    """Scale elevation data to the 8-bit range (0-255)."""
    scaled = (data - min_value) / (max_value - min_value) * 255
    return np.clip(scaled, 0, 255).astype(np.uint8)


def scale_to_16bit(data, min_value, max_value):
    """Scale elevation data to the 16-bit range (0-65535)."""
    scaled = (data - min_value) / (max_value - min_value) * 65535
    return np.clip(scaled, 0, 65535).astype(np.uint16)


# Step 3: Create GeoTIFF using GDAL
def create_geotiff(elevation_data, output_path, lon, lat, pixel_size, bit_depth):
    height, width = elevation_data.shape

    # Select GDAL data type based on bit depth
    gdal_data_type = gdal.GDT_Byte if bit_depth == 8 else gdal.GDT_UInt16

    # Create a GDAL GeoTIFF driver
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(output_path, width, height, 1, gdal_data_type)

    # Set geotransform (top-left corner coordinates and pixel size)
    geotransform = [lon, pixel_size, 0, lat, 0, -pixel_size]
    dataset.SetGeoTransform(geotransform)

    # Set projection (EPSG:4326 for WGS84)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    dataset.SetProjection(srs.ExportToWkt())

    # Write elevation data to band
    band = dataset.GetRasterBand(1)
    band.WriteArray(elevation_data)
    band.SetNoDataValue(0)  # Optional: Set 0 as no-data value if needed

    # Close and save
    dataset.FlushCache()
    dataset = None

    print(f"{bit_depth}-bit GeoTIFF created at {output_path}")


# Step 4: Process all PNG files in a directory
def process_directory(directory, lon, lat, pixel_size, bit_depth):
    converted_dir = "./converted"
    if not os.path.exists(converted_dir):
        os.makedirs(converted_dir)

    for file_name in os.listdir(directory):
        if file_name.endswith(".png"):
            file_path = os.path.join(directory, file_name)

            # Load the RGB tile
            img = Image.open(file_path).convert("RGB")
            rgb_array = np.array(img)

            # Extract RGB channels
            r = rgb_array[:, :, 0].astype(np.float32)
            g = rgb_array[:, :, 1].astype(np.float32)
            b = rgb_array[:, :, 2].astype(np.float32)

            # Calculate elevation
            elevation_array = rgb_to_elevation(r, g, b)

            # Scale elevation based on bit depth
            if bit_depth == 8:
                min_elevation = np.min(elevation_array)
                max_elevation = np.max(elevation_array)
                scaled_elevation = scale_to_8bit(
                    elevation_array, min_elevation, max_elevation
                )
            elif bit_depth == 16:
                min_elevation = np.min(elevation_array)
                max_elevation = np.max(elevation_array)
                scaled_elevation = scale_to_16bit(
                    elevation_array, min_elevation, max_elevation
                )
            else:
                raise ValueError("Bit depth must be either 8 or 16.")

            # Save the GeoTIFF
            output_file_name = (
                f"{os.path.splitext(file_name)[0]}_{bit_depth}bit_geotiff.tif"
            )
            output_path = os.path.join(converted_dir, output_file_name)
            create_geotiff(
                scaled_elevation, output_path, lon, lat, pixel_size, bit_depth
            )


# Step 5: Specify parameters and call the function
directory = "./tiles"  # Directory containing .png files
lon, lat = 44.308, 39.702  # Approx longitude and latitude of the top-left corner
pixel_size = 0.00028  # Adjust as per the tile resolution

process_directory(directory, lon, lat, pixel_size, 8)  # 8 bit
process_directory(directory, lon, lat, pixel_size, 16)  # 16 bit
