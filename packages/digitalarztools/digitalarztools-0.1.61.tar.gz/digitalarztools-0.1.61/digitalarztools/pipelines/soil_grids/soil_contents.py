import os
import time
import traceback
import urllib
from io import BytesIO

import numpy as np
import rasterio
import requests
from tqdm import tqdm

from digitalarztools.io.file_io import FileIO

from digitalarztools.io.raster.band_process import BandProcess
from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.utils.logger import da_logger
from digitalarztools.utils.waitbar_console import WaitBarConsole


class SoilContent:
    @classmethod
    def get_clay_content(cls, des_dir, lat_lim, lon_lim, level='sl1', wait_bar=1):
        """
        Downloads SoilGrids data from ftp://ftp.soilgrids.org/data/recent/

        this data includes a Digital Elevation Model (DEM)
        The spatial resolution is 90m (3s) or 450m (15s)

        The following keyword arguments are needed:
        des_dir -- path to store data
        lat_lim -- [ymin, ymax]
        lon_lim -- [xmin, xmax]
        level -- 'sl1' (Default)
                 'sl2'
                 'sl3'
                 'sl4'
                 'sl5'
                 'sl6'
                 'sl7'
        wait_bar -- '1' if you want a waitbar (Default = 1)
        """

        # Create directory if not exists for the output
        output_folder = os.path.join(des_dir, 'SoilGrids', 'Clay_Content')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Define the output map and create this if not exists
        fp_end = os.path.join(output_folder, 'ClayContentMassFraction_%s_SoilGrids_percentage.tif' % level)

        if not os.path.exists(fp_end):

            # Create Waitbar
            if wait_bar == 1:
                WaitBarConsole.print_bar_text('\nDownload Clay Content soil map of %s from SoilGrids.org' % level)

                total_amount = 1
                amount = 0
                WaitBarConsole.print_wait_bar(amount, total_amount, prefix='Progress:', suffix='Complete', length=50)

            # Download and process the data
            cls.download_data(output_folder, lat_lim, lon_lim, "CLAY", level)

            if wait_bar == 1:
                amount = 1
                WaitBarConsole.print_wait_bar(amount, total_amount, prefix='Progress:', suffix='Complete', length=50)

        else:
            if wait_bar == 1:
                da_logger.info(
                    f"\nClay Content soil map of {level} from SoilGrids.org already exists in {fp_end}")

    @classmethod
    def get_silt_content(cls, des_dir, lat_lim, lon_lim, level='sl1', wait_bar=1):
        """
        Downloads SoilGrids data from ftp://ftp.soilgrids.org/data/recent/

        The following keyword arguments are needed:
        Dir -- 'C:/file/to/path/'
        lat_lim -- [ymin, ymax]
        lon_lim -- [xmin, xmax]
        level -- 'sl1' (Default)
                 'sl2'
                 'sl3'
                 'sl4'
                 'sl5'
                 'sl6'
                 'sl7'
        wait_bar -- '1' if you want a waitbar (Default = 1)
        """

        # Create directory if not exists for the output
        output_folder = os.path.join(des_dir, 'SoilGrids', 'Silt_Content')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Define the output map and create this if not exists
        fp_end = os.path.join(output_folder, 'SiltContentMassFraction_%s_SoilGrids_percentage.tif' % level)

        if not os.path.exists(fp_end):

            # Create Waitbar
            if wait_bar == 1:
                WaitBarConsole.print_bar_text(
                    '\nDownload Silt Content Mass Fraction soil map of %s from SoilGrids.org' % level)
                total_amount = 1
                amount = 0
                WaitBarConsole.print_wait_bar(amount, total_amount, prefix='Progress:', suffix='Complete', length=50)

            # Download and process the data
            cls.download_data(output_folder, lat_lim, lon_lim, "SILT", level)

            if wait_bar == 1:
                amount = 1
                WaitBarConsole.print_wait_bar(amount, total_amount, prefix='Progress:', suffix='Complete', length=50)

        else:
            if wait_bar == 1:
                da_logger.info(
                    f"\nSilt Content Mass Fraction soil map of {level} from SoilGrids.org already exists in {fp_end}")

    @staticmethod
    def get_soil_data_level() -> dict:
        """
         https://www.isric.org/ soil grids data level in cm
        """
        dict_levels = dict()
        dict_levels["sl1"] = "0-5"
        dict_levels["sl2"] = "5-15"
        dict_levels["sl3"] = "15-30"
        dict_levels["sl4"] = "30-60"
        dict_levels["sl5"] = "60-100"
        dict_levels["sl6"] = "100-200"
        return dict_levels

    @staticmethod
    def get_soil_dataset_info(dataset_key=None) -> dict:

        # Define parameter depedent variables
        # conversion = None
        # if dataset == "BULKDENSITY":
        #     orig_fp = os.path.join(output_folder,
        #                       f'BulkDensity_{dict_levels[level]}_SoilGrids_cg_cm3.tif')
        #     conv_fp = os.path.join(output_folder,
        #                            f'BulkDensity_{dict_levels[level]}_SoilGrids_g_cm3.tif')
        #
        #     parameter = "bdod"
        #     conversion = 10  # cg/cm3 to kg/m3 or  g/cm3 (conversion factor remains 10 for kg/m³ to g/cm³)
        #     level_str = dict_levels[level]
        # if dataset == "NITROGEN":
        #     orig_fp = os.path.join(output_folder,
        #                       f'Nitrogen_{dict_levels[level]}_SoilGrids_cg_kg.tif')
        #     conv_fp = os.path.join(output_folder,
        #                            f'Nitrogen_{dict_levels[level]}_SoilGrids_g_kg.tif')
        #
        #     parameter = "nitrogen"
        #     level_str = dict_levels[level]
        #     conversion = 0.01  # cg/kg to g/kg
        # if dataset == "SOC": # Soil Organic Carbon Content
        #     orig_fp = os.path.join(output_folder,
        #                       f'SoilOrganicCarbonContent_{dict_levels[level]}_SoilGrids_dg_kg.tif')
        #     conv_fp = os.path.join(output_folder,
        #                            f'SoilOrganicCarbonContent_{dict_levels[level]}_SoilGrids_g_kg.tif')
        #
        #     parameter = "soc"
        #     level_str = dict_levels[level]
        #     conversion = 0.1  # dg/kg to g/kg
        #
        # if dataset == "SOD": # Soil Organic Carbon Density
        #     orig_fp = os.path.join(output_folder, f'SoilOrganicCarbonDensity_{dict_levels[level]}_SoilGrids_g_dm3.tif')
        #     # conv_fp = None
        #     parameter = "ocd"
        #     # conversion = 1.0
        #     level_str = dict_levels[level]
        # elif dataset == "SOM": # Soil Organic Matter
        #     orig_fp = os.path.join(output_folder,
        #                            f'SoilOrganicCarbonContent_{dict_levels[level]}_SoilGrids_dg_kg.tif')
        #     conv_fp = os.path.join(output_folder,
        #                            f'SoilOrganicMatterContent_{dict_levels[level]}_SoilGrids_g_kg.tif')
        #     parameter = "soc"  # SOC is used to derive SOM
        #     conversion = 0.1 * 1.724  # dg/kg to g/kg then converting SOC to SOM and keeping it as a fraction
        #     level_str = dict_levels[level]
        # if dataset == "PH":
        #     orig_fp = os.path.join(output_folder, f'SoilPH_{dict_levels[level]}_SoilGrids_pH10.tif')
        #     # conv_fp = None
        #     parameter = "phh2o"
        #     level_str = dict_levels[level]
        #     # conversion = 1.0
        # if dataset == "CLAY":
        #     orig_fp = os.path.join(output_folder,
        #                       f'ClayContentMassFraction_{dict_levels[level]}_SoilGrids_{"percentage" if apply_conversion else "g_kg"}.tif')
        #     orig_fp = os.path.join(output_folder,
        #                            f'ClayContentMassFraction_{dict_levels[level]}_SoilGrids_{"percentage" if apply_conversion else "g_kg"}.tif')
        #
        #     parameter = "clay"
        #     level_str = dict_levels[level]
        #     conversion = 0.1  # g/kg to percentage
        # if dataset == "SAND":
        #     orig_fp = os.path.join(output_folder,
        #                       f'SandContentMassFraction_{dict_levels[level]}_SoilGrids_{"percentage" if apply_conversion else "g_kg"}.tif')
        #     parameter = "sand"
        #     level_str = dict_levels[level]
        #     conversion = 0.1  # g/kg to percentage
        # if dataset == "SILT":
        #     orig_fp = os.path.join(output_folder,
        #                       f'SiltContentMassFraction_{dict_levels[level]}_SoilGrids_{"percentage" if apply_conversion else "g_kg"}.tif')
        #     conv_fp = os.path.join(output_folder,
        #                       f'SiltContentMassFraction_{dict_levels[level]}_SoilGrids_{"percentage" if apply_conversion else "g_kg"}.tif')
        #
        #     parameter = "silt"
        #     level_str = dict_levels[level]
        #     conversion = 0.1  # g/kg to percentage
        parameters_info = {
            "BULKDENSITY": {
                "name": "BulkDensity",
                "parameter": "bdod",
                "unit": "cg/cm3",
                "conversion_unit": "g/cm3",
                "conversion": 10,  # cg/cm3 to kg/m3 or g/cm3
            },
            "NITROGEN": {
                "name": "Nitrogen",
                "parameter": "nitrogen",
                "unit": "cg/kg",
                "conversion_unit": "g/kg",
                "conversion": 0.01,  # cg/kg to g/kg
            },
            "SOC": {  # Soil Organic Carbon Content
                "name": "SoilOrganicCarbonContent",
                "parameter": "soc",
                "unit": "dg/kg",
                "conversion_unit": "g/kg",
                "conversion": 0.1,  # dg/kg to g/kg
            },
            "SOD": {  # Soil Organic Carbon Density
                "name": "SoilOrganicCarbonDensity",
                "parameter": "ocd",
                "unit": "g/dm3",
                "conversion_unit": None,
                "conversion": None,  # No conversion needed
            },
            "SOM": {  # Soil Organic Matter
                "name": "SoilOrganicMatterContent",
                "parameter": "soc",  # SOC is used to derive SOM
                "unit": "dg/kg",
                "conversion_unit": "g/kg",
                "conversion": 0.1 * 1.724,  # dg/kg to g/kg, then SOC to SOM conversion
            },
            "PH": {
                "name": "SoilPH",
                "parameter": "phh2o",
                "unit": "pH10",
                "conversion_unit": None,
                "conversion": None,  # No conversion needed
            },
            "CLAY": {
                "name": "ClayContentMassFraction",
                "parameter": "clay",
                "unit": "g/kg",
                "conversion_unit": "percentage",
                "conversion": 0.1,  # g/kg to percentage
            },
            "SAND": {
                "name": "SandContentMassFraction",
                "parameter": "sand",
                "unit": "g/kg",
                "conversion_unit": "percentage",
                "conversion": 0.1,  # g/kg to percentage
            },
            "SILT": {
                "name": "SiltContentMassFraction",
                "parameter": "silt",
                "unit": "g/kg",
                "conversion_unit": "percentage",
                "conversion": 0.1,  # g/kg to percentage
            },
        }
        if dataset_key is not None and dataset_key not in parameters_info:
            raise ValueError(f"{dataset_key} doesn't exist in soil contents info")
        return parameters_info[dataset_key] if dataset_key is not None else parameters_info

    @classmethod
    def download_data(cls, output_folder, lat_lim, lon_lim, dataset, level, apply_conversion=True):
        """
        This function downloads SoilGrids data from SoilGrids.org in percentage
        Keyword arguments:
        output_folder -- directory of the result
        lat_lim -- [ymin, ymax] (values must be between -50 and 50)
        lon_lim -- [xmin, xmax] (values must be between -180 and 180)
        level -- "sl1" .... "sl7"
                dict_levels["sl1"] = "0-5_cm"
                dict_levels["sl2"] = "5-15_cm"
                dict_levels["sl3"] = "15-30_cm"
                dict_levels["sl4"] = "30-60_cm"
                dict_levels["sl5"] = "60-100_cm"
                dict_levels["sl6"] = "100-200_cm"
        dataset -- (in capital) clay, sand, silt, soc, sod, ph,  nitrogen, bulkdensity,\
        """

        dict_levels = cls.get_soil_data_level()

        FileIO.mkdirs(output_folder)

        # Example usage to generate file paths dynamically:
        info = cls.get_soil_dataset_info(dataset)
        orig_fp = cls.get_file_path(level, dataset, False, output_folder)
        dir = FileIO.mkdirs(orig_fp)
        try:
            if not os.path.exists(orig_fp):
                parameter = info["parameter"]
                level_str = dict_levels[level]
                print(f"Downloading {parameter} at {level_str}")
                url = f"https://maps.isric.org/mapserv?map=/map/{parameter}.map&SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID={parameter}_{level_str}cm_mean&FORMAT=image/tiff&SUBSET=long({lon_lim[0]},{lon_lim[1]})&SUBSET=lat({lat_lim[0]},{lat_lim[1]})&SUBSETTINGCRS=http://www.opengis.net/def/crs/EPSG/0/4326&OUTPUTCRS=http://www.opengis.net/def/crs/EPSG/0/4326"

                # Make an HTTP request to the URL with streaming enabled
                response = requests.get(url, stream=True)

                if response.status_code == 200:
                    # Get the total file size from the headers
                    total_size_in_bytes = int(response.headers.get('content-length', 0))
                    block_size = 1024  # 1 Kilobyte

                    # Create a progress bar
                    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

                    # Write the content to a file in chunks
                    with open(orig_fp, "wb") as f:
                        for data in response.iter_content(block_size):
                            progress_bar.update(len(data))
                            f.write(data)

                    progress_bar.close()

                    print("Image downloaded and saved successfully.")

                else:
                    print(f"Error: Unable to download the image. Status code: {response.status_code}")

            if apply_conversion and 'conversion' in info.keys():
                conversion = info['conversion']
                fp = cls.get_file_path(level, dataset, True, output_folder)
                if not os.path.exists(fp):
                    print(f"Conversion is applied with factor {conversion}")
                    raster = RioRaster(orig_fp)
                    # affine_transform = raster.get_geo_transform()
                    # proj = raster.get_crs()
                    data = raster.get_data_array(1)
                    time.sleep(1)
                    data = np.float_(data) * conversion
                    nodata_value = 0

                    data = BandProcess.gap_filling(data, nodata_value)
                    new_raster = raster.rio_raster_from_array(data)
                    new_raster.save_to_file(fp)
                # RioRaster.write_to_file(fp, data, raster.get_crs(), raster.get_geo_transform(), nodata_value)
            else:
                fp = orig_fp
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            # da_logger.error(traceback.print_stack())
            # da_logger.error(str(e))

        return fp

    @classmethod
    def get_organic_carbon_content(cls, des_dir, lat_lim, lon_lim, level, wait_bar=1):
        """
            Downloads SoilGrids data from ftp://ftp.soilgrids.org/data/recent/

            The following keyword arguments are needed:
            des_dir -- destination directory
            lat_lim -- [ymin, ymax]
            lon_lim -- [xmin, xmax]
            level -- 'sl1' (Default)
                     'sl2'
                     'sl3'
                     'sl4'
                     'sl5'
                     'sl6'
                     'sl7'
            wait_bar -- '1' if you want a waitbar (Default = 1)
            """

        # Create directory if not exists for the output
        output_folder = os.path.join(des_dir, 'SoilGrids', 'Soil_Organic_Carbon_Content')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Define the output map and create this if not exists
        fp_end = os.path.join(output_folder, 'SoilOrganicCarbonContent_%s_SoilGrids_g_kg.tif' % level)

        if not os.path.exists(fp_end):

            # Create Waitbar
            if wait_bar == 1:
                WaitBarConsole.print_bar_text(
                    '\nDownload Soil Organic Carbon Content soil map of %s from SoilGrids.org' % level)
                total_amount = 1
                amount = 0
                WaitBarConsole.print_wait_bar(amount, total_amount, prefix='Progress:', suffix='Complete', length=50)

            # Download and process the data
            cls.download_data(output_folder, lat_lim, lon_lim, "SOC", level)

            if wait_bar == 1:
                amount = 1
                WaitBarConsole.print_wait_bar(amount, total_amount, prefix='Progress:', suffix='Complete', length=50)

        else:
            if wait_bar == 1:
                da_logger.info(
                    f"\nSoil Organic Carbon Content soil map of {level} from SoilGrids.org already exists in {fp_end}")

    @classmethod
    def get_bulk_density(cls, des_dir, lat_lim, lon_lim, level, wait_bar=1):
        """
            Downloads data from SoilGrids (www.soilgrids.org)

            The following keyword arguments are needed:
            des_dir -- destination directory
            lat_lim -- [ymin, ymax]
            lon_lim -- [xmin, xmax]
            level -- 'sl1' (Default)
                     'sl2'
                     'sl3'
                     'sl4'
                     'sl5'
                     'sl6'
                     'sl7'
            wait_bar -- '1' if you want a waitbar (Default = 1)
            """

        # Create directory if not exists for the output
        output_folder = os.path.join(des_dir, 'SoilGrids', 'Bulk_Density')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Define the output map and create this if not exists
        fp_end = os.path.join(output_folder, 'BulkDensity_%s_SoilGrids_kg-m-3.tif' % level)

        if not os.path.exists(fp_end):
            # Create Waitbar
            if wait_bar == 1:
                WaitBarConsole.print_bar_text('\nDownload Bulk Density soil map of %s from SoilGrids.org' % level)
                total_amount = 1
                amount = 0
                WaitBarConsole.print_wait_bar(amount, total_amount, prefix='Progress:', suffix='Complete', length=50)

            # Download and process the data
            cls.download_data(output_folder, lat_lim, lon_lim, "BULKDENSITY", level)

            if wait_bar == 1:
                amount = 1
                WaitBarConsole.print_wait_bar(amount, total_amount, prefix='Progress:', suffix='Complete', length=50)

        else:
            if wait_bar == 1:
                da_logger.info(
                    f"\nBulk Density soil map of {level} from SoilGrids.org already exists in {fp_end}")

    @classmethod
    def get_file_path(cls, level, dataset, apply_conversion, output_folder=None):
        """
         orig_fp = os.path.join(output_folder, f'{info["name"]}{dict_levels[level]}_{info["unit"].replace("/","-")}.tif')
        fp = os.path.join(output_folder,
                                  f'{info["name"]}{dict_levels[level]}_{info["conversion_unit"].replace("/", "-")}.tif')

        @param output_folder:
        @param level:
        @param dataset:
        @param apply_conversion:
        @return:
        """

        info = cls.get_soil_dataset_info(dataset)
        dict_levels = cls.get_soil_data_level()
        unit = info['conversion_unit'] if apply_conversion and 'conversion' in info.keys() else info['unit']
        fn = f'{info["name"]}{dict_levels[level]}_{unit.replace("/", "-")}.tif'
        if output_folder:
            return os.path.join(output_folder, fn)
        return fn
