import os
import requests
from dotenv import load_dotenv


# Function to fetch a tile
def fetch_tile(z, x, y, access_token, save_dir, dem):
    url = f"https://api.mapbox.com/v4/{dem}/{z}/{x}/{y}@2x.pngraw?access_token={access_token}"
    response = requests.get(url)
    if response.status_code == 200:
        # Define the path where the tile will be saved
        dem_cleaned = dem.replace(".", "_")
        downloaded_tile = os.path.join(
            save_dir, f"tile_{dem_cleaned}_{z}zoom_{x}_{y}.png"
        )
        with open(downloaded_tile, "wb") as file:
            file.write(response.content)
        print(f"Tile saved: {downloaded_tile}")
        return downloaded_tile
    else:
        raise Exception(f"Failed to fetch tile: {response.status_code} {response.text}")


load_dotenv()

# Access token for Mapbox API
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Tile parameters
START_ZOOM = 14
END_ZOOM = 16
TILE_X = 8816
TILE_Y = 5744
TERRAIN_RGB = "mapbox.terrain-rgb"
TERRAIN_DEM = "mapbox.mapbox-terrain-dem-v1"
save_dir = "./tiles"

# Ensure the save directory exists
os.makedirs(save_dir, exist_ok=True)

# Download tiles for the given zoom levels
for z in range(START_ZOOM, END_ZOOM + 1):
    try:
        multiplier = 2 ** (z - START_ZOOM)
        adjusted_x = TILE_X * multiplier
        adjusted_y = TILE_Y * multiplier
        print(
            f"Fetching tile at zoom {z} with coordinates X: {adjusted_x}, Y: {adjusted_y}..."
        )
        fetch_tile(z, adjusted_x, adjusted_y, ACCESS_TOKEN, save_dir, TERRAIN_RGB)
        fetch_tile(z, adjusted_x, adjusted_y, ACCESS_TOKEN, save_dir, TERRAIN_DEM)
    except Exception as e:
        print(f"Zoom {z} failed: {e}")
