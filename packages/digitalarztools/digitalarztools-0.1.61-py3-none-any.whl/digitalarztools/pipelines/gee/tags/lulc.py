import os

import ee
import geopandas as gpd
from pyproj import CRS

from digitalarztools.adapters.data_manager import DataManager
from digitalarztools.io.file_io import FileIO
from digitalarztools.io.vector.gpd_vector import GPDVector

from digitalarztools.pipelines.gee.core.feature_collection import GEEFeatureCollection
from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.image_collection import GEEImageCollection
from digitalarztools.pipelines.gee.core.region import GEERegion



class GEELandUseLandCover:
    def __init__(self):
        pass

    @staticmethod
    def download_google_buildings_zxy_tiles(aoi_gdf: gpd.GeoDataFrame, base_folder:str, initial_zoom: int):

        open_buildings = ee.FeatureCollection('GOOGLE/Research/open-buildings/v3/polygons')
        # region = GEERegion.from_gdv(GPDVector(aoi_gdf))
        gee_fc = GEEFeatureCollection(open_buildings)
        gee_fc.download_feature_zxy_tiles(aoi_gdf, base_folder, initial_zoom)


    @staticmethod
    def get_google_buildings(region: GEERegion,) -> gpd.GeoDataFrame:
        open_buildings = ee.FeatureCollection('GOOGLE/Research/open-buildings/v3/polygons')
        gee_fc = GEEFeatureCollection(open_buildings, region)

        features_list = gee_fc.get_feature_list(region.bounds)
        gdf = GPDVector.from_geojson(features_list, crs= CRS.from_epsg(4326))
        return gdf

    @staticmethod
    def esa_world_cover_using_gee(region: GEERegion) -> GEEImage:
        """
        Extreact latest ESA world cover data (10m) from GEE. The details can be seen at
        https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200#description
            10	006400	Tree cover
            20	ffbb22	Shrubland
            30	ffff4c	Grassland
            40	f096ff	Cropland
            50	fa0000	Built-up
            60	b4b4b4	Bare / sparse vegetation
            70	f0f0f0	Snow and ice
            80	0064c8	Permanent water bodies
            90	0096a0	Herbaceous wetland
            95	00cf75	Mangroves
            100	fae6a0	Moss and lichen

        :param region:
        :return:
        """
        # if gee_auth.is_initialized:
        # date_range = (start_date, end_date)
        img_collection = (ee.ImageCollection('ESA/WorldCover/v200')
                          .filterBounds(region.bounds))
        img_collection = GEEImageCollection(img_collection)
        return GEEImage(img_collection.get_image('latest'))
        # else:
        #     da_logger.error("Please initialized GEE before further processing")
