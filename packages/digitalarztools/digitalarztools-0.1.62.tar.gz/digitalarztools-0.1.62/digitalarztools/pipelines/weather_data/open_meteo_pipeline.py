import json

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


class OpenMeteoPipeline:
    """
        https://open-meteo.com/en/docs#hourly=temperature_2m,relative_humidity_2m,precipitation,rain,snowfall,snow_depth,evapotranspiration,et0_fao_evapotranspiration,wind_speed_10m,wind_direction_10m&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,snowfall_sum,precipitation_hours,wind_speed_10m_max,et0_fao_evapotranspiration&forecast_days=16
        units
        Temperature: Degrees Celsius (°C)
        Rainfall: Millimeters (mm)
        Snowfall: Centimeters (cm)
        Evapotranspiration (ET): Millimeters (mm)
        Soil Moisture: m³/m³ Average soil water content as volumetric mixing ratio
        Wind Speed: Meters per second (m/s) or Km per hour
        Wind Direction: Degrees (°) (measured clockwise from true north)
        Time Format: ISO 8601 format (e.g., "2024-07-17T00:00:00Z" for UTC time)

    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=self.retry_session)
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.params = {
            "latitude": self.y,
            "longitude": self.x,
            "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "rain", "snowfall", "snow_depth",
                       "evapotranspiration", "et0_fao_evapotranspiration", "wind_speed_10m", "wind_direction_10m",
                       "soil_temperature_0cm", "soil_moisture_0_to_1cm", "soil_moisture_1_to_3cm"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "rain_sum", "snowfall_sum",
                      "precipitation_hours", "wind_speed_10m_max", "et0_fao_evapotranspiration"],

            "timezone": "auto",
            "forecast_days": 16,
            "temperature_unit": "celsius",  # Temperature in Celsius
            "precipitation_unit": "mm",  # Precipitation in millimeters
            "wind_speed_unit": "ms",  # Wind speed in meters per second
        }

    def fetch_data(self):
        responses = self.openmeteo.weather_api(self.url, params=self.params)
        response = responses[0]
        return response

    def extract_hourly_data_from_response(self, response):
        hourly = response.Hourly()
        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
            "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
            "precipitation": hourly.Variables(2).ValuesAsNumpy(),
            "rain": hourly.Variables(3).ValuesAsNumpy(),
            "snowfall": hourly.Variables(4).ValuesAsNumpy(),
            "snow_depth": hourly.Variables(5).ValuesAsNumpy(),
            "evapotranspiration": hourly.Variables(6).ValuesAsNumpy(),
            "et0_fao_evapotranspiration": hourly.Variables(7).ValuesAsNumpy(),
            "wind_speed_10m": hourly.Variables(8).ValuesAsNumpy(),
            "wind_direction_10m": hourly.Variables(9).ValuesAsNumpy(),
            "soil_temperature_0cm": hourly.Variables(10).ValuesAsNumpy(),
            "soil_moisture_0_to_1cm": hourly.Variables(11).ValuesAsNumpy(),
            "soil_moisture_1_to_3cm": hourly.Variables(12).ValuesAsNumpy()
        }
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        hourly_json = json.loads(hourly_dataframe.to_json(orient='records', date_format='iso'))
        return hourly_json

    def extract_daily_data_from_response(self, response):
        daily = response.Daily()
        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            ),
            "temperature_2m_max": daily.Variables(0).ValuesAsNumpy(),
            "temperature_2m_min": daily.Variables(1).ValuesAsNumpy(),
            "precipitation_sum": daily.Variables(2).ValuesAsNumpy(),
            "rain_sum": daily.Variables(3).ValuesAsNumpy(),
            "snowfall_sum": daily.Variables(4).ValuesAsNumpy(),
            "precipitation_hours": daily.Variables(5).ValuesAsNumpy(),
            "wind_speed_10m_max": daily.Variables(6).ValuesAsNumpy(),
            "et0_fao_evapotranspiration": daily.Variables(7).ValuesAsNumpy()
        }
        daily_dataframe = pd.DataFrame(data=daily_data)
        daily_json = json.loads(daily_dataframe.to_json(orient='records', date_format='iso'))
        return daily_json

    @staticmethod
    def aggregate_columns(hourly_df: pd.DataFrame, group_by_column: str) -> pd.DataFrame:
        # Group by 6-hour period and calculate statistics
        period_summary = hourly_df.groupby(group_by_column).agg({
            'rain': 'sum',
            'snowfall': 'sum',
            'snow_depth': 'mean',
            'precipitation': 'sum',
            'temperature_2m': ['mean', 'max', 'min'],
            'wind_speed_10m': 'mean',
            'evapotranspiration': 'sum',
            'wind_direction_10m': 'mean',
            'relative_humidity_2m': 'mean',
            'et0_fao_evapotranspiration': 'sum',
            "soil_temperature_0cm": ['mean', 'max', 'min'],
            "soil_moisture_0_to_1cm": 'mean',
            "soil_moisture_1_to_3cm": 'mean'
        }).reset_index()

        # Flatten multi-level column names
        period_summary.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in
                                  period_summary.columns]

        # Rename columns for clarity
        period_summary.rename(columns={
            '6hour_period_': 'date',
            'rain_sum': 'total_rain',
            'snowfall_sum': 'total_snowfall',
            'snow_depth_mean': 'avg_snow_depth',
            'precipitation_sum': 'total_precipitation',
            'temperature_2m_mean': 'avg_temperature',
            'temperature_2m_max': 'max_temperature',
            'temperature_2m_min': 'min_temperature',
            'wind_speed_10m_mean': 'avg_wind_speed',
            'evapotranspiration_sum': 'total_evapotranspiration',
            'wind_direction_10m_mean': 'avg_wind_direction',
            'relative_humidity_2m_mean': 'avg_relative_humidity',
            'et0_fao_evapotranspiration_sum': 'total_et0_fao_evapotranspiration',
            'soil_temperature_0cm_mean': 'avg_soil_temperature',
            'soil_temperature_0cm_max': 'max_soil_temperature',
            'soil_temperature_0cm_min': 'min_soil_temperature',
            'soil_moisture_0_to_1cm_mean': 'avg_soil_moisture_1cm',
            'soil_moisture_1_to_3cm':'avg_soil_moisture_3cm'

        }, inplace=True)

        return period_summary

    @classmethod
    def calculate_6hourly_stats_from_hourly_data(cls, hourly_df: pd.DataFrame) -> pd.DataFrame:
        # Ensure 'date' column is datetime
        hourly_df['date'] = pd.to_datetime(hourly_df['date'])

        # Create a new column representing each 6-hour period
        hourly_df['6hour_period'] = (hourly_df['date'].dt.floor('6H'))
        period_summary = cls.aggregate_columns(hourly_df, '6hour_period')
        return period_summary

    @classmethod
    def calculate_daily_stats_from_hourly_data(cls, hourly_df: pd.DataFrame) -> pd.DataFrame:
        # Convert date column to datetime
        hourly_df['date'] = pd.to_datetime(hourly_df['date'])

        # Extract date without time
        hourly_df['day'] = hourly_df['date'].dt.date

        day_summary = cls.aggregate_columns(hourly_df, 'day')
        return day_summary
