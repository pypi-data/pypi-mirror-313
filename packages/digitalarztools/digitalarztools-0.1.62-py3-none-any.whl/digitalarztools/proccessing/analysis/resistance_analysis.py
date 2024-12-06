import numpy as np


class ResistanceAnalysis:
    @staticmethod
    def atmospheric_canopy_resistance(lai_eff, stress_rad, stress_vpd,
                                      stress_temp, rs_min=70, rcan_max=1000000.):
        """
        Computes canopy resistance excluding soil moisture stress


        Parameters
        ----------
        lai_eff : np.ndarray or float
            effective leaf area index
            :math:`I_{lai,eff}`
            [-]
        stress_temp : np.ndarray or float
            stress factor for air temperature
            :math:`S_{t}`
            [-]
        stress_vpd : np.ndarray or float
            stress factor for vapour pressure deficit
            :math:`S_{v}`
            [-]
        stress_rad : np.ndarray or float
            stress factor for radiation
            :math:`S_{r}`
            [-]
        rs_min : np.ndarray or float
            Minimal stomatal resistance
            :math:`r_{s_min}`
            [sm-1]
        rcan_max : np.ndarray or float
            Maximum stomatal resistance
            :math:`r_{can_max}`
            [sm-1]

        Returns
        -------
        r_canopy_0 : np.ndarray or float
            atmospheric canopy resistance
            :math:`r_{canopy,0}`
            [sm-1]

        Examples
        --------
        ResistanceAnalysis.atmospheric_canopy_resistance(0.9, 0.4, 0.9, 0.94)
        229.839768846861
        """

        bulk_stress = stress_rad * stress_temp * stress_vpd
        max_mask = np.logical_or(bulk_stress == 0, lai_eff == 0)

        r_canopy_0 = (rs_min / lai_eff) / bulk_stress
        r_canopy_0[max_mask] = rcan_max

        return r_canopy_0

    @staticmethod
    def canopy_resistance(r_canopy_0, stress_moist, rcan_max=1000000.):
        """
        Computes canopy resistance

         math ::
            r_{canopy}=\frac{r_{canopy,0}}{S_{m}}

        Parameters
        ----------
        r_canopy_0 : np.ndarray or float
            Atmospheric canopy resistance
            :math:`r_{canopy_0}`
            [sm-1]
        stress_moist : np.ndarray or float
            stress factor for root zone soil moisture
            :math:`S_{m}`
            [-]
        rcan_max : np.ndarray or float
            Maximum stomatal resistance
            :math:`r_{can_max}`
            [sm-1]

        Returns
        -------
        r_canopy : np.ndarray or float
            canopy resistance
            :math:`r_{canopy}`
            [sm-1]

        Examples
        --------
        ResistanceAnalysis.canopy_resistance(218, 0.8)
        272.5
        """

        r_canopy = np.where(stress_moist == 0, rcan_max, r_canopy_0 / stress_moist)

        return r_canopy

    @staticmethod
    def soil_resistance(se_top, land_mask=1, r_soil_pow=-2.1, r_soil_min=800):
        """
        Computes soil resistance

        Parameters
        ----------
        r_soil_min : np.ndarray or float
            Minimum soil resistance
            :math:`r_{soil,min}`
            [sm-1]
        se_top : np.ndarray or float
            Top soil effective saturation
            :math:`S_{e,top}`
            [-]
        r_soil_pow : np.ndarray or float
            Power soil resistance function
            :math:`a`
            [-]
        land_mask : np.ndarray or int
            land use classification
            :math:`l`
            [-]

        Returns
        -------
        r_soil : np.ndarray or float
            soil resistance
            :math:`r_{soil}`
            [sm-1]

        Examples
        --------
        ResistanceAnalysis.soil_resistance(se_top=0.9)
        998.1153098304111
        """
        se_top = np.minimum(0.5, se_top)
        res = np.ones(land_mask.shape) * r_soil_min * se_top ** r_soil_pow
        res[land_mask == 2] = 0

        return res
