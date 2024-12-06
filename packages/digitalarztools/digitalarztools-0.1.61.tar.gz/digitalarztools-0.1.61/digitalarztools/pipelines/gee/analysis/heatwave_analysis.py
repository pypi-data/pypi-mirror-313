import json
import os
from datetime import date, timedelta
from pprint import pprint

import ee
import pandas as pd
from geopandas import GeoDataFrame
from tqdm import tqdm

from digitalarztools.io.file_io import FileIO
from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.image_collection import GEEImageCollection
from digitalarztools.pipelines.gee.core.region import GEERegion


class GEEHeatWaveAnalysis:
    def __init__(self, daily_temp_img_collection: ee.ImageCollection, region: GEERegion):
        self.daily_temp_img_collection = daily_temp_img_collection
        self.region = region

    @staticmethod
    def identify_heat_wave_days(img_collection: ee.ImageCollection, threshold):
        def identify(image):
            heatWaveDay = image.gt(ee.Number(threshold))  # Identify pixels exceeding threshold
            return heatWaveDay.rename('heat_wave_day').copyProperties(image, ['system:time_start'])

        return img_collection.map(identify)

    @staticmethod
    def aggregate_heat_wave_days(heat_wave_days_collection: ee.ImageCollection):
        def aggregate(current, previous):
            previous_image = ee.Image(previous)
            current_image = ee.Image(current)
            current_heat_wave_day = current_image.select('heat_wave_day')
            cumulative_heat_wave_days = current_heat_wave_day.add(previous_image)
            return cumulative_heat_wave_days.set('system:time_start', current_image.get('system:time_start'))

        # Create an initial image with all values set to zero and ensure the band name is consistent
        initial_image = ee.Image(0).rename('heat_wave_day')

        # Use the iterate function to apply the aggregation function to the image collection
        aggregated_result = heat_wave_days_collection.iterate(aggregate, initial_image)

        # Convert the result to an ImageCollection
        aggregated_collection = ee.ImageCollection([ee.Image(aggregated_result)])

        # If you need to print stats, handle it outside the iteration
        # def print_stats(image):
        # stats = GEEImage.get_image_stats(aggregated_collection.first(), 11000)
        # print("Cumulative heat wave stats: ", stats)

        # Map the print_stats function over the aggregated collection
        # aggregated_collection.map(print_stats)

        # Return the aggregated collection
        return aggregated_collection

    def execute_heat_waves(self, threshold, date_range:tuple) -> ee.Image:
        # dataset = self.temperature_analysis.get_daily_max_temperature_collection()
        yearly_data = self.daily_temp_img_collection.filterDate(date_range[0],date_range[1])

        heat_wave_days = self.identify_heat_wave_days(yearly_data, threshold)
        heat_wave_periods = self.aggregate_heat_wave_days(heat_wave_days)

        gee_img_coll = GEEImageCollection(heat_wave_periods)
        gee_img = gee_img_coll.get_image('max')
        gee_img = gee_img.clip(self.region.aoi)
        # stats = GEEImage.get_image_stats(gee_img, scale)
        # print(stats)

        return gee_img

    # def execute_heat_waves_in_gpd(self, boundaries_gpd: GeoDataFrame, image_stats_fp: str, threshold: float):
    #     df = GEEImageCollection.get_all_image_stats(self.daily_temp_img_collection, boundaries_gpd, image_stats_fp, scale=11000, band_names=['temperature_2m'])
    #     print(df.head())
    #     print(threshold)
