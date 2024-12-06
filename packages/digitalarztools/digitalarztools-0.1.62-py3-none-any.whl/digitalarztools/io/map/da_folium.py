import ee
import folium


class DAFolium(folium.Map):

    def __init__(self, location=None, zoom_start=10, tiles='OpenStreetMap', **kwargs):
        # Call the constructor of the base class (folium.Map)
        super().__init__(location=location, zoom_start=zoom_start, tiles=tiles, **kwargs)


    def add_layer_control(self):
        # Add a layer control panel to the map.
        self.add_child(folium.LayerControl())

    # Define a method for displaying Earth Engine image tiles to folium map.
    def add_ee_layer(self, ee_image_object, vis_params, name):
        map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
        folium.raster_layers.TileLayer(
            tiles=map_id_dict['tile_fetcher'].url_format,
            attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
            name=name,
            overlay=True,
            control=True
        ).add_to(self)
