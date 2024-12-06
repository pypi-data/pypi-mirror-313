### https://search.asf.alaska.edu/
import os.path
import traceback
from urllib.parse import urlencode
import geopandas as gpd
import asf_search as asf

from datetime import date

import numpy as np
import requests
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

from digitalarztools.io.file_io import FileIO
from digitalarztools.io.raster.rio_process import RioProcess
from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.io.vector.gpd_vector import GPDVector
from digitalarztools.utils.logger import da_logger


class ALOSUtils:
    """
    downloading and processing ALOS Palser data using asf (Alaska Satellite Facility: making remote-sensing data accessibl)
    https://search.asf.alaska.edu/
    """

    @staticmethod
    def get_date_range(no_of_months: int, rel_date=date.today(), is_end=True):
        if is_end:
            end_date = rel_date
            start_date = end_date + relativedelta(months=-no_of_months)
        else:
            start_date = rel_date
            end_date = start_date + relativedelta(months=+no_of_months)
        return start_date, end_date

    @classmethod
    def download_alos_palsar(cls, aoi: GPDVector, aoi_name: str, aoi_buffer: int) -> RioRaster:
        """
        :param aoi:  area of interest as GPDVector
        :param aoi_name: name of the area of interest
        :param aoi_buffer: buffer size in meter for cliping
        :return: DEM as RioRaster
        """
        EARTHSAT_USER = ""
        EARTHSAT_PASSWORD = ""
        MEDIA_DIR = os.path.join(os.path.dirname(__file__), '../media')
        output_path = os.path.join(MEDIA_DIR, 'alos_palsar_data')

        img_des = os.path.join(output_path, f"alos_dem_{aoi_name.lower().replace(' ', '_')}.tif")
        gpkg_file = os.path.join(output_path, f'aoi_{aoi_name}.gpkg')
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        if not os.path.exists(img_des):
            urls = cls.get_dem_urls(aoi, gpkg_file)
            session = asf.ASFSession()
            session.auth_with_creds(EARTHSAT_USER, EARTHSAT_PASSWORD)
            required_fn = []
            for i in tqdm(range(len(urls)), desc='ALOS PALSAR Downloading'):
                required_fn.append(urls[i].split("/")[-1])
                if not os.path.exists(os.path.join(output_path, required_fn[-1])):
                    da_logger.warning(f"\ndownloading:{urls[i]}")
                    asf.download_url(url=urls[i], path=output_path, session=session)
            da_logger.critical("\n Downloading finished")
            dem_raster = cls.extract_and_process_data(required_fn, output_path, aoi_name)
            aoi_buffer = aoi.apply_buffer(aoi_buffer)
            dem_raster = dem_raster.clip_raster(aoi_buffer.gdf, aoi.get_crs())
            dem_raster.change_datatype(new_dtype=np.float32)
            dem_raster.save_to_file(img_des)
            da_logger.critical(f"Alos palsar data downloaded at {img_des}")
        return RioRaster(img_des)

    @staticmethod
    def extract_and_process_data(file_list, output_path: str, aoi_name: str) -> RioRaster:
        # file_list = FileIO.get_files_list_in_folder(output_path, "zip")
        extracted_folder = os.path.join(output_path, f'{aoi_name}')
        for fp in file_list:
            fp = os.path.join(output_path, fp)
            try:
                fn = os.path.basename(fp)
                out_folder = FileIO.extract_zip_file(fp, output_path)
                src_folder = os.path.join(out_folder, f"{fn[:-4]}")
                src_file = os.path.join(src_folder, f"{fn[:-3]}dem.tif")
                if not os.path.exists(extracted_folder):
                    os.makedirs(extracted_folder)
                FileIO.copy_file(src_file, extracted_folder)
                FileIO.delete_folder(src_folder)
            except Exception as e:
                da_logger.error(f"error:{fp}")

        rio_raster = RioProcess.mosaic_images(extracted_folder)
        FileIO.delete_folder(extracted_folder)
        return rio_raster

    @classmethod
    def get_dem_urls(cls, aoi: GPDVector, gpkg_fp: str, layer='alos_palsar_dem') -> gpd.GeoDataFrame:
        if not os.path.exists(gpkg_fp):
            dir_name = FileIO.mkdirs(gpkg_fp)
            aoi = aoi.to_4326()
            da_logger.debug("Searching for ALOS Palsar data")
            # start_date, end_date = cls.get_date_range(18)
            # geom : Polygon = aoi.get_unary_union()
            # geom = geom.envelope
            # search_params = {
            #     'intersectsWith': geom.wkt,
            #     'platform':"SRTM",  #'ALOS', "SRTM",
            #     # 'instrument': asf.PALSAR, #'PALSAR',
            #     "output": "json"
            #     # 'processingLevel': [
            #     #     'RTC_LOW_RES',
            #     #     'RTC_HI_RES'
            #     # ],
            #     # 'flightDirection': 'Descending',
            #     # 'maxResults': 250
            #     # 'start': start_date,
            #     # 'end': end_date
            # }

            # Set up the ASF Geospatial Search API URL
            api_url = "https://api.daac.asf.alaska.edu/services/search/param"
            # Define a bounding box for the KSA region (adjust coordinates as needed)
            # bounding_box = [34.4959, 35.9402, 38.4110, 39.1201]  # [min_lon, min_lat, max_lon, max_lat]
            bounding_box = aoi.total_bounds
            # Set the search parameters for the specified bounding box and ALOS PALSAR DEM
            search_params = {
                "bbox": ",".join(map(str, bounding_box)),
                "platform": "ALOS",
                "processingLevel": "L1.5",
                "beamMode": "FBS",
                "output": "json"
            }

            full_url = f"{api_url}?{urlencode(search_params)}"
            # results = asf.geo_search(**search_params)
            try:
                # Make a GET request to the ASF Geospatial Search API
                response = requests.get(full_url)
                response.raise_for_status()

                # Parse the JSON response
                data = response.json()

                # Check if any scenes were found
                if len(data) == 0:
                    print("No ALOS PALSAR DEM data found for the specified region in KSA.")
                    return
                # res_gdf = gpd.read_file(str(data), driver='GeoJSON')
                # res_gdf = gpd.GeoDataFrame(data[0])
                res_gdv = GPDVector.from_xy(data[0], x_col='centerLon', y_col='centerLat')
                if not res_gdv.empty:
                    res_gdv = res_gdv.within_aoi(aoi)
                    # res_gdf = res_gdf.sort_values('startTime', ascending=False).drop_duplicates(['geometry'])
                    # res_gdf.drop_duplicates()
                    # res_df['startTime'] = res_df['startTime'].apply(lambda a: pd.to_datetime(a).date())
                    # res_df['stopTime'] = res_df['stopTime'].apply(lambda a: pd.to_datetime(a).date())
                    res_gdf = res_gdv.drop_duplicates()
                    da_logger.info('total tiles:', res_gdv.shape)

                    # res_df.to_excel(os.path.join(output_path, 'search_result.xlsx'))
                    res_gdf.to_file(gpkg_fp, layer=layer, driver="GPKG")
                else:
                    da_logger.info("no data found within aoi")

            except requests.exceptions.RequestException as e:
                da_logger.error(f"Error: {e}")
                traceback.print_stack()

            # getting latest datasets
        else:
            res_gdf = gpd.read_file(gpkg_fp, layer=layer, driver="GPKG")
        # return list(res_gdf['url'].values)
        return res_gdf
