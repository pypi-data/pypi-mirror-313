import os

import ee

from digitalarztools.io.file_io import FileIO
from digitalarztools.pipelines.gee.core.auth import GEEAuth
from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.image_collection import GEEImageCollection
from digitalarztools.pipelines.gee.core.region import GEERegion


class GEESentinel:
    def __init__(self, gee_auth: GEEAuth = None):
        if gee_auth is None:
            self.gee_auth = GEEAuth.gee_init_browser()
        else:
            self.gee_auth = gee_auth

    def get_image_collection(self, region: GEERegion, date_range: tuple, sensor_no: int):
        """
        sentinel 1 image collection
        :param region:
        :param date_range: tuple ('2020-01-01', '2020-04-01')
        """
        if self.gee_auth.is_initialized:
            if sensor_no == 1:
                sentinel = (ee.ImageCollection('COPERNICUS/S1_GRD')
                             .filterBounds(region.bounds)
                             .filterDate(date_range[0], date_range[1])
                             .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
                             .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
                             .filter(ee.Filter.eq('instrumentMode', 'IW'))
                             .sort('system:time_start'))
            if sensor_no==2:
                # Load Sentinel-2 data and sort by date in ascending order
                sentinel = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                             .filterBounds(region.bounds)
                             .filterDate(date_range[0], date_range[1])
                             .sort('system:time_start'))
            return GEEImageCollection(sentinel)

    def download_sentinel_1(self, region: GEERegion, date_range: tuple, output_folder: str):
        """
        Download sentinel 1
        :param region:
        :param date_range: tuple ('2020-01-01', '2020-04-01')
        :output_folder: path to save
        """
        if self.gee_auth.is_initialized:
            print("Downloading Sentinel")
            dir_path = FileIO.mkdirs(output_folder)
            img_collection = self.get_image_collection(region, date_range, sensor_no=1)
            gee_image: GEEImage = None
            for i, gee_image in img_collection.enumerate_collection():
                id = gee_image.get_gee_id()
                # band_names = gee_image.get_band_names()
                # for band_name in band_names:
                #     gee_band = GEEImage(gee_image.image.select(band_name))
                #     fp = os.path.join(output_folder, f"{id} {band_name}.tif")
                #     print(f"Downloading {band_name} of {id}")
                fp = os.path.join(output_folder, 'sentinel_1', f"{id}.tif")
                if not os.path.exists(fp):
                    gee_image.download_image(fp, region, 10, 16, within_aoi_only=False)

    def download_sentinel_2(self, region: GEERegion, date_range: tuple, output_folder: str, is_rgb=False):
        """
        Download sentinel 1
        :param region:
        :param date_range: tuple ('2020-01-01', '2020-04-01')
        :output_folder: path to save
        """
        if self.gee_auth.is_initialized:
            print("Downloading Sentinel")
            dir_path = FileIO.mkdirs(output_folder)
            img_collection = self.get_image_collection(region, date_range,sensor_no=2)
            if is_rgb:
                img_collection = img_collection.select_bands(['B2', 'B3', 'B4'])  # BGR

            gee_image: GEEImage = None
            for i, gee_image in img_collection.enumerate_collection():
                id = gee_image.get_gee_id()


                # for band_name in band_names:
                #     gee_band = GEEImage(gee_image.image.select(band_name))
                #     fp = os.path.join(output_folder, f"{id} {band_name}.tif")
                #     print(f"Downloading {band_name} of {id}")
                fp = os.path.join(output_folder, "sentinel_2", f"{id}.tif")
                if not os.path.exists(fp):
                    gee_image.download_bands(fp,region)
                    gee_image.download_image(fp, region, 10, 16, within_aoi_only=False)
