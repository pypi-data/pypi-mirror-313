from datetime import datetime
from pprint import pprint

import requests


class OpenWeatherMap():
    """
    units information at
    https://openweathermap.org/weather-data
    """
    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def convert_date(unix_time):
        return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d')

    def daily_forecast(self, lon: float, lat: float) -> dict:
        """
        https://docs.openweather.co.uk/api/forecast30
        """
        # url = f"https://pro.openweathermap.org/data/2.5/forecast/climate?lat={lat}&lon={lon}&appid={self.api_key}"
        url = f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt=16&appid={self.api_key}"
        response = requests.get(url)
        res = response.json()
        if response.status_code == 200:
            return res
        pprint(res)
        return dict()

    def one_call(self, lon: float, lat: float) -> dict:
        """
        documentation at : https://openweathermap.org/api/one-call-3
        """
        url = (f"https://api.openweathermap.org/data/3.0/onecall?"
               f"lat={float(lat)}&lon={float(lon)}&appid={self.api_key}"
               f"&units=metric &exclude=minutely")
        # print(url)
        response = requests.get(url)
        res = response.json()
        if response.status_code == 200:
            return res
        pprint(res)
        return dict()
