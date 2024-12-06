from math import log

import numpy as np


class ETAnalysis:
    @staticmethod
    def evaporative_fraction(et_24_mm, lh_24, rn_24, g0_24):
        """
        Computes the evaporative fraction.

        where the following constants are used

        * :math:`d_{sec}` seconds in the day = 86400 [s]

        Parameters
        ----------
        et_24_mm : np.ndarray or float
            daily actual evapotranspiration
            :math:`ET_{ref}`
            [mm]
        lh_24 : np.ndarray or float
            daily latent heat of evaporation
            :math:`\lambda_{24}`
            [J/kg]
        rn_24 : np.ndarray or float
            daily net radiation
            :math:`Q^{*}`
            [Wm-2]
        g0_24 : np.ndarray or float
            daily soil heat flux
            :math:`G`
            [W m-2]

        Returns
        -------
        ef_24 : np.ndarray or float
            evaporative fraction
            :math:`EF_{ref}`
            [-]
        """
        day_sec = 86400.0  # seconds in a day
        et_24 = et_24_mm * lh_24 / day_sec
        ef_24 = et_24 / (rn_24 - g0_24)

        return ef_24

    @staticmethod
    def interception_mm(P_24, vc, lai, int_max=0.2):
        r"""
        Computes the daily interception. The daily interception of a vegetated area
        is calculated according to von Hoyningen-Hüne (1983) [Ho1983]_
        and Braden(1985) [Br1985]_.

        math ::
            I^*=I_{max}*I_{lai}*\left(1-\left(\frac{1}{1+\frac{c_{veg}P24}
            {I_{max}I_{lai}}}\right)\right)

        Parameters
        ----------
        P_24 : np.ndarray or float
            daily rainfall
            :math:`P`
            [mm day :math:`^{-1}`]

        vc : np.ndarray or float
            vegetation cover
            :math:`c_{veg}`
            [-]

        lai : np.ndarray or float
            leaf area index
            :math:`I_{lai}`
            [-]

        int_max : np.ndarray or float
            maximum interception per leaf
            :math:`I_{max}`
            [mm day :math:`^{-1}`]

        Returns
        -------
        int_mm : np.ndarray or float
            interception
            :math:`I^*`
            [mm day :math:`^{-1}`]

        Examples
        --------


        References
        ----------
        .. [Br1985] Braden, H., Energiehaushalts- und Verdunstungsmodell für Wasser- und
            Stoffhaushalts-untersuchungen landwirtschaftlich genutzter
            Einzugsgebiete. Mitteilungen der Deutschen Bodenkundlichen
            Gesellschaft, (1985), 42, 254-299
        .. [Ho1983] von Hoyningen-Hüne, J., Die Interception des Niederschlags in
            landwirtschaftlichen Beständen. Schriftenreihe des DVWK, 1983, 57, 1-53


        """
        zero_mask = np.logical_or.reduce((lai == 0, vc == 0, P_24 == 0))

        res = int_max * lai * (1 - (1 / (1 + ((vc * P_24) / (int_max * lai)))))

        res[zero_mask] = 0

        return res

    @staticmethod
    def et_reference(rn_24_grass, ad_24, psy_24, vpd_24, ssvp_24, u_24):
        r"""
        Computes the reference evapotranspiration. The reference evapotranspiration
        :math:`ET_{ref}` is an important concept in irrigation science. The reference
        evapotranspiration can be inferred from routine meteorological
        measurements. The reference evapotranspiration is the evapotranspiration
        of grass under well watered conditions.
        First the aerodynamical resistance for grass :math:`r_{a1,grass}` [sm :math:`^{-1}`]
        is calculated

            math ::

            r_{a1,grass}=\frac{208}{u_{obs}}

        Then the reference evapotranspiration :math:`ET_{ref}` [W m :math:`^{-2}`] can be calculated
        as follows, with taking the default value for the grass surface resistance
        :math:`r_{grass}` = 70 sm :math:`^{-1}`

            math ::
            ET_{ref}=\frac{\Delta\left(Q_{grass}^{*}\right)+
            \rho c_{p}\frac{\Delta_{e}}{r_{a1,grass}}}
            {\Delta+\gamma\left(1+\frac{r_{grass}}{r_{a1,grass}}\right)}

        The soil heat flux is assumed to be zero or close to zero on a daily basis.

        Parameters
        ----------
        rn_24_grass : np.ndarray or float
            net radiation for reference grass surface
            :math:`Q^{*}_{grass}`
            [Wm-2]
        u_24 : np.ndarray or float
            daily wind speed at observation height
            :math:`u_{obs}`
            [m/s]
        ad_24 : np.ndarray or float
            daily air density
            :math:`\rho_{24}`
            [kg m-3]
        psy_24 : np.ndarray or float
            daily psychrometric constant
            :math:`\gamma_{24}`
            [mbar K-1]
        vpd_24 : np.ndarray or float
            daily vapour pressure deficit
            :math:`\Delta_{e,24}`
            [mbar]
        ssvp_24 : np.ndarray or float
            daily slope of saturated vapour pressure curve
            :math:`\Delta_{24}`
            [mbar K-1]

        Returns
        -------
        et_ref_24 : np.ndarray or float
            reference evapotranspiration (well watered grass) energy equivalent
            :math:`ET_{ref}`
            [W m-2]
        """
        r_grass = 70
        ra_grass = 208. / u_24
        sh = 1004.0  # specific heat J kg-1 K-1
        et_ref_24 = np.maximum(0, (ssvp_24 * rn_24_grass + ad_24 * sh * (vpd_24 / ra_grass)) / \
                               (ssvp_24 + psy_24 * (1 + r_grass / ra_grass)))
        return et_ref_24

    @staticmethod
    def et_reference_mm(et_ref_24, lh_24):
        """
        Computes the reference evapotranspiration.

         math ::

            ET_{ref}=ET_{ref}d_{sec}\lambda_{24}

        where the following constants are used

        * :math:`d_{sec}` seconds in the day = 86400 [s]

        Parameters
        ----------
        et_ref_24 : np.ndarray or float
            daily reference evapotranspiration energy equivalent
            :math:`ET_{ref}`
            [W m-2]
        lh_24 : np.ndarray or float
            daily latent heat of evaporation
            :math:`\lambda_{24}`
            [J/kg]

        Returns
        -------
        et_ref_24_mm : np.ndarray or float
            reference evapotranspiration (well watered grass)
            :math:`ET_{ref}`
            [mm d-1]
        """
        day_sec = 86400.0  # seconds in a day
        return et_ref_24 * day_sec / lh_24

    @staticmethod
    def et_actual_mm(e_24_mm, t_24_mm):
        """
        Computes the actual evapotranspiration based on the separate calculations
        of evaporation and transpiration:

          math ::
            ET = E + T

        Parameters
        ----------
        e_24_mm : np.ndarray or float
            daily evaporation in mm
            :math:`E`
            [mm d-1]
        t_24_mm : np.ndarray or float
            daily transpiration in mm
            :math:`T`
            [mm d-1]

        Returns
        -------
        et_24_mm : np.ndarray or float
            daily evapotranspiration in mm
            :math:`ET`
            [mm d-1]
        """
        return e_24_mm + t_24_mm

    @staticmethod
    def initial_sensible_heat_flux_soil_daily(rn_24_soil, e_24_init, g0_24):
        r"""
        Computes the initial sensible heat flux before the iteration which solves
        the stability corrections. The first estimation of transpiration is used
        to estimate the initial sensible heat flux.

         math ::

            H_{soil}=Q_{soil}^{*}-G_{0}-E

        Parameters
        ----------
        rn_24_soil : np.ndarray or float
            daily net radiation for the soil
            :math:`Q_{canopy}^{*}`
            [W m-2]
        g0_24 : np.ndarray or float
            daily soil heat flux
            :math:`G_{0}`
            [W m-2]
        e_24_init : np.ndarray or float
            initial estimate of daily evaporation
            :math:`E`
            [W m-2]

        Returns
        -------
        h_soil_24_init : np.ndarray or float
            initial estimate of the sensible heat flux
            :math:`H_{canopy}`
            [W m-2]
        """
        return rn_24_soil - g0_24 - e_24_init

    @staticmethod
    def initial_soil_aerodynamic_resistance(u_24, z_obs=2):
        r"""
        Computes the aerodynamic resistance for soil without stability corrections
        :math:`r_{a1,soil}^{0}`.

        math ::

            r_{a1,soil}^{0}=\frac{\ln\left(\frac{z_{obs}}{z_{0,soil}}\right)
                           \ln\left(\frac{z_{obs}}{0.1z_{0,soil}}\right)}
                           {k^{2}u_{obs}}


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
    def initial_daily_evaporation(rn_24_soil, g0_24, ssvp_24, ad_24, vpd_24,
                                  psy_24, r_soil, ra_soil_init):
        r"""
        Computes the soil evaporation based on the Penman Monteith equation
        adapted for soil.

        math ::

            E^{0}=\frac{\Delta\left(Q_{soil}^{*}-G\right)+\rho c_{p}
            \frac{\Delta_{e}}{r_{a1,soil}}}{\Delta+
            \gamma\left(1+\frac{r_{soil}}{r_{a1,soil}}\right)}

        where the following constants are used

        * :math:`c_{p}` specific heat for dry air = 1004 [J kg-1 K-1]
        * :math:`k` = karman constant = 0.41 [-]

        Parameters
        ----------
        rn_24_soil : np.ndarray or float
            daily net radiation for soil
            :math:`Q_{soil}^{*}`
            [W m-2]
        g0_24 : np.ndarray or float
            daily soil heat flux
            :math:`G`
            [W m-2]
        ssvp_24 : np.ndarray or float
           daily slope of saturated vapour pressure curve
           :math:`\Delta`
           [mbar K-1]
        ad_24 : np.ndarray or float
            daily air density
            :math:`\rho`
            [kg m-3]
        vpd_24 : np.ndarray or float
            daily vapour pressure deficit
            :math:`\Delta_{e}`
            [mbar]
        psy_24 : np.ndarray or float
            daily psychrometric constant
            :math:`\gamma`
            [mbar K-1]
        r_soil : np.ndarray or float
            soil resistance
            :math:`r_{soil}`
            [m s-1]
        ra_soil_init : np.ndarray or float
            initial soil aerodynamic resistance
            :math:`r_{a1,soil}`
            [m s-1]

        Returns
        -------
        e_24_init : np.ndarray or float
            initial estimate radiation equivalent daily evaporation
            :math:`E^{0}`
            [W m-2]

        """
        sh = 1004.0  # specific heat J kg-1 K-1
        numerator = (ssvp_24 * (rn_24_soil - g0_24) +
                     ad_24 * sh * (vpd_24 / ra_soil_init))
        denominator = (ssvp_24 + psy_24 * (1 + r_soil / ra_soil_init))
        return numerator / denominator

    @staticmethod
    def initial_daily_evaporation_mm(e_24_init, lh_24):
        r"""
        Computes the soil evaporation based on the Penman Monteith equation
        adapted for soil.

         math ::

            E^{0}=E^{0}d_{sec}\lambda_{24}

        where the following constants are used

        * :math:`d_{sec}` seconds in the day = 86400 [s]

        Parameters
        ----------
        e_24_init : np.ndarray or float
            initial estimate daily evaporation
            :math:`E^{0}`
            [W m-2]
        lh_24 : np.ndarray or float
            daily latent heat of evaporation
            :math:`\lambda_{24}`
            [J/kg]

        Returns
        -------
        e_24_init_mm : np.ndarray or float
            initial estimate daily evaporation in mm
            :math:`E^{0}`
            [mm d-1]
        """
        day_sec = 86400.0  # seconds in a day
        return e_24_init * day_sec / lh_24

    @staticmethod
    def initial_canopy_aerodynamic_resistance(u_24, z0m, z_obs=2):
        r"""
        Computes the aerodynamic resistance for a canopy soil without stability
        corrections :math:`r_{a1,}^{0}`.

         math ::

            r_{a1,canopy}^{0}=\frac{\ln\left(\frac{z_{obs}}{z_{0,m}}\right)\ln
            \left(\frac{z_{obs}}{0.1z_{0,m}}\right)}{k^{2}u_{obs}}

        where the following constants are used

        * :math:`k` = karman constant = 0.41 [-]

        The factor 0.1 is the ratio between the surface roughness for momentum and
        heat.

        Parameters
        ----------
        u_24 : np.ndarray or float
            daily wind speed at observation height
            :math:`u_obs`
            [m/s]
        z0m : np.ndarray or float
            roughness length
            :math:`z_{0,m}`
            [m]
        z_obs : np.ndarray or float
            observation height
            :math:`z_{obs}`
            [m]

        Returns
        -------
        ra_canopy_init : np.ndarray or float
            canopy resistance without stability corrections
            :math:`r_{a1,canopy}^{0}`
            [s/m]
        """
        k = 0.41  # karman constant (-)
        return (log(z_obs / z0m) * log(z_obs / (0.1 * z0m))) / (k ** 2 * u_24)

    @staticmethod
    def initial_daily_transpiration(rn_24_canopy, ssvp_24, ad_24, vpd_24,
                                    psy_24, r_canopy, ra_canopy_init):
        r"""
        Computes the soil evaporation based on the Penman Monteith equation adapted
        for soil.

        math ::

            T_{0}=\frac{\Delta\left(Q_{canopy}^{*}\right)
            +\rho c_{p}\frac{\Delta_{e}}
            {r_{a`,canopy}}}{\Delta+
            \gamma\left(1+\frac{r_{canopy}}{r_{a`,canopy}}\right)}

        where the following constants are used

        * :math:`c_{p}` specific heat for dry air = 1004 [J kg-1 K-1]
        * :math:`k` = karman constant = 0.41 [-]

        Parameters
        ----------
        rn_24_canopy : np.ndarray or float
            daily net radiation for the canopy
            :math:`Q_{soil}^{*}`
            [W m-2]
        ssvp_24 : np.ndarray or float
           daily slope of saturated vapour pressure curve
           :math:`\Delta`
           [mbar K-1]
        ad_24 : np.ndarray or float
            daily air density
            :math:`\rho`
            [kg m-3]
        vpd_24 : np.ndarray or float
            daily vapour pressure deficit
            :math:`\Delta_{e}`
            [mbar]
        psy_24 : np.ndarray or float
            daily psychrometric constant
            :math:`\gamma`
            [mbar K-1]
        r_canopy : np.ndarray or float
            canopy resistance
            :math:`r_{canopy}`
            [m s-1]
        ra_canopy_init : np.ndarray or float
            initial canopy aerodynamic resistance
            :math:`r_{a1,canopy}`
            [m s-1]

        Returns
        -------
        t_24_init : np.ndarray or float
            initial estimate radiation equivalent daily transpiration
            :math:`T^{0}`
            [W m-2]
        """
        sh = 1004.0  # specific heat J kg-1 K-1
        numerator = (ssvp_24 * rn_24_canopy + ad_24 *
                     sh * (vpd_24 / ra_canopy_init))
        denominator = (ssvp_24 + psy_24 * (1 + r_canopy / ra_canopy_init))
        return numerator / denominator

    @staticmethod
    def initial_daily_transpiration_mm(t_24_init, lh_24):
        r"""
        Computes the canopy transpiration based on the Penman Monteith equation
        adapted for canopy.

         math ::

            T^{0}=T^{0}d_{sec}\lambda_{24}

        where the following constants are used

        * :math:`d_{sec}` seconds in the day = 86400 [s]

        Parameters
        ----------
        t_24_init : np.ndarray or float
            initial estimate daily transpiration
            :math:`E^{0}`
            [W m-2]
        lh_24 : np.ndarray or float
            daily latent heat of evaporation
            :math:`\lambda_{24}`
            [J/kg]

        Returns
        -------
        t_24_init_mm : np.ndarray or float
            initial estimate daily transpiration in mm
            :math:`T^{0}`
            [mm d-1]
        """
        day_sec = 86400.0  # seconds in a day
        return t_24_init * day_sec / lh_24

    @staticmethod
    def epsilon_autotrophic_respiration():
        """
        Computes the epsilon autotrophic respiration

        Returns
        -------
        eps_a : np.ndarray or float
            epsilon autotrophic respiration
            :math:`I`
            [-]
        """

        eps_a = 1 - 0.23  # 23% of GPP

        return eps_a
