## About

Goal of research getting elevation data from mapbox tiles and create avalanche relief map.  

## Env UP

.env - `ACCESS_TOKEN=your_access_token_here`  

1. `brew install gdal`  
2. `python3 -m venv .` && `source bin/activate`  
3. `pip3 install -r requirements.txt`  

## Env Down

1. `deactivate`  

## Up & Running

1. `make download`  
2. `make convert`  
3. `make slope`  
4. `make paint`  

## Results  

![mapbox-terrain-dem-v1-14zoom](img/tile_mapbox_mapbox-terrain-dem-v1_14zoom_8816_5744_8bit_geotiff_slope_painted.tif)  
![mapbox_terrain-rgb-14zoom](img/tile_mapbox_terrain-rgb_14zoom_8816_5744_8bit_geotiff_slope_painted.tif)  
![mapbox_terrain-rgb-15zoom](img/tile_mapbox_terrain-rgb_15zoom_17632_11488_8bit_geotiff_slope_painted.tif)  
![mapbox_terrain-rgb-16zoom](tile_mapbox_terrain-rgb_16zoom_35264_22976_8bit_geotiff_slope_painted.tif)  


## Mapbox docs

[Access elevation data](https://docs.mapbox.com/data/tilesets/guides/access-elevation-data/)  
[Zoom level](https://docs.mapbox.com/help/glossary/zoom-level/)  
[Mapbox Terrain-DEM v1](https://docs.mapbox.com/data/tilesets/reference/mapbox-terrain-dem-v1/#layer-reference)  
