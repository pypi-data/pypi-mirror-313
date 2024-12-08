import datetime
import enum
import json
import os
import traceback

import ee
import pandas as pd
from geopandas import GeoDataFrame
from tqdm import tqdm

from digitalarztools.pipelines.gee.analysis.return_period_analysis import GEEReturnPeriodAnalysis
from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.image_collection import GEEImageCollection
from digitalarztools.pipelines.gee.core.region import GEERegion

class GEEPrecipitationDataset(enum.Enum):
    CHIRPS = { "tag": 'UCSB-CHG/CHIRPS/DAILY', "scale": 5000, "band_name":'precipitation'}
    ERA5 = {"tag": "ECMWF/ERA5_LAND/DAILY_AGGR","scale": 11000, "band_name": "total_precipitation_sum"}
class GEEPrecipitationAnalysis():
    image_collection: ee.ImageCollection
    date_range: (datetime.date, datetime.date)
    region: GEERegion
    dataset: GEEPrecipitationDataset

    def __init__(self, collection: ee.ImageCollection, dataset: GEEPrecipitationDataset, date_range: (datetime.date, datetime.date) = None,
                 region: GEERegion = None):
        """
        @param collection:
        @param date_range:
        @param region:
        """
        self.img_collection = collection
        self.date_range = date_range
        self.region = region
        self.dataset = dataset

    @classmethod
    def from_era5_daily_dataset(cls, date_range: (datetime.date, datetime.date),
                                region: GEERegion) -> 'GEEPrecipitationAnalysis':
        """"
        https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_DAILY_AGGR
        @param date_range: tuple of datetime.date
        @param region: GEERegion object
        """
        dataset = GEEPrecipitationDataset.ERA5
        era5 = (ee.ImageCollection(dataset.value["tag"])
                .select(dataset.value["band_name"]))
        precipitation = era5.filterDate(date_range[0].strftime('%Y-%m-%d'), date_range[1].strftime('%Y-%m-%d'))
        precipitation.filterBounds(region.aoi)
        return cls(precipitation, dataset, date_range,  region)

    @classmethod
    def from_chirps2_daily_dataset(cls, date_range: (datetime.date, datetime), region: GEERegion) -> 'GEEPrecipitationAnalysis':
        """

        @param date_range:
        @param region: GEERegion
        @return:
        """
        dataset = GEEPrecipitationDataset.CHIRPS
        aoi = region.aoi
        dates = ee.Filter.date(date_range[0].strftime('%Y-%m-%d'), date_range[1].strftime('%Y-%m-%d'))
        chirps = (ee.ImageCollection(dataset.value["tag"])
                   .filter(dates)
                   .filterBounds(aoi).select(dataset.value["band_name"]))
        # size = GEEImageCollection(precipitation).get_collection_size()
        # print("collection size", size)
        return cls(chirps, dataset, date_range,region)

    def extract_monthly_temperature(self, monthly_temp_fp: str) -> pd.DataFrame:
        """"
        Method to extract monthely precipitation data from the dataset
        """

        df = GEEImageCollection.get_collection_monthly_stats(self.img_collection,
                                                             region=self.region,
                                                             date_range=self.date_range,
                                                             monthly_fp=monthly_temp_fp,
                                                             band_name=self.dataset.value["band_name"],
                                                             scale=self.dataset.value["scale"])
        return df

    @staticmethod
    def calculate_return_period_threshold(return_period_years, df: pd.DataFrame):
        max_temperatures_df = df.groupby('year')['max'].max().reset_index()
        max_temperatures = max_temperatures_df['max'].values.tolist()
        rp_values = GEEReturnPeriodAnalysis.get_return_period_value_using_GEV(max_temperatures, [return_period_years])
        return rp_values[0]