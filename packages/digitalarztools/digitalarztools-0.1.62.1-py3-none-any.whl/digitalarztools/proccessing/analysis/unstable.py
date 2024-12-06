import numpy as np


class Unstable:
    @staticmethod
    def initial_sensible_heat_flux_canopy_daily(rn_24_canopy, t_24_init):
        r"""
        Computes the initial sensible heat flux before the iteration which solves
        the stability corrections. The first estimation of transpiration is used
        to estimate the initial sensible heat flux.

         math ::

            H_{canopy}=Q_{canopy}^{*}-T

        Parameters
        ----------
        rn_24_canopy : np.ndarray or float
            daily net radiation for the canopy
            :math:`Q_{canopy}^{*}`
            [W m-2]
        t_24_init : np.ndarray or float
            initial estimate of daily transpiration
            :math:`T`
            [W m-2]

        Returns
        -------
        h_canopy_24_init : np.ndarray or float
            initial estimate of the sensible heat flux
            :math:`H^{canopy}`
            [W m-2]
        """

        return rn_24_canopy - t_24_init

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
    def initial_friction_velocity_daily(u_b_24, z0m, disp, z_b=100):
        r"""
        Computes the initial friction velocity without using stability corrections.

         math ::

            u_{*}=\frac{ku_{b}}{ln\left(\frac{z_{b}-d}{z_{0,m}}\right)}

        Parameters
        ----------
        u_b_24 : np.ndarray or float
            daily wind speed at blending heigt
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
        u_star_24_init : np.ndarray or float
            initial estimate of the daily friction velocity
            :math:`u_{*}`
            [m s-1]
        """
        k = 0.41  # karman constant (-)
        return (k * u_b_24) / (np.log((z_b - disp) / z0m))

    @staticmethod
    def initial_friction_velocity_soil_daily(u_b_24, disp, z_b=100):
        r"""
        Computes the initial firction velocity without using stability corrections.

         math ::

            u_{*}=\frac{ku_{b}}{ln\left(\frac{z_{b}-d}{z_{0,m}}\right)}

        Parameters
        ----------
        u_b_24 : np.ndarray or float
            daily wind speed at blending heigt
            :math:`u_{b}`
            [m s-1]
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
        u_star_24_soil_init : np.ndarray or float
            initial estimate of the daily friction velocity for soil
            :math:`u_{*}`
            [m s-1]
        """
        k = 0.41  # karman constant (-)
        z0_soil = 0.001  # soil roughness m
        return (k * u_b_24) / (np.log((z_b - disp) / z0_soil))

    @staticmethod
    def monin_obukhov_length(h_flux, ad, u_star, t_air_k):
        r"""
        Computes the Monin-Obukhov length. The Monin-Obukhov length is used to
        describe the effects of buoyancy on turbulent flows. The Monin-Obukhov
        length is usually negative during daytime.

         math ::

            L=\frac{-\rho c_{p}u_{*}^{3}T_{a}}{kgH_{canopy}}

        Parameters
        ----------
        h_flux : np.ndarray or float
            sensible heat flux
            :math:`H`
            [W m-2]
        ad : np.ndarray or float
            air density
            :math:`\rho`
            [kg m-3]
        u_star : np.ndarray or float
            Monin Obukhov length
            :math:`L`
            [m]
        t_air_k : np.ndarray or float
            air tempererature in kelvin
            :math:`T_{a}`
            [K]

        Returns
        -------
        monin : np.ndarray or float
            monin obukhov length
            :math:`L`
            [m]
        """
        k = 0.41  # karman constant (-)
        sh = 1004.0  # specific heat J kg-1 K-1
        g = 9.807  # gravity m s-2
        return (-ad * sh * u_star ** 3 * t_air_k) / (k * g * h_flux)

    @staticmethod
    def stability_parameter(monin, disp, z_b=100):
        r"""
        Computes the stability parameter introduced by Monin and Obukhov. This
        parameter includes effects of both shear stress and buoyancy on turbulence.
        It is applicable to blend height.

         math ::

            x_{b}=1-16\left(\frac{z_{b}-d}{L}\right)^{0.25}

        Parameters
        ----------
        monin : np.ndarray or float
            monin obukhov length
            :math:`L`
            [m]
        z_b : np.ndarray or float
            blending height
            :math:`z_{b}`
            [m]
        disp : np.ndarray or float
            displacement height
            :math:`d`
            [m]

        Returns
        -------
        x_b : np.ndarray or float
            stability parameter used in stability correction
            :math:`x_{b}`
            [-]
        """
        return (1 - 16 * ((z_b - disp) / monin)) ** 0.25

    @staticmethod
    def stability_factor(x_b):
        r"""
        Computes the stability correction for heat at blending height.

         math ::

            \psi_{h,b}=2\ln\left(\frac{1+x_{b}}{2}\right)+
            \ln\left(\frac{1+x_{b}^{2}}{2}\right)-
            2\arctan\left(x_{b}\right)+0.5\pi

        Parameters
        ----------
        x_b : np.ndarray or float
            stability parameter used in stability correction
            :math:`x_{b}`
            [-]

        Returns
        -------
        sf : np.ndarray or float
            stability correction for heat
            :math:`\psi_{h,b}`
            [-]
        """
        return (
                2 * np.log((1 + x_b) / 2)
                + np.log((1 + x_b ** 2) / 2)
                - 2 * np.arctan(x_b)
                + 0.5 * np.pi
        )

    @staticmethod
    def stability_parameter_obs(monin, z_obs):
        r"""
        Computes the stability parameter introduced by Monin and Obukhov. This
        parameter includes effects of both shear stress and buoyancy on turbulence.
        It is applicable to observation height.

         math ::

            x_{obs}=1-16\left(\frac{z_{obs}}{L}\right)^{0.25}

        Parameters
        ----------
        monin : np.ndarray or float
            monin obukhov length
            :math:`L`
            [m]
        z_obs : np.ndarray or float
            observation height
            :math:`z_{obs}`
            [m]

        Returns
        -------
        x_b_obs : np.ndarray or float
            stability parameter used in stability correction for observation height
            :math:`x_{obs}`
            [-]
        """
        return (1 - 16 * (z_obs / monin)) ** 0.25

    @staticmethod
    def stability_correction_heat_obs(x_b_obs):
        r"""
        Computes the stability correction for heat at observation height.

         math ::

            \psi_{h,obs}=2\ln\left(\frac{1+x_{obs}^{2}}{2}\right)

        Parameters
        ----------
        x_b_obs : np.ndarray or float
            stability parameter used in stability correction for observation height
            :math:`x_{obs}`
            [-]

        Returns
        -------
        sf_obs : np.ndarray or float
            stability correction for heat for observation height
            :math:`\psi_{h,obs}`
            [-]
        """
        return 2 * np.log((1 + x_b_obs ** 2) / 2)

    @staticmethod
    def friction_velocity(u_b, z_b, z0m, disp, sf):
        r"""
        Computes the friction velocity

         math ::

            u_{*}=\frac{ku_{b}}{ln\left(\frac{z_{b}-d}{z_{0,m}}\right)-\psi_{h,b}}

        Parameters
        ----------
        u_b : np.ndarray or float
            windspeed at blending height
            :math:`u_{b}`
            [m]
        z_b : np.ndarray or float
            blending height
            :math:`z_{b}`
            [m]
        z0m : np.ndarray or float
            roughness length
            :math:`z_{0,m}`
            [m]
        disp : np.ndarray or float
            displacement height
            :math:`d`
            [m]
        sf : np.ndarray or float
            stability factor at blending height
            :math:`\psi_{h,b}`
            [m]

        Returns
        -------
        u_star : np.ndarray or float
            friction velocity
            :math:`u_{*}`
            [m s-1]
        """
        k = 0.41  # karman constant (-)
        return (k * u_b) / (np.log((z_b - disp) / z0m) - sf)

    @classmethod
    def ra_canopy(cls,
                  h_canopy_init, t_air_k, u_star_init, ad, z0m, disp, u_b, z_obs=2, z_b=100, iter_ra=3
                  ):
        r"""
        Computes the aerodynamical resistance for canopy using an iterative
        approach. The iteration is needed to compute the frication velocity at
        blending height Iteration stops either after five iterations or
        if the difference between two subsequent estimations is less than 0.01.

         math ::

            \begin{cases}
            \begin{array}{c}
            L=\frac{-\rho c_{p}u_{*}^{3}T_{a}}{kgH_{canopy}}\\
            x_{b}=1-16\left(\frac{z_{b}-d}{L}\right)^{0.25}\\
            \psi_{h,b}=2\ln\left(\frac{1+z_{b}}{2}\right)+
            \ln\left(\frac{1+z_{b}^{2}}{2}\right)-
            2\arctan\left(x_{b}\right)+0.5\pi\\
            u_{*}=\frac{ku_{b}}{ln\left(\frac{z_{b}-d}{z_{0,m}}\right)-\psi_{h,b}}
            \end{array}\end{cases}

        The friction velocity is independent of height. So this value can be used
        to calculate together with the stability correction for heat on observation
        heigth the aerodynamical resistance.

         math ::

            x_{obs}=1-16\left(\frac{z_{obs}}{L}\right)^{0.25}

            \psi_{h,obs}=2\ln\left(\frac{1+x_{obs}^{2}}{2}\right)

            r_{a1,canopy}=\frac{\ln\left(\frac{z_{obs}-d}
            {0.1z_{0,m}}\right)-\psi_{h,obs}}{ku_{*}}

        Parameters
        ----------
        h_canopy_init : np.ndarray or float
            initial estimate of the sensible heat flux
            :math:`H^{canopy}`
            [W m-2]
        t_air_k : np.ndarray or float
            air tempererature in kelvin
            :math:`T_{a}`
            [K]
        u_star_init : np.ndarray or float
            initial estimate of the daily friction velocity
            :math:`u_{*}`
            [m s-1]
        ad : np.ndarray or float
            air density
            :math:`\rho`
            [kg m-3]
        z_b : np.ndarray or float
            blending height
            :math:`z_{b}`
            [m]
        z_obs : np.ndarray or float
            observation height
            :math:`z_{obs}`
            [m]
        z0m : np.ndarray or float
            roughness length
            :math:`z_{0,m}`
            [m]
        disp : np.ndarray or float
            displacement height
            :math:`d`
            [m]
        u_b : np.ndarray or float
            windspeed at blending height
            :math:`u_{b}`
            [m/s]
        iter_ra : integer
            number of iterations for aerodynamical resistance
            :math:`n_{ra}`
            [-]

        Returns
        -------
        ra_canopy : np.ndarray or float
            aerodynamical resistance for canopy
            :math:`r_{a1,canopy}`
            [s m-1]
        """
        h_flux = h_canopy_init
        u_star_start = u_star_init
        iteration = 0
        epsilon = 10.0
        while (iteration < iter_ra) and (np.nanmax(epsilon) > 0.01):
            iteration += 1
            monin = cls.monin_obukhov_length(h_flux, ad, u_star_start, t_air_k)
            x_b = np.where(monin > 0, 1, cls.stability_parameter(monin, disp, z_b))
            sf = cls.stability_factor(x_b)
            u_star = cls.friction_velocity(u_b, z_b, z0m, disp, sf)
            epsilon = abs(u_star - u_star_start)
            u_star_start = u_star

        x_b_obs = np.where(monin <= 0, cls.stability_parameter_obs(monin, z_obs), 1)
        sf_obs = np.where(monin <= 0, cls.stability_correction_heat_obs(x_b_obs), 0)

        disp = np.minimum(disp, 1.5)
        k = 0.41  # karman constant (-)
        ra = (np.log((z_obs - disp) / (0.1 * z0m)) - sf_obs) / (k * u_star)
        ra = np.clip(ra, 25, 500)

        return ra

    @classmethod
    def transpiration(cls,
                      rn_24_canopy,
                      ssvp_24,
                      ad_24,
                      vpd_24,
                      psy_24,
                      r_canopy,
                      h_canopy_24_init,
                      t_air_k_24,
                      u_star_24_init,
                      z0m,
                      disp,
                      u_b_24,
                      z_obs=2,
                      z_b=100,
                      iter_h=3,
                      ):
        r"""
        Computes the transpiration using an iterative approach. The iteration is
        needed to compute the aerodynamical resistance.Iteration stops either after
        five iterations orif the difference between two subsequent estimations
        is less than 0.01. The iteration is started with an estimate on :math:`H`
        using the initial guess without stability corrections. Subsequent
        iterations use the guess with stability corrections.

         math ::

            T=\frac{\Delta\left(Q_{canopy}^{*}\right)+\rho c_{p}\
               frac{\Delta_{e}}{r_{a,canopy}}}{\Delta+
               \gamma\left(1+\frac{r_{canopy}}{r_{a,canopy}}\right)}

        Parameters
        ----------
        rn_24_canopy : np.ndarray or float
            net radiation for the canopy
            :math:`Q^{*}_{canopy}`
            [Wm-2]
        ssvp_24 : np.ndarray or float
           daily slope of saturated vapour pressure curve
           :math:`\Delta_{24}`
           [mbar K-1]
        ad_24 : np.ndarray or float
            daily air density
            :math:`\rho_{24}`
            [kg m-3]
        vpd_24 : np.ndarray or float
           daily vapour pressure deficit
           :math:`\Delta_{e,24}`
           [mbar]
        psy_24 : np.ndarray or float
            daily psychrometric constant
            :math:`\gamma_{24}`
            [mbar K-1]
        r_canopy : np.ndarray or float
            canopy resistance
            :math:`r_{canopy}`
            [sm-1]
        h_canopy_24_init : np.ndarray or float
            initial estimate of the sensible heat flux
            :math:`H^{canopy}`
            [W m-2]
        t_air_k_24 : np.ndarray or float
            daily air tempererature in kelvin
            :math:`T_{a}`
            [K]
        u_star_24_init : np.ndarray or float
            initial estimate of the daily friction velocity
            :math:`u_{*}`
            [m s-1]
        z0m : np.ndarray or float
            roughness length
            :math:`z_{0,m}`
            [m]
        disp : np.ndarray or float
            displacement height
            :math:`d`
            [m]
        u_b_24 : np.ndarray or float
            daily windspeed at blending height
            :math:`u_{b}`
            [m]
        z_b : np.ndarray or float
            blending height
            :math:`z_{b}`
            [m]
        z_obs : np.ndarray or float
            observation height
            :math:`z_{obs}`
            [m]
        iter_h : integer
            number of iterations for sensible heat flux
            :math:`n_h`
            [-]

        Returns
        -------
        t_24 : np.ndarray or float
            daily transpiration energy equivalent
            :math:`T_{24}`
            [W m-2]
        """
        iteration = 0
        epsilon = 10.0
        h_start = h_canopy_24_init

        while (iteration < iter_h) and (np.nanmax(epsilon) > 0.01):
            iteration += 1
            ra_canopy_start = cls.ra_canopy(
                h_start, t_air_k_24, u_star_24_init, ad_24, z0m, disp, u_b_24, z_obs, z_b
            )
            sh = 1004.0  # specific heat J kg-1 K-1
            t = (ssvp_24 * rn_24_canopy + ad_24 * sh * (vpd_24 / ra_canopy_start)) / (
                    ssvp_24 + psy_24 * (1 + r_canopy / ra_canopy_start)
            )
            h = rn_24_canopy - t
            epsilon = abs(h - h_start)
            h_start = h

            # print("max epsilon = %s" %np.nanmax(epsilon))

        return t, h

    @classmethod
    def ra_soil(
            cls, h_soil_24_init, t_air_k, u_star_24_init, ad, disp, u_b, z_obs=2, z_b=100, iter_ra=3
    ):
        r"""
        Computes the aerodynamical resistance for canopy using an iterative
        approach. The iteration is needed to compute the friction velocity at
        blending height Iteration stops either after five iterations or
        if the difference between two subsequent estimations is less than 0.01.

         math ::

            \begin{cases}
            \begin{array}{c}
            L=\frac{-\rho c_{p}u_{*}^{3}T_{a}}{kgH_{soil}}\\
            x_{b}=1-16\left(\frac{z_{b}-d}{L}\right)^{0.25}\\
            \psi_{h,b}=2\ln\left(\frac{1+z_{b}}{2}\right)+
            \ln\left(\frac{1+z_{b}^{2}}{2}\right)-
            2\arctan\left(x_{b}\right)+0.5\pi\\
            u_{*}=\frac{ku_{b}}{ln\left(\frac{z_{b}-d}{z_{0,soil}}\right)
            -\psi_{h,b}}
            \end{array}\end{cases}

        The friction velocity is independent of height. So this value can be used
        to calculate together with the stability correction for heat on observation
        heigth the aerodynamical resistance.

         math ::

            x_{obs}=1-16\left(\frac{z_{obs}}{L}\right)^{0.25}

            \psi_{h,obs}=2\ln\left(\frac{1+x_{obs}^{2}}{2}\right)

            r_{a1,soil}=\frac{\ln\left(\frac{z_{obs}-d}
            {0.1z_{0,soil}}\right)-\psi_{h,obs}}{ku_{*}}

        Parameters
        ----------
        h_soil_24_init : np.ndarray or float
            initial estimate of the sensible heat flux for soil
            :math:`H^{soil}`
            [W m-2]
        t_air_k : np.ndarray or float
            air tempererature in kelvin
            :math:`T_{a}`
            [K]
        u_star_24_init : np.ndarray or float
            initial estimate of the daily friction velocity
            :math:`u_{*}`
            [m s-1]
        ad : np.ndarray or float
            air density
            :math:`\rho`
            [kg m-3]
        z_b : np.ndarray or float
            blending height
            :math:`z_{b}`
            [m]
        z_obs : np.ndarray or float
            observation height
            :math:`z_{obs}`
            [m]
        disp : np.ndarray or float
            displacement height
            :math:`d`
            [m]
        u_b : np.ndarray or float
            windspeed at blending height
            :math:`u_{b}`
            [m]
        iter_ra : integer
            number of iterations for aerodynamical resistance
            :math:`n_{ra}`
            [-]

        Returns
        -------
        ra_soil : np.ndarray or float
            aerodynamical resistance for soil
            :math:`r_{a1,soil}`
            [s m-1]
        """
        h_flux = h_soil_24_init
        u_star_start = u_star_24_init
        iteration = 0
        epsilon = 10
        z0_soil = 0.001  # soil roughness m
        while (iteration < iter_ra) and (np.nanmax(epsilon) > 0.01):
            iteration += 1
            monin = cls.monin_obukhov_length(h_flux, ad, u_star_start, t_air_k)
            x_b = np.where(monin > 0, 0, cls.stability_parameter(monin, disp, z_b))
            sf = cls.stability_factor(x_b)
            u_star = cls.friction_velocity(u_b, z_b, z0_soil, disp, sf)
            epsilon = abs(u_star - u_star_start)
            u_star_start = u_star
        z0_soil = 0.001  # soil roughness m
        x_b_obs = np.where(monin <= 0, cls.stability_parameter_obs(monin, z_obs), 1)
        sf_obs = np.where(monin <= 0, cls.stability_correction_heat_obs(x_b_obs), 0)

        # 1.5 limit is from ETLook IDL
        disp = np.minimum(disp, 1.5)
        k = 0.41  # karman constant (-)
        ra = (np.log((z_obs - disp) / (0.1 * z0_soil)) - sf_obs) / (k * u_star)
        ra = np.maximum(ra, 25)

        return ra

    @classmethod
    def evaporation(
            cls,
            rn_24_soil,
            g0_24,
            ssvp_24,
            ad_24,
            vpd_24,
            psy_24,
            r_soil,
            h_soil_24_init,
            t_air_k_24,
            u_star_24_soil_init,
            disp,
            u_b_24,
            z_b=100,
            z_obs=2,
            iter_h=3,
    ):
        r"""
        Computes the evaporation using an iterative approach. The iteration is
        needed to compute the aerodynamic resistance.Iteration stops either after
        five iterations or if the difference between two subsequent estimations
        is less than 0.01. The iteration is started with an estimate on :math:`H`
        using the initial guess without stability corrections. Subsequent
        iterations use the guess with stability corrections.

         math ::

            E=\frac{\Delta\left(Q_{soil}^{*}-G\right)+
              \rho c_{p}\frac{\Delta_{e}}{r_{a,soil}}}
              {\Delta+\gamma\left(1+\frac{r_{soil}}{r_{a,soil}}\right)}

        Parameters
        ----------
        rn_24_soil : np.ndarray or float
            net radiation for the soil
            :math:`Q^{*}_{canopy}`
            [Wm-2]
        g0_24 : np.ndarray or float
            daily soil heat flux
            :math:`G`
            [Wm-2]
        ssvp_24 : np.ndarray or float
           daily slope of saturated vapour pressure curve
           :math:`\Delta_{24}`
           [mbar K-1]
        ad_24 : np.ndarray or float
            daily air density
            :math:`\rho_{24}`
            [kg m-3]
        vpd_24 : np.ndarray or float
           daily vapour pressure deficit
           :math:`\Delta_{e,24}`
           [mbar]
        psy_24 : np.ndarray or float
            daily psychrometric constant
            :math:`\gamma_{24}`
            [mbar K-1]
        r_soil : np.ndarray or float
            soil resistance
            :math:`r_{soil}`
            [sm-1]
        h_soil_24_init : np.ndarray or float
            initial estimate of the sensible heat flux for soil
            :math:`H^{soil}`
            [W m-2]
        t_air_k_24 : np.ndarray or float
            daily air temperature in kelvin
            :math:`T_{a}`
            [K]
        u_star_24_soil_init : np.ndarray or float
            initial estimate of the daily friction velocity for soil
            :math:`u_{*}`
            [m s-1]
        disp : np.ndarray or float
            displacement height
            :math:`d`
            [m]
        u_b_24 : np.ndarray or float
            daily wind speed at blending height
            :math:`u_{b}`
            [m]
        z_b : np.ndarray or float
            blending height
            :math:`z_{b}`
            [m]
        z_obs : np.ndarray or float
            observation height
            :math:`z_{obs}`
            [m]
        iter_h : integer
            number of iterations for sensible heat flux
            :math:`n_h`
            [-]

        Returns
        -------
        e_24 : np.ndarray or float
            daily evaporation energy equivalent
            :math:`E_{24}`
            [W m-2]
        """
        iteration = 0
        epsilon = 10
        h_start = h_soil_24_init
        sh = 1004.0  # specific heat J kg-1 K-1
        while (iteration < iter_h) and (np.nanmax(epsilon) > 0.1):
            iteration += 1
            ra_soil_start = cls.ra_soil(
                h_start, t_air_k_24, u_star_24_soil_init, ad_24, disp, u_b_24, z_obs, z_b
            )
            e = (
                        ssvp_24 * (rn_24_soil - g0_24) + ad_24 * sh * (vpd_24 / ra_soil_start)
                ) / (ssvp_24 + psy_24 * (1 + r_soil / ra_soil_start))
            h = rn_24_soil - g0_24 - e
            epsilon = abs(h - h_start)
            h_start = h

        e = e.clip(0, 100)

        return e

    @staticmethod
    def transpiration_mm(t_24, lh_24):
        r"""
        Computes the canopy transpiration based on the Penman Monteith equation
        adapted for canopy.

         math ::

            T=Td_{sec}\lambda_{24}

        where the following constants are used

        * :math:`d_{sec}` seconds in the day = 86400 [s]

        Parameters
        ----------
        t_24 : np.ndarray or float
            daily transpiration energy equivalent
            :math:`E^{0}`
            [W m-2]
        lh_24 : np.ndarray or float
            daily latent heat of evaporation
            :math:`\lambda_{24}`
            [J/kg]

        Returns
        -------
        t_24_mm : np.ndarray or float
            daily transpiration in mm
            :math:`T`
            [mm d-1]
        """
        day_sec = 86400.0  # seconds in a day
        return t_24 * day_sec / lh_24

    @staticmethod
    def evaporation_mm(e_24, lh_24):
        r"""
        Computes the soil evaporation based on the Penman Monteith equation
        adapted for soils.

         math ::

            E=Ed_{sec}\lambda_{24}

        where the following constants are used

        * :math:`d_{sec}` seconds in the day = 86400 [s]

        Parameters
        ----------
        e_24 : np.ndarray or float
            daily evaporation energy equivalent
            :math:`E^{0}`
            [W m-2]
        lh_24 : np.ndarray or float
            daily latent heat of evaporation
            :math:`\lambda_{24}`
            [J/kg]

        Returns
        -------
        e_24_mm : np.ndarray or float
            daily evaporation in mm
            :math:`E`
            [mm d-1]
        """
        day_sec = 86400.0  # seconds in a day
        return e_24 * day_sec / lh_24
