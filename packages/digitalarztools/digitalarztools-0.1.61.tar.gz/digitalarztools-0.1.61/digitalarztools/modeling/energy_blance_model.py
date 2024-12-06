import numpy as np

from digitalarztools.raster.analysis.meteo_analysis import MeteoAnalysis


class EnergyBalanceModel:

    @staticmethod
    def calculate_instantaneous_ET_fraction(LE_inst, rn_inst, g_inst):
        """
        Function to calculate the evaporative fraction
        :param LE_inst: EnergyBalanceModel.calculate_instantaneous_ET
        :param rn_inst: EnergyBalanceModel.calculate_instantaneous_net_radiation
        :param g_inst:  EnergyBalanceModel.calculate_instantaneous_soil_heat_flux
        :return:
        """
        EF_inst = LE_inst / (rn_inst - g_inst)  # Evaporative fraction
        EF_inst = EF_inst.clip(0.0, 1.8)
        EF_inst[LE_inst < 0] = 0

        return EF_inst

    @staticmethod
    def calculate_instantaneous_ET(rn_inst, g_inst, h_inst):
        """
        Instantaneous evapotranspiration
        :param rn_inst: EnergyBalanceModel.calculate_instantaneous_net_radiation
        :param g_inst:  EnergyBalanceModel.calculate_instantaneous_soil_heat_flux
        :param h_inst: EnergyBalanceModel.sensible_heat
        :return:
        """
        LE_inst = rn_inst - g_inst - h_inst
        return LE_inst

    @staticmethod
    def calculate_daily_net_radiation(Rs_24, surface_albedo, temp_24, act_vp_24, transmissivity_24, sb_const=5.6703E-8):
        """
             Rn=(1−α)×RS↓+RL↓−RL↑−(1−ε0)×RL↓
          `     where; RS↓ is incoming shortwave radiation (Wm−2),
                RL↓is incoming longwave radiation (Wm−2),
                RL↑ is outgoing longwave radiation (Wm−2);
                ε0 is surface thermal emissivity [-];
                 α is surface albedo [-].`
            RL↓−RL↑−(1−ε0)×RL↓ is calculated through Slob and FAO method
            which ever is minimum is used
        :param Rs_24:  daily short wavelength / solar radiation from swgdn_MERRA_W-m-2_daily
        :param surface_albedo: surface reflectivity using Landsat RioLandsat calculate_albedo
        :param temp_24: daily temperature from MERRA tms
        :param act_vp_24: daily actual vapour pressure using MeteoAnalysis.calculate_daily_actual_vapour_pressure
        :param transmissivity_24:  daily transmissivity  using SolarRadiation.calculate_daily_transmissivity
        :param sb_const: Stefan-Bolzmann constant (watt/m2/°K4) value is  5.6703E-8
        :return: net radiation, long wave radiation FAO, long wave radiation Slob
        """
        # Net shortwave radiation (W/m2):
        Rns_24 = Rs_24 * (1 - surface_albedo)

        # Net outgoing long wave radiation (W/m2):
        Rnl_24_FAO = (sb_const * np.power(temp_24 + 273.15, 4) *
                      (0.34 - 0.14 * np.power(act_vp_24, 0.5)) *
                      (1.35 * np.minimum(transmissivity_24 / 0.75, 1) - 0.35))

        # Rnl_24_FAO = (SB_const * np.power(Temp_24 + 273.15, 4) * (0.34-0.14 *
        #              np.power(eact_24, 0.5)) * (4.0 * np.minimum(Transm_24 / 0.75, 1) - 3.0))

        # Mean 24H Net longwave Radiation (Slob) in (W/m2)
        Rnl_24_Slob = 110 * transmissivity_24

        print('Mean 24H Net longwave Radiation (Slob) = -%0.3f (W/m2)' % np.nanmean(Rnl_24_Slob))
        print('Mean 24H Net longwave Radiation (FAO) = -%0.3f (W/m2)' % np.nanmean(Rnl_24_FAO))

        # Net 24 hrs radiation (W/m2):
        Rn_24_FAO = Rns_24 - Rnl_24_FAO  # FAO equation
        Rn_24_Slob = Rns_24 - Rnl_24_Slob  # Slob equation
        # Rn_24 = (Rn_24_FAO + Rn_24_Slob) / 2  # Average
        Rn_24 = np.minimum(Rn_24_FAO, Rn_24_Slob)

        print('Mean 24H Net Radiation (Slob) = %0.3f (W/m2)' % np.nanmean(Rn_24_Slob))
        print('Mean 24H Net Radiation (FAO) = %0.3f (W/m2)' % np.nanmean(Rn_24_FAO))

        return Rn_24, Rnl_24_FAO, Rnl_24_Slob

    @classmethod
    def calculate_instantaneous_net_radiation(cls, atmos_emis: np.ndarray, Temp_inst: np.ndarray, tir_emis: np.ndarray, surface_temp: np.ndarray, Rs_inst: np.ndarray, surf_albedo: np.ndarray, sb_const=5.6703E-8):
        """
             Rn=(1−α)×RS↓+RL↓−RL↑−(1−ε0)×RL↓
           `     where; RS↓ is incoming shortwave radiation (Wm−2),
                 RL↓is incoming longwave radiation (Wm−2),
                 RL↑ is outgoing longwave radiation (Wm−2);
                 ε0is surface thermal emissivity [-];
                  α is surface albedo [-].`
        :param atmos_emis: atomospheric emissivity  using EmissivityAnalysis.calculate_atmospheric_emissivity
        :param Temp_inst: instantaneous temperature from MERRA t2m in Celcius
        :param tir_emis: thermal infrared emissivity from EmissivityAnalysis.calculate_thermal_infrared_emissivity
        :param surface_temp: surface temperature sharpened using  ThermalAnalysis.Thermal_Sharpening
        :param rs_inst: short wavelenght  radiation from MERRA swgdn  using SolarRadiationAnalysis.calculate_instantaneous_incoming_short_wavelength_radiation
        :param surf_albedo: surface reflectivity /albedo from RioLandsat
        :param sb_const: Stefan-Bolzmann constant (watt/m2/°K4) value is  5.6703E-8
        :return:
        """

        lw_in_inst = cls.calculate_instantaneous_incoming_long_wave_radiation(atmos_emis, Temp_inst, sb_const)

        # Instantaneous outgoing longwave radiation:
        lw_out_inst = cls.calculate_instantaneous_outgoing_long_wave_radiation(tir_emis, surface_temp, sb_const)

        # Instantaneous net radiation
        rn_inst = (Rs_inst * (1 - surf_albedo) + lw_in_inst - lw_out_inst -
                   (1 - tir_emis) * lw_in_inst)
        return rn_inst

    @staticmethod
    def calculate_instantaneous_outgoing_long_wave_radiation(tir_emis, surface_temp, sb_const=5.6703E-8):
        """

        :param tir_emis: thermal Infra red emissivity EmissivityAnalysis.calculate_thermal_infrared_emissivity
        :param surface_temp:  surface temperature sharpened using  ThermalAnalysis.Thermal_Sharpening
        :param sb_const: Stefan-Bolzmann constant (watt/m2/°K4) value is  5.6703E-8
        :return:
        """
        return tir_emis * sb_const * np.power(surface_temp, 4)

    @staticmethod
    def calculate_instantaneous_incoming_long_wave_radiation(atmos_emis, Temp_inst, sb_const=5.6703E-8):
        """
        Calculate Instantaneous incoming longwave radiation:
        :param atmos_emis: atmospheric emissivity using EmissivityAnalysis.calculate_atmospheric_emissivity
        :param sb_const: # Stefan-Bolzmann constant (watt/m2/°K4) value is  5.6703E-8
        :param Temp_inst: Temp instantanous from MERRA t2m_MERRA_K_hourly
        :return:
        """
        return atmos_emis * sb_const * np.power(Temp_inst + 273.15, 4)

    @staticmethod
    def calculate_instantaneous_soil_heat_flux(rn_inst, water_mask, surface_temp, surf_albedo, ndvi):
        """
            Instantaneous Soil or ground heat flux
            G = Ts / α(0.0038α+0.0074α2)(1−0.98NDVI4) * Rn
            where; TS is land surface temperature (OC),
            α is the albedo [-] and NDVI is
            Normalized Difference Vegetation Index [-]. NDVI is a very sensitive parameter
            indicating the ratio of the differences in reflectivity for the NIR and RED bands
            to their sum expressed
        :param rn_inst: instantaneous net radiation from EnergyBalanceModel.calculate_instantaneous_net_radiation
        :param water_mask:  water mask
        :param surface_temp:  surface temperature sharpened using  ThermalAnalysis.Thermal_Sharpening
        :param surf_albedo:  surface reflectivity from RioLandsat.calculate_surface_albedo
        :param ndvi: VegetationAnalysis.calculate_ndvi
        :return:
        """
        g_inst = np.where(water_mask != 0.0, 0.4 * rn_inst,
                          ((surface_temp - 273.15) * (0.0038 + 0.0074 * surf_albedo) *
                           (1 - 0.978 * np.power(ndvi, 4))) * rn_inst)
        return g_inst

    @staticmethod
    def calculate_cold_pixel_value(hot_pixels_mean, cold_pixels_mean, cold_pixel_constant=0):
        """
        calculate cold pixel value
        :param hot_pixels_mean:
        :param cold_pixels_mean:
        :param cold_pixel_constant:
        :return: cold pixel value
        """
        # Calculate the difference between the hot and cold pixel value
        Diff_hot_cold = hot_pixels_mean - cold_pixels_mean

        # Calculate the col pixel value
        cold_pixel_value = cold_pixels_mean + cold_pixel_constant * Diff_hot_cold
        return cold_pixel_value

    @staticmethod
    def calculate_hot_pixel_value(hot_pixels_mean, cold_pixel_mean, hot_pixel_constant=0.2):
        """
        :param hot_pixels_mean: mean of hot pixel value
        :param cold_pixel_mean:  mean of cold pixel value
        :param hot_pixel_constant: consider 0.2
        :return: hot pixel value
        """
        # Calculate the difference between the hot and cold pixel value
        Diff_hot_cold = hot_pixels_mean - cold_pixel_mean

        # Calculate the hot pixel value
        hot_pixel_value = hot_pixels_mean + hot_pixel_constant * Diff_hot_cold
        return hot_pixel_value

    @staticmethod
    def calculate_hot_pixels(ts_dem, QC_Map, water_mask, NDVI, cold_pixels_mean, NDVIhot_low=0.03, NDVIhot_high=0.15):
        """
        Function to calculate the hot pixels based on the surface temperature and NDVI
        :param ts_dem: dem corrected surface temperture TemperatureAnalysis.correct_surface_temp_lapse_rate
        :param QC_Map: quality control map with total mask
        :param water_mask: water mask only using WaterAnalysis
        :param NDVI:  VegetationAnalysis.calculate_ndvi
        :param cold_pixels_mean: mean of cold pixels value
                if np.isnan(ts_dem_cold_mean) == True:
                    try:
                        ts_dem_cold_mean = np.nanmean(Temp_inst) # instantaneous Temperature in Calcius
                    except:
                        ts_dem_cold_mean = Temp_inst
        :param  NDVIhot_low: 0.03  # Lower NDVI treshold for hot pixels
        :param NDVIhot_high: 0.15  # Higher NDVI treshold for hot pixels
        :return: hot piexel mean and hot pixels np.ndarray
        """

        for_hot = np.copy(ts_dem)
        for_hot[NDVI <= NDVIhot_low] = 0.0
        for_hot[NDVI >= NDVIhot_high] = 0.0
        for_hot[np.logical_or(water_mask != 0.0, QC_Map != 0.0)] = 0.0
        hot_pixels = np.copy(for_hot)
        hot_pixels[for_hot < cold_pixels_mean] = np.nan
        ts_dem_hot_max = np.nanmax(hot_pixels)  # Max
        ts_dem_hot_mean = np.nanmean(hot_pixels)  # Mean
        ts_dem_hot_std = np.nanstd(hot_pixels)  # Standard deviation
        # ts_dem_hot = ts_dem_hot_max - 0.25 * ts_dem_hot_std
        # ts_dem_hot = (ts_dem_hot_max + ts_dem_hot_mean)/2

        print('hot : max= %0.3f (Kelvin)' % ts_dem_hot_max, ', sd= %0.3f (Kelvin)' % ts_dem_hot_std, \
              ', mean= %0.3f (Kelvin)' % ts_dem_hot_mean)

        return ts_dem_hot_mean, hot_pixels

    @staticmethod
    def calculate_cold_pixel_vegetation(ndvi, QC_Map, ts_dem):
        """
        Function to calculate the cold pixels based on vegetation
        :param ndvi:
        :param QC_Map:
        :param ts_dem: Temprature corrected at DEM Height use  DEMAnalysis.Correct_Surface_Temp_slop
        :return col_pixel_vegetation mean and cold_pixels_vegetation array
        """
        ndvi_max = np.nanmax(ndvi)
        ndvi_std = np.nanstd(ndvi)
        cold_pixels_vegetation = np.copy(ts_dem)
        cold_pixels_vegetation[np.logical_or(ndvi <= (ndvi_max - 0.1 * ndvi_std), QC_Map != 0.0)] = 0.0
        cold_pixels_vegetation[cold_pixels_vegetation == 0.0] = np.nan
        ts_dem_cold_std_veg = np.nanstd(cold_pixels_vegetation)
        ts_dem_cold_min_veg = np.nanmin(cold_pixels_vegetation)
        ts_dem_cold_mean_veg = np.nanmean(cold_pixels_vegetation)

        print('cold vegetation: min=%0.3f (Kelvin)' % ts_dem_cold_min_veg, ', sd= %0.3f (Kelvin)' % ts_dem_cold_std_veg,
              ', mean= %0.3f (Kelvin)' % ts_dem_cold_mean_veg)

        return ts_dem_cold_mean_veg, cold_pixels_vegetation

    @staticmethod
    def calculate_cold_pixels(ts_dem, water_mask, QC_Map, ts_dem_cold_veg_mean, cold_pixels_vegetation):
        """
        Function to calculate the cold pixels based on the surface temperature
        :param ts_dem: ts_dem Temprature corrected at DEM Height use  DEMAnalysis.Correct_Surface_Temp_slop
        :param water_mask
        :param QC_Map
        :param ts_dem_cold_veg_mean: Calculated using calculate_cold_pixel_vegetation
        :cold_pixels_vegetation Calculated using calculate_cold_pixel_vegetation
        :return cold pixels mean and  cold pixels array
        """
        for_cold = np.copy(ts_dem)
        for_cold[water_mask != 1.0] = 0.0
        for_cold[QC_Map != 0] = 0.0
        cold_pixels = np.copy(for_cold)
        cold_pixels[for_cold < 278.0] = np.nan
        cold_pixels[for_cold > 320.0] = np.nan
        # cold_pixels[for_cold < 285.0] = 285.0
        ts_dem_cold_std = np.nanstd(cold_pixels)  # Standard deviation
        ts_dem_cold_min = np.nanmin(cold_pixels)  # Min
        ts_dem_cold_mean = np.nanmean(cold_pixels)  # Mean

        # If average temperature is below zero or nan than use the vegetation cold pixel
        if ts_dem_cold_mean <= 0.0:
            ts_dem_cold_mean = ts_dem_cold_veg_mean
            cold_pixels[~np.isnan(cold_pixels_vegetation)] = cold_pixels_vegetation[~np.isnan(cold_pixels_vegetation)]
        if np.isnan(ts_dem_cold_mean) == True:
            ts_dem_cold_mean = ts_dem_cold_veg_mean
            cold_pixels[~np.isnan(cold_pixels_vegetation)] = cold_pixels_vegetation[~np.isnan(cold_pixels_vegetation)]
        else:
            ts_dem_cold_mean = ts_dem_cold_mean

        if ts_dem_cold_mean > ts_dem_cold_veg_mean:
            ts_dem_cold_mean = ts_dem_cold_veg_mean
            cold_pixels[~np.isnan(cold_pixels_vegetation)] = cold_pixels_vegetation[~np.isnan(cold_pixels_vegetation)]
        if np.isnan(ts_dem_cold_mean):
            ts_dem_cold_mean = ts_dem_cold_veg_mean
            cold_pixels[~np.isnan(cold_pixels_vegetation)] = cold_pixels_vegetation[~np.isnan(cold_pixels_vegetation)]

        print('cold water: min=%0.3f (Kelvin)' % ts_dem_cold_min, ', sd= %0.3f (Kelvin)' % ts_dem_cold_std, \
              ', mean= %0.3f (Kelvin)' % ts_dem_cold_mean)

        return ts_dem_cold_mean, cold_pixels

    @classmethod
    def calculate_reference_net_radiation(cls, water_mask, Rn_24, Ra_mountain_24, Transm_24, Rnl_24_FAO, Wind_24):
        """
        Function to calculate the net solar radiation
        :param water_mask:
        :param Rn_24:  daily net radiation
        :param Ra_mountain_24:  daily radiation from mountain or slop
        :param Transm_24:  daily transmissivity
        :param Rnl_24_FAO: daily net radiation long wave FAO
        :param Wind_24: daily Wind
        :return: Net radiation for grass, Reflected radiation at water surface and Aerodynamic resistance (s/m) for grass surface
        """

        # Reflected radiation at water surface: ??
        # Refl_rad_water = np.zeros(Rn_24.shape)
        Refl_rad_water = cls.calculate_reflected_radiation_at_water(water_mask, Rn_24)

        rah_grass = cls.calculate_areodynamic_resistance_for_grass_surface(Wind_24)

        # Net radiation for grass Rn_ref, eq 40, FAO56:
        Rn_ref = cls.calculate_net_radiation_for_grass(Ra_mountain_24, Transm_24, Rnl_24_FAO)
        return Rn_ref, Refl_rad_water, rah_grass

    @staticmethod
    def calculate_areodynamic_resistance_for_grass_surface(Wind_24):
        # Aerodynamic resistance (s/m) for grass surface:
        rah_grass = 208.0 / Wind_24
        print('rah_grass=', '%0.3f (s/m)' % np.nanmean(rah_grass))
        return rah_grass

    @staticmethod
    def calculate_reflected_radiation_at_water(water_mask, Rn_24):
        """
        :param water_mask:
        :param Rn_24: daily net radiation
        :return:
        """
        # constants:
        G24_water = 0.1  # G24 ratio for water - reflectivity?
        return np.where(water_mask != 0.0, G24_water * Rn_24, 0.0)

    @staticmethod
    def calculate_net_radiation_for_grass(Ra_mountain_24, Transm_24, Rnl_24_FAO):
        """
        :param Ra_mountain_24:  daily solar radiation from mountain or slope SolarRadiation.calculate_ra_mountain
        :param Transm_24:  daily transmissivity
        :param Rnl_24_FAO: daily net radiation long wave FAO
        :return:
        """
        # Net radiation for grass Rn_ref, eq 40, FAO56:
        return Ra_mountain_24 * Transm_24 * (1 - 0.23) - Rnl_24_FAO  # Rnl avg(fao-slob)?

    @staticmethod
    def compute_surface_roughness_for_momentum_trasnport(Surf_roughness, Temp_inst):
        """
        colculate surface roughness
        :param Surf_roughness: MeteoAnalysis.calculate_wind_speed_friction
        :param Temp_inst: instantaneous Temperature from MERRA dataset
        :return:
        """
        k_vk = 0.41  # Von Karman constant
        rah_pm_pot = ((np.log((2.0 - 0.0) / (Surf_roughness * 0.1)) * np.log((2.0 - 0.0) / (Surf_roughness))) / (k_vk * 1.5 ** 2)) * ((1 - 5 * (-9.82 * 4.0 * (2.0 - 0.0)) / ((273.15 + Temp_inst) * 1.5 ** 2)) ** (-0.75))
        rah_pm_pot[rah_pm_pot < 25] = 25
        return rah_pm_pot

    @staticmethod
    def calculate_potential_ET(LAI, Surface_temp, sl_es_24, air_dens, sat_vp_24, act_vap_24, Psychro_c, Rn_24, Refl_rad_water, rah_pm_pot, rl):
        """
        Function to calculate the potential evapotransporation
        :param LAI: VegetationAnalysis.calculate_leaf_area_index
        :param Surface_temp: RioLandsat.calculate_surface_temperature
        :param sl_es_24: MeteoAnalysis.calculate_slope_of_saturated_vapour_pressure
        :param air_dens: TemperatureAnalysis.calculate_air_density
        :param sat_vp_24:  MeteoAnalysis.calculate_daily_saturated_vapour_pressure(Temp_24)
        :param act_vap_24: MeteoAnalysis.calculate_daily_actual_vapour_pressure
        :param Psychro_c:  MeteoAnalysis.calculate_psychrometric_constant
        :param Rn_24:   EnergyBalanceModel.calculate_daily_net_radiation
        :param Refl_rad_water:  EnergyBalanceModel.calculate_reflected_radiation_at_water
        :param rah_pm_pot: EnergyBalanceModel.compute_surface_roughness_for_momentum_trasnport
        :param rl:  rl = 130  # Bulk stomatal resistance of the well-illuminated leaf (s/m)
        :return: Potential evaportranspiration (mm/d),  Latent heat of vaporization (J/kg), and Min (Bulk) surface resistance (s/m)
        """

        # Effective leaf area index involved, see Allen et al. (2006):
        LAI_eff = LAI / (0.3 * LAI + 1.2)
        rs_min = rl / LAI_eff  # Min (Bulk) surface resistance (s/m)
        # Latent heat of vaporization (J/kg):
        lhv = MeteoAnalysis.calculate_latent_heat_of_vapourization(Surface_temp)

        # Potential evapotranspiration
        # Penman-Monteith of the combination equation (eq 3 FAO 56) (J/s/m2)
        LETpot_24 = ((sl_es_24 * (Rn_24 - Refl_rad_water) + air_dens * 1004 *
                      (sat_vp_24 - act_vap_24) / rah_pm_pot) / (sl_es_24 + Psychro_c * (1 + rs_min / rah_pm_pot)))
        # Potential evaportranspiration (mm/d)
        ETpot_24 = LETpot_24 / (lhv * 1000) * 86400000
        ETpot_24[ETpot_24 > 15.0] = 15.0

        # LE_pot = ETpot_24 * (Lhv * 1000) / 86400000

        return ETpot_24, lhv, rs_min

    @staticmethod
    def calculate_instantaneous_ET_fraction(LE_inst, rn_inst, g_inst):
        """
        Function to calculate the evaporative fraction
        :param LE_inst: Calculated from ET potential and Latent heat of vaporization
            LE_pot = ETpot_24 * (Lhv * 1000) / 86400000
        :param rn_inst: instantenous net radiation
        :param g_inst: instantaneous ground  flux which might be zero cls.alculate_instantaneous_soil_heat_flux
        :return:
        """

        EF_inst = LE_inst / (rn_inst - g_inst)  # Evaporative fraction
        EF_inst = EF_inst.clip(0.0, 1.8)
        EF_inst[LE_inst < 0] = 0

        return EF_inst

    @staticmethod
    def corrected_value_for_aerodynamic_resistance(ustar_1):
        """
        Corrected value for the aerodynamic resistance (eq 41 with psi2 = psi1)
        :param usta_1: Friction velocity (m/s) MeteoAnalysis.calculate_wind_speed_friction
        :return:
        """
        k_vk = 0.41  # Von Karman constant
        rah1 = np.log(2.0 / 0.01) / (k_vk * ustar_1)
        return rah1

    @staticmethod
    def calculate_surface_temperature_gradiant(rn_inst, g_inst, rah, air_dens, hot_pixels, cold_pixels,
                                               ts_dem, ts_dem_hot, ts_dem_cold, slope, QC_Map, max_EF):
        """
        Calculate surface temperature gradiant dT
        :param rn_inst: net radiation instantaneous
        :param g_inst:  soil / ground heat flux
        :param rah: Corrected value for the aerodynamic resistance
        :param air_dens: TemperatureAnalysis.calculate_air_density
        :param hot_pixels: EnergyBalanceModel.calculate_hot_pixels
        :param cold_pixels:EnergyBalanceModel.calculate_cold_pixels
        :param ts_dem: TemperatureAnalysis.correct_surface_temp_lapse_rate
        :param ts_dem_hot:   EnergyBalanceModel.calculate_hot_pixel_value
        :param ts_dem_cold:  EnergyBalanceModel.calculate_cold_pixel_value
        :param slope: DEMAnalysis.calculate_slope
        :param QC_Map: Quality Control Map Total mask = water mask + snow mask + ndvi qc map
         :param max_EF:EnergyBalanceModel.calculate_instantaneous_ET_fraction
        :return:
        """

        # Near surface temperature difference (dT):
        dT_hot = (rn_inst - g_inst) * rah / (air_dens * 1004)
        dT_cold = (1 - max_EF) * (rn_inst - g_inst) * rah / (air_dens * 1004)

        # dT for hot pixels - hot, (dry) agricultural fields with no green veget.:
        dT_hot[ts_dem <= (ts_dem_hot - 0.5)] = np.nan
        dT_hot[QC_Map == 1] = np.nan
        dT_hot[dT_hot == 0] = np.nan
        if np.all(np.isnan(dT_hot)) == True:
            ts_dem_hot = np.nanpercentile(hot_pixels, 99.5)
            dT_hot[ts_dem <= (ts_dem_hot - 0.5)] = np.nan
            dT_hot[dT_hot == 0] = np.nan

        dT_hot = np.float32(dT_hot)
        dT_hot[slope > 10] = np.nan

        # dT for cold pixels - cold, (wet) agricultural fields with green veget.:
        dT_cold[np.logical_or(ts_dem >= ts_dem_cold + 0.5, np.isnan(cold_pixels))] = np.nan
        dT_cold[slope > 10] = np.nan

        dT_hot_mean = np.nanmean(dT_hot)
        dT_cold_mean = np.nanmean(dT_cold)
        dT_cold_mean = 0.0

        # Compute slope and offset of linear relationship dT = b + a * Ts
        slope_dt = (dT_hot_mean - dT_cold_mean) / (ts_dem_hot - ts_dem_cold)
        print('Slope dT ', slope_dt)
        '''
        # Adjust slope if needed
        if slope_dt < 0.8:
            slope_dt = 0.8
            print('Slope dT is adjusted to minimum ', slope_dt)
        if slope_dt > 1.2:
            slope_dt = 1.2
            print('Slope dT is adjusted to maximum ', slope_dt)     
        '''
        offset_dt = dT_hot_mean - slope_dt * ts_dem_hot

        dT = offset_dt + slope_dt * ts_dem
        return dT

    @staticmethod
    def calculate_sensible_heat_flux(air_dens, dT, rah, QC_Map):
        """
         Sensible heat flux:
        :param air_dens: TemperatureAnalysis.calculate_air_density
        :param dT:  surface tempearture gradiant
        :param rah: cls. corrected_value_for_aerodynamic_resistance
        :param QC_Map:
        :return:
        """
        h = air_dens * 1004 * dT / rah
        h[QC_Map == 1] = np.nan
        h[h == 0] = np.nan
        h[QC_Map != 0] = np.nan
        return h

    @classmethod
    def sensible_heat(cls, rah, ustar, rn_inst, g_inst, ts_dem, ts_dem_hot, ts_dem_cold,
                      air_dens, Surf_temp, k_vk, QC_Map, hot_pixels, cold_pixels, slope, max_EF):
        """
        This function computes the instantaneous sensible heat given the
        instantaneous net radiation, ground heat flux, and other parameters.
        :param rah:   Corrected value for the aerodynamic resistance
        :param ustar:   Friction velocity (m/s): MeteoAnalysis.calculate_wind_speed_friction
        :param rn_inst: net radiation instantaneous
        :param g_inst:  soil heat flux
        :param ts_dem: TemperatureAnalysis.correct_surface_temp_lapse_rate
        :param ts_dem_hot:   EnergyBalanceModel.calculate_hot_pixel_value
        :param ts_dem_cold:  EnergyBalanceModel.calculate_cold_pixel_value
        :param air_dens: TemperatureAnalysis.calculate_air_density
        :param Surf_temp: surface temperature sharpened TemperatureAnalysis.Thermal_Sharpening
        :param k_vk:  k_vk = 0.41  # Von Karman constant
        :param QC_Map: Quality Control Map Total mask = water mask + snow mask + ndvi qc map
        :param hot_pixels: EnergyBalanceModel.calculate_hot_pixels
        :param cold_pixels:EnergyBalanceModel.calculate_cold_pixels
        :param slope: DEMAnalysis.calculate_slope
        :param max_EF:EnergyBalanceModel.calculate_instantaneous_ET_fraction
        :return:
            Sensible heat flux, surface temperature gradiant,  Monin-Obukhov length (m): Stability correction for momentum, stable conditions,
            Stability correction for momentum and heat transport in psi
        """
        dT = cls.calculate_surface_temperature_gradiant(rn_inst, g_inst, rah, air_dens, hot_pixels, cold_pixels,
                                                        ts_dem, ts_dem_hot, ts_dem_cold, slope, QC_Map, max_EF)
        # Sensible heat flux:
        h = cls.calculate_sensible_heat_flux(air_dens, dT, rah, QC_Map)

        # Monin-Obukhov length (m):
        L_MO = ((-1.0 * air_dens * 1004 * np.power(ustar, 3) * Surf_temp) /
                (k_vk * 9.81 * h))
        L_MO[L_MO < -1000] = -1000

        # Stability correction for momentum, stable conditions (L_MO >= 0):
        psi_200_stable = -0.05 * 200 / L_MO

        # Stability correction for momentum and heat transport, unstable
        # conditions (L_MO < 0):
        x2 = np.power((1.0 - 16.0 * (2.0 / L_MO)), 0.25)  # x at 2m
        x200 = np.power(1.0 - 16.0 * (200 / L_MO), 0.25)  # x at 200m
        psi_h = 2 * np.log((1 + np.power(x2, 2)) / 2)
        psi_m200 = (2 * np.log((1 + x200) / 2) + np.log((1 + np.power(x200, 2)) /
                                                        2) - 2 * np.arctan(x200) + 0.5 * np.pi)
        print('Sensible Heat ', np.nanmean(h))
        print('dT', np.nanmean(dT))

        return h, dT, L_MO, psi_200_stable, psi_h, psi_m200

    @classmethod
    def iterate_friction_velocity(cls, k_vk, u_200, Surf_roughness, g_inst, rn_inst, ts_dem, ts_dem_hot, ts_dem_cold, air_dens, Surface_temp, L, psi, psi_m200, psi_m200_stable, QC_Map, hot_pixels, cold_pixels, slope, max_EF):
        """
        Function to correct the windspeed and aerodynamic resistance for the iterative process the output can be used as the new input for this model
        """
        # Sensible heat 2 (Step 6)
        # Corrected value for the friction velocity, unstable
        ustar_corr_unstable = (k_vk * u_200 / (np.log(200.0 / Surf_roughness) -
                                               psi_m200))
        # Corrected value for the friction velocity, stable
        ustar_corr_stable = (k_vk * u_200 / (np.log(200.0 / Surf_roughness) -
                                             psi_m200_stable))
        ustar_corr = np.where(L > 0.0, ustar_corr_stable, ustar_corr_unstable)
        ustar_corr[ustar_corr < 0.02] = 0.02

        rah_corr_unstable = (np.log(2.0 / 0.01) - psi) / (k_vk * ustar_corr)  # unstable
        rah_corr_stable = (np.log(2.0 / 0.01) - 0.0) / (k_vk * ustar_corr)  # stable
        rah_corr = np.where(L > 0.0, rah_corr_stable, rah_corr_unstable)
        h, dT, L_corr, psi_m200_corr_stable, psi_corr, psi_m200_corr = cls.sensible_heat(
            rah_corr, ustar_corr, rn_inst, g_inst, ts_dem, ts_dem_hot, ts_dem_cold,
            air_dens, Surface_temp, k_vk, QC_Map, hot_pixels, cold_pixels, slope, max_EF)
        return h, dT, L_corr, psi_corr, psi_m200_corr, psi_m200_corr_stable

    @staticmethod
    def calculate_rah_of_pm_ET_act(Surf_roughness, k_vk, dT, Temp_inst):
        """
        Calculate rah of PM for the ET act (dT after iteration) and ETpot (4 degrees)
        :param Surf_roughness:
        :param k_vk:
        :param dT:
        :param Temp_inst:
        :return:
        """
        rah_pm_act = ((np.log((2.0 - 0.0) / (Surf_roughness * 0.1)) * np.log((2.0 - 0.0) / (Surf_roughness))) / (k_vk * 1.5 ** 2)) * ((1 - 5 * (-9.82 * dT * (2.0 - 0.0)) / ((273.15 + Temp_inst) * 1.5 ** 2)) ** (-0.75))
        rah_pm_act[rah_pm_act < 25] = 25
        return rah_pm_act

    @staticmethod
    def calculate_latent_heat_of_vaporization(surface_temp):
        return (2.501 - 2.361e-3 * (surface_temp - 273.15)) * 1E6

    @staticmethod
    def calculate_reference_ET(surface_temp, sl_es_24, Rn_ref, air_dens, sat_vp_24, act_vp_24, rah_grass, Psychro_c):
        """
        Function to calculate the reference evapotransporation
        :param surface_temp: surface tempearture
        :param sl_es_24: MeteoAnalysis.calculate_slope_of_saturated_vapour_pressure
        :param Rn_ref: calculate_net_radiation_for_grass
        :param air_dens: TemperatureAnalysis.calculate_air_density
        :param sat_vp_24: MeteoAnalysis.calculate_daily_saturated_vapour_pressure(Temp_24)
        :param act_vp_24: daily actual vapour pressure using MeteoAnalysis.calculate_daily_actual_vapour_pressure
        :param rah_grass: cls.calculate_areodynamic_resistance_for_grass_surface
        :param Psychro_c: MeteoAnalysis.calculate_psychrometric_constant
        :return: Reference evapo transpiration(mm/day), Latent heat of vaporization
        """
        # Latent heat of vaporization (J/kg):
        Lhv = (2.501 - 2.361e-3 * (surface_temp - 273.15)) * 1E6

        # Reference evapotranspiration- grass
        # Penman-Monteith of the combination equation (eq 3 FAO 56) (J/s/m2)
        LET_ref_24 = ((sl_es_24 * Rn_ref + air_dens * 1004 * (sat_vp_24 - act_vp_24) /
                       rah_grass) / (sl_es_24 + Psychro_c * (1 + 70.0 / rah_grass)))
        # Reference evaportranspiration (mm/d):
        ETref_24 = LET_ref_24 / (Lhv * 1000) * 86400000

        return ETref_24, Lhv

    @staticmethod
    def calculate_daily_evaporation(sat_vp_24, act_v_24, EF_inst, Rn_24, Refl_rad_water, Lhv, image_type):
        """
        Function to calculate the daily evaporation
        :param sat_vp_24: MeteoAnalysis.calculate_daily_saturated_vapour_pressure(Temp_24)
        :param act_vp_24: daily actual vapour pressure using MeteoAnalysis.calculate_daily_actual_vapour_pressure
        :param EF_inst: EnergyBalanceModel.calculate_instantaneous_ET_fraction
        :param Rn_24:         EnergyBalanceModel.calculate_daily_net_radiation
        :param Refl_rad_water:  EnergyBalanceModel.calculate_reference_net_radiation
        :param Lhv: l EnergyBalanceModel.calculate_latent_heat_of_vaporization
        :param image_type:
        :return:
        """
        # Advection factor
        if image_type in [2, 4]:
            AF = np.ones(Rn_24.shape)
        else:
            AF = 1 + 0.985 * (np.exp((sat_vp_24 - act_v_24) * 0.08) - 1.0) * EF_inst

        # Daily evapotranspiration:
        ETA_24 = EF_inst * AF * (Rn_24 - Refl_rad_water) / (Lhv * 1000) * 86400000
        ETA_24 = ETA_24.clip(0, 15.0)
        return ETA_24, AF

    @staticmethod
    def calculate_bulk_surface_resistance(sl_es_24, rn_24, Refl_rad_water, air_dens, sat_vp_24, act_vp_24, rah_pm_act, ETA_24, Lhv, Psychro_c):
        """
        Function to calculate the bulk surface resistance
        :param sl_es_24:  MeteoAnalysis.calculate_slope_of_saturated_vapour_pressur
        :param rn_24:  EnergyBalanceModel.calculate_daily_net_radiation
        :param Refl_rad_water: use water radiation from  EnergyBalanceModel.calculate_reference_net_radiation
        :param air_dens: TemperatureAnalysis.calculate_air_density
        :param sat_vp_24: MeteoAnalysis.calculate_daily_saturated_vapour_pressure
        :param act_vp_24: MeteoAnalysis.calculate_daily_actual_vapour_pressure
        :param rah_pm_act: EnergyBalanceModel.calculate_rah_of_pm_ET_act
        :param ETA_24:  EnergyBalanceModel.calculate_daily_evaporation
        :param Lhv: cls calculate_latent_heat_of_vaporization
        :param Psychro_c:  MeteoAnalysis.calculate_psychrometric_constant
        :return:
        """
        # Bulk surface resistance (s/m):
        bulk_surf_resis_24 = ((((sl_es_24 * (rn_24 - Refl_rad_water) + air_dens *
                                 1004 * (sat_vp_24 - act_vp_24) / rah_pm_act) / (ETA_24 * Lhv / 86400) -
                                sl_es_24) / Psychro_c - 1.0) * rah_pm_act)
        bulk_surf_resis_24[ETA_24 <= 0.0] = 100000.0
        bulk_surf_resis_24 = bulk_surf_resis_24.clip(0.0, 100000.0)
        return (bulk_surf_resis_24)

    @staticmethod
    def calculate_crop_coefficient_kc(ETA_24, ETP_24, ETref_24 ):
        """
        Calculate crop coefficient
        :param ETA_24: EnergyBalanceModel.calculate_daily_evaporation
        :param ETP_24:  np.where(ETpot_24 < ETA_24, ETA_24, ETpot_24)
        :param ETref_24: EnergyBalanceModel.calculate_reference_ET
        :return: kc, kc_max
        """
        kc = ETA_24 / ETref_24  # Crop factor
        kc_max = ETP_24 / ETref_24
        return kc, kc_max

    @staticmethod
    def Separate_E_T(Light_use_extinction_factor, LAI, ETP_24, Theta_res_top, Theta_res_sub, Theta_sat_top, Theta_sat_sub, top_soil_moisture, sl_es_24, Psychro_c, moisture_stress_biomass_first, vegt_cover, ETA_24, SM_stress_trigger, root_zone_moisture_first, total_soil_moisture):
        """
        Separate the Evapotranspiration into evaporation and Transpiration
        :param Light_use_extinction_factor:  0.5
        :param LAI:
        :param ETP_24:
        :param Theta_res_top:
        :param Theta_res_sub:
        :param Theta_sat_top:
        :param Theta_sat_sub:
        :param top_soil_moisture:
        :param sl_es_24:
        :param Psychro_c:
        :param moisture_stress_biomass_first:
        :param vegt_cover:
        :param ETA_24:
        :param SM_stress_trigger:
        :param root_zone_moisture_first:
        :param total_soil_moisture:
        :return:
        """
        # constants

        Tpot_24_estimate = (1 - np.exp(-Light_use_extinction_factor * LAI)) * ETP_24
        SE_top = (top_soil_moisture - Theta_res_top) / (Theta_sat_top - Theta_res_top)
        Eact_24_estimate = np.minimum(1, 1 / np.power(SE_top + 0.1, -2.0)) * (ETP_24 - Tpot_24_estimate)
        # RS_soil = RS_soil_min * np.power(SE_top,-2.0)
        # Eact_24_estimate=(sl_es_24+Psychro_c*(1+RS_soil_min/Rah_PM))/(sl_es_24+Psychro_c*(1+RS_soil/Rah_PM))*(ETP_24-Tpot_24_estimate)
        n66_memory = moisture_stress_biomass_first * Tpot_24_estimate

        # calulate the first estimation of actual daily tranpiration
        Tact_24_estimate = np.copy(n66_memory)
        Tact_24_estimate[n66_memory > 0.99 * ETA_24] = ETA_24[n66_memory > 0.99 * ETA_24]
        Tact_24_estimate[vegt_cover == 0.0] = 0.0

        # calculate the second estimation and end estimation of the actual daily tranpiration
        Tact_24 = np.abs((Tact_24_estimate / (Tact_24_estimate + Eact_24_estimate)) * ETA_24)

        # calculate the actual daily potential transpiration
        Tpot_24 = np.copy(Tpot_24_estimate)
        Tpot_24[Tpot_24_estimate < Tact_24] = Tact_24[Tpot_24_estimate < Tact_24]

        # calculate moisture stress biomass
        moisture_stress_biomass = Tact_24 / Tpot_24

        # Calculate root zone moisture final
        Se_Poly = 2.23 * np.power(moisture_stress_biomass, 3) - 3.35 * np.power(moisture_stress_biomass, 2) + 1.98 * moisture_stress_biomass + 0.07
        root_zone_moisture1 = Se_Poly * (SM_stress_trigger + 0.02 - Theta_res_sub) + Theta_res_sub
        root_zone_moisture_final = np.where(root_zone_moisture1 > root_zone_moisture_first, root_zone_moisture1, root_zone_moisture_first)

        # Calculate top zone moisture final
        top_zone_moisture1 = (total_soil_moisture - root_zone_moisture_final * vegt_cover) / (1 - vegt_cover)
        top_zone_moisture_final = top_zone_moisture1.clip(Theta_res_top, Theta_sat_top)

        # calculate the actual daily evaporation
        Eact_24 = ETA_24 - Tact_24

        # calculate the Transpiration deficit
        T24_deficit = Tpot_24 - Tact_24

        # calculate the beneficial fraction
        beneficial_fraction = Tact_24 / ETA_24
        beneficial_fraction[ETA_24 == 0.0] = 0.0

        return Eact_24, Tpot_24, Tact_24, moisture_stress_biomass, T24_deficit, beneficial_fraction, root_zone_moisture_final, top_zone_moisture_final

    @staticmethod
    def Classify_Irrigation(moisture_stress_biomass, vegt_cover):
        """
        This function makes a classification with 4 categories which show the irrigation needs
        :param moisture_stress_biomass:
        :param vegt_cover:
        :return:
        """
        for_irrigation = np.copy(moisture_stress_biomass)

        # make a discreed irrigation needs map with the following categories
        # Irrigation needs:
        # 0: No need for irrigation
        # 1: Perhaps irrigate
        # 2: Irrigate
        # 3: Irrigate immediately
        irrigation_needs = np.copy(for_irrigation)
        irrigation_needs[np.where(irrigation_needs >= 1.0)] == 0.0
        irrigation_needs[np.logical_and(irrigation_needs >= 0.9, irrigation_needs < 1.0)] = 1.0
        irrigation_needs[np.where((irrigation_needs >= 0.8) & (irrigation_needs < 0.9))] = 2.0
        irrigation_needs[np.where(irrigation_needs < 0.8)] = 3.0
        irrigation_needs[vegt_cover <= 0.3] = 0.0
        return irrigation_needs
