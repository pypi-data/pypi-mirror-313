import datetime
import os

import ee
import pandas as pd
from dateutil import rrule
from geopandas import GeoDataFrame
from tqdm import tqdm

from digitalarztools.adapters.data_manager import DataManager
from digitalarztools.io.file_io import FileIO
from digitalarztools.io.raster.band_process import BandProcess
from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.pipelines.gee.analysis.return_period_analysis import GEEReturnPeriodAnalysis
from digitalarztools.pipelines.gee.core.image_collection import GEEImageCollection
from digitalarztools.pipelines.gee.core.region import GEERegion


class GEETemperatureAnalysis:
    img_collection: ee.ImageCollection
    date_range: (datetime.date, datetime.date)
    region: GEERegion
    band_name: str

    def __init__(self, collection: ee.ImageCollection, date_range: (datetime.date, datetime.date) = None,
                 region: GEERegion = None, band_name: str = None, scale: int = None):
        """
        @param collection:
        @param date_range:
        @param region:
        """
        self.img_collection = collection
        self.date_range = date_range
        self.region = region
        self.band_name = band_name
        self.scale = scale

    @classmethod
    def from_era5_daily_dataset(cls, date_range: (datetime.date, datetime.date),
                                region: GEERegion) -> 'GEETemperatureAnalysis':
        """"
        https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_DAILY_AGGR
        @param date_range: tuple of datetime.date
        @param region: GEERegion object
        """
        band = "temperature_2m"
        era5 = (ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
                .select(band)
                .map(lambda image: image.subtract(273.15).
                     copyProperties(image, ['system:time_start'])))
        temperature = era5.filterDate(date_range[0].strftime('%Y-%m-%d'), date_range[1].strftime('%Y-%m-%d'))
        temperature.filterBounds(region.aoi)
        return cls(temperature, date_range, region, band, 11000)

    @classmethod
    def from_era5_hourly_dataset(cls, date_range: (datetime.date, datetime.date),
                                 region: GEERegion) -> 'GEETemperatureAnalysis':
        """"
        https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_HOURLY
        @param date_range: tuple of datetime.date
        @param region: GEERegion object
        """
        band = "temperature_2m"
        era5 = (ee.ImageCollection("ECMWF/ERA5_LAND/HOURLY")
                .select(band)
                .map(lambda image: image.subtract(273.15).
                     copyProperties(image, ['system:time_start'])))
        temperature = era5.filterDate(date_range[0].strftime('%Y-%m-%d'), date_range[1].strftime('%Y-%m-%d'))
        temperature.filterBounds(region.aoi)
        return cls(temperature, date_range, region, band, 11000)

    @staticmethod
    def calculate_return_period_threshold(return_period_years, df: pd.DataFrame):
        max_temperatures_df = df.groupby('year')['max_temp'].max().reset_index()
        max_temperatures = max_temperatures_df['max_temp'].values.tolist()
        rp_values = GEEReturnPeriodAnalysis.get_return_period_value_using_GEV(max_temperatures, [return_period_years])
        return rp_values[0]

    def process_monthly_temperature(self, monthly_temp_fp: str) -> pd.DataFrame:
        df = GEEImageCollection.get_collection_monthly_stats(self.img_collection,
                                                             region=self.region,
                                                             date_range=self.date_range,
                                                             monthly_fp=monthly_temp_fp,
                                                             band_name=self.band_name, scale=11000)
        return df

    @staticmethod
    def extract_daily_temperature(data_manager: DataManager, date_range: (datetime.date, datetime.date),
                                  selected_gdf: GeoDataFrame, base_raster_path: str,
                                  base_raster_fn: str, name: str = None):
        """
        this function read from downloading images which are available in base_raster_path and have base_raster_fn
                like  fp = os.path.join(base_raster_path, f"{base_raster_fn}_{date_for_raster}.tif")
                :       date is attached with base_raster_fn
        @param data_manager:
        @param date_range:
        @param selected_gdf:
        @param base_raster_path:
        @param base_raster_fn:
        @param name:
        @return:
        """

        date_list = list(rrule.rrule(rrule.DAILY, dtstart=date_range[0], until=date_range[1]))

        for dt in tqdm(date_list, desc="Extracting governorate temperature data"):
            date_for_raster = dt.strftime("%Y%m%d")
            date_for_record = dt.strftime("%Y-%m-%d")

            # Check if the date has already been processed
            if data_manager.record_exists(date_for_record):
                continue

            fp = os.path.join(base_raster_path, f"{base_raster_fn}_{date_for_raster}.tif")

            try:

                geom = selected_gdf[selected_gdf.geometry.name].centroid.values[0]

                # Process raster data
                raster = RioRaster(fp)
                raster.clip_raster(selected_gdf)
                stats = BandProcess.get_summary_data(raster.get_data_array(1))
                stats["date"] = date_for_record
                # if name_column is not None:
                stats["name"] = name
                stats["raster_fp"] = os.path.relpath(fp, base_raster_fn)

                # Add record to the database
                data_manager.add_record(key=date_for_record, record=stats, geom=geom.wkb)

            except Exception as e:
                print(f"Error processing date {date_for_record}: {e}")

        data_manager.close()

    def download_temperature_data(self, base_folder):
        """
        @param base_folder_name:
        @param base_raster_fn:
        @return:
        """
        base_folder = os.path.join(base_folder, "temperature_data")
        base_raster_fn = "temperature_2m"
        FileIO.mkdirs(base_folder)
        GEEImageCollection.download_collection(self.img_collection, self.region,
                                               base_folder, base_raster_fn, self.scale)



        print("download")
        return base_folder
