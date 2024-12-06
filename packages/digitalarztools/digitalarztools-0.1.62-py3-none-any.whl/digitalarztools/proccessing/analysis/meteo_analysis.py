from datetime import datetime

import numpy as np
import pandas as pd

from digitalarztools.raster.analysis.vegitation_analysis import VegetationAnalysis
from digitalarztools.raster.band_process import BandProcess
from digitalarztools.raster.rio_raster import RioRaster


class MeteoAnalysis:
    @staticmethod
    def get_datasets_date_range(dates: pd.DatetimeIndex) -> (str, str, str, str):
        """
        Parameters
            dates: request dates

            return: merra and geos start and end date in %Y-%m-%d string format based on requested dates
        """

        # merra_last_date = MERRA.get_last_available_date()
        # # merra_last_date = datetime.strptime("2022-12-01", "%Y-%m-%d")
        # merra_dates = dates[dates < merra_last_date]
        # geos_dates = dates[dates >= merra_last_date]
        # start_date_merra = datetime.strftime(merra_dates[0], "%Y-%m-%d") if not merra_dates.empty else ""
        # end_date_merra = datetime.strftime(merra_dates[-1], "%Y-%m-%d") if not merra_dates.empty else ""
        # start_date_geos = datetime.strftime(geos_dates[0], "%Y-%m-%d") if not geos_dates.empty else ""
        # end_date_geos = datetime.strftime(dates[-1], "%Y-%m-%d") if not dates.empty else ""
        #
        # return start_date_merra, end_date_merra, start_date_geos, end_date_geos
        return '2022-02-08', '2022-02-15', '', '2022-02-15'

    @staticmethod
    def calculate_wind_and_humidity(start_date, end_date, start_date_merra, end_date_merra, start_date_geos,
                                    end_date_geos,
                                    Temp_folder, Pres_folder, Hum_folder, hum_out_folder, vwind_folder, uwind_folder,
                                    wind_out_folder, nodata_value=-9999):
        """
        calculate wind and humidity of at different dates and save it in wind and humidity out folder
        all folder are list of folder for merra and geos, 0 index have merra and 1 index have geos
        :param start_date:
        :param end_date:
        :param start_date_merra:
        :param end_date_merra:
        :param start_date_geos:
        :param end_date_geos:
        :param Temp_folder: list of Temperature data folder of merra and geos
        :param Pres_folder: list of Air Pressure data folder of mera and geos
        :param Hum_folder: list of Humidity data folder of merra and geos
        :param hum_out_folder:  list of humidity out folder for merra and geos
        :param vwind_folder: v wind
        :param uwind_folder:  u wind
        :param wind_out_folder: list of window out folder for merra ang geos
        :param nodata_value:
        """
        Dates = pd.date_range(start_date, end_date, freq="D")

        for Date in Dates:
            idx = -1
            if start_date_merra != "" and datetime \
                    .strptime(start_date_merra, "%Y-%m-%d") <= Date <= datetime.strptime(end_date_merra, "%Y-%m-%d"):
                idx = 0
            if start_date_geos != "" and datetime \
                    .strptime(start_date_geos, "%Y-%m-%d") <= Date <= datetime.strptime(end_date_geos, "%Y-%m-%d"):
                idx = 1
            if idx != -1:
                Day = Date.day
                Month = Date.month
                Year = Date.year

                temp_file_one = Temp_folder[idx].format(yyyy=Year, mm=Month, dd=Day)
                pressure_file_one = Pres_folder[idx].format(yyyy=Year, mm=Month, dd=Day)
                humidity_file_one = Hum_folder[idx].format(yyyy=Year, mm=Month, dd=Day)
                out_folder_one = hum_out_folder[idx].format(yyyy=Year, mm=Month, dd=Day)

                u_wind_file_one = uwind_folder[idx].format(yyyy=Year, mm=Month, dd=Day)
                v_wind_file_one = vwind_folder[idx].format(yyyy=Year, mm=Month, dd=Day)
                out_folder_one_wind = wind_out_folder[idx].format(yyyy=Year, mm=Month, dd=Day)

                # geo_out, proj, size_X, size_Y = Open_array_info(Tempfile_one)
                temp_raster = RioRaster(temp_file_one)
                nodata_value = nodata_value if temp_raster.get_nodata_value() is None else temp_raster.get_nodata_value()
                temp_data = temp_raster.get_data_array(band=1)
                temp_data = temp_data - 273.15
                temp_data[temp_data < -900] = nodata_value
                pressure_data = RioRaster(pressure_file_one).get_data_array(band=1)
                humidity_data = RioRaster(humidity_file_one).get_data_array(1)
                pressure_data[pressure_data < 0] = nodata_value
                humidity_data[humidity_data < 0] = nodata_value
                u_wind_data = RioRaster(u_wind_file_one).get_data_array(band=1)
                v_wind_data = RioRaster(v_wind_file_one).get_data_array(band=1)

                # gapfilling
                v_wind_data = BandProcess.gap_filling(v_wind_data, nodata_value)
                u_wind_data = BandProcess.gap_filling(u_wind_data, nodata_value)
                temp_data = BandProcess.gap_filling(temp_data, nodata_value)
                pressure_data = BandProcess.gap_filling(pressure_data, nodata_value)
                humidity_data = BandProcess.gap_filling(humidity_data, nodata_value)

                es_data = 0.6108 * np.exp((17.27 * temp_data) / (temp_data + 237.3))
                hum_data = np.minimum((1.6077717 * humidity_data * pressure_data / es_data), 1) * 100
                hum_data = hum_data.clip(0, 100)

                out_crs = temp_raster.get_crs()
                out_transform = temp_raster.get_geo_transform()
                # Save_as_tiff(out_folder_one, HumData, geo_out, "WGS84")
                RioRaster.write_to_file(out_folder_one, hum_data, out_crs, out_transform, nodata_value)

                wind_data = np.sqrt(v_wind_data ** 2 + u_wind_data ** 2)
                # Save_as_tiff(out_folder_one_wind, WindData, geo_out, "WGS84")
                RioRaster.write_to_file(out_folder_one_wind, wind_data, out_crs, out_transform, nodata_value)

    @staticmethod
    def calculate_hourly_saturated_vapour_pressure(Temp_inst):
        """
            Hourly Saturation Vapor Pressure at the air temperature (kPa):
        :param Temp_inst: hourly Tmperature
        :return:
        """
        return 0.6108 * np.exp(17.27 * Temp_inst / (Temp_inst + 237.3))

    @staticmethod
    def calculate_daily_saturated_vapour_pressure(Temp_24):
        """
            Daily  Saturation Vapor Pressure at the air temperature (kPa):
        :param Temp_24: daily Temperature
        :return:
        """
        return 0.6108 * np.exp(17.27 * Temp_24 / (Temp_24 + 237.3))

    @staticmethod
    def calculate_latent_heat_of_vapourization(Surface_temp):
        """
        :param Surface_temp: RioLandsat.calculate_surface_temperature
        :return:
        """
        return (2.501 - 2.361e-3 * (Surface_temp - 273.15)) * 1E6

    @staticmethod
    def calculate_hourly_actual_vapour_pressure(RH_inst, sat_vapour_inst):
        """
        Hourly Actual vapour pressure (kPa), FAO 56, eq 19.:
        :param RH_inst: hourly Relative Humidity from Humidity_MERRA_Percentage_1_hourly
        :param sat_vapour_inst: hourly saturated vapour pressure
        :return:
        """
        return RH_inst * sat_vapour_inst / 100

    @staticmethod
    def calculate_daily_actual_vapour_pressure(RH_24, sat_vapour_24):
        """
        Daily Actual vapour pressure (kPa), FAO 56, eq 19.:
        :param RH_24: Daily Relative Humidity from Humidity_MERRA_Percentage_1_daily
        :param sat_vapour_24: daily saturated vapour pressure
        :return:
        """
        return RH_24 * sat_vapour_24 / 100

    @staticmethod
    def calculate_atmospheric_pressure(dem_arr: np.ndarray):
        """
        # Atmospheric pressure for altitude:
        :param dem_arr: elevation data
        :return:
        """
        return 101.3 * np.power((293 - 0.0065 * dem_arr) / 293, 5.26)

    @staticmethod
    def calculate_psychrometric_constant(air_pressure: np.ndarray):
        """
        Psychrometric constant (kPa / °C), FAO 56, eq 8.:
        :param air_pressure:
        :return:
        """
        return 0.665E-3 * air_pressure

    @staticmethod
    def calculate_slope_of_saturated_vapour_pressure(sat_vp_24, Temp_24):
        """
        Slope of satur vapour pressure curve at air temp (kPa / °C)
        :param sat_vp_24: daily saturated vapour pressure
        :param Temp_24: daily temperature
        :return:
        """
        return 4098 * sat_vp_24 / np.power(Temp_24 + 237.3, 2)

    @classmethod
    def calculate_wind_speed_friction(cls, h_obst, Wind_inst, zx, lai, ndvi, surf_albedo, water_mask, surf_roughness_equation_used):
        """
        Function to calculate the windspeed and friction by using the Raupach or NDVI model
        :param h_obst:
        :param Wind_inst: instantaneous wind using MERRA dataset of Wind
        :param zx: Wind speed measurement height mostly used as 2 for MERRA
        :param lai: Leaf Area Index
        :param ndvi:
        :param surf_albedo:
        :param water_mask:
        :param surf_roughness_equation_used:
        :return: surface_rough, wind speed at blending height, and friction velocity
        """

        # constants
        k_vk = 0.41  # Von Karman constant
        h_grass = 0.12  # Grass height (m)
        cd = 5  # Free parameter for displacement height, default = 20.6
        # 1) Raupach model
        # zom_Raupach = Raupach_Model(h_obst, cd, lai)

        # 2) NDVI model
        # zom_NDVI = NDVI_Model(ndvi, surf_albedo, water_mask)

        if surf_roughness_equation_used == 1:
            Surf_roughness = VegetationAnalysis.Raupach_Model_based_surface_roughness(h_obst, cd, lai)
        else:
            Surf_roughness = VegetationAnalysis.NDVI_based_surface_roughness(ndvi, surf_albedo, water_mask)

        Surf_roughness[Surf_roughness < 0.001] = 0.001

        zom_grass = 0.123 * h_grass
        # Friction velocity for grass (m/s):
        ustar_grass = k_vk * Wind_inst / np.log(zx / zom_grass)
        print('u*_grass = ', '%0.3f (m/s)' % np.mean(ustar_grass))
        # Wind speed (m/s) at the "blending height" (200m):
        u_200 = ustar_grass * np.log(200 / zom_grass) / k_vk
        print('Wind Speed at the blending height, u200 =', '%0.3f (m/s)' % np.mean(u_200))
        # Friction velocity (m/s):
        ustar_1 = k_vk * u_200 / np.log(200 / Surf_roughness)

        return Surf_roughness, u_200, ustar_1

    @staticmethod
    def air_pressure_kpa2mbar(p_air_kpa):
        """Like :func:`p_air`

        Parameters
        ----------
        p_air_kpa : np.ndarray
            air pressure
            :math:`Pair_{a}`
            [kpa]

        Returns
        -------
        p_air_mbar : np.ndarray or float
            air pressure
            :math:`Pair_{a}`
            [mbar]
        """
        return p_air_kpa * 10

    @staticmethod
    def air_pressure(z, p_air_0=1013.25):
        r"""
        Computes air pressure :math:`P` at a certain elevation derived from the
        air pressure at sea level :math:`P_0`. Air pressure decreases with
        increasing elevation.


        where the following constants are used

        * :math:`P_0` = air pressure [mbar] at sea level :math:`z_0` = 1013.25 mbar
        * :math:`T_{ref,0,K}` = reference temperature [K] at sea level
          :math:`z_0` = 293.15 K
        * :math:`g` = gravitational acceleration = 9.807 [m/s2]
        * :math:`R` = specific gas constant = 287.0 [J kg-1 K-1]
        * :math:`\alpha_1` = constant lapse rate for moist air = 0.0065 [K m-1]

        Parameters
        ----------
        z : np.ndarray or float
            elevation
            :math:`z`
            [m]
        p_air_0 : np.ndarray or float
            air pressure at sea level
            :math:`P_0`
            [mbar]

        Returns
        -------
        p_air : np.ndarray or float
            air pressure
            :math:`P`
            [mbar]

        Examples
        --------
        MeteoAnalysis.air_pressure(z=1000)
        900.5832172948869

        """
        t_ref = 293.15  # reference temperature 20 degrees celcius
        lapse = -0.0065  # lapse rate K m-1
        z_ref = 0  # sea level m
        gc_spec = 287.0  # gas constant J kg-1 K-1
        g = 9.807  # gravity m s-2
        power = (g / (-lapse * gc_spec))

        return p_air_0 * ((t_ref + lapse * (z - z_ref)) / t_ref) ** power

    @classmethod
    def air_pressure_daily(cls, z, p_air_0_24=1013.25):
        r"""Like :func:`air_pressure` but as a daily average

        Parameters
        ----------
        z : np.ndarray or float
            elevation
            :math:`z`
            [m]
        p_air_0_24 : np.ndarray or float
            daily air pressure at sea level
            :math:`P_{0,24}`
            [mbar]

        Returns
        -------
        p_air_24 : np.ndarray or float
            daily air pressure
            :math:`P_{24}`
            [mbar]

        """
        return cls.air_pressure(z, p_air_0_24)

    @classmethod
    def air_temperature_kelvin_inst(cls, t_air_i):
        """Like :func:`air_temperature_kelvin` but as an instantaneous value

        Parameters
        ----------
        t_air_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a,i}`
            [C]

        Returns
        -------
        t_air_k_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a,i}`
            [K]
        """
        return cls.air_temperature_kelvin(t_air_i)

    @staticmethod
    def vapour_pressure_from_specific_humidity(qv, p_air):
        """
        Computes the vapour pressure :math:`e_a` in [mbar] using specific humidity
        and surface pressure

         math ::
            e_{a}=\frac{q_{v}P}{\varepsilon}

        where the following constant is used

        * :math:`\varepsilon` = ratio of molecular weight of water to
          dry air = 0.622 [-]


        Parameters
        ----------
        qv : np.ndarray or float
            specific humidity
            :math:`q_{v}`
            [kg/kg]
        p_air : np.ndarray or float
            air pressure
            :math:`P`
            [mbar]

        Returns
        -------
        vp : np.ndarray or float
            vapour pressure
            :math:`e_{a}`
            [mbar]
        """
        r_mw = 0.622  # ratio water particles/ air particles
        return (qv * p_air) / r_mw

    @classmethod
    def vapour_pressure_from_specific_humidity_daily(cls, qv_24, p_air_24):
        """Like :func:`vapour_pressure_from_specific_humidity` but as a daily average

        Parameters
        ----------
        qv_24 : np.ndarray or float
            daily specific humidity
            :math:`q_{v,24}`
            [kg/kg]
        p_air_24 : np.ndarray or float
            daily air pressure
            :math:`P_{24}`
            [mbar]

        Returns
        -------
        vp_24 : np.ndarray or float
            daily vapour pressure
            [mbar]
        """
        return cls.vapour_pressure_from_specific_humidity(qv_24, p_air_24)

    @classmethod
    def vapour_pressure_from_specific_humidity_inst(cls, qv_i, p_air_i):
        """Like :func:`vapour_pressure_from_specific_humidity` but as an instantaneous value

        Parameters
        ----------
        qv_i : np.ndarray or float
            instantaneous specific humidity
            :math:`q_{v,i}`
            [kg/kg]
        p_air_i : np.ndarray or float
            instantaneous air pressure
            :math:`P_{i}`
            [mbar]

        Returns
        -------
        vp_i : np.ndarray or float
            instantaneous vapour pressure
            :math:`e_{a,i}`
            [mbar]
        """
        return cls.vapour_pressure_from_specific_humidity(qv_i, p_air_i)

    @staticmethod
    def saturated_vapour_pressure_average(svp_24_max, svp_24_min):
        """
        Average saturated vapour pressure based on two saturated vapour pressure values
        calculated using minimum and maximum air temperature respectively. This is preferable
        to calculating saturated vapour pressure using the average air temperature, because
        of the strong non-linear relationship between saturated vapour pressure and air
        temperature


        Parameters
        ----------
        svp_24_max : np.ndarray or float
            daily saturated vapour pressure based on maximum air temperature
            :math:`e_{s,max}`
            [mbar]
        svp_24_min : np.ndarray or float
            daily saturated vapour pressure based on minimum air temperature
            :math:`e_{s,min}`
            [mbar]

        Returns
        -------
        svp_24 : np.ndarray or float
            daily saturated vapour pressure
            :math:`e_{s,24}`
            [mbar]

        """
        return (svp_24_max + svp_24_min) / 2

    @staticmethod
    def vapour_pressure_deficit(svp, vp):
        r"""
        Computes the vapour pressure deficit :math:`\Delta_e` in [mbar]

        .. math ::
            \Delta_e=e_s-e_a

        Parameters
        ----------
        svp : np.ndarray or float
            saturated vapour pressure
            :math:`e_s`
            [mbar]
        vp : np.ndarray or float
            actual vapour pressure
            :math:`e_a`
            [mbar]

        Returns
        -------
        vpd : np.ndarray or float
           vapour pressure deficit
           :math:`\Delta_e`
           [mbar]

        Examples
        --------
        MeteoAnalysis.vapour_pressure_deficit(12.5, 5.4)
        7.1
        MeteoAnalysis.vapour_pressure_deficit(vp=5.4, svp=12.3)
        6.9

        """
        vpd = svp - vp
        vpd[vpd < 0] = 0

        return vpd

    @classmethod
    def vapour_pressure_deficit_daily(cls, svp_24, vp_24):
        """Like :func:`vapour_pressure_deficit` but as a daily average

        Parameters
        ----------
        svp_24 : np.ndarray or float
            daily saturated vapour pressure
            :math:`e_{s,24}`
            [mbar]
        vp_24 : np.ndarray or float
            daily actual vapour pressure
            :math:`e_{a,24}`
            [mbar]

        Returns
        -------
        vpd_24 : np.ndarray or float
           daily vapour pressure deficit
           [mbar]
        """
        return cls.vapour_pressure_deficit(svp_24, vp_24)

    @staticmethod
    def stress_vpd(vpd_24, vpd_slope=-0.3):
        r"""
        Computes the stress for plants if the vpd increases too much. With
        lower slopes the stress increases faster. The slope of the curve
        is between -0.3 and -0.7

        math ::
            S_{v}=m\ln(0.1\Delta_{e}+\frac{1}{2})+1

        Parameters
        ----------
        vpd_24 : np.ndarray or float
            daily vapour pressure deficit
            :math:`\Delta_{e}`
            [mbar]
        vpd_slope : np.ndarray or float
            vapour pressure stress curve slope
            :math:`m`
            [mbar-1]

        Returns
        -------
        stress_vpd : np.ndarray or float
            stress factor for vapour pressure deficit
            :math:`S_{v}`
            [-]

        Examples
        --------
        MeteoAnalysis.stress_vpd(15)
        0.79205584583201638
        MeteoAnalysis.stress_vpd(15, vpd_slope=-0.7)
        0.51479697360803833
        MeteoAnalysis.stress_vpd(15, vpd_slope=-0.3)
        0.79205584583201638

        """
        stress = vpd_slope * np.log(vpd_24 / 10. + 0.5) + 1
        stress = np.clip(stress, 0, 1)

        return stress

    @staticmethod
    def saturated_vapour_pressure(t_air):
        """
        Computes saturated vapour pressure :math:`e_s` [mbar], it provides
        the vapour pressure when the air is fully saturated with water. It is
        related to air temperature :math:`T_a` [C]:

        math ::
            e_{s}=6.108\exp\left[\frac{17.27T_{a}}{T_{a}+237.3}\right]

        Parameters
        ----------
        t_air : np.ndarray or float
            air temperature
            :math:`T_a`
            [C]

        Returns
        -------
        svp : np.ndarray or float
            saturated vapour pressure
            :math:`e_s`
            [mbar]

        Examples
        --------
        MeteoAnalysis.saturated_vapour_pressure(20)
        23.382812709274457

        """
        return 6.108 * np.exp(((17.27 * t_air) / (237.3 + t_air)))

    @classmethod
    def saturated_vapour_pressure_daily(cls, t_air_24):
        """Like :func:`saturated_vapour_pressure` but as a daily average

        Parameters
        ----------
        t_air_24 : np.ndarray
            daily air temperature
            :math:`T_{a,24}`
            [C]

        Returns
        -------
        svp_24 : np.ndarray or float
            daily saturated vapour pressure
            :math:`e_{s,24}`
            [mbar]

        """
        return cls.saturated_vapour_pressure(t_air_24)

    @classmethod
    def saturated_vapour_pressure_inst(cls, t_air_i):
        """Like :func:`saturated_vapour_pressure` but as an instantaneous value

        Parameters
        ----------
        t_air_i : np.ndarray
            instantaneous air temperature
            :math:`T_{a,i}`
            [C]

        Returns
        -------
        svp_i : np.ndarray or float
            instantaneous saturated vapour pressure
            :math:`e_{s,i}`
            [mbar]

        """
        return cls.saturated_vapour_pressure(t_air_i)

    @classmethod
    def saturated_vapour_pressure_minimum(cls, t_air_min_coarse):
        """Like :func:`saturated_vapour_pressure` but based on daily minimum air temperature. This
        is only relevant for reference ET calculations

        Parameters
        ----------
        t_air_min_coarse : np.ndarray or float
            daily minimum air temperature
            [C]

        Returns
        -------
        svp_24_min : np.ndarray or float
            daily saturated vapour pressure based on minimum air temperature
            :math:`e_{s,min}`
            [mbar]

        """
        return cls.saturated_vapour_pressure(t_air_min_coarse)

    @classmethod
    def saturated_vapour_pressure_maximum(cls, t_air_max_coarse):
        """Like :func:`saturated_vapour_pressure` but based on daily maximum air temperature. This
        is only relevant for reference ET calculations

        Parameters
        ----------
        t_air_max_coarse : np.ndarray or float
            daily maximum air temperature
            [C]

        Returns
        -------
        svp_24_max : np.ndarray or float
            daily saturated vapour pressure based on maximum air temperature
            :math:`e_{s,max}`
            [mbar]

        """
        return cls.saturated_vapour_pressure(t_air_max_coarse)

    @staticmethod
    def air_temperature_kelvin(t_air):
        r"""
        Converts air temperature from Celcius to Kelvin, where 0 degrees Celcius
        is equal to 273.15 degrees Kelvin

        Parameters
        ----------
        t_air : np.ndarray or float
            air temperature
            :math:`T_a`
            [C]

        Returns
        -------
        t_air_k : np.ndarray or float
            air temperature
            :math:`T_a`
            [K]

        Examples
        --------
        MeteoAnalysis.air_temperature_kelvin(12.5)
        285.65
        """
        zero_celcius = 273.15  # 0 degrees C in K
        return t_air + zero_celcius

    @classmethod
    def air_temperature_kelvin_daily(cls, t_air_24):
        """Like :func:`air_temperature_kelvin` but as a daily average

        Parameters
        ----------
        t_air_24 : np.ndarray or float
            daily air temperature
            [C]

        Returns
        -------
        t_air_k_24 : np.ndarray or float
            daily air temperature
            [K]
        """
        return cls.air_temperature_kelvin(t_air_24)

    @staticmethod
    def latent_heat(t_air):
        r"""
        Computes latent heat of evaporation :math:`\lambda` [J kg-1], describing
        the amount of energy needed to evaporate one kg of water at constant
        pressure and temperature. At higher temperatures less energy will be
        required than at lower temperatures.

         math ::

            \lambda=(\lambda_0 + \Delta_\lambda T_{a})

        where the following constants are used

        * :math:`\lambda_0` = latent heat of evaporation at 0 C = 2501000 [J kg-1]
        * :math:`\Delta_\lambda` = rate of change of latent heat with respect to temperature = -2361 [J Kg-1 C-1]

        Parameters
        ----------
        t_air : np.ndarray or float
            air temperature
            :math:`T_a`
            [C]

        Returns
        -------
        lh : np.ndarray or float
            latent heat of evaporation
            :math:`\lambda`
            [J/kg]

        Examples
        --------
        MeteoAnalysis.latent_heat(20)
        2453780.0

         plot:: pyplots/meteo/plot_latent_heat.py
        """
        lh_rate = -2361  # rate of latent heat vs temperature [J/kg/C]
        lh_0 = 2501000.0  # latent heat of evaporation at 0 C [J/kg]
        return lh_0 + lh_rate * t_air

    @classmethod
    def latent_heat_daily(cls, t_air_24):
        """Like :func:`latent_heat` but as a daily average

        Parameters
        ----------
        t_air_24 : np.ndarray or float
            daily air temperature
            :math:`T_{a1,24}`
            [C]

        Returns
        -------
        lh_24 : np.ndarray or float
            daily latent heat of evaporation
            [J/kg]

        """
        return cls.latent_heat(t_air_24)

    @staticmethod
    def moist_air_density(vp, t_air_k):
        r"""
        Computes moist air density :math:`\rho_{s}` in [kg m-3]

        math ::
            \rho_{s}=\frac{e_{a}}{R_{v}T_{a1,K}}

        where the following constants are used

        * :math:`R_v` = gas constant for moist air = 4.61 mbar K-1 m3 kg-1

        Parameters
        ----------
        vp : np.ndarray or float
            vapour pressure
            :math:`e_{a}`
            [mbar]
        t_air_k : np.ndarray or float
            air temperature
            :math:`T_{a1,K}`
            [K]

        Returns
        -------
        ad_moist : np.ndarray or float
            moist air density
            :math:`\rho_{s}`
            [kg m-3]

        Examples
        --------
        MeteoAnalysis.moist_air_density(vp=17.5, t_air_k = 293.15)
        0.012949327800393881



        """
        gc_moist = 4.61  # moist air gas constant mbar K-1 m3 kg-1
        return vp / (t_air_k * gc_moist)

    @classmethod
    def moist_air_density_daily(cls, vp_24, t_air_k_24):
        r"""
        Like :func:`moist_air_density` but as a daily average

        Parameters
        ----------
        vp_24 : np.ndarray or float
            daily vapour pressure
            :math:`e_{a1,24}`
            [mbar]
        t_air_k_24 : np.ndarray or float
            daily air temperature
            :math:`T_{a1,K,24}`
            [K]

        Returns
        -------
        ad_moist_24 : np.ndarray or float
            daily moist air density
            :math:`\rho_{s,24}`
            [kg m-3]

        """
        return cls.moist_air_density(vp_24, t_air_k_24)

    @classmethod
    def moist_air_density_inst(cls, vp_i, t_air_k_i):
        r"""
        Like :func:`moist_air_density` but as an instantaneous value

        Parameters
        ----------
        vp_i : np.ndarray or float
            instantaneous vapour pressure
            :math:`e_{a1,i}`
            [mbar]
        t_air_k_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a1,K,i}`
            [K]

        Returns
        -------
        ad_moist_i : np.ndarray or float
            instantaneous moist air density
            :math:`\rho_{s,i}`
            [kg m-3]

        """
        return cls.moist_air_density(vp_i, t_air_k_i)

    @staticmethod
    def air_density(ad_dry, ad_moist):
        """
        Computes air density :math:`\rho` in [kg m-3]

        Parameters
        ----------
        ad_dry : np.ndarray or float
            dry air density
            :math:`\rho_{d}`
            [kg m-3]
        ad_moist : np.ndarray or float
            moist air density
            :math:`\rho_{s}`
            [kg m-3]

        Returns
        -------
        ad : np.ndarray or float
            air density
            :math:`\rho`
            [kg m-3]

        Examples
        --------

        ad_moist = MeteoAnalysis.moist_air_density(vp=17.5, t_air_k = 293.15)
        ad_dry = MeteoAnalysis.dry_air_density(p_air=900, vp=17.5, t_air_k=293.15)
        MeteoAnalysis.air_density(ad_dry=ad_dry, ad_moist=ad_moist)
        1.0618706622660472



        """
        return ad_dry + ad_moist

    @classmethod
    def air_density_daily(cls, ad_dry_24, ad_moist_24):
        r"""

        Like :func:`air_density` but as a daily average

        Parameters
        ----------
        ad_dry_24 : np.ndarray or float
            daily dry air density
            :math:`\rho_{d,24}`
            [kg m-3]
        ad_moist_24 : np.ndarray or float
            daily moist air density
            :math:`\rho_{s,24}`
            [kg m-3]

        Returns
        -------
        ad_24 : np.ndarray or float
            daily air density
            :math:`\rho_{24}`
            [kg m-3]

        """
        return cls.air_density(ad_dry_24, ad_moist_24)

    @classmethod
    def air_density_inst(cls, ad_dry_i, ad_moist_i):
        r"""
        Like :func:`air_density` but as an instantaneous value

        Parameters
        ----------
        ad_dry_i : np.ndarray or float
            instantaneous dry air density
            :math:`\rho_{d,i}`
            [kg m-3]
        ad_moist_i : np.ndarray or float
            instantaneous moist air density
            :math:`\rho_{s,i}`
            [kg m-3]

        Returns
        -------
        ad_i : np.ndarray or float
            instantaneous air density
            :math:`\rho_{i}`
            [kg m-3]

        """
        return cls.air_density(ad_dry_i, ad_moist_i)

    @staticmethod
    def dry_air_density(p_air, vp, t_air_k):
        r"""
        Computes dry air density :math:`\rho_{d}` in [kg m-3]

        math ::
            \rho_{d}=\frac{P-e_{a}}{\Re T_{a1,K}}

        where the following constants are used

        * :math:`\Re` = gas constant for dry air = 2.87 mbar K-1 m3 kg-1

        Parameters
        ----------
        p_air : np.ndarray or float
            air pressure
            :math:`P`
            [mbar]
        vp : np.ndarray or float
            vapour pressure
            :math:`e_{a}`
            [mbar]
        t_air_k : np.ndarray or float
            daily air temperature
            :math:`T_{a}`
            [K]

        Returns
        -------
        ad_dry : np.ndarray or float
            dry air density
            :math:`\rho_{d}`
            [kg m-3]

        Examples
        --------

        MeteoAnalysis.dry_air_density(p_air=900, vp=17.5, t_air_k=293.15)
        1.0489213344656534



        """
        gc_dry = 2.87  # dry air gas constant mbar K-1 m3 kg-1
        return (p_air - vp) / (t_air_k * gc_dry)

    @classmethod
    def dry_air_density_daily(cls, p_air_24, vp_24, t_air_k_24):
        """
        Like :func:`dry_air_density` but as a daily average

        Parameters
        ----------
        p_air_24 : np.ndarray or float
            daily air pressure
            :math:`P_{24}`
            [mbar]
        vp_24 : np.ndarray or float
            daily vapour pressure
            :math:`e_{a1,24}`
            [mbar]
        t_air_k_24 : np.ndarray or float
            daily air temperature
            :math:`T_{a1,24}`
            [K]

        Returns
        -------
        ad_dry_24 : np.ndarray or float
            daily dry air density
            :math:`\rho_{d,24}`
            [kg m-3]
        """
        return cls.dry_air_density(p_air_24, vp_24, t_air_k_24)

    @classmethod
    def dry_air_density_inst(cls, p_air_i, vp_i, t_air_k_i):
        r"""
        Like :func:`dry_air_density` but as an instantaneous value

        Parameters
        ----------
        p_air_i : np.ndarray or float
            instantaneous air pressure
            :math:`P_{i}`
            [mbar]
        vp_i : np.ndarray or float
            instantaneous vapour pressure
            :math:`e_{a1,i}`
            [mbar]
        t_air_k_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a1,i}`
            [K]

        Returns
        -------
        ad_dry_i : np.ndarray or float
            instantaneous dry air density
            :math:`\rho_{d,i}`
            [kg m-3]
        """
        return cls.dry_air_density(p_air_i, vp_i, t_air_k_i)

    @classmethod
    def wet_bulb_temperature_kelvin_inst(cls, t_wet_i):
        """
        Converts wet bulb temperature from Celcius to Kelvin, where 0
        degrees Celcius is equal to 273.15 degrees Kelvin

        Parameters
        ----------
        t_wet_i : np.ndarray or float
            instantaneous wet bulb temperature
            :math:`T_{w,i}`
            [C]

        Returns
        -------
        t_wet_k_i : np.ndarray or float
            instantaneous wet bulb temperature
            :math:`T_{w,i}`
            [K]
        """
        return cls.air_temperature_kelvin(t_wet_i)

    @staticmethod
    def wind_speed_blending_height(u, z_obs=2, z_b=100):
        """
        Computes the wind speed at blending height :math:`u_{b}` [m/s] using the
        logarithmic wind profile

        Parameters
        ----------
        u : np.ndarray or float
            wind speed at observation height
            :math:`u_{obs}`
            [m/s]
        z_obs : np.ndarray or float
            observation height of wind speed
            :math:`z_{obs}`
            [m]
        z_b : np.ndarray or float
            blending height
            :math:`z_{b}`
            [m]

        Returns
        -------
        u_b : np.ndarray or float
            wind speed at blending height
            :math:`u_{b}`
            [m/s]

        Examples
        --------
        MeteoAnalysis.wind_speed_blending_height(u=3.0, z_obs=2, z_b=100)
        5.4646162953650572


        """

        z0m = 0.0171
        k = 0.41  # karman constant (-)

        ws = (k * u) / np.log(z_obs / z0m) * np.log(z_b / z0m) / k
        ws = np.clip(ws, 1, 150)

        return ws

    @classmethod
    def wind_speed_blending_height_daily(cls, u_24, z_obs=2, z_b=100):
        """Like :func:`wind_speed_blending_height` but as a daily average

        Parameters
        ----------
        u_24 : np.ndarray or float
            daily wind speed at observation height
            :math:`u_{obs,24}`
            [m/s]
        z_obs : np.ndarray or float
            observation height of wind speed
            :math:`z_{obs}`
            [m]
        z_b : np.ndarray or float
            blending height
            :math:`z_{b}`
            [m]

        Returns
        -------
        u_b_24 : np.ndarray or float
            daily wind speed at blending height
            :math:`u_{b, 24}`
            [m/s]

        """
        return cls.wind_speed_blending_height(u_24, z_obs, z_b)

    @staticmethod
    def psychrometric_constant(p_air, lh):
        r"""
        Computes the psychrometric constant :math:`\gamma` [mbar K-1] which
        relates the partial pressure of water in air to the air temperature

        math ::

            \gamma=\frac{Pc_{p}}{\varepsilon\lambda}

        where the following constants are used

        * :math:`c_{p}` = specific heat for dry air = 1004 [J Kg-1 K-1]
        * :math:`\varepsilon` = ratio of molecular weight of water to
          dry air = 0.622 [-]

        Parameters
        ----------
        p_air : np.ndarray or float
            air pressure
            :math:`P`
            [mbar]
        lh : np.ndarray or float
            latent heat of evaporation
            :math:`\lambda`
            [J/kg]

        Returns
        -------
        psy : np.ndarray or float
            psychrometric constant
            :math:`\gamma`
            [mbar K-1]

        Examples
        --------
        MeteoAnalysis.psychrometric_constant(p_air = 1003.0, lh = 2500000.0)
        0.6475961414790997
        MeteoAnalysis.psychrometric_constant(1003.0, 2500000.0)
        0.6475961414790997


        """
        sh = 1004.0  # specific heat J kg-1 K-1
        r_mw = 0.622  # ratio water particles/ air particles
        return (sh * p_air) / (r_mw * lh)

    @classmethod
    def psychrometric_constant_daily(cls, p_air_24, lh_24):
        """Like :func:`psychrometric_constant` but as a daily average

        Parameters
        ----------
        p_air_24 : np.ndarray or float
            daily air pressure
            :math:`P_{24}`
            [mbar]
        lh_24 : np.ndarray or float
            daily latent heat of evaporation
            :math:`\lambda_{24}`
            [J/kg]

        Returns
        -------
        psy_24 : np.ndarray or float
            daily psychrometric constant
            :math:`\gamma_{24}`
            [mbar K-1]

        """
        return cls.psychrometric_constant(p_air_24, lh_24)

    @classmethod
    def slope_saturated_vapour_pressure(cls, t_air):
        r"""
        Computes the rate of change of vapour pressure :math:`\Delta` in [mbar K-1]
        for a given air temperature :math:`T_a`. It is a function of the air
        temperature :math:`T_a` and the saturated vapour pressure :math:`e_s`
        [mbar] which in itself is a function of :math:`T_a`.

         math ::
            \Delta=\frac{4098e_{s}}{\left(237.3+T_{a}\right)^{2}}

        for :math:`e_s` see :func:`saturated_vapour_pressure`

        Parameters
        ----------
        t_air : np.ndarray or float
           air temperature
           :math:`T_a`
           [C]

        Returns
        -------
        ssvp : np.ndarray or float
           slope of saturated vapour pressure curve
           :math:`\Delta`
           [mbar K-1]

        Examples
        --------
        MeteoAnalysis.slope_saturated_vapour_pressure(20)
        1.447401881124136
        """
        svp = cls.saturated_vapour_pressure(t_air)
        return (4098 * svp) / (237.3 + t_air) ** 2

    @classmethod
    def slope_saturated_vapour_pressure_daily(cls, t_air_24):
        """Like :func:`slope_saturated_vapour_pressure` but as a daily average

        Parameters
        ----------
        t_air_24 : np.ndarray or float
           daily air temperature
           :math:`T_{a1,24}`
           [C]

        Returns
        -------
        ssvp_24 : np.ndarray or float
           daily slope of saturated vapour pressure curve
           :math:`\Delta_{24}`
           [mbar K-1]


        """
        return cls.slope_saturated_vapour_pressure(t_air_24)

    @classmethod
    def slope_saturated_vapour_pressure_inst(cls, t_air_i):
        """Like :func:`slope_saturated_vapour_pressure` but as an instantaneous
        value

        Parameters
        ----------
        t_air_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a1,i}`
            [C]

        Returns
        -------
        ssvp_i : np.ndarray or float
            instantaneous slope of saturated vapour pressure curve
            :math:`e_{s,i}`
            [mbar]
        """
        return cls.slope_saturated_vapour_pressure(t_air_i)
