import webbrowser

import ee
from folium import Map

# from geemap.foliumap import Map

from digitalarztools.pipelines.gee.core.region import GEERegion


class GEEMap():
    def __init__(self, region: GEERegion):
        center = region.center.getInfo()
        coordinates = center['coordinates']
        loc = [coordinates[1], coordinates[0]]
        self.Map = Map(location=loc, zoom_start=11)
        self.Map.addLayerControl()
        self.Map.add_minimap()
        # self.map.add

    def save_map(self):
        self.Map.save("../templates/map.html")

    def show(self):
        self.save_map()
        browser = webbrowser.get('chrome')
        browser.open("../templates/map.html")

    def add_raster_layer(self, ee_image_object, vis_params, name):
        """Adds a method for displaying Earth Engine image tiles to folium map."""
        map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
        print("map_id_dict", map_id_dict)
        url = map_id_dict['tile_fetcher'].url_format
        print("url format", url)
        self.Map.add_tile_layer(url, name=name, attribution='Google')
