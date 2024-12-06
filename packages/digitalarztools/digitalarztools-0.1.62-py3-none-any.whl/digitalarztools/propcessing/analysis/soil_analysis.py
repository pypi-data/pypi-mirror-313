from math import log

import numpy as np
from digitalarztools.io.raster.rio_raster import RioRaster

from digitalarztools.pipelines.soil_grids.theta_fc import ThetaFC
from digitalarztools.pipelines.soil_grids.theta_res import ThetaRes
from digitalarztools.pipelines.soil_grids.theta_sat2 import ThetaSat2


class SoilAnalysis:
    @staticmethod
    def calculate_sub_soil_parameters(content_dir, lat_lim, lon_lim) -> (str, str, str):
        """
        Calculate and save Soil parameter like Theta Field Capacity (FC), Theta residual soil characteristic (Res),
        and Theta saturated soil characteristic (Sat)
        :param content_dir:
        :param lat_lim:
        :param lon_lim:
        :return: file path of sat, fc, and res of sub soil
        """
        lat_lim_SG = [lat_lim[0] - 0.5, lat_lim[1] + 0.5]
        lon_lim_SG = [lon_lim[0] - 0.5, lon_lim[1] + 0.5]
        sat_sub_fp = ThetaSat2.sub_soil(content_dir, lat_lim_SG, lon_lim_SG)
        fc_sub_fp = ThetaFC.sub_soil(content_dir, lat_lim_SG, lon_lim_SG)
        res_sub_fp = ThetaRes.sub_soil(content_dir, lat_lim_SG, lon_lim_SG)
        return sat_sub_fp, fc_sub_fp, res_sub_fp

    @staticmethod
    def calculate_top_soil_parameters(content_dir, lat_lim, lon_lim) -> (str, str, str):
        """
        Calculate and save Soil parameter like Theta Field Capacity (FC), Theta residual soil characteristic (Res),
        and Theta saturated soil characteristic (Sat)
        :param content_dir:
        :param lat_lim:
        :param lon_lim:
        :return: file path of sat, fc, and res of top soil
        """
        lat_lim_SG = [lat_lim[0] - 0.5, lat_lim[1] + 0.5]
        lon_lim_SG = [lon_lim[0] - 0.5, lon_lim[1] + 0.5]
        sat_top_fp = ThetaSat2.top_soil(content_dir, lat_lim_SG, lon_lim_SG)
        fc_top_fp = ThetaFC.top_soil(content_dir, lat_lim_SG, lon_lim_SG)
        res_top_fp = ThetaRes.top_soil(content_dir, lat_lim_SG, lon_lim_SG)
        return sat_top_fp, fc_top_fp, res_top_fp

    @staticmethod
    def calculate_soil_moisture(ETA_24, EF_inst, QC_Map, water_mask, vegt_cover, Theta_sat_top, Theta_sat_sub, Theta_res_top, Theta_res_sub, depl_factor, Field_Capacity, FPAR, Soil_moisture_wilting_point):
        """
        Function to calculate soil characteristics
        :param ETA_24: EnergyBalanceModel.calculate_daily_evaporation
        :param EF_inst: EnergyBalanceModel.calculate_instantaneous_ET_fraction
        :param QC_Map: Total Quality map snow_mask + water_mask + ndvi_qc_mask
        :param water_mask: RioLandsat.water_mask
        :param vegt_cover:  VegetationAnalysis.vegtetation_cover
        :param Theta_sat_top:
        :param Theta_sat_sub:
        :param Theta_res_top:
        :param Theta_res_sub:
        :param depl_factor: 0.43
        :param Field_Capacity: Theta_FC2_Subsoil_SoilGrids
        :param FPAR: VegetationAnalysis.calculate_FPAR
        :param Soil_moisture_wilting_point: 0.14
        :return:
        Critical value under which plants get stressed,
        Total soil water content (cm3/cm3)
        Root zone moisture first
         moisture stress biomass
         Top zone moisture
         Root zone moisture NAN
        """
        # constants:
        Veg_Cover_Threshold_RZ = 0.9  # Threshold vegetation cover for root zone moisture

        # Average fraction of TAW that can be depleted from the root zone
        # before stress:
        p_factor = depl_factor + 0.04 * (5.0 - ETA_24)  # page 163 of FAO 56
        # The factor p differs from one crop to another. It normally varies from
        # 0.30 for shallow rooted plants at high rates of ETc (> 8 mm d-1)
        # to 0.70 for deep rooted plants at low rates of ETc (< 3 mm d-1)

        # Critical value under which plants get stressed:
        SM_stress_trigger = Field_Capacity - p_factor * (Field_Capacity - Soil_moisture_wilting_point)
        EF_inst[EF_inst >= 1.0] = 0.999

        # Total soil water content (cm3/cm3):
        total_soil_moisture = Theta_sat_sub * np.exp((EF_inst - 1.0) / 0.421)  # asce paper Scott et al. 2003
        total_soil_moisture[np.logical_or(water_mask == 1.0, QC_Map == 1.0)] = 1.0  # In water and snow is 1
        total_soil_moisture[QC_Map == 1.0] = np.nan  # Where clouds no data

        # Root zone soil moisture:
        RZ_SM = np.copy(total_soil_moisture)
        RZ_SM[vegt_cover <= Veg_Cover_Threshold_RZ] = np.nan
        if np.isnan(np.nanmean(RZ_SM)) == True:
            Veg_Cover_Threshold_RZ = np.nanpercentile(vegt_cover, 80)
            RZ_SM = np.copy(total_soil_moisture)
            RZ_SM[vegt_cover <= Veg_Cover_Threshold_RZ] = np.nan
            print('No RZ_SM so the vegetation Threshold for RZ is adjusted from 0,9 to =', '%0.3f' % Veg_Cover_Threshold_RZ)

        # RZ_SM = RZ_SM.clip(Theta_res, (0.85 * Theta_sat))
        # RZ_SM[np.logical_or(water_mask == 1.0, water_mask == 2.0)] = 1.0
        RZ_SM_NAN = np.copy(RZ_SM)
        RZ_SM_NAN[RZ_SM == 0] = np.nan
        RZ_SM_min = np.nanmin(RZ_SM_NAN)
        RZ_SM_max = np.nanmax(RZ_SM_NAN)
        RZ_SM_mean = np.nanmean(RZ_SM_NAN)
        print('Root Zone Soil moisture mean =', '%0.3f (cm3/cm3)' % RZ_SM_mean)
        print('Root Zone Soil moisture min =', '%0.3f (cm3/cm3)' % RZ_SM_min)
        print('Root Zone Soil moisture max =', '%0.3f (cm3/cm3)' % RZ_SM_max)

        Max_moisture_RZ = vegt_cover * (RZ_SM_max - RZ_SM_mean) + RZ_SM_mean

        # Soil moisture in the top (temporary)
        top_soil_moisture_temp = np.copy(total_soil_moisture)
        top_soil_moisture_temp[np.logical_or(vegt_cover <= 0.02, vegt_cover >= 0.1)] = 0
        top_soil_moisture_temp[top_soil_moisture_temp == 0] = np.nan
        top_soil_moisture_std = np.nanstd(top_soil_moisture_temp)
        top_soil_moisture_mean = np.nanmean(top_soil_moisture_temp)
        print('Top Soil moisture mean =', '%0.3f (cm3/cm3)' % top_soil_moisture_mean)
        print('Top Soil moisture Standard Deviation', '%0.3f (cm3/cm3)' % top_soil_moisture_std)

        # calculate root zone moisture
        root_zone_moisture_temp = (total_soil_moisture - (top_soil_moisture_mean + top_soil_moisture_std) * (1 - vegt_cover)) / vegt_cover  # total soil moisture = soil moisture no vegtatation *(1-vegt_cover)+soil moisture root zone * vegt_cover
        try:
            root_zone_moisture_temp[root_zone_moisture_temp <= Theta_res_sub] = Theta_res_sub[root_zone_moisture_temp <= Theta_res_sub]
        except:
            root_zone_moisture_temp[root_zone_moisture_temp <= Theta_res_sub] = Theta_res_sub

        root_zone_moisture_temp[root_zone_moisture_temp >= Max_moisture_RZ] = Max_moisture_RZ[root_zone_moisture_temp >= Max_moisture_RZ]

        root_zone_moisture_first = np.copy(root_zone_moisture_temp)
        root_zone_moisture_first[np.logical_or(QC_Map == 1.0, np.logical_or(water_mask == 1.0, vegt_cover < 0.0))] = 0

        # Normalized stress trigger:
        norm_trigger = (root_zone_moisture_first - Soil_moisture_wilting_point) / (SM_stress_trigger + 0.02 - Soil_moisture_wilting_point)
        norm_trigger[norm_trigger > 1.0] = 1.0

        # moisture stress biomass:
        moisture_stress_biomass_first = norm_trigger - (np.sin(2 * np.pi * norm_trigger)) / (2 * np.pi)
        moisture_stress_biomass_first = np.where(moisture_stress_biomass_first < 0.5 * FPAR, 0.5 * FPAR, moisture_stress_biomass_first)
        moisture_stress_biomass_first[moisture_stress_biomass_first <= 0.0] = 0
        moisture_stress_biomass_first[moisture_stress_biomass_first > 1.0] = 1.0

        # Soil moisture in the top layer - Recalculated ??
        top_soil_moisture = ((total_soil_moisture - root_zone_moisture_first * vegt_cover) / (1.0 - vegt_cover))

        try:
            top_soil_moisture[top_soil_moisture > Theta_sat_top] = Theta_sat_top[top_soil_moisture > Theta_sat_top]
        except:
            top_soil_moisture[top_soil_moisture > Theta_sat_top] = Theta_sat_top

        top_soil_moisture[np.logical_or(water_mask == 1.0, QC_Map == 1.0)] = 1.0

        return SM_stress_trigger, total_soil_moisture, root_zone_moisture_first, moisture_stress_biomass_first, top_soil_moisture, RZ_SM_NAN

    @staticmethod
    def soil_fraction(lai):
        """
        Computes the effect of the vegetation has in separating the net radiation
        into a soil and canopy component. If the canopy has a full cover almost
        no radiation reaches the soil.

        Parameters
        ----------
        lai : np.ndarray or float
            leaf area index
            :math:`I_{lai}`
            [-]

        Returns
        -------
        sf_soil : np.ndarray or float
            soil fraction
            :math:`s_f`
            [-]

        Examples
        --------
            import ETLook.radiation as rad
            rad.soil_fraction(3.0)
            0.16529888822158656
        """
        return np.exp(-0.6 * lai)

    @staticmethod
    def initial_soil_aerodynamic_resistance(u_24, z_obs=2):
        """
        Computes the aerodynamic resistance for soil without stability corrections

        where the following constants are used

        * :math:`z_{0,soil}` soil roughness = 0.001 [m]
        * :math:`k` = karman constant = 0.41 [-]

        The factor 0.1 is the ratio between the surface roughness for momentum and
        heat.

        Parameters
        ----------
        u_24 : np.ndarray or float
            daily wind speed at observation height
            :math:`u_obs`
            [m/s]

        z_obs : np.ndarray or float
            observation height
            :math:`z_{obs}`
            [m]

        Returns
        -------
        ra_soil_init : np.ndarray or float
            aerodynamic resistance without stability corrections
            :math:`r_{a1,soil}^{0}`
            [s/m]

        """
        z0_soil = 0.001  # soil roughness m
        k = 0.41  # karman constant (-)
        return (log(z_obs / z0_soil) * log(z_obs / (0.1 * z0_soil))) / (k ** 2 * u_24)

    @classmethod
    def calculate_soil_porosity(cls, clay: RioRaster, sand:RioRaster, silt:RioRaster) -> RioRaster:
        """
        Calculate the texture based soil porosity using
        Porosity=1 − ((Clay+Silt)/100)*0.67 - (Sand/100)*0.35
        Porosity = 1 - a - b
        """
        clay_band = clay.get_data_array(1)
        sand_band = sand.get_data_array(1)
        silt_band = silt.get_data_array(1)
        a = (clay_band + silt_band)/100 * 0.67
        b = sand_band/100 * 0.35
        porosity = 1 - a -b
        porosity_raster = RioRaster.raster_from_array(porosity, clay.get_crs(), clay.get_geo_transform(), clay.get_nodata_value())
        return porosity_raster