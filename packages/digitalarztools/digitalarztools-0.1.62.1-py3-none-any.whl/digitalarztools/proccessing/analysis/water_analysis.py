import numpy as np


class WaterAnalysis:
    @staticmethod
    def calculate_water_mask(green_band: np.ndarray, red_band: np.ndarray,
                             nir08_band: np.ndarray, swir16_band: np.ndarray):
        """
        Calculates the water and cloud mask from TOA planetary Reflectance Rho Lambda (ρλ)
        :param green_band:
        :param red_band:
        :param nir08_band:
        :param swir16_band:
        :return:
        """
        mask = np.zeros(green_band.shape)
        mask[np.logical_and(nir08_band < red_band,
                            swir16_band < green_band)] = 1.0
        # water_mask = np.copy(mask)
        return mask

