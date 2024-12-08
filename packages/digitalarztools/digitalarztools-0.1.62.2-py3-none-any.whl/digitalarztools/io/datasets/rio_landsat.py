import json
import os
from datetime import datetime
from math import cos
from typing import Literal

import numpy as np
import pandas as pd
import pyproj
import xmltodict

from digitalarztools.io.file_io import FileIO
from digitalarztools.io.raster.rio_process import RioProcess
from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.utils.logger import da_logger


class RioLandsat:
    base_folder_path: str
    stac_data: dict = None
    metadata: dict = None

    def __init__(self, fp):
        """
        Read and Process the downloaded Landsat file
        :param fp: path of the downloaded tar file
        """
        if os.path.isfile(fp):
            fn, ext = FileIO.get_file_name_ext(os.path.basename(fp))
            # if ext == "tar":
            #     self.file_path = FileIO.extract_data_tar(fp)
            self.base_folder_path = FileIO.extract_data(fp)
            self.info = self.get_file_info(fn)
        if os.path.isdir(fp):
            self.base_folder_path = fp
        if not os.path.isdir(self.base_folder_path):
            raise Exception("Provide  landsat band folder")
        self.metadata = self.get_mtl_metadata()
        self.stac_data = self.get_stac_data()

        # print(self.stac_data)

    def get_crs(self) -> pyproj.CRS:
        """
        :return: projection in pyproj CRS
        """
        srid = self.get_srid()
        return pyproj.CRS.from_epsg(srid)

    def get_sensor_info(self):
        landsat_nr = self.get_landsat_no()
        # tim required sensors for sabel
        # sensor1 = f'LS{landsat_nr}'
        # sensor2 = f'LS{landsat_nr}'

        sensors = [f'LS{landsat_nr}']
        return sensors

    @staticmethod
    def get_mss_pixel_spacing() -> int:
        return 30

    def get_mss_spatial_resolutions(self):
        # tim required resolution for sabel
        # res1 = '30m'
        # res2 = '30m'
        # res3 = '30m'
        res = [f'{self.get_mss_pixel_spacing()}m']
        return res

    def get_product_id(self):
        """
        :return: product id in the format LXSS_LLLL_PPPRRR_YYYYMMDD_yyyymmdd_CC_TX
        """
        if not self.metadata:
            dir_path = os.path.dirname(self.base_folder_path) if os.path.isfile(
                self.base_folder_path) else self.base_folder_path
            return dir_path.replace("\\", "/").split("/")[-1]
        return self.metadata["PRODUCT_CONTENTS"]["LANDSAT_PRODUCT_ID"]

    def get_mtl_metadata(self):
        """
        :return: meta_data json
        """
        mtl_fp = f"{self.base_folder_path}/{self.get_product_id()}_MTL.json"
        if os.path.exists(mtl_fp):
            with open(mtl_fp) as file:
                meta_data = json.loads(file.read())
                return meta_data["LANDSAT_METADATA_FILE"]
        else:
            mtl_fp = f"{self.base_folder_path}/{self.get_product_id()}_MTL.xml"
            if os.path.exists(mtl_fp):
                with open(mtl_fp) as xml_file:
                    meta_data = xmltodict.parse(xml_file.read())
                    return meta_data["LANDSAT_METADATA_FILE"]

    def get_stac_data(self):
        """
        :return: stac json
        """
        stac_fp = f"{self.base_folder_path}/{self.get_product_id()}_stac.json"
        if os.path.exists(stac_fp):
            with open(stac_fp) as file:
                stac = json.loads(file.read())
                return stac

    @staticmethod
    def get_band_name_from_fp(fp: str):
        """
        param fp: file path with extention
        :return:
        """
        if os.path.isfile(fp):
            fn_parts = os.path.basename(fp)[:-4].split("_")
            return "_".join(fn_parts[7:])
        return None

    @classmethod
    def get_file_info(cls, fp: str):
        """
        param fp: path of file basename.tar or tif
         basename in the form LXSS_LLLL_PPPRRR_YYYYMMDD_yyyymmdd_CC_TX
        Where:
            L = Landsat
            X = Sensor (“C”=OLI/TIRS combined, “O”=OLI-only, “T”=TIRS-only, “E”=ETM+, “T”=“TM, “M”=MSS)
            SS = Satellite ( 7 =Landsat 7, 8=Landsat 8)
            LLL = Processing correction level (L1TP/L1GT/L1GS)
            PPP = WRS path
            RRR = WRS row
            YYYYMMDD = Acquisition year, month, day
            yyyymmdd - Processing year, month, day
            CC = Collection number (01, 02, …)
            TX = Collection category (“RT”=Real-Time, “T1”=Tier 1, “T2”=Tier 2)
            BN = Band Name
        return: info dict
        """
        # fn = cls.get_base_name(basename)
        basename = os.path.basename(fp)[:-4] if os.path.isfile(fp) else os.path.basename(fp)
        fn_parts = basename.split("_")
        info = {
            "basename": basename,
            "acq_date": datetime.strptime(fn_parts[3], "%Y%m%d"),
            "proc_date": datetime.strptime(fn_parts[4], "%Y%m%d"),
            "cc_no": int(fn_parts[5]), "cc_cat": fn_parts[6],
            "path": int(fn_parts[2][0:3]),
            "row": int(fn_parts[2][3:6]),
            "ls_no": int(fn_parts[0][2:4]),
            # "band_name": cls.get_band_name()
        }
        return info

    # def get_asset_names(self) -> list:
    #     return list(self.stac_data['assets'].keys())

    # def get_asset_list(self) -> list:
    #     return list(self.stac_data['assets']) if self.stac_data is not None else

    def get_data_asset_list(self) -> list:
        """
        :return: list of the asset name corresponds to the spectral bands
        """
        # assets = list(self.stac_data['assets'].keys())
        if self.stac_data:
            assets = self.stac_data['assets']
            bands = list()
            for asset in assets:
                if "data" in assets[asset]['roles']:
                    bands.append(asset)
            return bands
        else:
            assets = self.metadata["PRODUCT_CONTENTS"]
            bands = list()
            for key in assets:
                if "FILE_NAME_BAND" in key:
                    bands.append(assets[key])
            return bands

    def get_band_file_path(self, asset_name: str):
        """
        param asset_name: "blue" , "green", "red","nir08", "pan", "cirrus"
        :return:
        """
        asset_info = self.stac_data['assets'][asset_name]["href"]
        return f"{self.base_folder_path}/{asset_info.split('/')[-1]}"

    def get_band_name(self, asset_name):
        """
        param asset_name: like "blue", "red", "green"
        :return: band name like B1, B2, B3
        """
        return self.stac_data['assets'][asset_name]['eo:bands'][0]['name'] if "eo:bands" in self.stac_data['assets'][
            asset_name] else None

    def get_band_center_wavelength(self, asset_name):
        """
        param asset_name: like "blue", "red", "green"
        :return: center wavelength of the band
        """
        return self.stac_data['assets'][asset_name]['eo:bands'][0]['center_wavelength']

    def get_band_resolution(self, asset_name) -> float:
        """
        param asset_name: like "blue", "green", "red"
        :return: resolution in float
        """
        return self.stac_data['assets'][asset_name]['eo:bands'][0]['gsd'] if 'eo:bands' in self.stac_data['assets'][
            asset_name] else None

    def get_band_rio_raster(self, asset_name="blue") -> RioRaster:
        """
        param asset_name:
        :return: RioRaster
        """
        return RioRaster(self.get_band_file_path(asset_name))

    @staticmethod
    def get_atmospheric_transmissivity_constant():
        """
        This value is used for atmospheric correction of broad band albedo.
        This value is used for now, would be better to use tsw.
        τsw=0.75+2×10−5×z where z is elevation
        :return:
        """
        apparent_atmosf_transm = 0.89
        return apparent_atmosf_transm

    def create_band_stacks(self, asset_name_list: list):
        """
        create band_stacks
        :param asset_name_list:
        :return:
        """
        file_list = list()
        for asset in asset_name_list:
            file_list.append(self.get_band_file_path(asset))
        ms_raster = RioProcess.stack_bands(file_list, lambda x: self.get_band_name_from_fp(x))
        return ms_raster

    def create_visual_image(self, img_des):
        """
        Create a pan sharpened visual image using mss and pan raster. MSS will consist of Blue, Green, Red, and Near Infra Red Band
        :param img_des: destination of image
        :return:
        """
        if not os.path.exists(img_des):
            start_time = datetime.now()
            ms_assets = ["blue", "green", "red", "nir08"]
            file_list = []
            for asset in ms_assets:
                file_list.append(self.get_band_file_path(asset))
            ms_raster = RioProcess.stack_bands(file_list, lambda x: self.get_band_name_from_fp(x))
            pan_raster = RioRaster(self.get_band_file_path("pan"))
            final_raster = RioProcess.pansharpend(ms_raster, pan_raster)
            final_raster.save_to_file(img_des=img_des)
            end_time = datetime.now()
            da_logger.critical(f"Pan sharpened image created in {end_time - start_time} at {img_des}")

    def get_scene_center_time(self):
        """
        :return: scene center time in hr and minutes
        """
        center_time = self.metadata["IMAGE_ATTRIBUTES"]["SCENE_CENTER_TIME"]
        time_list = center_time.split(":")
        hour = float(time_list[0])  # take the first word of time_list
        minutes = float(time_list[1]) + float(time_list[2][:-1]) / 60
        return hour, minutes

    def get_doy_acquired(self):
        """
        :return: day of the year and year for acquired date
        """
        date_acquired = self.metadata["IMAGE_ATTRIBUTES"]["DATE_ACQUIRED"]
        date_acquired = datetime.strptime(date_acquired, "%Y-%m-%d").timetuple()
        doy = date_acquired.tm_yday
        year = date_acquired.tm_year
        return doy, year

    def get_srid(self) -> int:
        """
        :return: srid of the utm zone in integer
        """
        srid = '32'
        srid += '6' if "NORTH" in self.metadata["PROJECTION_ATTRIBUTES"]["ORIENTATION"] else '7'
        srid += self.metadata["PROJECTION_ATTRIBUTES"]["UTM_ZONE"]
        return int(srid)

    def get_utm_zone(self):
        """
        :return: utm zone number
        """
        zone = int(self.metadata["PROJECTION_ATTRIBUTES"]["UTM_ZONE"])
        orientation = "N" if "NORTH" in self.metadata["PROJECTION_ATTRIBUTES"]["ORIENTATION"] else "S"
        return f"{zone}{orientation}"

    def get_sun_elevation(self):
        """
        Get Sun elevation at the time of acquisition
        :return:
        """
        return float(self.metadata["IMAGE_ATTRIBUTES"]["SUN_ELEVATION"] or 0)

    def get_sun_azimuth(self) -> float:
        """
        :return: sun azimuth
        """
        return float(self.metadata['IMAGE_ATTRIBUTES']['SUN_AZIMUTH'])

    def get_landsat_no(self):
        """
        :return: Landsat no 7, 9 , or 0
        """
        return self.get_file_info(self.get_product_id())["ls_no"]

    def get_collection_no(self):
        """
        :return: collection no
        """
        # self.stac_data['collection']
        return self.info['cc_no']

    def get_acquisition_date(self):
        """
        :return: acquisition date of the product
        """
        doy, year = self.get_doy_acquired()
        acquisition_date = pd.to_datetime("%d%d" % (year, doy), format='%Y%j')
        return acquisition_date

    def get_time_info(self):
        """
            This function retrieves general information of the Landsat image
            (date and time acquired, UTM zone, sun elevation) from the
            metadata file.
        """
        doy, year = self.get_doy_acquired()
        hour, minutes = self.get_scene_center_time()
        utm_zone = self.get_utm_zone()
        sun_elevation = self.get_sun_elevation()
        ls_no = self.get_landsat_no()
        return year, doy, hour, minutes, utm_zone, sun_elevation, ls_no

    def get_band_roles(self, asset_name):
        """
        param asset_name: blue ,green, red, etc.
        :return:
        """
        return self.stac_data['assets'][asset_name]["roles"]

    def get_band_radiance(self, band_no: int, radiance_type: Literal["min", "max"]):
        """
        :param band_no: 2, 3, 4 etc
        :param radiance_type: min or max
        :return:
        """
        radiance = self.metadata['LEVEL1_MIN_MAX_RADIANCE']
        if radiance_type == 'min' and f'RADIANCE_MINIMUM_BAND_{band_no}' in radiance.keys():
            return float(radiance[f'RADIANCE_MINIMUM_BAND_{band_no}'])
        if radiance_type == 'max' and f'RADIANCE_MAXIMUM_BAND_{band_no}' in radiance.keys():
            return float(radiance[f'RADIANCE_MAXIMUM_BAND_{band_no}'])

    def get_band_thermal_const(self, band_no: int, const_type: Literal["k1", "k2"]):
        """
        param band_no: 1, 2, 3
        :param const_type: k1 or k2
        :return:
        """
        thermal_constants = self.metadata['LEVEL1_THERMAL_CONSTANTS']
        if const_type == "k1" and f'K1_CONSTANT_BAND_{band_no}' in thermal_constants.keys():
            return float(thermal_constants[f'K1_CONSTANT_BAND_{band_no}'])
        if const_type == "k2" and f'K2_CONSTANT_BAND_{band_no}' in thermal_constants.keys():
            return float(thermal_constants[f'K2_CONSTANT_BAND_{band_no}'])

    def get_bands_meta_data_df(self):
        """
         retrieves Landsat minimum & maximum radiance and TIRS_Thermal constant k1, k2 from th MTL.txt
        :return:
        """
        data_assets = self.get_data_asset_list()
        # data_assets = self.get_asset_list()
        roles = list()
        band_names = list()
        band_nos = list()
        band_fps = list()
        band_resolution = list()
        max_radiance = list()
        min_radiance = list()
        k1_thermal_constant = list()
        k2_thermal_constant = list()
        for asset_name in data_assets:
            roles.append(", ".join(self.get_band_roles(asset_name)))
            band_fps.append(self.get_band_file_path(asset_name))
            band_resolution.append(self.get_band_resolution(asset_name))
            band_names.append(self.get_band_name(asset_name))
            band_no = int(band_names[-1][1:]) if band_names[-1] is not None else -1
            band_nos.append(band_no)
            max_radiance.append(self.get_band_radiance(band_no, "max"))
            min_radiance.append(self.get_band_radiance(band_no, "min"))
            k1_thermal_constant.append(self.get_band_thermal_const(band_no, "k1"))
            k2_thermal_constant.append(self.get_band_thermal_const(band_no, "k2"))
        df = pd.DataFrame({"asset_name": data_assets, "band_name": band_names,
                           "band_no": band_nos, "resolution": band_resolution,
                           "roles": roles,
                           "max_radiance": max_radiance, "min_radiance": min_radiance,
                           "k1_thermal_const": k1_thermal_constant, "k2_thermal_const": k2_thermal_constant,
                           "file_path": band_fps})
        return df

    def get_ESUN(self, band_no, ls_no=None):
        """
        Mean solar Exo-atmospheric spectral solar irradiance (ESUN) e for each band (W/m2/μm)

        https://www.cell.com/action/showFullTableHTML?isHtml=true&tableId=tbl1&pii=S2405-8440%2821%2900931-2
        for the different Landsat images (L5, L7, L8, or L9)
        :return:
        """
        if ls_no is None:
            ls_no = self.get_landsat_no()
        # for band 1, 2, 3, 4, 5, 7, 6 in landsat 5
        ESUN_L5 = {"B1": 1983, "B2": 1796, "B3": 1536, "B4": 1031, "B5": 220, "B7": 83.44}
        # for band 1, 2, 3, 4, 5, 7, 6 in landsat 7
        ESUN_L7 = {"B1": 1997, "B2": 1812, "B3": 1533, "B4": 1039, "B5": 230.8, "B7": 84.9}
        # for band  2, 3, 4, 5, 6, 7 in landsat 8 and 9 (source tim)
        ESUN_L8 = {"B2": 1973.28, "B3": 1842.68, "B4": 1565.17, "B5": 963.69, "B6": 245, "B7": 82.106}
        if ls_no in [5]:
            return ESUN_L5[band_no]
        if ls_no in [7]:
            return ESUN_L7[band_no]
        if ls_no in [8, 9]:
            return ESUN_L8[band_no]

    def get_reference_ls_raster(self, ref_raster: RioRaster):
        ls_ref_raster = self.get_band_rio_raster("blue")
        ls_extent = ls_ref_raster.get_raster_extent()
        y_size_ls, x_size_ls = ls_ref_raster.get_img_resolution()
        print('Original LANDSAT Image - ')
        print('  Size :', x_size_ls, y_size_ls)
        print('  Upper Left corner x, y: ', ls_extent[0], ', ', ls_extent[3])
        print('  Lower right corner x, y: ', ls_extent[2], ', ', ls_extent[1])
        envelop = ref_raster.get_envelop()

        ls_ref_raster.make_coincident_with(ref_raster)
        ref_extent = ls_ref_raster.get_raster_extent()
        shape_lsc = ls_ref_raster.get_img_resolution()
        # shape_lsc = (y_size_lsc, x_size_lsc)

        print('--- ')
        print('Cropped LANDSAT Image - ')
        print('  Size (rows, cols) :', shape_lsc[0], shape_lsc[1])
        print('  Upper Left corner x, y: ', ref_extent[0], ', ', ref_extent[3])
        print('  Lower right corner x, y: ', ref_extent[2], ', ', ref_extent[1])
        return ls_ref_raster

    def create_QC_map(self, ls_ref_raster: RioRaster) -> np.ndarray:
        """
        create cloud mask  image for Quality control
        Read https://www.usgs.gov/landsat-missions/landsat-collection-1-level-1-quality-assessment-band
        for Quality Assessment
        If landsat 5 or 7 is used then first create a mask for removing the no data stripes
        If landsat 8 or 9 then use 0 refelectance of landsat band 10 and 11 of lwir (long wavelength ir band)
        To reverse the mask image use (-1 * mask_image + 1)
        :return: mask image as np.ndarray  where 1 mean having some value and 0 mean all required band have 0 value

        """
        # create mask image
        # if landsat 5 or 7 is used then first create a mask for removing the no data stripes
        # If landsat 8 or 9 then use landsat band 10 and 11
        Landsat_nr = self.get_landsat_no()
        bands_df = self.get_bands_meta_data_df()
        shape_lsc = ls_ref_raster.get_img_resolution()
        mask_img = np.ones(shape_lsc)

        if Landsat_nr in [5, 7]:
            band_no = [1, 2, 3, 4, 5, 6, 7]
            asset_names = bands_df[bands_df.band_no.isin(band_no)]['asset_name'].tolist()
            stack_raster = self.create_band_stacks(asset_names)
            ls_data = stack_raster.get_data_array(1)
            ls_data_2 = stack_raster.get_data_array(2)
            ls_data_3 = stack_raster.get_data_array(3)
            ls_data_4 = stack_raster.get_data_array(4)
            ls_data_5 = stack_raster.get_data_array(5)
            ls_data_6 = stack_raster.get_data_array(6)
            ls_data_7 = stack_raster.get_data_array(7)
            # create and save the landsat mask for all images based on band 11
            mask_img = np.where(np.logical_or.reduce((ls_data == 0, ls_data_2 == 0, ls_data_3 == 0, ls_data_4 == 0,
                                                      ls_data_5 == 0, ls_data_6 == 0, ls_data_7 == 0)), 0, 1)
        elif Landsat_nr in [8, 9]:
            band_no = [10, 11]  # lwir11, lwir12
            asset_names = bands_df[bands_df.band_no.isin(band_no)]['asset_name'].tolist()
            stack_raster = self.create_band_stacks(asset_names)
            stack_raster.make_coincident_with(ls_ref_raster)
            ls_data_10 = stack_raster.get_data_array(1)
            ls_data_11 = stack_raster.get_data_array(2)
            # create and save the landsat mask for all images based on band 10 and 11

            mask_img = np.where(np.logical_or(ls_data_11 == 0, ls_data_10 == 0), 0, 1)
        else:
            # raise Exception('Landsat image not supported, use Landsat 7, 8, or 9')
            print('Landsat image not supported, use Landsat 7, 8, or 9')
        return mask_img

    @staticmethod
    def calculate_snow_water_mask(ndvi: np.ndarray, water_mask: np.ndarray, Surface_temp: np.ndarray):
        """
        Devides the temporaly water mask into a snow and water mask by using the surface temperature
        :param ndvi:
        :param water_mask:
        :param Surface_temp:
        :return:
        """
        # shape_lsc = ls_ref_raster.get_img_resolution()
        NDVI_nan = np.copy(ndvi)
        NDVI_nan[ndvi == 0] = np.nan
        NDVI_nan = np.float32(NDVI_nan)
        NDVI_std = np.nanstd(NDVI_nan)
        NDVI_max = np.nanmax(NDVI_nan)
        NDVI_treshold_cold_pixels = NDVI_max - 0.1 * NDVI_std
        print('NDVI treshold for cold pixels = ', '%0.3f' % NDVI_treshold_cold_pixels)
        ts_moist_veg_min = np.nanmin(Surface_temp[ndvi > NDVI_treshold_cold_pixels])

        # calculate new water mask
        mask = np.zeros(ndvi.shape)
        mask[np.logical_and(np.logical_and(water_mask == 1, Surface_temp <= 275), ndvi >= 0.3)] = 1
        snow_mask = np.copy(mask)

        # calculate new water mask
        mask = np.zeros(ndvi.shape)
        mask[np.logical_and(water_mask == 1, Surface_temp > 273)] = 1
        water_mask = np.copy(mask)

        return snow_mask, water_mask, ts_moist_veg_min, NDVI_max, NDVI_std

    def calculate_surface_albedo(self, reflectance, path_radiance, apparent_atmospheric_transmission):
        """
        Calculate surface albedo which is an expression of the ability of surfaces to reflect sunlight (heat from the sun).
        bands for reflectance are
        if Landsat_nr == 5 or Landsat_nr == 7:
            bands = np.array([1, 2, 3, 4, 5, 7, 6])
        if Landsat_nr == 8 or Landsat_nr == 9:
            bands = np.array([2, 3, 4, 5, 6, 7])
        :param reflectance: TOA planetary Reflectance Rho Lambda (ρλ) for each band
        :param path_radiance: Recommended, Range: [0.025 - 0.04], based on Bastiaanssen (2000).
        param apparent_atmospheric_transmission:
        :return:
        """
        # surf_albedo = np.ndarray([])
        ls_number = self.get_landsat_no()
        if ls_number in [5, 7]:
            # Surface albedo:
            surf_albedo = (0.254 * reflectance[:, :, 0] + 0.149 * reflectance[:, :, 1] +
                           0.147 * reflectance[:, :, 2] + 0.311 * reflectance[:, :, 3] +
                           0.103 * reflectance[:, :, 4] + 0.036 * reflectance[:, :, 5] -
                           path_radiance) / np.power(apparent_atmospheric_transmission, 2)

        if ls_number in [8, 9]:
            # Surface albedo:
            surf_albedo = (0.3 * reflectance[:, :, 0] + 0.277 * reflectance[:, :, 1] +
                           0.233 * reflectance[:, :, 2] + 0.143 * reflectance[:, :, 3] +
                           0.036 * reflectance[:, :, 4] + 0.012 * reflectance[:, :, 5] -
                           path_radiance) / np.power(apparent_atmospheric_transmission, 2)

        # Better tsw instead of Apparent_atmosf_transm ??
        surf_albedo = surf_albedo.clip(0.0, 0.6)

        return surf_albedo

    def get_bands_for_TOA_calculation(self):
        """
        Band combination for TOA calculation
        :return:
        """
        Landsat_nr = self.get_landsat_no()
        # Define ls bands used for surface reflectance calculation
        bands = np.array([])
        if Landsat_nr in [5, 7]:
            # bands = np.array([1, 2, 3, 4, 5, 7, 6])
            bands = np.array([1, 2, 3, 4, 5, 7])
        elif Landsat_nr in [8, 9]:
            # band 10 and 11 (LWIR) are for Quality Control
            # bands = np.array([2, 3, 4, 5, 6, 7, 10, 11])
            bands = np.array([2, 3, 4, 5, 6, 7])
        else:
            raise Exception('Landsat image not supported, use Landsat 7 or 8')
        return bands

    def calculate_TOA_reflectance_radiance(self, band, cos_zn: np.ndarray, ls_ref_raster: RioRaster, QC_Map=None,
                                           band_metadata_df=None):
        """
        This function calculates TOA spectral radiance L lambda and
        TOA planetary Reflectance rho lambda
        https://www.usgs.gov/landsat-missions/landsat-surface-reflectance
        https://above.nasa.gov/pdfs/Landsat_Surface_Reflectance_ABoVE_21Apr2017.pdf
        :param band:
        :param cos_zn: cos zenith sun angle
        :param ls_ref_raster: landsat reference raster
        :param QC_Map: quality control map
        :param band_metadata_df: bands metadata dataframe
        :return:
        """
        if QC_Map is None:
            QC_Map = self.create_QC_map(ls_ref_raster)
        if band_metadata_df is None:
            band_metadata_df = self.get_bands_meta_data_df()
        # Open original Landsat  for the band number
        # src_FileName = os.path.join(input_folder, Name_Landsat_Image, '%s_B%1d.TIF' % (Name_Landsat_Image, band))
        asset_name = band_metadata_df[band_metadata_df.band_no == band].asset_name.values[0]
        # band_raster.make_coincident_with(ls_ref_raster, envelop=ls_ref_raster.get_envelope())
        # band_raster.get_dataset_under_envelop(envelop=ls_ref_raster.get_envelope())
        # invert QC_Map 0 t0 1 1 to 0 before multiply
        band_raster = self.get_band_rio_raster(asset_name)
        band_raster.make_coincident_with(ls_ref_raster)
        ls_data = band_raster.get_data_array(1) * QC_Map

        # index = np.where(bands[:-(len(bands) - 6)] == band)[0][0]
        band_metadata_row = band_metadata_df[band_metadata_df.band_no == band]

        band_no = band_metadata_row.band_name.values[0]
        Lmax = band_metadata_row.max_radiance.values[0]
        Lmin = band_metadata_row.min_radiance.values[0]
        # da_logger.info(f"index {index} Lmas {Lmax} Lmin {Lmin}")
        # Spectral radiance for each band:
        spectral_radiance = self.Landsat_L_lambda(Lmin, Lmax, ls_data)
        # Reflectivity for each band:
        reflectance = self.calculate_rho_lambda(spectral_radiance, band_no, cos_zn)
        reflectance = reflectance.clip(0.0, 1.0)
        return reflectance, spectral_radiance

    def calculate_earth_sun_inverse_relative_distance(self):
        """
            Calculate Inverse relative distance Earth-Sun dr
            dr=1+0.033×cos(Julian_day×2π365)
            :return: dr
        """
        # self.metadata['IMAGE_ATTRIBUTES']['EARTH_SUN_DISTANCE']
        doy, year = self.get_doy_acquired()
        dr = 1 + 0.033 * cos(doy * 2 * np.pi / 365)
        return dr

    def Landsat_L_lambda(self, Lmin, Lmax, ls_data, landsat_nr=None):
        """
        Calculates the  Lλ which is TOA spectral radiance (Watts/(m2/srad/μm)),
                    Lλ=ML×Qcal+AL
                ML is band-specific multiplicative rescaling factor from the metadata given as: RADIANCE_MULT_BAND_x, where x is the band number,
                AL is band-specific additive rescaling factor from the metadata (RADIANCE_ADD_BAND_x),
                and Qcal is Quantized and calibrated standard product pixel values (DN)
        """
        l_lambda = None
        if landsat_nr is None:
            landsat_nr = self.get_landsat_no()
        if landsat_nr == 8 or landsat_nr == 9:
            l_lambda = ((Lmax - Lmin) / (65535 - 1) * ls_data + Lmin)
        elif landsat_nr == 5 or landsat_nr == 7:
            l_lambda = (Lmax - Lmin) / 255 * ls_data + Lmin
        return l_lambda

    def calculate_rho_lambda(self, L_lambda, band_no, cos_zn):
        """
        Calculates the ρλ  which is TOA planetary reflectance for each band
        ρλ=(π×Lλ) /(ESUNλ×cosθ×dr)

        dr  is the inverse squared relative Earth-sun distance in astronomical terms [-],
         ESUNλ is mean solar exo-atmospheric spectral irradiance on a surface perpendicular to the sun's ray (W/m2/μm).
        and cosθ is solar zenith angle
        """
        dr = self.calculate_earth_sun_inverse_relative_distance()
        ESUN = self.get_ESUN(band_no)
        da_logger.info(f"band_no {band_no} ESUN {ESUN}")
        rho_lambda = np.pi * L_lambda / (ESUN * cos_zn * dr)
        return rho_lambda

    """
       Landsat  Thermal Parameter  Collection
    """

    def get_bands_for_thermal_calculation(self):
        Landsat_nr = self.get_landsat_no()
        # Define bands used for each Landsat number
        # bands = np.ndarray([])
        if Landsat_nr == 5 or Landsat_nr == 7:
            bands = np.array([1, 2, 3, 4, 5, 7, 6])
        elif Landsat_nr == 8 or Landsat_nr == 9:
            bands = np.array([2, 3, 4, 5, 6, 7, 10, 11])
        else:
            print('Landsat image not supported, use Landsat 7 or 8')
        return bands

    def get_thermal_bands_meta_data(self) -> pd.DataFrame:
        # in casae landsat 8, 9 its band 10 and 11 and
        # for landsat 5 and 7 its band 7 and 6
        metadata_df = self.get_bands_meta_data_df()
        thermal_df = metadata_df[metadata_df['roles'].str.contains('temperature', na=False)]
        thermal_df = thermal_df.reset_index(drop=True)
        return thermal_df

    def get_thermal_data(self, ls_ref_raster: RioRaster) -> np.ndarray:
        """
        :param ls_ref_raster:
        :return:
        """
        shape_lsc = ls_ref_raster.get_img_resolution()
        # Bands = self.get_bands_for_thermal_calculation()
        QC_Map = self.create_QC_map(ls_ref_raster)
        # ClipLandsat = (-1 * QC_Map) + 1
        thermal_df = self.get_thermal_bands_meta_data()
        thermal_data = np.zeros((shape_lsc[0], shape_lsc[1], len(thermal_df)))
        # for band in Bands[-(len(Bands) - 6):]:
        for index, row in thermal_df.iterrows():
            asset_name = row.asset_name
            band_fp = self.get_band_file_path(asset_name)
            # if not os.path.exists(band_fp):
            #     src_FileName = os.path.join(os.path.dirname(band_fp), '%s_B%1d_VCID_2.TIF'
            #                                 % (Name_Landsat_Image, band))
            band_raster = RioRaster(band_fp)
            band_raster.make_coincident_with(ls_ref_raster)
            ls_data = band_raster.get_data_array(1) * QC_Map
            # index = np.where(Bands[:] == band)[0][0] - 6
            thermal_data[:, :, index] = ls_data
        return thermal_data

    def get_cloud_threshold(self, collection=None, landsat_nr=None):
        cloud_threshold = np.array([])
        if landsat_nr is None:
            landsat_nr = self.get_landsat_no()
        if collection is None:
            collection = self.get_collection_no()
        if collection == 1:
            if landsat_nr == 8:
                cloud_threshold = np.array([1, 2, 2722, 2720, 2724, 2728, 2732])
            if landsat_nr == 5 or landsat_nr == 7:
                cloud_threshold = np.array([1, 672, 676, 680, 684])

        if collection == 2:
            if landsat_nr == 8 or landsat_nr == 9:
                cloud_threshold = np.array([1, 21824, 21890, 21952, 22080, 23826])  # 2720 =21824, 2724=23826
            if landsat_nr == 5 or landsat_nr == 7:
                cloud_threshold = np.array([1, 5440, 5442, 5504, 5696])  # 672 =5440

        return cloud_threshold

    def is_bqa_assets_exist(self) -> bool:
        """
        :return:
        """
        asset_names = self.get_asset_names()
        bqa_res = [n for n in asset_names if "bqa" in n.lower()]
        return len(bqa_res) > 0

    def calculate_cloud_mask(self, ls_ref_raster: RioRaster):
        """
        Calculate cloud mask
        :param ls_ref_raster:
        :return:
        """
        # df = self.get_bands_meta_data_df()
        asset_names = self.get_asset_names()
        # search bqa or qa_pixel
        qa_res = [n for n in asset_names if "qa_pixel" in n.lower()]
        bqa_res = [n for n in asset_names if "bqa" in n.lower()]
        fp, collection = (None, -1)
        if len(qa_res) > 0:
            fp = self.get_band_file_path(qa_res[0])
            collection = 2
        elif len(bqa_res) > 0:
            fp = self.get_band_file_path(bqa_res[0])
            collection = 1
        else:
            da_logger.error("Quality Assessment Data is not available")
        if fp and collection != -1:
            bqa_raster = RioRaster(fp)
            bqa_raster.make_coincident_with(ls_ref_raster)
            ls_data_bqa = bqa_raster.get_data_array(1)
            ls_data_bqa = np.where(ls_data_bqa == 0, 1, ls_data_bqa)

            cloud_threshold = self.get_cloud_threshold(collection)
            print("create cloud array")
            cloud_mask = np.where(np.isin(ls_data_bqa, cloud_threshold), 0, 1)
            # Surface_temp, cloud_mask_temp = self.calculate_surface_temperature(ls_ref_raster)

            return cloud_mask

    @staticmethod
    def calculate_TOA_temperature(L_lambda, k1_const, k2_const):
        return k2_const / np.log(k1_const / L_lambda + 1.0)

    def calculate_surface_temperature(self, ls_ref_raster: RioRaster, Temp_inst, b10_emissivity, act_vap_inst,
                                      water_mask, cloud_mask=None):
        """
        Calculates the surface temperature
        :param ls_ref_raster:
        :param Temp_inst:
        :param b10_emissivity:
        :param act_vap_inst: actual vapour pressure hourly
        :param water_mask:
        :param cloud_mask: Optional
        :return:
        """

        Landsat_nr = self.get_landsat_no()
        # bands = self.get_bands_for_thermal_calculation()
        # bands_df = self.get_bands_meta_data_df()
        # Lmax = bands_df[bands_df.band_no.isin(bands)]['max_radiance'].tolist()
        # Lmin = bands_df[bands_df.band_no.isin(bands)]['min_radiance'].tolist()
        # k1_c = bands_df[bands_df.band_no.isin(bands)]['k1_thermal_const'].dropna().tolist()
        # k2_c = bands_df[bands_df.band_no.isin(bands)]['k2_thermal_const'].dropna().tolist()

        # Spectral radiance for termal
        thermal_df = self.get_thermal_bands_meta_data()
        # therm_data = self.get_thermal_data(ls_ref_raster)
        # bands_thermal = 2  # reading for Excel file used for input sabel
        bands_thermal = len(thermal_df)
        # surface_temp = np.ndarray([])
        if Landsat_nr in [8, 9]:
            if bands_thermal == 1:
                b_10 = thermal_df.loc[thermal_df.band_no == 10]
                b_10_raster = RioRaster(self.get_band_file_path(b_10.asset_name.values[0]))
                b_10_raster.make_coincident_with(ls_ref_raster)
                L_lambda_b10 = (b_10.max_radiance.values[0] - b_10.min_radiance.values[0]) / (
                        65535 - 1) * b_10_raster.get_data_array(1) + b_10.min_radiance.values[0]

                # Get Temperature
                surface_temp = self.get_thermal(L_lambda_b10, Temp_inst, b10_emissivity,
                                                b_10.k1_thermal_const.values[0], b_10.k2_thermal_const.values[0])

            elif bands_thermal == 2:
                b_10 = thermal_df.loc[thermal_df.band_no == 10]
                b_10_raster = RioRaster(self.get_band_file_path(b_10.asset_name.values[0]))
                b_10_raster.make_coincident_with(ls_ref_raster)
                L_lambda_b10 = (b_10.max_radiance.values[0] - b_10.min_radiance.values[0]) / (
                        65535 - 1) * b_10_raster.get_data_array(1) + b_10.min_radiance.values[0]

                b_11 = thermal_df.loc[thermal_df.band_no == 11]
                b_11_raster = RioRaster(self.get_band_file_path(b_11.asset_name.values[0]))
                b_11_raster.make_coincident_with(ls_ref_raster)
                L_lambda_b11 = (b_11.max_radiance.values[0] - b_11.min_radiance.values[0]) / (
                        65535 - 1) * b_11_raster.get_data_array(1) + b_11.min_radiance.values[0]

                # Brightness temperature
                # From Band 10:
                Temp_TOA_10 = (b_10.k2_thermal_const.values[0] / np.log(
                    b_10.k1_thermal_const.values[0] / L_lambda_b10 + 1.0))
                # From Band 11:
                Temp_TOA_11 = (b_11.k2_thermal_const.values[0] / np.log(
                    b_11.k1_thermal_const.values[0] / L_lambda_b11 + 1.0))
                # Combined:
                surface_temp = (Temp_TOA_10 + 1.378 * (Temp_TOA_10 - Temp_TOA_11) +
                                0.183 * np.power(Temp_TOA_10 - Temp_TOA_11, 2) - 0.268 +
                                (54.30 - 2.238 * act_vap_inst) * (1 - b10_emissivity))

        elif Landsat_nr == 7:
            k1 = 666.09
            k2 = 1282.71
            b_6 = thermal_df.loc[thermal_df.band_no == 6]
            b_6_raster = RioRaster(self.get_band_file_path(b_6.asset_name.values[0]))
            b_6_raster.make_coincident_with(ls_ref_raster)
            L_lambda_b6 = (b_6.max_radiance.values[0] - b_6.min_radiance.values[0]) / (
                    256 - 1) * b_6_raster.get_data_array(1) + b_6.min_radiance.values[0]

            # Brightness temperature - From Band 6:
            surface_temp = self.get_thermal(L_lambda_b6, Temp_inst, b10_emissivity, k1, k2)

        elif Landsat_nr == 5:
            k1 = 607.76
            k2 = 1260.56
            b_6 = thermal_df.loc[thermal_df.band_no == 6]
            b_6_raster = RioRaster(self.get_band_file_path(b_6.asset_name[0]))
            b_6_raster.make_coincident_with(ls_ref_raster)
            L_lambda_b6 = ((b_6.max_radiance[0] - b_6.min_radiance[0]) / (256 - 1) * b_6_raster.get_data_array(1) +
                           b_6.min_radiance[0])

            # Brightness temperature - From Band 6:
            surface_temp = self.get_thermal(L_lambda_b6, Temp_inst, b10_emissivity, k1, k2)
        # Surface temperature
        surface_temp = surface_temp.clip(230.0, 360.0)

        temp_water = np.copy(surface_temp)
        temp_water[water_mask == 0.0] = np.nan
        temp_water_sd = np.nanstd(temp_water)  # Standard deviation
        temp_water_mean = np.nanmean(temp_water)  # Mean
        print('Mean water temperature = ', '%0.3f (Kelvin)' % temp_water_mean)
        print('SD water temperature = ', '%0.3f (Kelvin)' % temp_water_sd)

        if cloud_mask is None:
            surf_temp_offset = self.get_surface_temperature_offset_constant()
            cloud_mask = np.zeros(surface_temp.shape)
            cloud_mask[surface_temp < np.minimum((temp_water_mean - 1.0 * temp_water_sd -
                                                  surf_temp_offset), 290)] = 1.0

        surface_temp[cloud_mask == 1] = np.nan
        thermal_sharpening_not_needed = 0
        print('Mean Surface Temperature = %s Kelvin' % np.nanmean(surface_temp))

        return surface_temp, cloud_mask, thermal_sharpening_not_needed

    def thermal_sharpen_temperature_data(surface_temp):
        pass

    @staticmethod
    def get_transmissivity_of_air_constant():
        """
        Narrowband transmissivity of air, range: [10.4-12.5 µm]
        :return:
        """
        tau_sky = 0.866
        return tau_sky

    @staticmethod
    def get_surface_temperature_offset_constant():
        """
        Surface temperature offset for water
        :return:
        """
        surf_temp_offset = 30  # was3
        return surf_temp_offset

    @staticmethod
    def get_path_radiance_constant(is_band_range_10_to_12):
        """
        Recommended, Range: [0.025 - 0.04], based on Bastiaanssen (2000).
        Path radiance (Rp) is 0.91  in the 10.4-12.5 µm band (W/m2/sr/µm)
        :return: path radiance
        """
        if is_band_range_10_to_12:
            return 0.91  # this is for Rp
        else:
            return 0.03

    def get_thermal(self, lambda_b10, Temp_inst, TIR_Emissivity, k1, k2):
        # Narrow band downward thermal radiation from clear sky, rsky (W/m2/sr/µm)
        rsky = (1.807E-10 * np.power(Temp_inst + 273.15, 4) * (1 - 0.26 *
                                                               np.exp(-7.77E-4 * np.power((-Temp_inst), -2))))

        print('Rsky = ', '%0.3f (W/m2/sr/µm)' % np.nanmean(rsky))

        # Corrected thermal radiance from the surface, Wukelikc et al. (1989):
        tau_sky = self.get_transmissivity_of_air_constant()
        Rp = self.get_path_radiance_constant(True)
        correc_lambda_b10 = ((lambda_b10 - Rp) / tau_sky -
                             (1.0 - TIR_Emissivity) * rsky)

        # Brightness temperature - From Band 10:
        temp_toa = (k2 / np.log(TIR_Emissivity * k1 /
                                correc_lambda_b10 + 1.0))

        return temp_toa

    @staticmethod
    def get_file_name_format():
        """
        :return: filename format
        """
        return "LC*_L***_*_*_*_T1_*.TIF"

    @staticmethod
    def get_row_path(name):
        """
        :param cls:
        :param name:
        :return:
        """
        row_path = name.split("_")[2]
        return row_path

    @staticmethod
    def get_sensor_no(name):
        sensor = name.split("_")[0][2:]
        return int(sensor)

    def create_brovey_transformation(self):
        asset_list = self.get_data_asset_list()
        band_stacks = self.create_band_stacks()
        print(len(band_stacks))


if __name__ == '__main__':
    file_fp = "/Users/atherashraf/PycharmProjects/DigitalArz/IPI/media/LS/LC08_L1TP_150039_20220211_20220222_02_T1.tar"
    media_dir = "/Users/atherashraf/PycharmProjects/DigitalArz/da_ipi/media"
    out_dir = os.path.join(media_dir, "Output_Data/LS_SEBAL/15039_20220211/")
    radiation_balance_fp = os.path.join(out_dir, 'Output_radiation_balance')
    example_fp = os.path.join(radiation_balance_fp, 'proy_DEM_30m.tif')
    example_raster = RioRaster(example_fp)
    # cos_zn_fp = os.path.join(radiation_balance_fp, 'cos_zn_30m_20220211.tif')
    # cos_zenith = RioRaster(cos_zn_fp).get_data_array(1)
    #
    input_rio_ds = RioLandsat(file_fp)
    sun_elevation = input_rio_ds.get_sun_elevation()
    # ref_raster_ls = input_rio_ds.get_reference_ls_raster(ref_raster=example_raster)
    # temp_folder = os.path.join(radiation_balance_fp, 'Temp')
    # if not os.path.exists(temp_folder):
    #     os.makedirs(temp_folder)
    # ref_raster_ls.save_to_file(os.path.join(temp_folder, 'ls_blue_band.tif'))
    """ Vegetation Parameter"""
    # reflect, radiance = input_rio_ds.calculate_TOA_reflectance_radiance(cos_zenith, ls_ref_raster=ref_raster_ls, output_folder=out_dir)
    # input_rio_ds.get_para_veg(out_dir, ref_raster_ls, reflect, radiance)
    """ thermal parameter"""
    # thermal_arr = input_rio_ds.get_thermal_data(ls_ref_raster=ref_raster_ls)
    # input_rio_ds.create_cloud_mask()
