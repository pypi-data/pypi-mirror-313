from math import sin, cos, tan

import numpy as np


class SolarRadiationAnalysis:
    @classmethod
    def calculate_declination_angle(cls, DOY):
        """
        Declination angle (radians)
        :param DOY: Day of the year
        :return:
        """
        B = 360. / 365 * (DOY - 81)  # (degrees)
        # Computation of cos(theta), where theta is the solar incidence angle relative to the normal to the land surface
        delta = np.arcsin(np.sin(np.deg2rad(23.45)) * np.sin(np.deg2rad(B)))  #
        return delta

    @classmethod
    def calculate_ra_mountain(cls, lon: np.ndarray, DOY: int, hour_loc: np.ndarray or float, minutes_loc: float, lon_proy: np.ndarray, lat_proy: np.ndarray, slope: np.ndarray, aspect: np.ndarray):
        """
        Calculates the extra-terrestiral solar radiation or radiation from mountain/slop by using the date, slope and aspect.
        parameters
        :param lon: longitude raster (np.ndarray)
        :param DOY:  day of the year
        :param hour_loc:
        :param minutes_loc:
        :param lon_proy: x value raster in meter (np.ndarray)
        :param lat_proy: y value raster in meter (np.ndarray)
        :param slope:  slope raster (np.ndarray)
        :param aspect: aspect raster (np.ndarray)
        :return:
        """
        # Constants
        Min_cos_zn = 0.1  # Min value for cos zenith angle
        Max_cos_zn = 1.0  # Maximum value for cos zenith angle
        Gsc = 1367  # Solar constant (W / m2)

        # Rounded difference of the local time from Greenwich (GMT) (hours):
        offset_GTM = round(lon[int(lon.shape[0] / 2), int(lon.shape[1] / 2)] * 24 / 360)

        try:
            GMT_time = float(hour_loc) - offset_GTM + float(minutes_loc) / 60  # Local time (hours)
            Loc_time = float(hour_loc) + float(minutes_loc) / 60  # Local time (hours)
        except:
            GMT_time = np.float_(hour_loc) - offset_GTM + np.float_(minutes_loc) / 60  # Local time (hours)
            Loc_time = np.float_(hour_loc) + np.float_(minutes_loc) / 60  # Local time (hours)

        print('  Local Time: ', '%0.3f' % np.nanmean(Loc_time))
        print('  GMT Time: ', '%0.3f' % np.nanmean(GMT_time))
        print('  Difference of local time (LT) from Greenwich (GMT): ', offset_GTM)

        # 1. Calculation of extraterrestrial solar radiation for slope and aspect
        # Computation of Hour Angle (HRA = w)
        B = 360. / 365 * (DOY - 81)  # (degrees)
        # Computation of cos(theta), where theta is the solar incidence angle relative to the normal to the land surface
        delta = cls.calculate_declination_angle(DOY)  # Declination angle (radians)
        phi = cls.calculate_latitude_of_pixel(lat_proy)
        s = np.deg2rad(slope)  # Surface slope (radians)
        gamma = np.deg2rad(aspect - 180)  # Surface aspect angle (radians)
        w = cls.w_time(GMT_time, lon_proy, DOY)  # Hour angle (radians)
        a, b, c = cls.constants_for_solar_radiation(delta, s, gamma, phi)
        cos_zn = cls.cos_zenith_angle(a, b, c, w)
        cos_zn = cos_zn.clip(Min_cos_zn, Max_cos_zn)

        print('Average Cos Zenith Angle: ', '%0.3f (Radians)' % np.nanmean(cos_zn))

        dr = 1 + 0.033 * cos(DOY * 2 * np.pi / 365)  # Inverse relative distance Earth-Sun
        # Instant. extraterrestrial solar radiation (W/m2), Allen et al.(2006):
        Ra_inst = Gsc * cos_zn * dr

        # 24-hours extraterrestrial radiation
        # 1. determine if there are one or two periods of sun
        # 2. calculate the 24-hours extraterrestrial radiation if there are two periods of sun
        # 3. calculate the 24-hours extraterrestrial radiation if there is one period of sun

        # 4. determine amount of sun periods
        Ra_24 = np.zeros(np.shape(lat_proy)) * np.nan
        constant = Gsc * dr / (2 * np.pi)
        TwoPeriod = cls.TwoPeriods(delta, s, phi)  # all input in radians

        # 2.) calculate the 24-hours extraterrestrial radiation (2 periods)
        ID = np.where(np.ravel(TwoPeriod == True))
        Ra_24.flat[ID] = cls.TwoPeriodSun(constant, delta, s.flat[ID], gamma.flat[ID], phi.flat[ID])

        # 3.) calculate the 24-hours extraterrestrial radiation (1 period)
        ID = np.where(np.ravel(TwoPeriod == False))
        Ra_24.flat[ID] = cls.OnePeriodSun(constant, delta, s.flat[ID], gamma.flat[ID], phi.flat[ID])

        # Horizontal surface
        ws = np.arccos(-np.tan(delta) * np.tan(phi))  # Sunrise/sunset time angle

        # Extraterrestial radiation for a horizontal surface for 24-h period:
        Ra_hor_24 = (Gsc * dr / np.pi * (np.sin(delta) * np.sin(phi) * ws + np.cos(delta) * np.cos(phi) * np.sin(ws)))
        # cos_theta_flat = (np.sin(delta) * np.sin(phi) + np.cos(delta) * np.cos(phi) * np.cos(w))

        # Mountain radiation
        Ra_mountain_24 = np.where(Ra_24 > Min_cos_zn * Ra_hor_24, Ra_24 / np.cos(s),
                                  Ra_hor_24)
        Ra_mountain_24[Ra_mountain_24 > 600.0] = 600.0

        return Ra_mountain_24, Ra_inst, cos_zn, dr, phi, delta

    @staticmethod
    def radiation_daily_for_flat_surface(phi, delta):
        """
         Daily 24 hr radiation - For flat terrain only !  which sunset hour angle ws
        :param phi:  latitude in radians
        :param delta: Declination angle (radians)
        :return:
        """
        return np.arccos(-np.tan(phi) * tan(delta))

    @staticmethod
    def w_time(GMT, lon_proy, DOY):
        """
        This function computes the hour angle (radians) of an image given the
        local time, longitude, and day of the year
        :param GMT:
        :param lon_proy:  longitude raster
        :param DOY:  day of the year
        :return: hour angle of the image
        """
        nrow, ncol = lon_proy.shape

        # Difference of the local time (LT) from Greenwich Mean Time (GMT) (hours):
        delta_GTM = lon_proy[int(nrow / 2), int(ncol / 2)] * 24 / 360
        if np.isnan(delta_GTM):
            delta_GTM = np.nanmean(lon_proy) * np.nanmean(lon_proy) * 24 / 360

        # Local Standard Time Meridian (degrees):
        LSTM = 15 * delta_GTM

        # Ecuation of time (EoT, minutes):
        B = 360. / 365 * (DOY - 81)  # (degrees)
        EoT = 9.87 * sin(np.deg2rad(2 * B)) - 7.53 * cos(np.deg2rad(B)) - 1.5 * sin(np.deg2rad(B))

        # Net Time Correction Factor (minutes) at the center of the image:
        TC = 4 * (lon_proy - LSTM) + EoT  # Difference in time over the longitude
        LST = GMT + delta_GTM + TC / 60  # Local solar time (hours)
        HRA = 15 * (LST - 12)  # Hour angle HRA (degrees)
        w = np.deg2rad(HRA)  # Hour angle HRA (radians)
        return w

    @staticmethod
    def constants_for_solar_radiation(delta, s, gamma, phi):
        """
        Based on Richard G. Allen 2006 equation 11
        determines constants for calculating the exterrestial solar radiation
        B = 360. / 365 * (DOY - 81)  # (degrees)
        # Computation of cos(theta), where theta is the solar incidence angle relative to the normal to the land surface
        delta = np.arcsin(np.sin(np.deg2rad(23.45)) * np.sin(np.deg2rad(B)))  # Declination angle (radians)
        Parameter
        :param delta:
        :param s: slope in radians
        :param gamma: slope direction in radians
        :param phi:  latitude in radians
        :return:
        """
        a = np.sin(delta) * np.cos(phi) * np.sin(s) * np.cos(gamma) - np.sin(delta) * np.sin(phi) * np.cos(s)
        b = np.cos(delta) * np.cos(phi) * np.cos(s) + np.cos(delta) * np.sin(phi) * np.sin(s) * np.cos(gamma)
        c = np.cos(delta) * np.sin(s) * np.sin(gamma)

        return a, b, c

    @staticmethod
    def cos_zenith_angle(a, b, c, w):
        """
        Based on Richard G. Allen 2006
        Calculate the cos zenith angle of the image by using the hour angle of the image and constants
        :param a:
        :param b:
        :param c:
        :param w:
        :return:
        """
        angle = -a + b * np.cos(w) + c * np.sin(w)

        return angle

    @staticmethod
    def TwoPeriods(delta, s, phi):
        """
        Based on Richard G. Allen 2006
        Create a boolean map with True values for places with two sunsets
        :param delta:
        :param s:
        :param phi:
        :return:
        """
        TwoPeriods = (np.sin(s) > np.ones(s.shape) * np.sin(phi) * np.cos(delta) + np.cos(phi) * np.sin(delta))

        return TwoPeriods

    @classmethod
    def OnePeriodSun(cls, constant, delta, s, gamma, phi):
        '''
        Based on Richard G. Allen 2006
        Calculate the 24-hours extraterrestrial radiation when there is one sun period
        '''
        sunrise, sunset = cls.SunHours(delta, s, gamma, phi)
        vals = cls.IntegrateSlope(constant, sunrise, sunset, delta, s, gamma, phi)

        return vals

    @classmethod
    def TwoPeriodSun(cls, constant, delta, s, gamma, phi):
        """
        Based on Richard G. Allen 2006
        Calculate the 24-hours extraterrestrial radiation when there are two sun period
        :param constant:
        :param delta:
        :param s:
        :param gamma:
        :param phi:
        :return:
        """
        A1, A2 = cls.SunHours(delta, s, gamma, phi)
        a, b, c = cls.constants_for_solar_radiation(delta, s, gamma, phi)
        riseSlope, setSlope = cls.BoundsSlope(a, b, c)
        B1 = np.maximum(riseSlope, setSlope)
        B2 = np.minimum(riseSlope, setSlope)
        Angle_B1 = cls.cos_zenith_angle(a, b, c, B1)
        Angle_B2 = cls.cos_zenith_angle(a, b, c, B2)

        B1[abs(Angle_B1) > 0.001] = np.pi - B1[abs(Angle_B1) > 0.001]
        B2[abs(Angle_B2) > 0.001] = -np.pi - B2[abs(Angle_B2) > 0.001]

        # Check if two periods really exist
        ID = np.ravel_multi_index(np.where(np.logical_and(B2 >= A1, B1 >= A2) == True), a.shape)
        Val = cls.IntegrateSlope(constant, B2.flat[ID], B1.flat[ID], delta, s.flat[ID], gamma.flat[ID], phi.flat[ID])
        ID = ID[Val < 0]

        # Finally calculate resulting values
        vals = np.zeros(B1.shape)

        vals.flat[ID] = (cls.IntegrateSlope(constant, A1.flat[ID], B2.flat[ID], delta, s.flat[ID], gamma.flat[ID], phi.flat[ID]) +
                         cls.IntegrateSlope(constant, B1.flat[ID], A2.flat[ID], delta, s.flat[ID], gamma.flat[ID], phi.flat[ID]))
        ID = np.ravel_multi_index(np.where(vals == 0), a.shape)
        vals.flat[ID] = cls.IntegrateSlope(constant, A1.flat[ID], A2.flat[ID], delta, s.flat[ID], gamma.flat[ID], phi.flat[ID])

        return vals

    @staticmethod
    def BoundsSlope(a, b, c):
        """
        Based on Richard G. Allen 2006 equation 13
        This function calculates candidate values for sunrise and sunset hour angles
        :param a:
        :param b:
        :param c:
        :return:
        """
        Div = (b ** 2 + c ** 2)
        Div[Div <= 0] = 0.00001
        sinB = (a * c + b * np.sqrt(b ** 2 + c ** 2 - a ** 2)) / Div
        sinA = (a * c - b * np.sqrt(b ** 2 + c ** 2 - a ** 2)) / Div

        sinB[sinB < -1] = -1
        sinB[sinB > 1] = 1  # Limits see appendix A.2.i
        sinA[sinA < -1] = -1
        sinA[sinA > 1] = 1  # Limits see appendix A.2.i

        sunrise = np.arcsin(sinA)
        sunset = np.arcsin(sinB)

        return sunrise, sunset

    @staticmethod
    def BoundsHorizontal(delta, phi):
        """
        Based on Richard G. Allen 2006
        This function calculates sunrise hours based on earth inclination and latitude
        If there is no sunset or sunrise hours the values are either set to 0 (polar night) or pi (polar day)
        :param delta:
        :param phi:
        :return:
        """
        bound = np.arccos(-np.tan(delta) * np.tan(phi))
        bound[abs(delta + phi) > np.pi / 2] = np.pi
        bound[abs(delta - phi) > np.pi / 2] = 0

        return bound

    @classmethod
    def SunHours(cls, delta, slope, slopedir, lat):
        # Define sun hours in case of one sunlight period
        a, b, c = cls.constants_for_solar_radiation(delta, slope, slopedir, lat)
        riseSlope, setSlope = cls.BoundsSlope(a, b, c)
        bound = cls.BoundsHorizontal(delta, lat)

        Calculated = np.zeros(slope.shape, dtype=bool)
        RiseFinal = np.zeros(slope.shape)
        SetFinal = np.zeros(slope.shape)

        # First check sunrise is not nan
        # This means that there is either no sunrise (whole day night) or no sunset (whole daylight)
        # For whole daylight, use the horizontal sunrise and whole day night a zero.
        Angle4 = cls.cos_zenith_angle(a, b, c, -bound)
        RiseFinal[np.logical_and(np.isnan(riseSlope), Angle4 >= 0.0)] = -bound[np.logical_and(np.isnan(riseSlope), Angle4 >= 0.0)]
        Calculated[np.isnan(riseSlope)] = True

        # Step 1 > 4
        Angle1 = cls.cos_zenith_angle(a, b, c, riseSlope)
        Angle2 = cls.cos_zenith_angle(a, b, c, -bound)

        ID = np.ravel_multi_index(np.where(np.logical_and(np.logical_and(Angle2 < Angle1 + 0.001, Angle1 < 0.001), Calculated == False) == True), a.shape)
        RiseFinal.flat[ID] = riseSlope.flat[ID]
        Calculated.flat[ID] = True
        # step 5 > 7
        Angle3 = cls.cos_zenith_angle(a, b, c, -np.pi - riseSlope)

        ID = np.ravel_multi_index(np.where(np.logical_and(np.logical_and(-bound < (-np.pi - riseSlope), Angle3 <= 0.001), Calculated == False) == True), a.shape)
        RiseFinal.flat[ID] = -np.pi - riseSlope.flat[ID]
        Calculated.flat[ID] = True

        # For all other values we use the horizontal sunset if it is positive, otherwise keep a zero
        RiseFinal[Calculated == False] = -bound[Calculated == False]

        # Then check sunset is not nan or < 0
        Calculated = np.zeros(slope.shape, dtype=bool)

        Angle4 = cls.cos_zenith_angle(a, b, c, bound)
        SetFinal[np.logical_and(np.isnan(setSlope), Angle4 >= 0.0)] = bound[np.logical_and(np.isnan(setSlope), Angle4 >= 0.0)]
        Calculated[np.isnan(setSlope)] = True

        # Step 1 > 4
        Angle1 = cls.cos_zenith_angle(a, b, c, setSlope)
        Angle2 = cls.cos_zenith_angle(a, b, c, bound)

        ID = np.ravel_multi_index(np.where(np.logical_and(np.logical_and(Angle2 < Angle1 + 0.001, Angle1 < 0.001), Calculated == False) == True), a.shape)
        SetFinal.flat[ID] = setSlope.flat[ID]
        Calculated.flat[ID] = True
        # step 5 > 7
        Angle3 = cls.cos_zenith_angle(a, b, c, np.pi - setSlope)

        ID = np.ravel_multi_index(np.where(np.logical_and(np.logical_and(bound > (np.pi - setSlope), Angle3 <= 0.001), Calculated == False) == True), a.shape)
        SetFinal.flat[ID] = np.pi - setSlope.flat[ID]
        Calculated.flat[ID] = True

        # For all other values we use the horizontal sunset if it is positive, otherwise keep a zero
        SetFinal[Calculated == False] = bound[Calculated == False]

        #    Angle4 = AngleSlope(a,b,c,bound)
        #    SetFinal[np.logical_and(Calculated == False,Angle4 >= 0)] = bound[np.logical_and(Calculated == False,Angle4 >= 0)]

        # If Sunrise is after Sunset there is no sunlight during the day
        SetFinal[SetFinal <= RiseFinal] = 0.0
        RiseFinal[SetFinal <= RiseFinal] = 0.0

        return RiseFinal, SetFinal

    @staticmethod
    def IntegrateSlope(constant, sunrise, sunset, delta, s, gamma, phi):
        """
        Based on Richard G. Allen 2006 equation 5
        Calculate the 24 hours extraterrestrial radiation
        :param constant:
        :param sunrise:
        :param sunset:
        :param delta:
        :param s:
        :param gamma:
        :param phi:
        :return:
        """
        # correct the sunset and sunrise angels for days that have no sunset or no sunrise
        SunOrNoSun = np.logical_or(((np.abs(delta + phi)) > (np.pi / 2)), ((np.abs(delta - phi)) > (np.pi / 2)))
        integral = np.zeros(s.shape)
        ID = np.where(np.ravel(SunOrNoSun == True))

        # No sunset
        IDNoSunset = np.where(np.ravel(abs(delta + phi.flat[ID]) > (np.pi / 2)))
        if np.any(IDNoSunset) == True:
            sunset1 = np.pi
            sunrise1 = -np.pi
            integral.flat[IDNoSunset] = constant * (np.sin(delta) * np.sin(phi) * np.cos(s) * (sunset1 - sunrise1)
                                                    - np.sin(delta) * np.cos(phi) * np.sin(s) * np.cos(gamma) * (sunset1 - sunrise1)
                                                    + np.cos(delta) * np.cos(phi) * np.cos(s) * (np.sin(sunset1) - np.sin(sunrise1))
                                                    + np.cos(delta) * np.sin(phi) * np.sin(s) * np.cos(gamma) * (np.sin(sunset1) - np.sin(sunrise1))
                                                    - np.cos(delta) * np.sin(s) * np.sin(gamma) * (np.cos(sunset1) - np.cos(sunrise1)))

        # No sunrise
        elif np.any(IDNoSunset) == False:
            integral.flat[IDNoSunset == False] = constant * (np.sin(delta) * np.sin(phi) * np.cos(s) * (0)
                                                             - np.sin(delta) * np.cos(phi) * np.sin(s) * np.cos(gamma) * (0)
                                                             + np.cos(delta) * np.cos(phi) * np.cos(s) * (np.sin(0) - np.sin(0))
                                                             + np.cos(delta) * np.sin(phi) * np.sin(s) * np.cos(gamma) * (np.sin(0) - np.sin(0))
                                                             - np.cos(delta) * np.sin(s) * np.sin(gamma) * (np.cos(0) - np.cos(0)))

        ID = np.where(np.ravel(SunOrNoSun == False))
        integral.flat[ID] = constant * (np.sin(delta) * np.sin(phi) * np.cos(s) * (sunset - sunrise)
                                        - np.sin(delta) * np.cos(phi) * np.sin(s) * np.cos(gamma) * (sunset - sunrise)
                                        + np.cos(delta) * np.cos(phi) * np.cos(s) * (np.sin(sunset) - np.sin(sunrise))
                                        + np.cos(delta) * np.sin(phi) * np.sin(s) * np.cos(gamma) * (np.sin(sunset) - np.sin(sunrise))
                                        - np.cos(delta) * np.sin(s) * np.sin(gamma) * (np.cos(sunset) - np.cos(sunrise)))

        return integral

    @classmethod
    def calculate_latitude_of_pixel(cls, lat: np.ndarray):
        """

        :param lat:
        :return:
        """
        return np.deg2rad(lat)  # latitude of the pixel (radians)

    @staticmethod
    def calculate_extraterrestrial_daily_radiation(ws_angle, phi, dr, delta, nrow, ncol, Gsc_const=1367):
        """
        caclulate Extraterrestrial daily radiation, Ra (W/m2):
        :param ws_angle:   Daily 24 hr radiation - For flat terrain only
        :param phi:  lat in rad
        :param dr: nverse relative distance Earth-Sun
        :param delta: delination angle in radian
        :param nrow:  no of rows
        :param ncol: no of cols
        :param Gsc_const:  Solar constant (W / m2) value is  1367
        :return:
        """
        Ra24_flat = (Gsc_const / np.pi * dr * (ws_angle * np.sin(phi[int(nrow / 2), int(ncol / 2)]) * np.sin(delta) +
                                               np.cos(phi[int(nrow / 2), int(ncol / 2)]) * np.cos(delta) * np.sin(ws_angle)))
        return Ra24_flat

    @staticmethod
    def calculate_daily_solar_radiation(Ra_mountain_24, Transm_24):
        """
        calculate daily radiation if transmissivity is available method 2
        :param Ra_mountain_24: diation from mountain or slop using calculate_ra_mountain
        :param Transm_24: SolarRadiationAnalysis.calculate_hourly_solar_radiation
        :return:
        """
        return Ra_mountain_24 * Transm_24

    @staticmethod
    def calculate_transmissivity_correction(Transm_inst: np.ndarray):
        """
        Parameters
        :param Transm_inst: either through dataset like MERRA or using  SolarRadiationAnalysis.calculate_instant_transmissivity(Rs_inst, Ra_inst)
        :return:
        """
        # Atmospheric emissivity, by Bastiaanssen (1995):
        transm_corr = np.copy(Transm_inst)
        transm_corr[Transm_inst < 0.001] = 0.1
        transm_corr[Transm_inst > 1] = 1
        return transm_corr

    @staticmethod
    def calculate_instantaneous_incoming_short_wavelength_radiation(Ra_inst: np.ndarray, transmissivity_correction: np.ndarray):
        """
        calculate hourly radiation if transmissivity is available method 2
        :param Ra_inst: radiation from mountain or slop using calculate_ra_mountain
        :param transmissivity_correction: transmissivity correction using  SolarRadiationAnalysis.calculate_transmissivity_correction
        :return:
        """
        # Instantaneous incoming short wave radiation (W/m2):
        Rs_inst = Ra_inst * transmissivity_correction
        return Rs_inst

    @staticmethod
    def calculate_daily_transmissivity(Rs_24, Ra_mountain_24):
        """
        calculate daily transmissivity if radiation is available method 1
        :param Rs_24: daily radiation can be extracted from MERRA swgdn_MERRA_W-m-2
        :param Ra_mountain_24: Radiation from mountain or slop using calculate_ra_mountain
        :return:
        """

        return Rs_24 / Ra_mountain_24

    @staticmethod
    def calculate_instant_transmissivity(Rs_instant, Ra_inst):
        """
        calculate hourly transmissivity if radiation is available method 1
        :param Rs_instant: instantenous short wavelength radiation (W/m2):  which can be extracted from MERRA swgdn_MERRA_W-m-2
        :param Ra_inst: Radiation from mountain or slop using calculate_ra_mountain
        :return:
        """

        return Rs_instant / Ra_inst

    @staticmethod
    def calculate_daily_solar_radiation_from_extraterrestrial_radiation(Ra24_flat, Transm_24):
        """
        Parameters
        :param Ra24_flat: daily extraterrestrial_radiation using SolarRadiationAnalysis.calculate_extraterrestrial_daily_radiation
        :param Transm_24: daily transmissivity using SolarRadiationAnalysis.calculate_daily_transmissivity
        :return:
        """
        return Ra24_flat * Transm_24

    @staticmethod
    def inverse_earth_sun_distance(doy):
        """
        Computes the inverse earth sun distance (iesd) in Angstrom Unit where 1 AU is 1.496e8 km

        Parameters
        ----------
        doy : np.ndarray or float
            julian day of the year
            :math:`J`
            [-]

        Returns
        -------
        iesd : np.ndarray or float
            inverse earth sun distance
            :math:`d_{r}`
            [AU]

        Examples
        --------
        SolarRadiationAnalysis.inverse_earth_sun_distance(180)
        0.96703055420162642
        """

        return 1 + 0.033 * np.cos(doy * 2 * np.pi / 365.0)

    @staticmethod
    def seasonal_correction(doy):
        r"""
        Computes the seasonal correction for solar time  in hours


        Parameters
        ----------
        doy : np.ndarray or float
            julian day of the year
            :math:`J`
            [-]

        Returns
        -------
        sc : np.ndarray or float
            seasonal correction
            :math:`s_{c}`
            [hours]

        Examples
        --------
        SolarRadiationAnalysis.seasonal_correction(180)
        -0.052343379605521212
        """
        b = 2 * np.pi * (doy - 81) / 365.0
        return 0.1645 * np.sin(2 * b) - 0.1255 * np.cos(b) - 0.025 * np.sin(b)

    @staticmethod
    def day_angle(doy):
        """

        Computes the day angle. 0 is january

        Parameters
        ----------
        doy : np.ndarray or float
            day of year
            :math:`j`
            [-]

        Returns
        -------
        day_angle : np.ndarray or float
            day angle
            :math:`j^{\prime}`
            [rad]

        """
        return 2 * np.pi * doy / 365.25

    @staticmethod
    def hour_angle(sc, dtime, lon=0):
        """
        Computes the hour angle which is zero at noon and -pi at 0:00 am and
        pi at 12:00 pm

        Parameters
        ----------
        sc : np.ndarray or float
            seasonal correction
            :math:`s_{c}`
            [hours]
        dtime : np.ndarray or float
            decimal time
            :math:`t`
            [hours]
        lon : np.ndarray or float
            longitude
            :math:`\phi`
            [rad]

        Returns
        -------
        ha : np.ndarray or float
            hour_angle
            :math:`\omega`
            [rad]

        Examples
        --------
        SolarRadiationAnalysis.hour_angle(sc=solrad.seasonal_correction(75), dtime=11.4)
        -0.19793970172084141
        """
        dtime = dtime  # + (lon / (15*np.pi/180.0))
        return (np.pi / 12.0) * (dtime + sc - 12.0)

    @staticmethod
    def declination(doy):
        """
        Computes the solar declination which is the angular height of the sun
        above the astronomical equatorial plane in radians


        Parameters
        ----------
        doy : np.ndarray or float
            julian day of the year
            :math:`J`
            [-]

        Returns
        -------
        decl : np.ndarray or float
            declination
            :math:`\delta`
            [rad]

        Examples
        --------

        SolarRadiationAnalysis.declination(180)
        0.40512512455439242
        """
        B = 360. / 365 * (doy - 81)
        decl = np.arcsin(np.sin(np.deg2rad(23.45)) * np.sin(np.deg2rad(B)))

        return decl

    @staticmethod
    def longitude_rad(lon_deg):
        r"""
        Converts longitude from degrees to radians.

        Parameters
        ----------
        lon_deg : np.ndarray or float
            longitude in degrees
            [deg]

        Returns
        -------
        lon : np.ndarray or float
            longitude
            [rad]

        """
        return lon_deg * np.pi / 180.0

    @staticmethod
    def latitude_rad(lat_deg):
        """
        Converts latitude from degrees to radians.

        Parameters
        ----------
        lat_deg : np.ndarray
            latitude in degrees
            :math:`\lambda`
            [deg]

        Returns
        -------
        lat : np.ndarray or float
            latitude
            :math:`\lambda`
            [rad]

        """
        return lat_deg * np.pi / 180.0

    @staticmethod
    def slope_rad(slope_deg):
        """
        Converts slope from degrees to radians.

        Parameters
        ----------
        slope_deg : np.ndarray
            slope in degrees
            :math:`s`
            [deg]

        Returns
        -------
        slope : np.ndarray or float
            slope
            :math:`\Delta`
            [rad]

        """
        return slope_deg * np.pi / 180.0

    @staticmethod
    def aspect_rad(aspect_deg):
        """
        Converts aspect from degrees to radians.

        Parameters
        ----------
        aspect_deg : np.ndarray
            aspect in degrees
            :math:`s`
            [deg]

        Returns
        -------
        aspect : np.ndarray or float
            aspect (0 is north; pi is south)
            :math:`\alpha`
            [rad]
        """
        return aspect_deg * np.pi / 180.0

    @classmethod
    def daily_solar_radiation_toa_new(cls, sc, decl, iesd, lat, doy, slope=0, aspect=0):
        """
        Computes the daily solar radiation at the top of the atmosphere.


        Parameters
        ----------
        iesd : np.ndarray or float
            inverse earth sun distance
            :math:`d_{r}`
            [AU]
        decl : np.ndarray or float
            solar declination
            :math:`\delta`
            [rad]
        sc : np.ndarray or float
            seasonal correction
            :math:`s_{c}`
            [hours]
        lat : np.ndarray
            latitude
            :math:`\lambda`
            [rad]
        slope : np.ndarray or float
            slope
            :math:`\Delta`
            [rad]
        aspect : np.ndarray or float
            aspect (0 is north; pi is south)
            :math:`\alpha`
            [rad]

        Returns
        -------
        ra_24_toa : np.ndarray or float
            daily solar radiation at the top of atmosphere
            :math:`S_{toa}`
            [Wm-2]

        Examples
        --------
        doy = 1
        sc = SolarRadiationAnalysis.seasonal_correction(doy)
        decl = SolarRadiationAnalysis.declination(doy)
        iesd = SolarRadiationAnalysis.inverse_earth_sun_distance(doy)
        SolarRadiationAnalysis.daily_solar_radiation_toa(sc, decl, iesd, lat=25*pi/180.0)
        265.74072308978026
        """
        # print(type(slope))
        if type(slope) == int:
            slope = np.zeros(lat.shape)
        # print(type(aspect))
        if type(aspect) == int:
            aspect = np.zeros(lat.shape)

        gamma = np.deg2rad(np.rad2deg(aspect) - 180)  # Surface aspect angle (radians)
        a, b, c = cls.constants_for_solar_radiation(decl, slope, gamma, lat)

        ra24 = np.zeros(np.shape(lat)) * np.nan
        dr = 1 + 0.033 * np.cos(doy * 2 * np.pi / 365)  # Inverse relative distance Earth-Sun
        sol = 1367  # maximum solar radiation at top of atmosphere W m-2
        constant = sol * dr / (2 * np.pi)
        TwoPeriod = cls.TwoPeriods(decl, slope, lat)  # all input in radians

        # 2.) calculate the 24-hours extraterrestrial radiation (2 periods)
        ID = np.where(np.ravel(TwoPeriod == True))
        ra24.flat[ID] = cls.TwoPeriodSun(constant, decl, slope.flat[ID], gamma.flat[ID], lat.flat[ID])

        # 3.) calculate the 24-hours extraterrestrial radiation (1 period)
        ID = np.where(np.ravel(TwoPeriod == False))
        ra24.flat[ID] = cls.OnePeriodSun(constant, decl, slope.flat[ID], gamma.flat[ID], lat.flat[ID])

        # Horizontal surface
        ws = np.arccos(-np.tan(decl) * np.tan(lat))  # Sunrise/sunset time angle

        # Extraterrestial radiation for a horizontal surface for 24-h period:
        Ra_hor_24 = (sol * dr / np.pi * (np.sin(decl) * np.sin(lat) * ws + np.cos(decl) * np.cos(lat) * np.sin(ws)))
        # cos_theta_flat = (np.sin(delta) * np.sin(phi) + np.cos(delta) * np.cos(phi) * np.cos(w))

        # Mountain radiation
        ra24 = np.where(ra24 > 0.1 * Ra_hor_24, ra24 / np.cos(slope),
                        Ra_hor_24)
        ra24[ra24 > 600.0] = 600.0

        return ra24

    @staticmethod
    def sunset_hour_angle(lat, decl):
        """
        Computes the sunset hour angle


        Parameters
        ----------
        decl : np.ndarray or float
            solar declination
            :math:`\delta`
            [rad]
        lat : np.ndarray or float
            latitude
            :math:`\lambda`
            [rad]

        Returns
        -------
        ws : np.ndarray or float
            sunset hour angle
            :math:`w_{s}`
            [rad]

        """
        return np.arccos(-(np.tan(lat) * np.tan(decl)))

    @staticmethod
    def daily_solar_radiation_toa_flat(decl, iesd, lat, ws):
        """
        Computes the daily solar radiation at the top of the atmosphere for a flat
        surface.

        Parameters
        ----------
        decl : np.ndarray or float
            solar declination
            :math:`\delta`
            [rad]
        iesd : np.ndarray or float
            inverse earth sun distance
            :math:`d_{inv,r}`
            [AU]
        lat : np.ndarray or float
            latitude
            :math:`\lambda`
            [rad]
        ws : np.ndarray or float
            sunset hour angle
            :math:`w_{s}`
            [rad]

        Returns
        -------
        ra_24_toa_flat : np.ndarray or float
            daily solar radiation at the top of atmosphere for a flat surface
            :math:`S_{toa,f}`
            [Wm-2]

        """
        sol = 1367  # maximum solar radiation at top of atmosphere W m-2
        ra_flat = (sol / np.pi) * iesd * (ws * np.sin(lat) * np.sin(decl) +
                                          np.cos(lat) * np.cos(decl) * np.sin(ws))

        return ra_flat

    @staticmethod
    def daily_solar_radiation_flat(ra_24_toa_flat, trans_24):
        """
        Computes the daily solar radiation at the earth's surface


        Parameters
        ----------
        ra_24_toa_flat : np.ndarray or float
            daily solar radiation at the top of atmosphere for a flat surface
            :math:`S_{toa}`
            [Wm-2]
        trans_24 : np.ndarray or float
            daily atmospheric transmissivity
            :math:`\tau`
            [-]

        Returns
        -------
        ra_24 : np.ndarray or float
            daily solar radiation for a flat surface
            :math:`S^{\downarrow}`
            [Wm-2]

        """
        return ra_24_toa_flat * trans_24

    @staticmethod
    def diffusion_index(trans_24, diffusion_slope=-1.33, diffusion_intercept=1.15):
        r"""
        Computes the diffusion index, the ratio between diffuse and direct
        solar radiation. The results are clipped between 0 and 1.


        Parameters
        ----------
        trans_24 : np.ndarray
            daily atmospheric transmissivity
            :math:`\tau`
            [-]
        diffusion_slope : np.ndarray or float
            slope of diffusion index vs transmissivity relationship
            :math:`b_{diff}`
            [-]
        diffusion_intercept : np.ndarray or float
            intercept of diffusion index vs transmissivity relationship
            :math:`a_{diff}`
            [-]

        Returns
        -------
        diffusion_index : np.ndarray or float
            diffusion_index
            :math:`I_{diff}`
            [-]

        """
        res = diffusion_intercept + trans_24 * diffusion_slope

        res = np.clip(res, 0, 1)

        return res

    @staticmethod
    def daily_total_solar_radiation(ra_24_toa, ra_24_toa_flat, diffusion_index, trans_24):
        """
        Computes the daily solar radiation at the earth's surface taken
        diffuse and direct solar radiation into account

        Parameters
        ----------
        ra_24_toa : np.ndarray or float
            daily solar radiation at the top of atmosphere
            :math:`S_{toa}`
            [Wm-2]
        ra_24_toa_flat : np.ndarray or float
            daily solar radiation at the top of atmosphere for a flat surface
            :math:`S_{toa,f}`
            [Wm-2]
        diffusion_index : np.ndarray or float
            diffusion_index
            :math:`I_{diff}`
            [-]
        trans_24 : np.ndarray or float
            daily atmospheric transmissivity
            :math:`\tau`
            [-]

        Returns
        -------
        ra_24 : np.ndarray or float
            daily solar radiation
            :math:`S^{\downarrow}`
            [Wm-2]

        """
        diffuse = trans_24 * ra_24_toa_flat * diffusion_index
        direct = trans_24 * ra_24_toa * (1 - diffusion_index)
        return diffuse + direct

    @staticmethod
    def stress_radiation(ra_24):
        """
        Computes the stress for plants when there is insufficient radiation


        Parameters
        ----------
        ra_24 : np.ndarray or float
            daily solar radiation
            :math:`S^{\downarrow}`
            [Wm-2]

        Returns
        -------
        stress_rad : np.ndarray or float
            stress factor for radiation
            :math:`S_{r}`
            [-]


        Examples
        --------
        SolarRadiationAnalysis.stress_radiation()
        0.0
        SolarRadiationAnalysis.stress_radiation(500)
        1.0
        SolarRadiationAnalysis.stress_radiation(700)
        1.0
       SolarRadiationAnalysis.stress_radiation(250)
        0.90322580645161288
        """
        stress = ra_24 / (ra_24 + 60.) * (1 + 60. / 500.)
        stress = np.clip(stress, 0, 1)

        return stress

    @staticmethod
    def longwave_radiation_fao(t_air_k_24, vp_24, trans_24, vp_slope=0.14, vp_offset=0.34,
                               lw_slope=1.35, lw_offset=-0.35):
        r"""
        Computes the net longwave radiation according to the FAO 56 manual.


        where the following constant is used

        * :math:`\sigma` = Stefan Boltzmann constant = 5.67 e-8 J s-1 m-2 K-4

        Parameters
        ----------
        t_air_k_24 : np.ndarray or float
            daily air temperature in Kelvin
            :math:`T_{a1,K}`
            [-]
        vp_24 : np.ndarray or float
            daily vapour pressure
            :math:`e_{a}`
            [mbar]
        trans_24 : np.ndarray or float
            daily atmospheric transmissivity
            :math:`\tau`
            [-]
        vp_slope : np.ndarray or float
            slope of the vp-term in the FAO-56 longwave radiation relationship
            :math:`vp_{slope}`
            [-]
        vp_offset : np.ndarray or float
            offset of the vp-term in the FAO-56 longwave radiation relationship
            :math:`vp_{off}`
            [-]
        lw_slope : np.ndarray or float
            slope of the tau-term in the FAO-56 longwave radiation relationship
            :math:`lw_{slope}`
            [-]
        lw_offset : np.ndarray or float
            offset of the tau-term in the FAO-56 longwave radiation relationship
            :math:`lw_{off}`
            [-]

        Returns
        -------
        l_net : np.ndarray or float
            daily net longwave radiation
            :math:`L^{*}`
            [Wm-2]

        Examples
        --------

        SolarRadiationAnalysis.longwave_radiation_fao(t_air_k=302.5, vp=10.3, trans_24=0.6)
        68.594182173686306
        """
        sb = 5.67e-8  # stefan boltzmann constant
        return sb * t_air_k_24 ** 4 * (vp_offset - vp_slope * np.sqrt(0.1 * vp_24)) * (lw_offset + lw_slope * (trans_24 / 0.75))

    @staticmethod
    def interception_wm2(int_mm, lh_24):
        r"""
        Computes the energy equivalent for the interception in Wm-2 if it
        is provided in mm/day

        math ::
            I = \frac{\lambda I^*}{86400}

        Parameters
        ----------
        int_mm : np.ndarray or float
            interception
            :math:`I^*`
            [mm day-1]

        lh_24 : np.ndarray or float
            daily latent heat for evaporation
            :math:`\lambda`
            [J kg-1]

        Returns
        -------
        int_wm2 : np.ndarray or float
            interception
            :math:`I`
            [W m-2]

        Examples
        --------
        lh = MeteoAnalysis.latent_heat_daily(20.0)
        SolarRadiationAnalysis.interception_wm2(1.0, lh)
        28.40023148148148

        """
        day_sec = 86400.0  # seconds in a day
        return int_mm * (lh_24 / day_sec)

    @staticmethod
    def net_radiation(r0, ra_24, l_net, int_wm2):
        """
        Computes the net radiation


        Parameters
        ----------
        r0 : np.ndarray or float
            albedo
            :math:`\alpha_{0}`
            [-]
        ra_24 : np.ndarray or float
            daily solar radiation
            :math:`S^{\downarrow}`
            [Wm-2]
        l_net : np.ndarray or float
            daily net longwave radiation
            :math:`L^{*}`
            [wm-2]
        int_wm2 : np.ndarray or float
            interception
            :math:`I`
            [Wm-2]

        Returns
        -------
        rn_24 : np.ndarray or float
            daily net radiation
            :math:`Q^{*}`
            [Wm-2]

        Examples
        --------

        SolarRadiation.net_radiation(r0=0.10, ra_24=123., l_net=24., int_wm2=0)
        86.7
        """
        rn_24 = (1 - r0) * ra_24 - l_net - int_wm2
        rn_24 = rn_24.clip(20, 2000)
        return rn_24

    @staticmethod
    def net_radiation_canopy(rn_24, sf_soil):
        r"""
        Computes the net radiation for the canopy

         math ::
            Q^{*}_{canopy} = \left(1-s_f\right) Q^{*}

        Parameters
        ----------
        rn_24 : np.ndarray or float
            net radiation
            :math:`Q^{*}`
            [Wm-2]
        sf_soil : np.ndarray or float
            soil fraction
            :math:`s_f`
            [-]

        Returns
        -------
        rn_24_canopy : np.ndarray or float
            net radiation for the canopy
            :math:`Q^{*}_{canopy}`
            [Wm-2]

        Examples
        --------
        SolarRadiation.net_radiation_canopy(rn_24=200, sf_soil=0.4)
        120.0

        """
        return rn_24 * (1 - sf_soil)

    @staticmethod
    def net_radiation_soil(rn_24, sf_soil):
        """
        Computes the net radiation for the soil

         math ::
            Q^{*}_{soil} = s_f Q^{*}

        Parameters
        ----------
        rn_24 : np.ndarray or float
            net radiation
            :math:`Q^{*}`
            [Wm-2]
        sf_soil : np.ndarray or float
            soil fraction
            :math:`s_f`
            [-]

        Returns
        -------
        rn_24_soil : np.ndarray or float
            net radiation for the soil
            :math:`Q^{*}_{soil}`
            [Wm-2]

        Examples
        --------
        SolarRadiation.net_radiation_soil(rn_24=200, sf_soil=0.4)
        80.0
        """
        return rn_24 * sf_soil

    @staticmethod
    def net_radiation_grass(ra_24, l_net, r0_grass=0.23):
        r"""
        Computes the net radiation for reference grass

         math ::
            Q^{*} = \left[\left(1-\alpha_{0, grass}\right)S^{\downarrow}-L^{*}-I\right]

        Parameters
        ----------
        ra_24 : np.ndarray or float
            daily solar radiation
            :math:`S^{\downarrow}`
            [Wm-2]
        l_net : np.ndarray or float
            daily net longwave radiation
            :math:`L^{*}`
            [wm-2]
        r0_grass : np.ndarray or float
            albedo for reference grass
            :math:`\alpha_{0, grass}`
            [-]

        Returns
        -------
        rn_24_grass : np.ndarray or float
            daily net radiation for reference grass
            :math:`Q^{*}`
            [Wm-2]

        Examples
        --------
        SolarRadiation.net_radiation_grass(ra_24=123., l_net=24.)
        70.7
        """
        return (1 - r0_grass) * ra_24 - l_net

    @staticmethod
    def volumetric_heat_capacity(se_top=1.0, porosity=0.4):
        """
        Computes the volumetric heat capacity of the soil

        Parameters
        ----------
        se_top : np.ndarray or float
            effective saturation of the topsoil
            :math:`S_{e,top}`
            [-]
        porosity : np.ndarray or float
            porosity of the soil
            :math:`\phi`
            [-]

        Returns
        -------
        vhc : np.ndarray or float
            volumetric heat capacity
            :math:`\rho c_{p}`
            [J m-3 K-1]

        Examples
        --------
        SolarRadiationAnalysis.volumetric_heat_capacity(se_top=0.4, porosity = 0.5)
        23400000.0
        """
        return ((1 - porosity) ** 2 + 2.5 * porosity + 4.2 * porosity * se_top) * 10 ** 6

    @staticmethod
    def soil_thermal_conductivity(se_top):
        """
        Computes the soil thermal conductivity
        Parameters
        ----------
        se_top : np.ndarray or float
            effective saturation of the topsoil
            :math:`S_{e,top}`
            [-]

        Returns
        -------
        stc : np.ndarray or float
            soil thermal conductivity
            :math:`k`
            [W m-1 K-1]

        Examples
        --------
        SolarRadiationAnalysis.soil_thermal_conductivity(se_top=0.4)
        0.8900000000000001
        """
        return 0.15 + 1.85 * se_top

    @staticmethod
    def damping_depth(stc, vhc):
        """
        Computes the damping depth

        with the following constant

        * :math:`P` period (seconds within a year)

        Parameters
        ----------
        stc : np.ndarray or float
            soil thermal conductivity
            :math:`k`
            [W m-1 K-1]
        vhc : np.ndarray or float
            volumetric heat capacity
            :math:`\rho c_{p}`
            [J m-3 K-1]

        Returns
        -------
        dd : np.ndarray or float
            damping depth
            :math:`z_{d}`
            [m]

        Examples
        --------
        SolarRadiationAnalysis.damping_depth(stc=0.9, vhc=volumetric_heat_capacity())
        0.54514600029013294
        """
        day_sec = 86400.0  # seconds in a day
        year_sec = day_sec * 365  # seconds in a year
        return np.sqrt((2 * stc * year_sec) / (vhc * 2 * np.pi))

    # TODO north-south transition with regard to latitude
    @staticmethod
    def bare_soil_heat_flux(doy, dd, stc, t_amp_year, lat):
        r"""
        Computes the bare soil heat flux
        where the following constant is used

        * :math:`P` period (seconds within a year)

        The term :math:`-\frac{\pi}{4}` is a phase shift for northern latitudes.
        For southern latitudes the phase shift will be :math:`-\frac{\pi}{4}+\pi`

        Parameters
        ----------
        stc : np.ndarray or float
            soil thermal conductivity
            :math:`k`
            [W m-1 K-1]
        dd : np.ndarray or float
            damping depth
            :math:`z_{d}`
            [m]
        t_amp_year : np.ndarray or float
            yearly air temperature amplitude
            :math:`A_{t,year}`
            [m]
        doy : np.ndarray or float
            julian day of the year
            :math:`J`
            [-]
        lat : np.ndarray or float
            latitude
            :math:`\lambda`
            [rad]

        Returns
        -------
        g0_bs : np.ndarray or float
            bare soil heat flux
            :math:`G_{0}`
            [m]

        Examples
        --------
        stc = SolarRadiationAnalysis.soil_thermal_conductivity(se_top=1.0)
        vhc = SolarRadiationAnalysis.volumetric_heat_capacity(se_top=1.0)
        dd = SolarRadiationAnalysis.damping_depth(stc,vhc)
        rad.bare_soil_heat_flux(126, dd, stc, t_amp_year=13.4, lat=40*(math.pi/180.0))
        array([ 45.82350561])
        """

        phase = np.where(lat > 0, -np.pi / 4.0, -np.pi / 4.0 + np.pi)

        day_sec = 86400.0  # seconds in a day
        year_sec = day_sec * 365  # seconds in a year
        out = (np.sqrt(2.0) * t_amp_year * stc * np.sin(2 * np.pi / year_sec * doy * day_sec + phase)) / dd

        return out

    @staticmethod
    def soil_heat_flux(g0_bs, sf_soil, land_mask, rn_24_soil, trans_24, ra_24, l_net, rn_slope=0.92, rn_offset=-61.0):
        """
        Computes the soil heat flux
        Parameters
        ----------
        g0_bs : np.ndarray or float
            bare soil heat flux
            :math:`G_{0}`
            [W m-2]
        sf_soil : np.ndarray or float
            soil fraction
            :math:`s_f`
            [-]
        land_mask : np.ndarray or  int
            land use classification
            :math:`l`
            [-]
        rn_24_soil : np.ndarray or float
            net radiation for the soil
            :math:`Q^{*}_{soil}`
            [Wm-2]
        trans_24 : np.ndarray or float
            daily atmospheric transmissivity
            :math:`\tau`
            [-]
        rn_slope : np.ndarray or float
            slope rn/g0 relation water
            :math:`lws`
            [-]
        rn_offset : np.ndarray or float
            offset rn/g0 relation water
            :math:`lwo`
            [-]
        ra_24 : np.ndarray or float
            daily solar radiation
            :math:`S^{\downarrow}`
            [Wm-2]
        l_net : np.ndarray or float
            daily net longwave radiation
            :math:`L^{*}`
            [wm-2]

        Returns
        -------
        g0_24 : np.ndarray or float
            daily soil heat flux
            :math:`G`
            [W m-2]

        Examples
        --------
        SolarRadiationAnalysis.soil_heat_flux(g0_bs=12.4, sf_soil=0.4)
        4.960000000000001
        """

        def land_city_func(g0_bs, sf_soil):
            return g0_bs * sf_soil

        def water_func(ra_24, trans_24, l_net, rn_slope, rn_offset, rn_24_soil):
            rn_24_clear = 0.95 * ra_24 / trans_24 - l_net
            g0_24_clear = rn_24_clear * rn_slope + rn_offset
            g0_24_clear = np.minimum(g0_24_clear, 0.5 * rn_24_clear)

            # adjust water heat storage to current net radiation conditions
            g0_24 = g0_24_clear * rn_24_soil / rn_24_clear

            return g0_24

        g0 = np.zeros_like(land_mask)
        g0 = np.where(land_mask == 1, land_city_func(g0_bs, sf_soil), g0)
        g0 = np.where(land_mask == 2, water_func(ra_24, trans_24, l_net, rn_slope, rn_offset, rn_24_soil), g0)
        g0 = np.where(land_mask == 3, land_city_func(g0_bs, sf_soil), g0)

        return g0
