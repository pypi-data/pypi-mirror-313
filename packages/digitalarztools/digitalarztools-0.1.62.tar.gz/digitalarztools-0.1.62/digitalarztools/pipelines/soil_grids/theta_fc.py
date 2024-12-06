import os

import numpy as np

from digitalarztools.pipelines.soil_grids.n_van_genuchten import NVanGenuchten
from digitalarztools.pipelines.soil_grids.theta_res import ThetaRes
from digitalarztools.pipelines.soil_grids.theta_sat2 import ThetaSat2
from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.utils.logger import da_logger


class ThetaFC:
    @classmethod
    def top_soil(cls, des_dir, lat_lim, lon_lim) -> str:
        """
        This function calculates the Theta Field Capacity soil characteristic (15cm)

        Keyword arguments:
        :param des_dir: destination director
        :param lat_lim: latitude limit
        :param lon_lim: longitude limit
        :return filepath of the top soil
        """

        da_logger.info('\nCreate Theta Field Capacity map of the topsoil from SoilGrids')

        # Define parameters to define the topsoil
        SL = "sl3"

        return cls.calc_property(des_dir, lat_lim, lon_lim, SL)

    @classmethod
    def sub_soil(cls, des_dir, lat_lim, lon_lim) -> str:
        """
        This function calculates the Theta Field Capacity characteristic (100cm)

        Keyword arguments:
        :param des_dir: destination director
        :param lat_lim: latitude limit
        :param lon_lim: longitude limit
        :return filename of the sub soil
        """

        da_logger.info('\nCreate Theta Field Capacity map of the subsoil from SoilGrids')

        # Define parameters to define the subsoil	
        SL = "sl6"

        return cls.calc_property(des_dir, lat_lim, lon_lim, SL)

    @staticmethod
    def calc_property(des_dir, lat_lim, lon_lim, SL) -> str:

        """
        :param des_dir: destination folder
        :param lat_lim: latitude limit / extent
        :param lon_lim: longitude limit / extent
        :param SL: Soil level value in "sl3" for top soil or "sl6" for sub soil
        :return file path of the file
        """
        # Define level
        if SL == "sl3":
            level = "Topsoil"
        elif SL == "sl6":
            level = "Subsoil"

            # check if you need to download
        filename_out_thetasat = os.path.join(des_dir, 'SoilGrids', 'Theta_Sat',
                                             'Theta_Sat2_%s_SoilGrids_kg-kg.tif' % level)
        if not os.path.exists(filename_out_thetasat):
            if SL == "sl3":
                ThetaSat2.top_soil(des_dir, lat_lim, lon_lim)
            elif SL == "sl6":
                ThetaSat2.sub_soil(des_dir, lat_lim, lon_lim)

        filename_out_thetares = os.path.join(des_dir, 'SoilGrids', 'Theta_Res',
                                             'Theta_Res_%s_SoilGrids_kg-kg.tif' % level)
        if not os.path.exists(filename_out_thetares):
            if SL == "sl3":
                ThetaRes.top_soil(des_dir, lat_lim, lon_lim)
            elif SL == "sl6":
                ThetaRes.sub_soil(des_dir, lat_lim, lon_lim)

        filename_out_n_genuchten = os.path.join(des_dir, 'SoilGrids', 'N_van_genuchten',
                                                'N_genuchten_%s_SoilGrids_-.tif' % level)
        if not os.path.exists(filename_out_n_genuchten):
            if SL == "sl3":
                NVanGenuchten.top_soil(des_dir, lat_lim, lon_lim)
            elif SL == "sl6":
                NVanGenuchten.sub_soil(des_dir, lat_lim, lon_lim)

        filedes_dir_out_thetafc = os.path.join(des_dir, 'SoilGrids', 'Theta_FC')
        if not os.path.exists(filedes_dir_out_thetafc):
            os.makedirs(filedes_dir_out_thetafc)

            # Define theta field capacity output
        filename_out_thetafc = os.path.join(filedes_dir_out_thetafc, 'Theta_FC2_%s_SoilGrids_cm3-cm3.tif' % level)

        if not os.path.exists(filename_out_thetafc):
            # Get info layer
            # geo_out, proj, size_X, size_Y = RC.Open_array_info(filename_out_thetasat)
            theta_sat_raster = RioRaster(filename_out_thetasat)
            # Open dataset
            theta_sat = theta_sat_raster.get_data_array(1)
            theta_res = RioRaster(filename_out_thetares).get_data_array(1)
            n_genuchten = RioRaster(filename_out_n_genuchten).get_data_array(1)

            # Calculate theta field capacity
            theta_FC = np.ones(theta_sat.shape) * -9999
            # theta_FC = np.where(theta_sat < 0.301, 0.042, np.arccosh(theta_sat + 0.7) - 0.32 * (theta_sat + 0.7) + 0.2)        
            # theta_FC = np.where(theta_sat < 0.301, 0.042, -2.95*theta_sat**2+3.96*theta_sat-0.871)   

            theta_FC = theta_res + (theta_sat - theta_res) / (1 + (0.02 * 200) ** n_genuchten) ** (1 - 1 / n_genuchten)
            # Save as tiff
            RioRaster.write_to_file(filename_out_thetafc, theta_FC, theta_sat_raster.get_pyproj_crs(),
                                    theta_sat_raster.get_geo_transform(), theta_sat_raster.get_nodata_value())

        return filename_out_thetafc
