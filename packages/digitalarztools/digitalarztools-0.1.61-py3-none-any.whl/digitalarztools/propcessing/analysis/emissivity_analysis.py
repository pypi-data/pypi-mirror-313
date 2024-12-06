import numpy as np


class EmissivityAnalysis:
    """
        Emissivity is the measure of an object's ability to emit infrared energy
        Emissivity can have a value from 0 (shiny mirror) to 1.0 (blackbody)
    """

    @staticmethod
    def calculate_b10_emissivity(water_mask, lai):
        """
        Calculate b10 emissivity (b10 may be band 10 of landsat which is LWIR need to dig out)
        :param water_mask:
        :param lai: leaf area index
        :return:
        """
        b10_emissivity = np.where(lai <= 3.0, 0.95 + 0.01 * lai, 0.98)
        b10_emissivity[water_mask != 0.0] = 1.0
        return b10_emissivity

    @staticmethod
    def calculate_thermal_infrared_emissivity(ndvi, water_mask):
        """
        Calculate Thermal infrared emissivity
        :param ndvi:
        :param water_mask:
        :return:
        """
        tir_emis = 1.009 + 0.047 * np.log(ndvi)
        tir_emis[np.logical_or(water_mask == 1.0, water_mask == 2.0)] = 1.0
        tir_emis[np.logical_and(ndvi < 0.125, water_mask == 0.0)] = 0.92
        return tir_emis

    @staticmethod
    def calculate_atmospheric_emissivity(transmissivity_corr):
        """
        :param transmissivity_corr: Transmissivity Correction using SolarRadiationAnalysis.calculate_transmissivity_correction
        :return:
        """
        atmos_emis = 0.85 * np.power(-np.log(transmissivity_corr), 0.09)
        return atmos_emis