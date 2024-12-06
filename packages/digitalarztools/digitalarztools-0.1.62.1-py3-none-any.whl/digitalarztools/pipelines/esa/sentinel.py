# from sentinelsat import SentinelAPI
import os.path

import asf_search as asf
import geopandas as gpd
import pandas as pd
from tqdm import tqdm
import requests
from requests.auth import HTTPBasicAuth
import getpass


class Sentinel(object):
    def __init__(self, username, password):
        """
            # username = 'your_username'
            # password = 'your_password'
        """
        # Create SentinelAPI instance
        # self.api = SentinelAPI(username, password, 'https://scihub.copernicus.eu/dhus')
        self.search_res_gdf = None
        self.session = asf.ASFSession()
        self.session.auth_with_creds(username, password)

    # Function to download Sentinel-1 data using sentinelsat
    def download_sentinel1(self, aoi_wkt: str, date_range: tuple, output_folder: str):
        """
        # Define parameters
        aoi: area of interest in WKT
        date_range: tuple of start and end date in YYYY-MM-DD like ('2021-01-01', '2021-12-31')
        """
        results = asf.geo_search(platform=[asf.PLATFORM.SENTINEL1], intersectsWith=aoi_wkt,
                                 start=date_range[0], end=date_range[1])
        # geojson = {
        #     "type": "FeatureCollection",
        #     "features": [
        #         {
        #             "geometry": data.geometry,
        #             "properties": {
        #                 **data.properties,
        #                 **{f"meta_{key}": value for key, value in data.meta.items()}
        #             }
        #         }
        #         for data in results.data
        #     ]
        #
        # }
        # self.search_res_gdf = gpd.GeoDataFrame.from_features(geojson)
        # urls = [data.umm['RelatedUrls'][0]['URL'] for data in results.data]
        i = 0
        for data in tqdm(results.data, desc='Downloading files'):
            if i == 3:
                break
            url = data.umm['RelatedUrls'][0]['URL']
            asf.download_url(url, path=output_folder , session=self.session)
            i = i + 1
        # asf.download_urls(urls=urls[:2],path=output_folder, session=self.session)

    @staticmethod
    def download_sentinel1_using_asf(aoi_wkt: str):

        # Enter your ASF API credentials
        username = input("Enter your ASF username: ")
        password = getpass.getpass("Enter your ASF password: ")

        # Define your Area of Interest (AOI)
        # Example using WKT:
        # aoi_wkt = "POLYGON((lon1 lat1, lon2 lat2, lon3 lat3, lon4 lat4, lon1 lat1))"
        # or use a GeoJSON file, shapefile, etc.

        # ASF API endpoint for searching data
        search_url = "https://api.daac.asf.alaska.edu/services/search/param"

        # Search parameters
        search_params = {
            "platform": "Sentinel-1",
            "processingLevel": "SLC",
            "beamMode": "IW",
            "start": "2022-01-01T00:00:00",
            "end": "2022-12-31T23:59:59",
            "intersectsWith": aoi_wkt,
        }

        # Send a POST request to the ASF API for search
        response = requests.post(search_url, json=search_params, auth=HTTPBasicAuth(username, password))

        # Check if the search was successful
        if response.status_code == 200:
            # Extract the product IDs from the response
            product_ids = [entry["downloadUrl"].split("/")[-1] for entry in response.json()["results"]]

            # Download the products
            for product_id in product_ids:
                download_url = f"https://api.daac.asf.alaska.edu/services/data/{product_id}"
                print(f"Downloading product {product_id}...")
                product_response = requests.get(download_url, auth=HTTPBasicAuth(username, password))

                # Save the product to a file (adjust file path as needed)
                with open(f"{product_id}.zip", "wb") as file:
                    file.write(product_response.content)
        else:
            print(f"Failed to search for data. Status code: {response.status_code}")
            print(response.text)



    def get_sentinel1_meta_data(self, product_id: str):
        product_metadata = self.api.get_product_odata(product_id)
        return product_metadata

    def get_sentinel1_wavelength(self, product_metadata):
        return product_metadata['radarInstrument']['wavelength']

    def get_sentinel1_pixel_size(self, product_metadata):
        return product_metadata['grid']['pixelSize']

