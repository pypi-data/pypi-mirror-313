# -*- coding: utf-8 -*-
'''
Authors: Ather Ashraf
Module: Products/SoilGrids
'''

import os
import numpy as np

from digitalarztools.pipelines.soil_grids.soil_contents import SoilContent
from digitalarztools.io.raster.band_process import BandProcess
from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.utils.logger import da_logger


class ThetaSat2:
    @classmethod
    def top_soil(cls, des_dir, lat_lim, lon_lim, GF=True) -> str:
        """
        This function calculates the topsoil saturated soil characteristic (15cm)

        Keyword arguments:
        :param des_dir: destination director
        :param lat_lim: latitude limit
        :param lon_lim: longitude limit
        :param GF: boolean for gap filling
        :return file path of the file
        """

        da_logger.info('\nCreate Theta Saturated map of the topsoil from SoilGrids')

        # Define parameters to define the topsoil
        SL = "sl3"

        return cls.calc_property(des_dir, lat_lim, lon_lim, SL, GF)

    @classmethod
    def sub_soil(cls, des_dir, lat_lim, lon_lim, GF=True) -> str:
        """
        This function calculates the subsoil saturated soil characteristic (100cm)

        Keyword arguments:
        :param des_dir: desitination director
        :param lat_lim: latitude limit
        :param lon_lim: longitude limit
        :param GF: boolean for gap filling
        :return file path of the file
        """

        da_logger.info('\nCreate Theta Saturated map of the subsoil from SoilGrids')

        # Define parameters to define the subsoil
        SL = "sl6"

        return cls.calc_property(des_dir, lat_lim, lon_lim, SL, GF)

    @staticmethod
    def calc_property(des_dir, lat_lim, lon_lim, SL, GF=True) -> str:
        """
        :param des_dir: content destination
        :param lat_lim: latitude limit
        :param lon_lim: longitude limit
        :param SL: Soil level value in "sl3" for top soil or "sl6" for sub soil
        :param GF:  Gap Filling Boolean
        :return file path of the file
        """
        # import watertools.Collect.SoilGrids as SG

        # Download needed layers
        SoilContent.get_clay_content(des_dir, lat_lim, lon_lim, level=SL)
        SoilContent.get_silt_content(des_dir, lat_lim, lon_lim, level=SL)
        SoilContent.get_organic_carbon_content(des_dir, lat_lim, lon_lim, level=SL)
        SoilContent.get_bulk_density(des_dir, lat_lim, lon_lim, level=SL)

        # Define path to layers
        filename_clay = os.path.join(des_dir, 'SoilGrids', 'Clay_Content',
                                     'ClayContentMassFraction_%s_SoilGrids_percentage.tif' % SL)
        filename_soc = os.path.join(des_dir, 'SoilGrids', 'Soil_Organic_Carbon_Content',
                                    'SoilOrganicCarbonContent_%s_SoilGrids_g_kg.tif' % SL)
        filename_bulkdensity = os.path.join(des_dir, 'SoilGrids', 'Bulk_Density',
                                            'BulkDensity_%s_SoilGrids_kg-m-3.tif' % SL)
        filename_silt = os.path.join(des_dir, 'SoilGrids', 'Silt_Content',
                                     'SiltContentMassFraction_%s_SoilGrids_percentage.tif' % SL)

        # Define path for output
        if SL == "sl3":
            level = "Topsoil"
        elif SL == "sl6":
            level = "Subsoil"

        filedir_out_densbulk = os.path.join(des_dir, 'SoilGrids', 'Bulk_Density')
        if not os.path.exists(filedir_out_densbulk):
            os.makedirs(filedir_out_densbulk)
        filedir_out_thetasat = os.path.join(des_dir, 'SoilGrids', 'Theta_Sat')
        if not os.path.exists(filedir_out_thetasat):
            os.makedirs(filedir_out_thetasat)

            # filename_out_densbulk = os.path.join(filedir_out_densbulk ,'Bulk_Density_%s_SoilGrids_g-cm-3.tif' %level)
        filename_out_thetasat = os.path.join(filedir_out_thetasat, 'Theta_Sat2_%s_SoilGrids_kg-kg.tif' % level)

        # if not (os.path.exists(filename_out_densbulk) and os.path.exists(filename_out_thetasat)):
        if not os.path.exists(filename_out_thetasat):

            # Open datasets
            # dest_clay = gdal.Open(filename_clay)
            # dest_soc = gdal.Open(filename_soc)
            # dest_bulk = gdal.Open(filename_bulkdensity)
            # dest_silt = gdal.Open(filename_silt)
            clay_raster = RioRaster(filename_clay)
            soc_raster = RioRaster(filename_soc)
            bulk_density_raster = RioRaster(filename_bulkdensity)
            silt_raster = RioRaster(filename_silt)

            # Open Array info
            # geo_out, proj, size_X, size_Y = RC.Open_array_info(filename_clay)

            # Open Arrays
            # Clay = dest_clay.GetRasterBand(1).ReadAsArray()
            # SOC = dest_soc.GetRasterBand(1).ReadAsArray()
            # Silt = dest_silt.GetRasterBand(1).ReadAsArray()
            Clay = clay_raster.get_data_array(1)
            SOC = soc_raster.get_data_array(1)
            Silt = silt_raster.get_data_array(1)

            Clay = np.float_(Clay)
            Clay = BandProcess.gap_filling(Clay, 0, method=1)
            OM = np.float_(SOC) * 1.72  # organic carbon to organic matter g/kg
            OM = BandProcess.gap_filling(OM, 0, method=1)
            Silt = np.float_(Silt)
            Silt = BandProcess.gap_filling(Silt, 0, method=1)
            Clay[Clay > 100] = np.nan
            Silt[Silt > 100] = np.nan
            OM = OM / 10  # g/kg to %

            Clay[Clay == 0] = np.nan
            Silt[Silt == 0] = np.nan
            OM[OM == 0] = np.nan

            # Calculate bulk density
            # bulk_dens1 = dest_bulk.GetRasterBand(1).ReadAsArray()
            bulk_dens1 = bulk_density_raster.get_data_array(1)
            bulk_dens1 = bulk_dens1 / 1000  # kg/m2 to gr/cm3
            bulk_dens1 = np.float_(bulk_dens1)
            bulk_dens1 = BandProcess.gap_filling(bulk_dens1, 0, method=1)

            bulk_dens2 = 1 / (0.6117 + 0.3601 * Clay / 100 + 0.002172 * np.power(OM, 2) + 0.01715 * np.log(OM))
            bulk_dens2 = BandProcess.gap_filling(bulk_dens2, 0, method=1)

            bulk_dens = bulk_dens2  # np.where(bulk_dens1>bulk_dens2, bulk_dens1, bulk_dens2)

            '''
            # Calculate theta saturated
            theta_sat = 0.85 * (1- (bulk_dens/2.65)) + 0.13 * Clay/100
            '''
            # Nieuwe methode gebaseerd op Toth et al (2014)

            # Calculate silt fraction based on clay fraction
            # Silt_fraction = 0.7 * (Clay/100) ** 2 + 0.308 * Clay/100
            Silt_fraction = Silt / 100

            # Calculate theta sat
            nodata_value = -9999
            theta_sat = 0.8308 - 0.28217 * bulk_dens + 0.02728 * Clay / 100 + 0.0187 * Silt_fraction
            theta_sat[Clay == 0] = nodata_value

            if GF:
                theta_sat = BandProcess.gap_filling(theta_sat, nodata_value, method=1)

            # Save data
            # # DC.Save_as_tiff(filename_out_densbulk, bulk_dens, geo_out, "WGS84")
            # DC.Save_as_tiff(filename_out_thetasat, theta_sat, geo_out, "WGS84")
            RioRaster.write_to_file(filename_out_thetasat, theta_sat, clay_raster.get_crs(),
                                    clay_raster.get_geo_transform(), nodata_value)
            return filename_out_thetasat
