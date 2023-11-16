"""Main module for interactive map"""
import os
import ipyleaflet
from ipyleaflet import (DrawControl, ScaleControl, LayersControl, MeasureControl, basemap_to_tiles,
                        basemaps, FullScreenControl, TileLayer, GeoJSON)
import shapefile
from .utils import (shapefile_to_geojson, read_geojson, ee_tile_layer)


ZOOM = 5
CENTER = (21.02, 105.83)
HEIGHT = "650px"
WIDTH = "450px"
SCROLL_ZOOM = True


class Map(ipyleaflet.Map):
    def __init__(self, **kwargs):
        # Set up some default attributes
        if "center" not in kwargs:
            kwargs["center"] = CENTER
        if "zoom" not in kwargs:
            kwargs["zoom"] = ZOOM
        if "height" not in kwargs:
            kwargs["height"] = HEIGHT
        if "width" not in kwargs:
            kwargs["width"] = WIDTH
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = SCROLL_ZOOM
        self.styles = {
            "color": "black",
            "fillColor": None,
            "fillOpacity": 0,
            "weight": 1
        }
        super().__init__(**kwargs)

        if "google_map" not in kwargs:
            map_layer = TileLayer(url="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
                                  attribution="Google", name="Google Satellite")
            self.add_layer(map_layer)
        self.add_layer(basemap_to_tiles(basemaps.OpenTopoMap))

        dark_matter_layer = basemap_to_tiles(basemaps.CartoDB.DarkMatter)
        dark_matter_layer.name = 'Dark Map'
        self.add_layer(dark_matter_layer)

        terrain_layer = basemap_to_tiles(basemaps.Stamen.Terrain)
        terrain_layer.name = "Terrain Map"
        self.add_layer(terrain_layer)

        water_layer = basemap_to_tiles(basemaps.Strava.Water)
        water_layer.name = "Water Map"
        self.add_layer(water_layer)

        self.add_control(FullScreenControl())
        self.add_control(ScaleControl(position="bottomleft"))
        self.add_control(LayersControl(position="topright"))
        self.add_control(DrawControl(position="topleft"))
        self.add_control(MeasureControl())

    def add_shapefile(self, file_path, style=None, layer_name=None):
        """Add a shapefile to Map.

        Args:
            file_path (str): The input shapefile path.
            style (dict, optional): A dict contains styling map. Defaults to None.
            layer_name (str, optional): The displaying name on the map. Defaults to None.
        """
        data = shapefile_to_geojson(file_path=os.path.abspath(file_path))
        if style is None:
            style = self.styles
        if layer_name is None:
            layer_name = "Map"
        geojson_data = GeoJSON(data=data, style=style, name=layer_name)
        self.add_layer(geojson_data)

    def add_geojson(self, file_path, style=None, layer_name=None):
        """Add a vector in GeoJSON format to the map.

        Args:
            file_path (str): The input GeoJSON file.
            style (str, optional): The styling map to display. Defaults to None.
            layer_name (str, optional): The displaying name on the map. Defaults to None.
        """
        data = read_geojson(os.path.abspath(file_path))
        if style is None:
            style = self.styles
        if layer_name is None:
            layer_name = "Map"
        geojson_data = GeoJSON(data=data, style=style, name=layer_name)
        self.add_layer(geojson_data)

    def add_ee_layer(self, ee_object, vis_params={}, layer_name="Image", show=True, opacity=1):
        img = ee_tile_layer(ee_object, vis_params=vis_params,
                            layer_name=layer_name, show=show, opacity=opacity)
        self.add_layer(img)
    addLayer = add_ee_layer
