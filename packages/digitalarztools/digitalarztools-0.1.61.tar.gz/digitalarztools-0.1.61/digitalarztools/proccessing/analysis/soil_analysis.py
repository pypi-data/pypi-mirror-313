from math import log
from typing import List, Tuple

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
    def calculate_soil_moisture(ETA_24, EF_inst, QC_Map, water_mask, vegt_cover, Theta_sat_top, Theta_sat_sub,
                                Theta_res_top, Theta_res_sub, depl_factor, Field_Capacity, FPAR,
                                Soil_moisture_wilting_point):
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
            print('No RZ_SM so the vegetation Threshold for RZ is adjusted from 0,9 to =',
                  '%0.3f' % Veg_Cover_Threshold_RZ)

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
        root_zone_moisture_temp = (total_soil_moisture - (top_soil_moisture_mean + top_soil_moisture_std) * (
                1 - vegt_cover)) / vegt_cover  # total soil moisture = soil moisture no vegtatation *(1-vegt_cover)+soil moisture root zone * vegt_cover
        try:
            root_zone_moisture_temp[root_zone_moisture_temp <= Theta_res_sub] = Theta_res_sub[
                root_zone_moisture_temp <= Theta_res_sub]
        except:
            root_zone_moisture_temp[root_zone_moisture_temp <= Theta_res_sub] = Theta_res_sub

        root_zone_moisture_temp[root_zone_moisture_temp >= Max_moisture_RZ] = Max_moisture_RZ[
            root_zone_moisture_temp >= Max_moisture_RZ]

        root_zone_moisture_first = np.copy(root_zone_moisture_temp)
        root_zone_moisture_first[np.logical_or(QC_Map == 1.0, np.logical_or(water_mask == 1.0, vegt_cover < 0.0))] = 0

        # Normalized stress trigger:
        norm_trigger = (root_zone_moisture_first - Soil_moisture_wilting_point) / (
                SM_stress_trigger + 0.02 - Soil_moisture_wilting_point)
        norm_trigger[norm_trigger > 1.0] = 1.0

        # moisture stress biomass:
        moisture_stress_biomass_first = norm_trigger - (np.sin(2 * np.pi * norm_trigger)) / (2 * np.pi)
        moisture_stress_biomass_first = np.where(moisture_stress_biomass_first < 0.5 * FPAR, 0.5 * FPAR,
                                                 moisture_stress_biomass_first)
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

    @staticmethod
    def calculate_soil_porosity(clay: RioRaster, sand: RioRaster, silt: RioRaster) -> RioRaster:
        """
        Calculate the texture based soil porosity using
        Porosity=1 − ((Clay+Silt)/100)*0.67 - (Sand/100)*0.35
        Porosity = 1 - a - b
        """
        clay_band = clay.get_data_array(1)
        sand_band = sand.get_data_array(1)
        silt_band = silt.get_data_array(1)
        a = (clay_band + silt_band) / 100 * 0.67
        b = sand_band / 100 * 0.35
        porosity = 1 - a - b
        porosity_raster = RioRaster.raster_from_array(porosity, clay.get_crs(), clay.get_geo_transform(),
                                                      clay.get_nodata_value())
        return porosity_raster

    @staticmethod
    def convert_volumetric_fraction_to_mm(bulk_density_raster: RioRaster, surface_raster: RioRaster,
                                          surface_depth_mm: int):
        """
        @param bulk_density_raster: soil density raster
        @param surface_raster:  whoes pixel are in volumetric fraction like field_capacity, soil_moisture etc
        @param surface_depth_mm:  surface depth in mm
        @return:
        """

        # surface_res = surface_raster.get_spatial_resoultion()[0]
        # bulk_density = bulk_density_raster.get_spatial_resoultion()[0]
        bulk_density_raster.make_coincident_with(surface_raster)
        surface = surface_raster.get_data_array(1)
        bulk_density = bulk_density_raster.get_data_array(1)

        # Ensure values are within valid ranges
        if not (0 <= surface.all() <= 1):
            raise ValueError("Volumetric soil moisture must be between 0 and 1")
        # if not (0 < bulk_density.all()):
        #     raise ValueError("Bulk density must be greater than 0")

        particle_density = 2.65
        # Adjust bulk density based on your assumption
        bulk_density = np.where(
            bulk_density <= 0, np.ones(surface.shape), bulk_density
        )  # Replace invalid values with 1

        # Calculate pore space fraction
        pore_space = 1 - bulk_density / particle_density

        # Calculate soil moisture depth
        surface_in_mm = surface * surface_depth_mm * pore_space

        surface_mm_raster = surface_raster.rio_raster_from_array(surface_in_mm)
        return surface_mm_raster

    @staticmethod
    def calculate_field_capacity(clay: RioRaster, sand: RioRaster, silt: RioRaster, organic_matter_raster: RioRaster,
                                 bulk_density_raster: RioRaster) -> RioRaster:
        """"
        Calculate field capacity using the Saxton and Rawls (2006) formula
        FC=0.7919+0.001691⋅C−0.29619⋅S−0.000001491⋅(Si^2)+0.0000821⋅(C^2)+0.02427⋅(1/S )+0.01113⋅log(Si)

        where:
            FC is the soil field capacity (volumetric water content, m³/m³).
            S is the sand content (fraction).
            Si is the silt content (fraction).
            C is the clay content (fraction)
        units of FC is Volumetric Water Content: It represents the volume of water held in the soil per unit volume of soil.
        For example, a field capacity value of 0.25 means that 25% of the soil volume is occupied by water when the soil is at field capacity.
        @param sand: data  in percentage
        @param silt: data in percentage
        @param clay: in percentage
        @param organic_matter_raster: in percentage
        @param bulk_density_raster: in g /cm3
        @return: field_capacity raster in Volumetric Water Content
        """
        # Convert percentages to fractions as data is in percentage
        sand_frac = sand.get_data_array(1) / 100.0
        silt_frac = silt.get_data_array(1) / 100.0
        clay_frac = clay.get_data_array(1) / 100.0
        organic_matter_frac = organic_matter_raster.get_data_array(1)
        bulk_density = bulk_density_raster.get_data_array(1)


        # Calculate field capacity using the Saxton and Rawls (2006) formula
        field_capacity = (
                0.7919 +
                0.001691 * clay_frac -
                0.29619 * sand_frac -
                0.000001491 * (silt_frac ** 2) +
                0.0000821 * (clay_frac ** 2) +
                0.02427 * (1 / sand_frac) +
                0.01113 * np.log(silt_frac)
        )
        # field_capacity = (
        #         0.257 +
        #         0.0024 * clay_frac +
        #         0.0017 * silt_frac +
        #         0.0023 * organic_matter_frac -
        #         0.010 * sand_frac +
        #         0.270 * bulk_density -
        #         0.048 * np.log(sand_frac) -
        #         0.025 * np.log(clay_frac)
        # )
        field_capacity = np.minimum(field_capacity, 1)
        field_capacity_raster = sand.rio_raster_from_array(field_capacity)
        return field_capacity_raster

    @staticmethod
    def aggregate_field_capacity_at_target_depth(target_depth, rasters: List[RioRaster],
                                                 depth_intervals: List[Tuple]) -> np.ndarray:
        """
        Aggregate field capacity values up to a specified depth.
            let say i need Total Field Capacity for 0-10 mm:
                    FC_0-10mm = FC_0-5mm + 5/10 * FC_5-15mm
        Parameters:
        - rasters: list of RioRasters
        - depth_intervals: list of tuples
            A list of tuples where each tuple represents the depth range (in mm) of the corresponding raster.
            Example: [(0, 5), (5, 15), (15, 30)]
        - target_depth: int or float
            The depth (in mm) up to which to aggregate field capacity values.

        Returns:
        - np.ndarray
            The aggregated field capacity values up to the target depth.
        Example:
            raster_paths = [raster_fc_0_5mm, raster_fc_5_10mm, raster_fc_15_30mm]
            depth_intervals = [(0, 5), (5, 15), (15, 30)]
            target_depth = 10  # 0-10 mm

            aggregated_fc = aggregate_field_capacity(raster_paths, depth_intervals, target_depth)

        """
        total_field_capacity = None

        for fc_data, (start_depth, end_depth) in zip(rasters, depth_intervals):
            if start_depth >= target_depth:
                break

            # Load the raster data
            # with rasterio.open(path) as src:
            #     fc_data = src.read(1)  # Read the first band

            # Calculate the depth to be considered for this layer
            depth_to_consider = min(end_depth, target_depth) - start_depth

            # Scale the field capacity data according to the depth considered
            fc_scaled = (depth_to_consider / (end_depth - start_depth)) * fc_data.get_data_array(1)
            fc_scaled = np.minimum(fc_scaled, 1)
            # Initialize or aggregate the field capacity
            if total_field_capacity is None:
                total_field_capacity = fc_scaled
            else:
                total_field_capacity += fc_scaled

        return total_field_capacity
