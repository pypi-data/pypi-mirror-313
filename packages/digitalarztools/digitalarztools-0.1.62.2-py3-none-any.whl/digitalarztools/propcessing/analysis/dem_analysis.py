from math import cos
from typing import Optional

import numpy as np
import pandas as pd
from digitalarztools.raster.rio_raster import RioRaster


class DEMAnalysis:
    def __init__(self, dem: RioRaster):
        self.dem = dem

    def get_z_factor(self, z_in="m", lat=None) -> float:
        """
        get z_factor value
        :param z_in: either in m of ft
        :param lat: if dem x,y in dd then  this need to pass for z
        :return:
        """
        z = 1
        unit = self.dem.get_unit()
        if unit == "m":
            z = 1
        elif unit in ["dd", "dms"]:
            if lat is None:
                raise Exception("latitude can't be null if raster unit are in dd or dms")
            df = pd.DataFrame({
                "latitude": [0, 10, 20, 30, 40, 50, 60, 70, 80],
                "z_meter": [0.00000898, 0.00000912, 0.00000956, 0.00001036, 0.00001171, 0.00001395,
                            0.00001792, 0.00002619, 0.00005156],
                "z_feet": [0.00000273, 0.00000278, 0.00000291, 0.00000316, 0.00000357, 0.00000425,
                           0.00000546, 0.00000798, 0.00001571]
            })
            lat = round(lat)
            row = df.loc[df.latitude == lat]
            z = row.z_meter if z_in == "m" else row.z_feet
        elif unit == "ft" and z_in == "m":
            z = 3.28
        elif unit == "m" and z_in == "ft":
            z = 0.3048
        return z

    @staticmethod
    def get_rad_2_degree():
        return 180.0 / np.pi

    @staticmethod
    def get_degree_2_radian(self):
        return np.pi / 180

    def get_slope_data(self, gradiant_x=None, gradiant_y=None) -> np.ndarray:
        """
        calculate slope raster using gradiant_x and gradiant_y
        :param gradiant_x:
        :param gradiant_y:
        :return:
        """
        if gradiant_x is None or gradiant_y is None:
            gradiant_x, gradiant_y = self.get_gradient()
        hypotenuse_array = np.hypot(gradiant_x, gradiant_y)
        slope = np.arctan(hypotenuse_array) * self.get_rad_2_degree()
        # slope = np.arctan(np.sqrt(np.square(x/pixel_spacing) + np.square(y/pixel_spacing))) * rad2deg
        # slope_ds = RioRaster.rio_dataset_from_array(slope, self.dem.get_metadata_copy())
        return slope

    def get_aspect_data(self, gradient_x=None, gradient_y=None) -> np.ndarray:
        """
        calculate aspect from the gradient of the dem
        :param gradient_x:
        :param gradient_y:
        :return:
        """
        if gradient_x is None or gradient_y is None:
            gradient_x, gradient_y = self.get_gradient()
        res_x, res_y = self.dem.get_spatial_resoultion()
        aspect = np.arctan2(gradient_y / res_y, -gradient_x / res_x) * self.get_rad_2_degree()
        aspect = 180 + aspect
        # aspect_ds = RioRaster.rio_dataset_from_array(aspect, self.dem.get_metadata_copy())
        return aspect

    def get_gradient(self):
        """
        calculate gradient of elevation data
        :return: gradient_x, and gradient_y
        """

        res_x, res_y = self.dem.get_spatial_resoultion()
        elevation_data = self.dem.get_data_array(1)
        # elevation_data[elevation_data == self.dem.get_nodata_value()] = np.nan
        elevation_data = elevation_data * self.get_z_factor()

        return np.gradient(elevation_data, res_x, res_y)

    def calculate_slope_aspect_raster(self):
        gradient_x, gradient_y = self.get_gradient()
        # Calculate slope
        slope_raster = self.get_slope_raster(gradient_x, gradient_y)
        # calculate aspect
        aspect_raster = self.get_aspect_raster(gradient_x, gradient_y)

        return slope_raster, aspect_raster
