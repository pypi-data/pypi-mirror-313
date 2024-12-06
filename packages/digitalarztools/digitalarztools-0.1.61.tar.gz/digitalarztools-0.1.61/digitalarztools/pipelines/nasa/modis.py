import os
from datetime import date, datetime, timedelta
import requests
from modis_tools.auth import ModisSession
from modis_tools.granule_handler import GranuleHandler
from modis_tools.resources import CollectionApi, GranuleApi
from pyproj import Proj, transform
from requests.auth import HTTPBasicAuth


class Modis:
    @staticmethod
    def earthdata_login(username: str, password: str) -> requests.Session:
        session = requests.Session()
        auth_url = 'https://urs.earthdata.nasa.gov/login'
        login_url = 'https://urs.earthdata.nasa.gov/oauth/authorize'

        auth_data = {
            'client_id': 'YOUR_CLIENT_ID',
            'response_type': 'code',
            'redirect_uri': 'https://urs.earthdata.nasa.gov/home',
            'state': 'your_state',
            'username': username,
            'password': password,
        }

        response = session.post(auth_url, data=auth_data)
        response.raise_for_status()

        return session

    @staticmethod
    def latlon_to_modis_tile(lat, lon):
        # Convert latitude and longitude to MODIS sinusoidal projection coordinates
        modis_proj = Proj(init='epsg:4326')
        modis_x, modis_y = transform(modis_proj, {'proj': 'sinu', 'lon_0': 0, 'x_0': 0, 'y_0': 0}, lon, lat)

        # Calculate MODIS tile coordinates (h, v)
        tile_h = int((modis_x + 1111950.519667) / 1111950.519667)
        tile_v = int((modis_y + 1111950.519667) / 1111950.519667)

        return tile_h, tile_v

    @staticmethod
    def download_modis_data(session, year, day_of_year, tile_h, tile_v, output_dir) -> str:
        url = f'https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/6/MOD13Q1/{year}/{day_of_year:03d}/MOD13Q1.A{year}{day_of_year:03d}.h{tile_h:02d}v{tile_v:02d}.006.NDVI.006.hdf'
        filename = f'MOD13Q1_A{year}{day_of_year:03d}_h{tile_h:02d}v{tile_v:02d}_006_NDVI.hdf'
        fp = os.path.join(output_dir, filename)
        if not os.path.exists(fp) and session is not None:
            # response = requests.get(url, stream=True)
            # with open(fp, 'wb') as file:
            #     for chunk in response.iter_content(chunk_size=128):
            #         file.write(chunk)
            # response = requests.get(url, stream=True)
            # response.raise_for_status()
            response = session.get(url, stream=True)
            response.raise_for_status()

            with open(fp, 'wb') as file:
                for chunk in response.iter_content(chunk_size=128):
                    if chunk:
                        file.write(chunk)

        print(f'Downloaded: {filename}')
        return fp

    def execute_download(self, extent_in_4326, output_dir, username: str, password: str, start_date=None,
                         end_date=None):
        # Bounding box for Pakistan
        # extent = [23.6345, 60.872, 37.0841, 77.8375]  # [min_lat, min_lon, max_lat, max_lon]

        # Determine MODIS tiles for the bounding box
        tile_min_h, tile_min_v = self.latlon_to_modis_tile(extent_in_4326[0], extent_in_4326[1])
        tile_max_h, tile_max_v = self.latlon_to_modis_tile(extent_in_4326[2], extent_in_4326[3])

        if start_date is None or end_date is None:
            # Define the date range
            # start_date = datetime(2022, 1, 1)
            # end_date = datetime(2022, 12, 31)
            end_date = date.today()
            start_date = (end_date - timedelta(days=7))
        # session = self.earthdata_login(username, password)
        # # Iterate over each day in the date range
        # current_date = start_date
        # while current_date <= end_date:
        #     year = current_date.year
        #     day_of_year = current_date.timetuple().tm_yday
        #
        #     # Download MODIS data for each tile within the specified bounding box
        #     file_paths = []
        #     for tile_h in range(tile_min_h, tile_max_h + 1):
        #         for tile_v in range(tile_min_v, tile_max_v + 1):
        #             fp = self.download_modis_data(session, year, day_of_year, tile_h, tile_v, output_dir)
        #             file_paths.append(fp)
        #     current_date += timedelta(days=1)
        #     return file_paths

        # Authenticate a session
        session = ModisSession(username=username, password=password)

        # Query the MODIS catalog for collections
        collection_client = CollectionApi(session=session)
        collections = collection_client.query(short_name="MCD19A1", version="061")
        # Query the selected collection for granules
        granule_client = GranuleApi.from_collection(collections[0], session=session)

        extent_granules = granule_client.query(start_date=start_date.strftime('%Y-%m-%d'),
                                               end_date=end_date.strftime('%Y-%m-%d'),
                                               bounding_box=list(extent_in_4326))

        # Download the granules
        paths = GranuleHandler.download_from_granules(extent_granules, session, ext='hdf', force=False, path=output_dir)

        print(f'Downloaded', paths)
        return paths