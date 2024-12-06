"""
    The soil_moisture module contains all functions related to soil moisture data components.

"""
import numpy as np

from digitalarztools.raster.analysis.unstable import Unstable


class SoilMoistureAnalysis:
    @classmethod
    def wet_bulb_temperature_inst(cls, t_air_i, t_dew_i, p_air_i):
        r"""
        Computes the instantaneous wet bulb temperature.

        Parameters
        ----------
        t_air_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a}`
            [C]
        t_dew_i : np.ndarray or float
            instantaneous dew point temperature
            :math:`Td_{a}`
            [C]

        Returns
        -------
        t_wet_i : np.ndarray or float
            instantaneous wet bulb temperature
            :math:`Tw_{a}`
            [C]
        """
        tw = cls.wetbulb_temperature_iter(t_air_i, t_dew_i, p_air_i)

        return tw

    @staticmethod
    def wet_bulb_temperature_inst_new(t_air_i, qv_i, p_air_i):
        r"""
        Computes the instantaneous wet bulb temperature.

        Parameters
        ----------
        t_air_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a}`
            [C]
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
        t_wet_i : np.ndarray or float
            instantaneous wet bulb temperature
            :math:`Tw_{a}`
            [C]
        """
        es_i = 0.6108 * np.exp((17.27 * t_air_i) / (t_air_i + 237.3))
        rh_i = np.minimum((1.6077717 * qv_i / 10 * p_air_i / es_i), 1) * 100
        rh_i = rh_i.clip(0, 100)

        tw = t_air_i * np.arctan(0.152 * (rh_i + 8.3136) ** (1 / 2)) + np.arctan(t_air_i + rh_i) - np.arctan(rh_i - 1.6763) + 0.00391838 * rh_i ** (3 / 2) * np.arctan(0.0231 * rh_i) - 4.686

        return tw

    @staticmethod
    def wet_bulb_temperature_inst_new2(t_air_i):
        r"""
        Computes the instantaneous wet bulb temperature.

        Parameters
        ----------
        t_air_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a}`
            [C]

        Returns
        -------
        t_wet_i : np.ndarray or float
            instantaneous wet bulb temperature
            :math:`Tw_{a}`
            [C]
        """

        temp_tw = (17.27 * t_air_i) / (237.3 + t_air_i)
        tw = 1.0919 * temp_tw ** 2 + 13.306 * temp_tw + 0.1304

        return tw

    @staticmethod
    def dew_point_temperature_inst(vp_i):
        r"""
        Computes the instantaneous dew point temperature.

        Parameters
        ----------
        vp_i : np.ndarray or float
            instantaneous vapour pressure
            :math:`e_{a}`
            [mbar]

        Returns
        -------
        t_dew_i : np.ndarray or float
            instantaneous dew point temperature
            :math:`Td_{a}`
            [K]
        """
        t_dew_i = (237.3 * np.log(vp_i / 6.108)) / (17.27 - np.log(vp_i / 6.108))

        return t_dew_i

    @staticmethod
    def dew_point_temperature_coarse_inst(vp_i):
        r"""
        Computes the instantaneous dew point temperature.

        Parameters
        ----------
        vp_i : np.ndarray or float
            instantaneous vapour pressure
            :math:`e_{a}`
            [mbar]

        Returns
        -------
        t_dew_coarse_i : np.ndarray or float
            instantaneous dew point temperature
            :math:`Td_{a}`
            [K]
        """
        t_dew_i = (237.3 * np.log(vp_i / 6.108)) / (17.27 - np.log(vp_i / 6.108))

        return t_dew_i

    # only used internally
    @staticmethod
    def latent_heat_iter(t):
        # temperature in celcius
        lv = 1000 * (2501 - 2.361 * t)

        return lv

    # only used internally
    @staticmethod
    def psychometric_constant_iter(lv, p=1013.25, cp=1004, rm=0.622):
        # lv: latent heat of vaporization (J/s?)
        # p:  pressure in hPa
        # cp: specific heat
        # rm: ratio of molecular weight

        psy = (cp * p) / (lv * rm)

        return psy

    # only used internally
    @staticmethod
    def vapor_pressure_iter(t):
        # t: temperature in Celcius

        vp = 6.108 * np.exp((17.27 * t) / (237.3 + t))

        return vp

    # only used internally
    @classmethod
    def wetbulb_temperature_iter(cls, ta, td, pressure):
        maxiter = 1000
        tol = 1e-7
        # pressure = 1013.25

        lv = cls.latent_heat_iter(ta)
        psy = cls.psychometric_constant_iter(lv, p=pressure)

        tw = td + ((ta - td) / 3)
        ea_ta = cls.vapor_pressure_iter(td)

        n = 0

        prev_dir = np.zeros_like(ta)
        step = (ta - td) / 5.

        while abs(np.nanmax(step)) > tol:

            ea_tw = cls.vapor_pressure_iter(tw) - psy * (ta - tw)

            direction = (-1) ** ((ea_tw - ea_ta) > 0)

            step = np.where(prev_dir != direction, step * 0.5, step)

            tw += step * direction
            prev_dir = direction

            n += 1
            if n >= maxiter:
                return tw

        return tw

    # some internal functions for the stability correction based on Brutsaert
    @staticmethod
    def psi_m(y):
        r"""
        Computes the stability correction for momentum based on
        Brutsaert (1999) [2]_.

         math ::
            \Psi_{M}(y)=\ln(a+y)-3by^{\frac{1}{3}}+ \\
            \frac{ba^{\frac{1}{3}}}{2}\ln[\frac{(1+x)^{2}}{(1-x+x^{2})}]+\\
            \sqrt{3}ba^{\frac{1}{3}}\arctan[\frac{(2x-1)}{\sqrt{3}}]+\Psi_{0}

        where the following constants are used

        * :math:`a` = 0.33
        * :math:`b` = 0.41

        in which

         math ::
            x = (\frac{y}{a})^{\frac{1}{3}}

        and

         math ::
            y = \frac{-(z-d)}{L}

        where :math:`L` is the monin obukhov length defined by
        :func:`ETLook.unstable.monin_obukhov_length`,
        :math:`z` and :math:`d` are the
        measurement height and displacement height respectively. All aforementioned
        parameters are different for the bare soil and full canopy solutions.

        The symbol :math:`\Psi_{0}` denotes a constant of integration, given by

         math ::
           \Psi_{0}=-\ln{a}+\sqrt{3}ba^{\frac{1}{3}}\frac{\pi}{6}

         plot:: pyplots/soil_moisture/plot_psi_m.py

        Notes
        -----
        This function should not be used as an input function for a ETLook tool.
        This function is used internally by :func:`aerodynamical_resistance_bare`
        and :func:`aerodynamical_resistance_full` and :func:`wind_speed_soil`.

        References
        ----------
         [2] Brutsaert, W., Aspect of bulk atmospheric boundary layer similarity
            under free-convective conditions,
            Reviews of Geophysics, 1999, 37(4), 439-451.
        """
        a = 0.33
        b = 0.41
        x = (y / a) ** (1. / 3.)
        phi_0 = -np.log(a) + np.sqrt(3) * b * a ** (1. / 3.) * np.pi / 6.
        res = (
                np.log(a + y)
                - 3 * b * y ** (1. / 3.)
                + (b * a ** (1. / 3.)) / 2. * np.log((1 + x) ** 2 / (1 - x + x ** 2))
                + np.sqrt(3) * b * a ** (1. / 3.) * np.arctan((2 * x - 1) / np.sqrt(3))
                + phi_0
        )
        return res

    @staticmethod
    def psi_h(y):
        r"""
        Computes the stability correction for momentum based on
        Brutsaert (1999) [2]_.

         math ::
            \Psi_{H}(y)=[\frac{(1-d)}{n}]\ln{\frac{(c+y^n)}{c}}

        where the following constants are used

        * :math:`c` = 1.00
        * :math:`d` = 0.057
        * :math:`n` = 0.78

        in which

         math ::
            y = \frac{-(z-d)}{L}

        where :math:`L` is the monin obukhov length defined by
        :func:`ETLook.unstable.monin_obukhov_length`,
        :math:`z` and :math:`d` are the
        measurement height and displacement height respectively. All aforementioned
        parameters are different for the bare soil and full canopy solutions.

         plot:: pyplots/soil_moisture/plot_psi_h.py

        Notes
        -----
        This function should not be used as an input function for a tool.
        This function is used internally by :func:`aerodynamical_resistance_bare`
        and :func:`aerodynamical_resistance_full` and :func:`wind_speed_soil`.

        References
        ----------
         [2] Brutsaert, W., Aspect of bulk atmospheric boundary layer similarity
            under free-convective conditions,
            Reviews of Geophysics, 1999, 37(4), 439-451.
        """
        c = 0.33
        d = 0.057
        n = 0.78
        return ((1 - d) / n) * np.log((c + y ** n) / c)

    @staticmethod
    def initial_friction_velocity_inst(u_b_i, z0m, disp, z_b=100):
        r"""
        Computes the initial instantaneous friction velocity without stability
        corrections.

         math ::
            u_{*}=\frac{ku_{b}}{\ln\left(\frac{z_{b}-d}{z_{0,m}}\right)}

        Parameters
        ----------
        u_b_i : np.ndarray or float
            instantaneous wind speed at blending height
            :math:`u_{b}`
            [m s-1]
        z0m : np.ndarray or float
            surface roughness
            :math:`z_{0,m}`
            [m]
        disp : np.ndarray or float
            displacement height
            :math:`d`
            [m]
        z_b : np.ndarray or float
            blending height
            :math:`z_{b}`
            [m]


        Returns
        -------
        u_star_i_init : np.ndarray or float
            initial estimate of the instantaneous friction velocity
            :math:`u_{*,i}`
            [m s-1]
        """
        k = 0.41  # karman constant (-)
        return (k * u_b_i) / (np.log((z_b - disp) / z0m))

    @staticmethod
    def atmospheric_emissivity_inst(vp_i, t_air_k_i):
        r"""
        Computes the atmospheric emissivity according to Brutsaert [1]_.

         math ::
            \varepsilon_{a}=a\left(\frac{e_{a}}{T_{a}}\right)^{b}

        where the following constants are used

        * :math:`a` = 1.24
        * :math:`b` = 1/7

        Parameters
        ----------
        vp_i : np.ndarray or float
            instantaneous vapour pressure
            :math:`e_{a}`
            [mbar]
        t_air_k_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a}`
            [K]

        Returns
        -------
        emiss_atm_i : np.ndarray or float
            instantaneous atmospheric emissivity
            :math:`\varepsilon_{a}`
            [-]

        References
        ----------
         [1] Brutsaert, W., On a derivable formula for long-wave radiation
            from clear skies, Water Resour. Res, 1975, 11, 742-744.
        """
        return 1.24 * (vp_i / t_air_k_i) ** (1. / 7.)

    @staticmethod
    def net_radiation_bare(ra_hor_clear_i, emiss_atm_i, t_air_k_i, lst, r0_bare=0.38):
        r"""
        Computes the net radiation for the bare soil with zero evaporation

         math ::

            Q_{bare}^{*}=\left(1-\alpha_{0,bare}\right)S_{d}+\varepsilon_{s}\varepsilon_{a}\sigma T_{a}^{4}-\varepsilon_{s}\sigma T_{s}^{4}

        Parameters
        ----------
        ra_hor_clear_i : np.ndarray or float
            Total clear-sky irradiance on a horizontal surface
            :math:`S_{d}`
            [W/m2]
        emiss_atm_i : np.ndarray or float
            instantaneous atmospheric emissivity
            :math:`\varepsilon_{a}`
            [-]
        t_air_k_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a}`
            [K]
        lst : np.ndarray or float
            surface temperature
            :math:`T_{0}`
            [K]
        r0_bare : np.ndarray or float
            dry bare soil surface albedo
            :math:`\alpha_{0, bare}`
            [-]


        Returns
        -------
        rn_bare : np.ndarray or float
            net radiation bare soil
            :math:`Q^*_{bare}`
            [Wm-2]
        """
        emiss_bare = 0.95
        sb = 5.67e-8  # stefan boltzmann constant
        rn_bare = (
                (1 - r0_bare) * ra_hor_clear_i
                + emiss_atm_i * emiss_bare * sb * t_air_k_i ** 4
                - emiss_bare * sb * lst ** 4
        )

        return rn_bare

    @staticmethod
    def net_radiation_full(ra_hor_clear_i, emiss_atm_i, t_air_k_i, lst, r0_full=0.18):
        r"""
        Computes the net radiation at full canopy with zero evaporation

         math ::

            Q_{full}^{*}=\left(1-\alpha_{0,full}\right)S_{d}+\varepsilon_{c}\varepsilon_{a}\sigma T_{a}^{4}-\varepsilon_{c}\sigma T_{s}^{4}

        Parameters
        ----------
        ra_hor_clear_i : np.ndarray or float
            Total clear-sky irradiance on a horizontal surface
            :math:`ra_hor_clear_i`
            [W/m2]
        emiss_atm_i : np.ndarray or float
            instantaneous atmospheric emissivity
            :math:`P`
            [-]
        t_air_k_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a}`
            [K]
        lst : np.ndarray or float
            surface temperature
            :math:`T_{0}`
            [K]
        r0_full : np.ndarray or float
            surface albedo full vegetation
            :math:`\alpha_{0, full}`
            [-]

        Returns
        -------
        rn_full : np.ndarray or float
            net radiation full vegetation
            :math:`Q^*_{full}`
            [Wm-2]
        """
        emiss_full = 0.99
        sb = 5.67e-8  # stefan boltzmann constant
        rn_full = (
                (1 - r0_full) * ra_hor_clear_i
                + emiss_atm_i * emiss_full * sb * t_air_k_i ** 4
                - emiss_full * sb * lst ** 4
        )

        return rn_full

    @staticmethod
    def sensible_heat_flux_bare(rn_bare, fraction_h_bare=0.65):
        r"""
        Computes the bare soil sensible heat flux

         math ::

            H_{bare} = H_{f, bare}Q^*_{bare}

        Parameters
        ----------
        rn_bare : np.ndarray or float
            net radiation bare soil
            :math:`Q^*_{bare}`
            [Wm-2]
        fraction_h_bare : np.ndarray or float
            fraction of H of net radiation bare soil
            :math:`H_{f, bare}`
            [-]

        Returns
        -------
        h_bare : np.ndarray or float
            sensible heat flux bare soil
            :math:`H_{bare}`
            [Wm-2]
         """
        return rn_bare * fraction_h_bare

    @staticmethod
    def sensible_heat_flux_full(rn_full, fraction_h_full=0.95):
        r"""
        Computes the full canopy sensible heat flux

         math ::

            H_{full} = H_{f, full}Q^*_{full}

        Parameters
        ----------
        rn_full : np.ndarray or float
            net radiation full vegetation
            :math:`Q^*_{full}`
            [Wm-2]
        fraction_h_full : np.ndarray or float
            fraction of H of net radiation full vegetation
            :math:`H_{f, full}`
            [-]

        Returns
        -------
        h_full : np.ndarray or float
            sensible heat flux full vegetation
            :math:`H_{full}`
            [Wm-2]
         """
        return rn_full * fraction_h_full

    @staticmethod
    def wind_speed_blending_height_bare(u_i, z0m_bare=0.001, z_obs=10, z_b=100):
        r"""
        Computes the wind speed at blending height :math:`u_{b}` [m/s] using the
        logarithmic wind profile

         math ::
            u_{b}=\frac{u_{obs}\ln\left(\frac{z_{b}}{z_{0,m}}\right)}
            {\ln\left(\frac{z_{obs}}{z_{0,m}}\right)}

        Parameters
        ----------
        u_i : np.ndarray or float
            instantaneous wind speed at observation height
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
        z0m_bare : np.ndarray or float
            surface roughness bare soil
            :math:`z_{0,m}`
            m

        Returns
        -------
        u_b_i_bare : np.ndarray or float
            instantaneous wind speed at blending height for bare soil
            :math:`u_{b,i,bare}`
            [m/s]
        """
        k = 0.41  # karman constant (-)
        ws = (k * u_i) / np.log(z_obs / z0m_bare) * np.log(z_b / z0m_bare) / k

        ws = np.clip(ws, 1, 150)

        return ws

    @staticmethod
    def wind_speed_blending_height_full_inst(u_i, z0m_full=0.1, z_obs=10, z_b=100):
        r"""
        Computes the wind speed at blending height :math:`u_{b}` [m/s] using the
        logarithmic wind profile

         math ::
            u_{b}=\frac{u_{obs}\ln\left(\frac{z_{b}}{z_{0,m}}\right)}
            {\ln\left(\frac{z_{obs}}{z_{0,m}}\right)}

        Parameters
        ----------
        u_i : np.ndarray or float
            instantaneous wind speed at observation height
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
        z0m_full : np.ndarray or float
            surface roughness vegetation
            :math:`z_{0,m}`
            [m]

        Returns
        -------
        u_b_i_full : np.ndarray or float
            instantaneous wind speed at blending height for full vegetation
            :math:`u_{b,i,full}`
            [m s-1]
        """
        k = 0.41  # karman constant (-)
        ws = (k * u_i) / np.log(z_obs / z0m_full) * np.log(z_b / z0m_full) / k

        ws = np.clip(ws, 1, 150)

        return ws

    @classmethod
    def friction_velocity_full_inst(cls, u_b_i_full, z0m_full=0.1, disp_full=0.667, z_b=100):
        r"""
        Like :func:`initial_friction_velocity_inst` but with full vegetation parameters

        Parameters
        ----------
        u_b_i_full : np.ndarray or float
            instantaneous wind speed blending height for full vegetation
            :math:`u_{b,d}`
            [m s-1]
        z0m_full : np.ndarray or float
            surface roughness vegetation
            :math:`z_{0,m,b}`
            [m]
        disp_full : np.ndarray or float
            displacement height vegetation
            :math:`d^{b}`
            [m]
        z_b : np.ndarray or float
            blending height
            :math:`z_b`
            [m]

        Returns
        -------
        u_star_i_full : np.ndarray or float
            instantaneous friction velocity vegetation
            :math:`u_{f}^{*}`
            [m s-1]

        """
        return cls.initial_friction_velocity_inst(u_b_i_full, z0m_full, disp_full, z_b=100)

    @classmethod
    def friction_velocity_bare_inst(cls, u_b_i_bare, z0m_bare=0.001, disp_bare=0.0, z_b=100):
        r"""
        Like :func:`initial_friction_velocity_inst` but with bare soil parameters

        Parameters
        ----------
        u_b_i_bare : np.ndarray or float
            instantaneous wind speed blending height bare soil
            :math:`u_{b,d}`
            [W m-2]
        z0m_bare : np.ndarray or float
            surface roughness bare soil
            :math:`z_{0,m,b}`
            [m]
        disp_bare : np.ndarray or float
            displacement height bare soil
            :math:`d^{b}`
            [m]
        z_b : np.ndarray or float
            blending height
            :math:`z_b`
            [m]

        Returns
        -------
        u_star_i_bare : np.ndarray or float
            instantaneous friction velocity bare soil
            :math:`u_{b}^{*}`
            [m s-1]

        """
        return cls.initial_friction_velocity_inst(u_b_i_bare, z0m_bare, disp_bare, z_b=100)

    @staticmethod
    def monin_obukhov_length_bare(h_bare, ad_i, u_star_i_bare, t_air_k_i):
        r"""
        Like :func:`unstable.monin_obukhov_length` but with bare soil parameters

        Parameters
        ----------
        h_bare : np.ndarray or float
            sensible heat flux for dry bare soil
            :math:`H_{b,d}`
            [W m-2]
        ad_i : np.ndarray or float
            instantaneous air density
            :math:`\rho`
            [k g m-3]
        u_star_i_bare : np.ndarray or float
            instantaneous friction velocity bare soil
            :math:`u^{*}_{b}`
            [m s-1]
        t_air_k_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a}`
            [K]

        Returns
        -------
        L_bare : np.ndarray or float
            monin obukhov length dry vegetation
            :math:`L_{b,d}`
            [m]

        """
        return Unstable.monin_obukhov_length(h_bare, ad_i, u_star_i_bare, t_air_k_i)

    @staticmethod
    def monin_obukhov_length_full(h_full, ad_i, u_star_i_full, t_air_k_i):
        r"""
        Like :func:`unstable.monin_obukhov_length` but with full canopy parameters

        Parameters
        ----------
        h_full : np.ndarray or float
            sensible heat flux for dry full vegetation
            :math:`H_{f,d}`
            [W m-2]
        ad_i : np.ndarray or float
            instantaneous air density
            :math:`\rho`
            [k g m-3]
        u_star_i_full : np.ndarray or float
            instantaneous friction velocity vegetation
            :math:`u^{*}_{b}`
            [m s-1]
        t_air_k_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a}`
            [K]

        Returns
        -------
        L_full : np.ndarray or float
            monin obukhov length dry vegetation
            :math:`L_{f,d}`
            [m]

        """
        return Unstable.monin_obukhov_length(h_full, ad_i, u_star_i_full, t_air_k_i)

    @classmethod
    def aerodynamical_resistance_full(cls, u_i, L_full, z0m_full=0.1, disp_full=0.667, z_obs=10):
        r"""
        Computes the aerodynamical resistance for a full canopy.

         math ::
            z_{1} = \frac{z_{obs}-d}{z_{0,m}}

            z_{2} = \frac{z_{obs}-d}{L}

            z_{3} = \frac{z_{0,m}}{L}

            z_{4} = \frac{z_{obs}-d}{\frac{z_{0,m}}{7}}

            z_{5} = \frac{\frac{z_{0,m}}{7}}{L}

            r_{a1,c}=\frac{(\ln(z_{1})-\phi_{m}(-z_{2})+\phi_{m}(-z_{3}))(\ln(z_{4})-\phi_{h}(-z_{2})+\phi_{h}(-z_{5}))}{k^{2}u}

        Parameters
        ----------
        u_i : np.ndarray or float
            instantaneous wind speed at observation height
            :math:`u_{obs}`
            [m/s]
        z_obs : np.ndarray or float
            observation height of wind speed
            :math:`z_{obs}`
            [m]
        disp_full : np.ndarray or float
            displacement height
            :math:`d`
            [m]
        z0m_full : np.ndarray or float
            surface roughness
            :math:`z_{0,m}`
            [m]
        L_full : np.ndarray or float
            monin obukhov length
            :math:`L`
            [m]

        Returns
        -------
        rac : np.ndarray or float
            aerodynamical resistance canopy
            :math:`r_{a1,c}`
            [sm-1]

        """
        z1 = (z_obs - disp_full) / z0m_full
        z2 = (z_obs - disp_full) / L_full
        z3 = z0m_full / L_full
        z4 = (z_obs - disp_full) / (z0m_full / 7)
        z5 = (z0m_full / 7) / L_full

        k = 0.41  # karman constant (-)
        res_stable = (np.log(z_obs / z0m_full) - -5 * z_obs / L_full + -5 * z0m_full / L_full) / (k * u_i)
        res_unstable = ((np.log(z1) - cls.psi_m(-z2) + cls.psi_m(-z3)) * (np.log(z4) - cls.psi_h(-z2) + cls.psi_h(-z5))) / (k ** 2 * u_i)

        res = np.where(L_full > 0, np.nan, res_unstable)
        res = res.clip(5, 400)

        return res

    @classmethod
    def aerodynamical_resistance_bare(cls, u_i, L_bare, z0m_bare=0.001, disp_bare=0.0, z_obs=10):
        r"""
        Computes the aerodynamical resistance for a dry bare soil.

         math ::
            z_{1} = \frac{z_{obs}-d}{z_{0,b,m}}

            z_{2} = \frac{z_{obs}-d}{L_{b}}

            r_{a1,a}=\frac{(\ln(z_{1})-\phi_{m}(-z_{2}))(\ln(z_{1})-\phi_{h}(-z_{2}))}{k^{2}u}

        Parameters
        ----------
        u_i : np.ndarray or float
            instantaneous wind speed at observation height
            :math:`u_{obs}`
            [m/s]
        z_obs : np.ndarray or float
            observation height of wind speed
            :math:`z_{obs}`
            [m]
        disp_bare : np.ndarray or float
            displacement height
            :math:`d`
            [m]
        z0m_bare : np.ndarray or float
            surface roughness
            :math:`z_{0,b,m}`
            [m]
        L_bare : np.ndarray or float
            monin obukhov length
            :math:`L_{b}`
            [m]

        Returns
        -------
        raa : np.ndarray or float
            aerodynamical resistance dry surface
            :math:`r_{a1,a}`
            [sm-1]

        """

        z1 = (z_obs - disp_bare) / z0m_bare
        z2 = (z_obs - disp_bare) / L_bare
        k = 0.41  # karman constant (-)
        res_stable = (np.log(z_obs / z0m_bare) - -5 * z_obs / L_bare + -5 * z0m_bare / L_bare) / (k * u_i)
        res_unstable = ((np.log(z1) - cls.psi_m(-z2)) * (np.log(z1) - cls.psi_h(-z2))) / (k ** 2 * u_i)

        res = np.where(L_bare > 0, np.nan, res_unstable)
        res = res.clip(5, 400)

        return res

    @classmethod
    def wind_speed_soil_inst(cls, u_i, L_bare, z_obs=10):
        r"""
        Computes the instantaneous wind speed at soil surface

         math ::

            u_{i,s}=u_{obs}\frac{\ln\left(\frac{z_{obs}}{z_{0}}\right)}
                  {\ln\left(\frac{z_{obs}}{z_{0,s}}\right)-\psi_{m}\left(\frac{-z_{0}}{L}\right)}

        Parameters
        ----------
        u_i : np.ndarray or float
            wind speed at observation height
            :math:`u_{obs}`
            [m/s]
        z_obs : np.ndarray or float
            observation height of wind speed
            :math:`z_{obs}`
            [m]
        L_bare : np.ndarray or float
            monin obukhov length
            :math:`L`
            [m]

        Returns
        -------
        u_i_soil : np.ndarray or float
            instantaneous wind speed just above soil surface
            :math:`u_{i,s}`
            [ms-1]

        """
        z0_soil = 0.01
        z0_free = 0.1
        k = 0.41  # karman constant (-)
        res_stable = (np.log(z_obs / z0_free) - -5 * z_obs / L_bare + -5 * z0_free / L_bare) / (k * u_i)
        res_unstable = u_i * ((np.log(z0_free / z0_soil)) / (np.log(z_obs / z0_soil) - cls.psi_m(-z0_free / L_bare)))

        res = np.where(L_bare > 0, np.nan, res_unstable)
        res = res.clip(5, 400)

        return (res)

    @staticmethod
    def aerodynamical_resistance_soil(u_i_soil):
        r"""
        Computes the aerodynamical resistance of the soil

         math ::
            r_{a1,s}=\frac{1}{\left(0.0025T_{dif}^{\frac{1}{3}}+0.012u_{i,s}\right)}

        Parameters
        ----------
        u_i_soil : np.ndarray or float
            instantaneous wind speed just above soil surface
            :math:`u_{i,s}`
            [m s-1]

        Returns
        -------
        ras : np.ndarray or float
            aerodynamical resistance
            :math:`r_{a1,s}`
            [sm-1]

        """
        Tdif = 10.0
        return 1. / (0.0025 * (Tdif) ** (1. / 3.) + 0.012 * u_i_soil)

    @staticmethod
    def maximum_temperature_full(
            ra_hor_clear_i, emiss_atm_i, t_air_k_i, ad_i, rac, r0_full
    ):
        r"""
        Computes the maximum temperature under fully vegetated conditions

         math ::

            T_{c,max}=\frac{\left(1-\alpha_{c}\right)S_{d}+\varepsilon_{c}\varepsilon_{a}\sigma
                      T_{a}^{4}-\varepsilon_{c}\sigma T_{a}^{4}}{4\varepsilon_{s}\sigma
                      T_{a}^{3}+\rho C_{p}/r_{a1,c}}+T_{a}

        Parameters
        ----------
        ra_hor_clear_i : np.ndarray or float
            Total clear-sky irradiance on a horizontal surface
            :math:`ra_hor_clear_i`
            [W/m2]
        emiss_atm_i : np.ndarray or float
            instantaneous atmospheric emissivity
            :math:`P`
            [-]
        t_air_k_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a}`
            [K]
        rac : np.ndarray or float
            aerodynamic resistance canopy
            :math:`r_{a1,c}`
            [sm-1]
        ad_i : np.ndarray or float
            instantaneous air density
            :math:`\rho`
            [kg m-3]
        r0_full : np.ndarray or float
            surface albedo full vegetation cover
            :math:`\alpha_{0, full}`
            [-]

        Returns
        -------
        t_max_full : np.ndarray or float
            maximum temperature at full vegetation cover
            :math:`T_{c,max}`
            [K]

        """
        emiss_full = 0.99
        sb = 5.67e-8  # stefan boltzmann constant
        sh = 1004.0  # specific heat J kg-1 K-1
        tc_max_num = (
                (1 - r0_full) * ra_hor_clear_i
                + emiss_full * emiss_atm_i * sb * (t_air_k_i) ** 4
                - emiss_full * sb * (t_air_k_i) ** 4
        )
        tc_max_denom = 4 * emiss_full * sb * (t_air_k_i) ** 3 + (ad_i * sh) / rac
        tc_max = tc_max_num / tc_max_denom + t_air_k_i

        return tc_max

    @staticmethod
    def maximum_temperature_bare(
            ra_hor_clear_i, emiss_atm_i, t_air_k_i, ad_i, raa, ras, r0_bare
    ):
        r"""
        Computes the maximum temperature under dry bare soil conditions

         math ::

            T_{s,max}=\frac{\left(1-\alpha_{s}\right)S_{d}+\varepsilon_{s}\varepsilon_{a}\sigma
            T_{a}^{4}-\varepsilon_{s}\sigma T_{a}^{4}}{4\varepsilon_{s}\sigma T_{a}^{3}+
            \rho C_{p}/\left[\left(r_{a1,a}+r_{a1,s}\right)\left(1-G/R_{n,s}\right)\right]}+T_{a}

        Parameters
        ----------
        ra_hor_clear_i : np.ndarray or float
            Total clear-sky irradiance on a horizontal surface
            :math:`ra_hor_clear_i`
            [W/m2]
        emiss_atm_i : np.ndarray or float
            instantaneous atmospheric emissivity
            :math:`P`
            [-]
        t_air_k_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a}`
            [K]
        ad_i : np.ndarray or float
            instantaneous air density
            :math:`\rho`
            [kg m-3]
        raa : np.ndarray or float
            aerodynamical resistance
            :math:`r_{a1,a}`
            [sm-1]
        ras : np.ndarray or float
            aerodynamical resistance
            :math:`r_{a1,s}`
            [sm-1]
        r0_bare : np.ndarray or float
            dry bare soil surface albedo
            :math:`\alpha_{0, bare}`
            [-]

        Returns
        -------
        t_max_bare : np.ndarray or float
            maximum temperature at bare soil
            :math:`T_{c,max}`
            [K]

        """
        emiss_bare = 0.95
        sb = 5.67e-8  # stefan boltzmann constant
        sh = 1004.0  # specific heat J kg-1 K-1
        ts_max_num = (
                (1 - r0_bare) * ra_hor_clear_i
                + emiss_bare * emiss_atm_i * sb * (t_air_k_i) ** 4
                - emiss_bare * sb * (t_air_k_i) ** 4
        )
        ts_max_denom = 4 * emiss_bare * sb * (t_air_k_i) ** 3 + (ad_i * sh) / (
                (raa + ras) * (1 - 0.35)
        )
        return ts_max_num / ts_max_denom + t_air_k_i

    @staticmethod
    def minimum_temperature_full(
            ra_hor_clear_i, emiss_atm_i, t_air_k_i, ad_i, rac, lst_zone_mean, r0_full
    ):
        r"""
        Computes the minimum temperature under fully vegetated conditions

         math ::


        Parameters
        ----------
        ra_hor_clear_i : np.ndarray or float
            Total clear-sky irradiance on a horizontal surface
            :math:`ra_hor_clear_i`
            [W/m2]
        emiss_atm_i : np.ndarray or float
            instantaneous atmospheric emissivity
            :math:`P`
            [-]
        t_air_k_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a}`
            [K]
        ad_i : np.ndarray or float
            instantaneous air density
            :math:`\rho`
            [kg m-3]
        rac : np.ndarray or float
            aerodynamical resistance
            :math:`r_{a1,a}`
            [sm-1]
        lst_zone_mean : np.ndarray or float
            land surface temperature zone mean
            [K]
        r0_full : np.ndarray or float
            surface albedo full vegetation cover
            :math:`\alpha_{0, full}`
            [-]

        Returns
        -------
        t_min_full : np.ndarray or float
            minimum temperature at full vegetation cover
            :math:`T_{c,max}`
            [K]

        """

        emiss_full = 0.99
        g_rn_ratio = 0.0
        LE_Rn_ratio = 1.1

        x_full = 1 - g_rn_ratio - LE_Rn_ratio
        sb = 5.67e-8  # stefan boltzmann constant
        sh = 1004.0  # specific heat J kg-1 K-1# t
        c1 = x_full * emiss_full * sb * lst_zone_mean ** 3 + (ad_i * sh) / rac

        ts_min_full = (x_full * (1 - r0_full) * ra_hor_clear_i + x_full * emiss_atm_i * sb * t_air_k_i ** 4 + (ad_i * sh * t_air_k_i) / rac) / c1

        return ts_min_full

    @staticmethod
    def minimum_temperature_bare(
            ra_hor_clear_i, emiss_atm_i, t_air_k_i, ad_i, raa, ras, lst_zone_mean, r0_bare_wet
    ):
        r"""
        Computes the minimum temperature under dry bare soil conditions

         math ::


        Parameters
        ----------
        ra_hor_clear_i : np.ndarray or float
            Total clear-sky irradiance on a horizontal surface
            :math:`ra_hor_clear_i`
            [W/m2]
        emiss_atm_i : np.ndarray or float
            instantaneous atmospheric emissivity
            :math:`P`
            [-]
        t_air_k_i : np.ndarray or float
            instantaneous air temperature
            :math:`T_{a}`
            [K]
        ad_i : np.ndarray or float
            instantaneous air density
            :math:`\rho`
            [kg m-3]
        raa : np.ndarray or float
            aerodynamical resistance
            :math:`r_{a1,a}`
            [sm-1]
        ras : np.ndarray or float
            aerodynamical resistance
            :math:`r_{a1,a}`
            [sm-1]
        lst_zone_mean : np.ndarray or float
            land surface temperature zone mean
            [K]
        r0_bare_wet : np.ndarray or float
            wet bare soil surface albedo
            :math:`\alpha_{0, bare}`
            [-]

        Returns
        -------
        t_min_bare : np.ndarray or float
            maximum temperature at bare soil
            :math:`T_{c,max}`
            [K]

        """

        emiss_bare = 0.95
        g_rn_ratio = 0.15
        LE_Rn_ratio = 1.1

        x_bare = 1 - g_rn_ratio - LE_Rn_ratio
        sb = 5.67e-8  # stefan boltzmann constant
        sh = 1004.0  # specific heat J kg-1 K-1
        c1 = x_bare * emiss_bare * sb * lst_zone_mean ** 3 + (ad_i * sh) / (raa + ras)

        ts_min_bare = (x_bare * (1 - r0_bare_wet) * ra_hor_clear_i + x_bare * emiss_atm_i * sb * t_air_k_i ** 4 + (ad_i * sh * t_air_k_i) / (raa + ras)) / c1

        return ts_min_bare

    @staticmethod
    def maximum_temperature(t_max_bare, t_max_full, vc):
        r"""
        Computes the maximum temperature at dry conditions

         math ::

            T_{0,max} = c_{veg}(T_{c,max}-T_{s,max})+T_{s,max}


        Parameters
        ----------
        t_max_bare : np.ndarray or float
            maximum temperature at bare soil
            :math:`T_{s,max}`
            [K]
        t_max_full : np.ndarray or float
            maximum temperature at full dry vegetation
            :math:`T_{c,max}`
            [K]
        vc : np.ndarray or float
            vegetation cover
            :math:`c_{veg}`
            [-]


        Returns
        -------
        lst_max : np.ndarray or float
            maximum temperature at dry conditions
            :math:`T_{0,max}`
            [K]

        """
        return vc * (t_max_full - t_max_bare) + t_max_bare

    @staticmethod
    def minimum_temperature(t_wet_k_i, t_air_k_i, vc):
        r"""
        Computes the maximum temperature at dry conditions

         math ::

            T_{0,min} = c_{veg}(T_{a1,i}-T_{w})+T_{w}


        Parameters
        ----------
        t_wet_k_i : np.ndarray or float
            minimum temperature at bare soil
            :math:`T_{s,max}`
            [K]
        t_air_k_i : np.ndarray or float
            minimum temperature at full vegetation
            :math:`T_{c,max}`
            [K]
        vc : np.ndarray or float
            vegetation cover
            :math:`c_{veg}`
            [-]


        Returns
        -------
        lst_min : np.ndarray or float
            minimum temperature at wet conditions
            :math:`T_{0,min}`
            [K]

        """
        return vc * (t_air_k_i - t_wet_k_i) + t_wet_k_i

    @staticmethod
    def soil_moisture_from_maximum_temperature(lst_max, lst, lst_min):
        r"""
        Computes the relative root zone soil moisture based on estimates of
        maximum temperature and wet bulb temperature and measured land
        surface temperature

         math ::

            \Theta = \frac{T_{0}-T_{0,min}}{T_{0,max}-T_{0,min}}

        Parameters
        ----------
        lst : np.ndarray or float
            land surface temperature
            :math:`T_{0}`
            [K]
        lst_max : np.ndarray or float
            maximum temperature at dry conditions
            :math:`T_{0,max}`
            [K]
        lst_min : np.ndarray or float
            minimum temperature at wet conditions
            :math:`T_{0, min}`
            [K]


        Returns
        -------
        se_root : np.ndarray or float
            soil moisture root zone soil moisture (based on LST)
            :math:`\Theta`
            [cm3/cm3]

        """
        ratio = (lst - lst_min) / (lst_max - lst_min)
        ratio = np.clip(ratio, 0, 1)
        ratio = 1 - ratio
        se_root = np.exp((ratio - 1.0) / 0.421)

        return se_root

    @staticmethod
    def stress_moisture(se_root, tenacity=1.5):
        """
        Computes the stress for plants when there is insufficient soil
        moisture in the root zone

        math ::
            S_{m}=K_{sf}S_{e,root}-\frac{\sin\left(2\pi S_{e,root}\right)}{2\pi}

        The tenacity factor :math:`K_{sf}` ranges from 1 for sensitive plants to
        1.5 for moderately sensitive plants to 3 for insensitive
        (tenacious plants).

        Parameters
        ----------
        se_root : np.ndarray or float
            effective saturation root zone moisture
            `S_{e,root}`
            [-]
        tenacity : np.ndarray or float
            tenacity factor
            `K_{sf}`
            [-]

        Returns
        -------
        stress_moist : np.ndarray or float
            stress factor for root zone moisture
            :math:`S_{m}`
            [-]

        Examples
        --------
        SoilMoistureAnalysis.stress_moisture(0.5)
        0.75
        SoilMoistureAnalysis.stress_moisture(0.5, tenacity = 1)
        0.5
        SoilMoistureAnalysis.stress_moisture(0.5, tenacity = 3)
        1.0
        """
        stress = tenacity * se_root - (np.sin(2 * np.pi * se_root)) / (2 * np.pi)
        stress = np.clip(stress, 0, 1)

        return stress
