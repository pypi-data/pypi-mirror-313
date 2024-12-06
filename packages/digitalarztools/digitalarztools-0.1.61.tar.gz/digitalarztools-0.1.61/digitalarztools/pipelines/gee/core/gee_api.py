import json

import geopandas as gpd
from ee.data import getTileUrl

from digitalarztools.pipelines.gee.core.auth import GEEAuth
from digitalarztools.pipelines.gee.core.image import GEEImage


class GEEApi:
    is_initialized = False

    def __init__(self, user=None):
        if user:
            self.is_initialized = GEEAuth.gee_init_users(user)
        else:
            self.is_initialized = GEEAuth.geo_init_personal()

    @classmethod
    def get_aoi_geojson(cls, gdf: gpd.GeoDataFrame):
        geojson = json.loads(gdf.to_json())
        gdf['geometry'] = gdf.geometry.buffer(0.0001)
        return geojson

    def calculate_ndbi(self, gee_img: GEEImage, bands: tuple, name: str = 'ndwi') -> GEEImage:
        """
        :param gee_img:
        :param bands: tuple in the form of (mir_band, nir_band_name) like  ('B6', 'B5') for landsat
        :param name: name for the image
        :return:
        """
        img = gee_img.image.normalizedDifference(bands).rename(name)
        ndwi = GEEImage(img=img)
        return ndwi

    def calculate_ndwi(self, gee_img: GEEImage, bands: tuple, name: str = 'ndwi') -> GEEImage:
        """
        :param gee_img:
        :param bands: tuple in the form of (nir_band_name, green_band_name) like  ('B5', 'B3') for landsat
        :param name: name for the image
        :return:
        """
        img = gee_img.image.normalizedDifference(bands).rename(name)
        ndwi = GEEImage(img=img)
        return ndwi

    def calculate_ndvi(self, gee_img: GEEImage, bands: tuple, name: str = 'ndvi') -> GEEImage:
        """
        :param gee_img:
        :param bands: tuple in the form of (nir_band_name, red_band_name) like  ('B5', 'B4') for landsat
        :param name: name for the image
        :return:
        """
        img = gee_img.image.normalizedDifference(bands).rename(name)
        # nir = self.image.select('B5')
        # red = self.image.select('B4')
        # ndvi = nir.subtract(red).divide(nir.add(red)).rename(name)
        ndvi = GEEImage(img=img)
        # output_image.set_vis_params({min: -1, max: 1, "palette": ['blue', 'white', 'green']})
        # return self.get_image_url(output_image.)
        # ndvi.download_image(name)
        return ndvi

    @staticmethod
    def get_ndvi_tms_url(ndvi_img: GEEImage, is_template=False):
        url = ndvi_img.get_url_template({min: -1, max: 1, "palette": ['blue', 'white', 'green']})
        # if not is_template:
        #     url = f'{url}\{z}/{x}/{y}.png'
        return url

    @staticmethod
    def get_tile_url(img: GEEImage, extent: list, vis_params: dict):
        map_id = img.get_map_id_dict(vis_params)
        z = 18
        x = 0
        y = 0
        url = getTileUrl(map_id, x, y, z)
        return url
