import numpy as np


class VegetationAnalysis:
    @staticmethod
    def calculate_nitrogen(NDVI):
        """
        Compute Nitrogen amount
        :param NDVI:
        :return:
        """
        # Vegetation Index - Regression model from Bagheri et al. (2013)
        VI = 38.764 * np.square(NDVI) - 24.605 * NDVI + 5.8103

        # Nitrogen computation
        nitrogen = np.copy(VI)
        nitrogen[VI <= 0.0] = 0.0
        nitrogen[NDVI <= 0.0] = 0.0
        return nitrogen

    @staticmethod
    def calculate_vegetation_cover(ndvi):
        """
        Compute vegitation cover
        :param ndvi:
        :return:
        """
        vegt_cover = 1 - np.power((0.8 - ndvi) / (0.8 - 0.125), 0.7)
        vegt_cover[ndvi < 0.125] = 0.0
        vegt_cover[ndvi > 0.8] = 0.99
        return vegt_cover

    @staticmethod
    def calculate_leaf_area_index(vegetation_cover, ndvi):
        """
        calculate leaf area index
        :param vegetation_cover:
        :param ndvi:
        :return:
        """
        lai_1 = np.log(-(vegetation_cover - 1)) / -0.45
        lai_1[lai_1 > 8] = 8.0
        lai_2 = (9.519 * np.power(ndvi, 3) + 0.104 * np.power(ndvi, 2) +
                 1.236 * ndvi - 0.257)
        lai = (lai_1 + lai_2) / 2.0  # Average LAI
        lai[lai < 0.001] = 0.001
        return lai

    @staticmethod
    def calculate_ndvi_qc_map(ndvi) -> np.ndarray:
        """
         create vegitation quality map
        :param ndvi:
        :return:
        """
        QC_Map = np.zeros(ndvi.shape)
        QC_Map[np.isnan(ndvi)] = 1
        return QC_Map

    @staticmethod
    def calculate_ndvi(nir_band, red_band) -> np.ndarray:
        """
        calculate ndvi using TOA planetary Reflectance Rho Lambda (ρλ)
        BOA vs TOA https://feed.terramonitor.com/ndvi-boa-ndvi-toa/
        :param nir_band:
        :param red_band:
        :return:
        """
        ndvi = ((nir_band - red_band) / (nir_band + red_band))

        return ndvi

    @staticmethod
    def calculate_FPAR(ndvi):
        """
        Calculate Fraction of photosynthetically active radiation (FPAR)
        https://en.wikipedia.org/wiki/Fraction_of_absorbed_photosynthetically_active_radiation
        :param ndvi:
        :return:
        """
        fpar = -0.161 + 1.257 * ndvi
        fpar[ndvi < 0.125] = 0.0
        return fpar

    # @staticmethod
    # def calculate_vegetation_indices(ndvi):
    #     """
    #     Vegetation Index - Regression model from Bagheri et al. (2013)
    #     :param ndvi:
    #     :return:
    #     """
    #     vi = 38.764 * np.square(ndvi) - 24.605 * ndvi + 5.8103
    #     return vi

    @staticmethod
    def Calc_Biomass_production(moisture_stress_biomass, ETA_24, Ra_mountain_24, Transm_24, FPAR, esat_24, eact_24, Th, Kt, Tl, Temp_24, LUEmax):
        """
         Function to calculate the biomass production and water productivity
        :param moisture_stress_biomass:
        :param ETA_24:
        :param Ra_mountain_24:
        :param Transm_24:
        :param FPAR:
        :param esat_24:
        :param eact_24:
        :param Th:
        :param Kt:
        :param Tl:
        :param Temp_24:
        :param LUEmax: Light Use Efficiency
        :return:
        """

        Ksolar = Ra_mountain_24 * Transm_24

        # Incident Photosynthetically active radiation (PAR, MJ/m2) per time period
        PAR = 0.48 * Ksolar

        # Aborbed Photosynthetical Active Radiation (APAR) by the vegetation:
        APAR = FPAR * PAR

        vapor_stress = 0.88 - 0.183 * np.log(esat_24 - eact_24)
        vapor_stress_biomass = vapor_stress.clip(0.0, 1.0)
        Jarvis_coeff = (Th - Kt) / (Kt - Tl)
        heat_stress_biomass = ((Temp_24 - Tl) * np.power(Th - Temp_24, Jarvis_coeff) /
                               ((Kt - Tl) * np.power(Th - Kt, Jarvis_coeff)))
        print('vapor stress biomass =', '%0.3f' % np.nanmean(vapor_stress_biomass))
        print('heat stress biomass =', '%0.3f' % np.nanmean(heat_stress_biomass))

        # Light use efficiency, reduced below its potential value by low
        # temperature or water shortage:
        LUE = (LUEmax * heat_stress_biomass * vapor_stress_biomass * moisture_stress_biomass)

        # Dry matter production (kg/ha/d):
        Biomass_prod = APAR * LUE * 0.864  # C3 vegetation

        # Water productivity
        Biomass_wp = Biomass_prod / (ETA_24 * 10)  # C3 vegetation
        Biomass_wp[ETA_24 == 0.0] = 0.0

        # Water deficit
        Biomass_deficit = (Biomass_prod / moisture_stress_biomass -
                           Biomass_prod)

        return (LUE, Biomass_prod, Biomass_wp, Biomass_deficit)

    @staticmethod
    def Raupach_Model_based_surface_roughness(h_obst, cd, LAI):
        """
        Function for the Raupach model to calculate the surface roughness (based on Raupach 1994)
        """
        # constants
        cw = 2.0
        LAIshelter = 2.5

        # calculate psi
        psi = np.log(cw) - 1 + np.power(2.0, -1)  # Vegetation influence function

        # Calculate Ustar divided by U
        ustar_u = np.power((0.003 + 0.3 * LAI / 2), 0.5)
        ustar_u[LAI < LAIshelter] = 0.3

        # calculate: 1 - d/hv
        inv_d_hv = (1 - np.exp(-1 * np.power((cd * LAI), 0.5))) / np.power((cd * LAI), 0.5)

        # Calculate: surface roughness/hv
        zom_hv = inv_d_hv * np.exp(-0.41 / ustar_u - psi)

        # Calculate: surface roughness
        zom_Raupach = zom_hv * h_obst

        return zom_Raupach

    @staticmethod
    def NDVI_based_surface_roughness(NDVI, Surf_albedo, water_mask):
        """
        Function for the NDVI model to calculate the surface roughness
        """
        zom_NDVI = np.exp(1.096 * NDVI / Surf_albedo - 5.307)
        zom_NDVI[water_mask == 1.0] = 0.001
        zom_NDVI[zom_NDVI > 10.0] = 10.0

        return zom_NDVI

    @staticmethod
    def canopy_resistance(r_canopy_0, stress_moist, rcan_max=1000000.):
        """
        Computes canopy resistance
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
        VegetationAnalysis.canopy_resistance(218, 0.8)
        272.5
        """

        r_canopy = np.where(stress_moist == 0, rcan_max, r_canopy_0 / stress_moist)

        return r_canopy

    @staticmethod
    def initial_canopy_aerodynamic_resistance(u_24, z0m, z_obs=2):
        """
        Computes the aerodynamic resistance for a canopy soil without stability
        corrections :math:`r_{a,}^{0}`.

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
            :math:`r_{a,canopy}^{0}`
            [s/m]
        """
        k = 0.41  # karman constant (-)
        return (np.log(z_obs / z0m) * np.log(z_obs / (0.1 * z0m))) / (k ** 2 * u_24)
