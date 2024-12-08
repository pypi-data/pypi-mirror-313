import gzip
import os
import re
from datetime import datetime
from io import BytesIO

import geopandas as gpd

import numpy as np
import rasterio
import requests
from bs4 import BeautifulSoup
from digitalarztools.io.file_io import FileIO
from digitalarztools.io.raster.band_process import BandProcess

from digitalarztools.io.raster.rio_raster import RioRaster

from settings import MEDIA_DIR


class CHIRP:
    """"
    download chirps from
     https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p05
    """
    raster: RioRaster

    def __init__(self, raster: RioRaster):
        self.raster = raster

    @staticmethod
    def get_last_available_date():
        """
        :return: chirps and chirp end dates
        """
        url = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p05"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        Years = []
        for link in soup.findAll('a'):
            link_str = str(link.get('href'))
            if link_str[0] == "1" or link_str[0] == "2":
                Years.append(int(link_str[:-1]))

        files = []
        for Year in Years[-5:]:
            url = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p05/%d" % Year
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            for link in soup.findAll('a')[-5:]:
                link_str = str(link.get('href'))
                # print(link_str)
                if link_str.startswith("chirps") and (link_str.endswith(".tif") or link_str.endswith(".tif.gz")):
                    files.append(link_str)

        chirps_end_dates_tif = [datetime.strptime(k, "chirps-v2.0.%Y.%m.%d.tif").toordinal() for k in files if
                                k.endswith(".tif")]
        chirps_end_dates_tif_gz = [datetime.strptime(k, "chirps-v2.0.%Y.%m.%d.tif.gz").toordinal() for k in
                                   files if k.endswith(".tif.gz")]
        chirps_end_dates = chirps_end_dates_tif_gz + chirps_end_dates_tif
        chirps_end_date = datetime.fromordinal(np.max(chirps_end_dates))

        url = "https://data.chc.ucsb.edu/products/CHIRP/daily"
        r = requests.get(url)

        soup = BeautifulSoup(r.text, "html.parser")

        Years = []
        for link in soup.findAll('a'):
            link_str = str(link.get('href'))
            if link_str[0] == "1" or link_str[0] == "2":
                Years.append(int(link_str[:-1]))

        files = []
        for Year in Years[-5:]:

            url = "https://data.chc.ucsb.edu/products/CHIRP/daily/%d" % Year
            r = requests.get(url)

            soup = BeautifulSoup(r.text, "html.parser")

            for link in soup.findAll('a')[-5:]:
                link_str = str(link.get('href'))
                if link_str.startswith("chirp") and (link_str.endswith(".tif") or link_str.endswith(".tif.gz")):
                    files.append(link_str)

        chirp_end_dates_tif = [datetime.strptime(k, "chirp.%Y.%m.%d.tif").toordinal() for k in files if
                               k.endswith(".tif")]
        chirp_end_dates_tif_gz = [datetime.strptime(k, "chirp.%Y.%m.%d.tif.gz").toordinal() for k in files if
                                  k.endswith(".tif.gz")]
        chirp_end_dates = chirp_end_dates_tif_gz + chirp_end_dates_tif
        chirp_end_date = datetime.fromordinal(np.max(chirp_end_dates))

        return chirps_end_date, chirp_end_date

    @staticmethod
    def get_available_years():
        """
        Get the file name
        """
        # get years list
        url = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p05"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        years = []
        for link in soup.findAll('a'):
            link_str = str(link.get('href'))
            if link_str[0] == "1" or link_str[0] == "2":
                years.append(int(link_str[:-1]))
        return years

    @staticmethod
    def get_available_file_of_year(year: str):
        """
        Get the file name
        """
        # get file names
        files = []
        # url = "https://data.chc.ucsb.edu/products/CHIRP/daily/%d" % year
        url = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p05/{year}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        for link in soup.findAll('a'):
            link_str = str(link.get('href'))
            # if link_str.startswith("chirp") and (link_str.endswith(".tif") or link_str.endswith(".tif.gz")):
            if link_str.startswith("chirp") and link_str.endswith(".tif.gz"):
                files.append(link_str)

        return files

    @classmethod
    def download_2_raster(cls, year: str, file_name: str):
        url = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p05/{year}/{file_name}"
        # print(url)
        # file_name = url.strip().split('/')[-1][:-7].replace(".", "_")


        # Download the compressed file
        response = requests.get(url)
        compressed_data = BytesIO(response.content)

        with gzip.GzipFile(fileobj=compressed_data, mode='rb') as decompressed_data:
            # Open the decompressed data using rasterio
            with rasterio.open(decompressed_data) as dataset:
                # Access the raster data or metadata as needed
                raster = RioRaster(dataset)
                return cls(raster)

    def save_2_file(self, output_fp: str, aoi: gpd.GeoDataFrame = None):
        if not os.path.exists(output_fp):
            # aoi.to_crs(epsg=4326, inplace=True)
            if str(self.raster.get_crs()).lower() != str(aoi.crs).lower():
                aoi.to_crs(crs=self.raster.get_crs(), inplace=True)
            clip_raster = RioRaster(self.raster.clip_raster(aoi.unary_union, crs=aoi.crs, in_place=False))
            clip_raster.save_to_file(output_fp)

    def get_summary_data(self, gdf):
        """
        Rainfall - CHIRPS daily	rainfall	in mm
        @param gdf:
        @return:
        """
        clipped_raster : RioRaster = self.raster.clip_raster(gdf,in_place=False,crs=gdf.crs)
        band = clipped_raster.get_data_array(1)
        summary_data = BandProcess.get_summary_data(band, clipped_raster.get_nodata_value())
        if summary_data['sum'] > 0 :
            return summary_data
        return None

    @staticmethod
    def get_date_from_file_name(file_path: str):
        """

        @param file_path: in the form of chirps-v2_0_1981_01_01.tif
        @return:
        """
        # Extract the file name from the file path
        file_name = os.path.basename(file_path)

        # Use regular expressions to extract the date part from the file name
        match = re.search(r'(\d{4})_(\d{2})_(\d{2})', file_name)
        if match:
            year, month, day = match.groups()
            date_str = f"{year}-{month}-{day}"
            # Convert to a datetime object
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj