import ee
import numpy as np
import pandas as pd
from scipy.stats import genextreme, gumbel_r
from tqdm import tqdm

from digitalarztools.pipelines.gee.core.feature_collection import GEEFeatureCollection
from digitalarztools.pipelines.gee.core.region import GEERegion
from digitalarztools.utils.unit_conversion import TemperatureConverter


class GEEReturnPeriodAnalysis:

    @staticmethod
    def get_annual_maxima(data: ee.ImageCollection, year):
        """

        @param data:  ee.ImageCollection
        @param year:   like range(2000, 2024)
        @return:
        """
        return data.filter(ee.Filter.calendarRange(year, year, 'year')).reduce(ee.Reducer.max())

    @staticmethod
    def get_monthly_maxima(data: ee.ImageCollection, year: int, gee_region: GEERegion, property_name) -> list:
        monthly_maxima = []
        for month in range(1, 13):
            try:
                filtered_data = data.filter(ee.Filter.calendarRange(year, year, 'year')) \
                    .filter(ee.Filter.calendarRange(month, month, 'month'))
                monthly_max = filtered_data.reduce(ee.Reducer.max()).sampleRegions(gee_region.aoi, scale=11132)

                # Extract max temperature_2m_max value
                feature_collection = monthly_max.getInfo()
                max_values = GEEFeatureCollection.get_max_value(feature_collection, property_name)
                monthly_maxima.append({"year": year, "month": month, "value": max_values})
            except Exception as e:
                # print(f"Error retrieving data for year {year}, month {month}: {e}")
                max_values = 0
        return monthly_maxima

    @staticmethod
    def get_return_period_value_using_gumbel(max_values: list, return_periods: list):
        """
        Calculate value against return period using gumbel distribution
        @param max_values: list of maximum values
        @param return_periods: list of return periods like [2, 5, 10, 20, 50, 100]
        @return:
        """
        # Fit Gumbel distribution
        params = gumbel_r.fit(max_values)
        return_levels = gumbel_r.ppf(1 - 1 / np.array(return_periods), *params)
        return return_levels

    @staticmethod
    def get_return_period_value_using_GEV(max_values: list, return_periods: list):
        """
        calculate value against return periods using Generalized Extreme Value (GEV) distribution
        @param max_values: list of maximum values
        @param return_periods: list of return periods like [2, 5, 10, 20, 50, 100]
        @return:
        """
        # Fit GEV distribution
        params = genextreme.fit(max_values)
        return_levels = genextreme.ppf(1 - 1 / np.array(return_periods), *params)
        return return_levels

    @classmethod
    def rp_value_using_ERA5_daily_aggregated(cls, year_range: tuple, region: GEERegion, band_info: dict,
                                             return_periods: list = None):
        """
        https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_DAILY_AGGR
        https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_HOURLY
        https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_MONTHLY_AGGR
        dataset_name is "ERA5-Land Hourly - ECMWF Climate Reanalysis"
        @param year_range:   tuple (start_year, eng_year)  (2000,2023)
        @param region:
        @param band_info: {'band_name":"xyz", "stats":"max"}
        @param return_periods:
        @return: data DataFrame and rp DataFrame
        """
        if return_periods is None:
            return_periods = [2, 5, 10, 20, 50, 100]
        years = range(year_range[0], year_range[1])
        start_date = f"{year_range[0]}-01-01"
        end_date = f"{year_range[1]}-12-31"
        # band_name = 'temperature_2m'
        # Get temperature data from ERA5
        # temperature_data = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY') \
        temperature_data = ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR") \
            .select(band_info["band_name"]) \
            .filterDate(start_date, end_date) \
            .filterBounds(region.aoi)

        # maxima = [{"year": year, "value": cls.get_annual_maxima(temperature_data, year).sampleRegions(region.aoi,
        #                                                                                               scale=1000).getInfo()}
        #           for year in years]

        maxima = []
        for year in years:
            print("working on year:", year)
            monthly_maxima = cls.get_monthly_maxima(temperature_data, year, region,
                                                    property_name=band_info["band_name"])
            print(monthly_maxima)
            maxima += monthly_maxima  # Concatenate the values (lists) into maxima

        # Convert to DataFrame for analysis
        data_df = pd.DataFrame(maxima)

        # Convert the 'value' column to numeric in case it's not
        data_df['value'] = pd.to_numeric(data_df['value'])
        data_df["value"] = data_df["value"].apply(lambda x: TemperatureConverter.kelvin_to_celsius(x))
        data_df['unit'] = "Celsius"

        max_temperatures_df = data_df.groupby('year')['value'].max().reset_index()
        max_temperatures = max_temperatures_df['value'].values.tolist()

        rp_values = cls.get_return_period_value_using_GEV(max_temperatures, return_periods)
        rp_df = pd.DataFrame({"return_period": return_periods, "value": rp_values})
        return data_df, rp_df

    @classmethod
    def rp_value_using_CHIRPS(cls, year_range: tuple, gee_region: GEERegion, return_periods=None):

        if return_periods is None:
            return_periods = [2, 5, 10, 20, 50, 100]

        years = range(year_range[0], year_range[1])
        start_date = f"{year_range[0]}-01-01"
        end_date = f"{year_range[1]}-12-31"
        band_name = 'precipitation'
        img_collection = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY") \
            .select(band_name) \
            .filterDate(start_date, end_date) \
            .filterBounds(gee_region.aoi)

        maxima = []
        for year in tqdm(years, desc=f'"year progress', leave=False):
            # print("working on year:", year)
            monthly_maxima = cls.get_monthly_maxima(img_collection, year, gee_region,
                                                    property_name=band_name)
            # print('monthly maxima:', monthly_maxima)
            maxima += monthly_maxima  # Concatenate the values (lists) into maxima

        # print(maxima)
        # Convert to DataFrame for analysis
        data_df = pd.DataFrame(maxima)

        try:
            data_df['value'] = pd.to_numeric(data_df['value'])
            data_df['band'] = band_name
            data_df['unit'] = "mm/d"
            print(data_df.head())
            max_temperatures_df = data_df.groupby('year')['value'].max().reset_index()
            max_temperatures = max_temperatures_df['value'].values.tolist()

            rp_values = cls.get_return_period_value_using_GEV(max_temperatures, return_periods)
            rp_df = pd.DataFrame({"return_period": return_periods, "value": rp_values})
            return data_df, rp_df
        except KeyError:
            print("The column 'value' does not exist in the DataFrame.")
            return None, None
