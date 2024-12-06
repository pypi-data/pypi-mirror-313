import os

import numpy as np

from digitalarztools.pipelines.soil_grids.theta_sat2 import ThetaSat2
from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.utils.logger import da_logger


class ThetaRes:
    @classmethod
    def top_soil(cls, des_dir, lat_lim, lon_lim) -> str:
        """
        This function calculates the topsoil Theta residual soil characteristic (15cm)

        Keyword arguments:
        :param des_dir: destination directory
        :param lat_lim: latitude limit/extent
        :param lon_lim: longitude limit/extent
        :return file path of the top soil
        """

        da_logger.info('\nCreate Theta residual map of the topsoil from SoilGrids')

        # Define parameters to define the topsoil
        SL = "sl3"

        return cls.calc_property(des_dir, lat_lim, lon_lim, SL)

    @classmethod
    def sub_soil(cls, des_dir, lat_lim, lon_lim) -> str:
        """
        This function calculates the subsoil Theta residual soil characteristic (100cm)

        Keyword arguments:
        :param des_dir: destination directory
        :param lat_lim: latitude limit/extent
        :param lon_lim: longitude limit/extent
        :return file path of the sub soil
        """

        da_logger.info('\nCreate Theta residual map of the subsoil from SoilGrids')

        # Define parameters to define the subsoil
        SL = "sl6"

        return cls.calc_property(des_dir, lat_lim, lon_lim, SL)

    @staticmethod
    def calc_property(des_dir, lat_lim, lon_lim, SL) -> str:
        """
        :param des_dir: destination directory
        :param lat_lim: latitude limit/extent
        :param lon_lim: longitude limit/extent
        :param SL: Soil level value in "sl3" for top soil or "sl6" for sub soil
        :return: file path of the property
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

        filedes_dir_out_thetares = os.path.join(des_dir, 'SoilGrids', 'Theta_Res')
        if not os.path.exists(filedes_dir_out_thetares):
            os.makedirs(filedes_dir_out_thetares)

            # Define theta field capacity output
        filename_out_thetares = os.path.join(filedes_dir_out_thetares, 'Theta_Res_%s_SoilGrids_kg-kg.tif' % level)

        if not os.path.exists(filename_out_thetares):
            # Get info layer
            # geo_out, proj, size_X, size_Y = RC.Open_array_info(filename_out_thetasat)

            # Open dataset
            theta_sat_raster = RioRaster(filename_out_thetasat)
            theta_sat = theta_sat_raster.get_data_array(1)

            # Calculate theta field capacity
            theta_Res = np.ones(theta_sat.shape) * -9999
            # theta_Res = np.where(theta_sat < 0.351, 0.01, 0.4 * np.arccosh(theta_sat + 0.65) - 0.05 * np.power(theta_sat + 0.65, 2.5) + 0.02)
            theta_Res = np.where(theta_sat < 0.351, 0.01, 0.271 * np.log(theta_sat) + 0.335)
            # Save as tiff
            RioRaster.write_to_file(filename_out_thetares, theta_Res, theta_sat_raster.get_pyproj_crs(),
                                    theta_sat_raster.get_geo_transform(), theta_sat_raster.get_nodata_value())
        return filename_out_thetares
