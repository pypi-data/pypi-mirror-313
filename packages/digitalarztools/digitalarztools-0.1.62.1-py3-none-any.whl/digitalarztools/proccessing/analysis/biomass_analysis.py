# -*- coding: utf-8 -*-

class BiomassAnalysis:
    @staticmethod
    def lue(lue_max, stress_temp, stress_moist, eps_a):
        r"""
        Computes the light use efficiency

        Parameters
        ----------
        lue_max : np.ndarray or float
            maximal light use efficiency
            :math:`EF_{ref}`
            [gr/MJ]
        stress_temp : np.ndarray or float
            stress factor for air temperature
            :math:`S_{T}`
            [-]
        stress_moist : np.ndarray or float
            stress soil moisture
            :math:`I`
            [-]
        eps_a : np.ndarray or float
            epsilon autotrophic respiration
            :math:`I`
            [-]

        Returns
        -------
        lue : np.ndarray or float
            light use efficiency
            :math:`I`
            [gr/MJ]
        """

        lue = lue_max * stress_temp * stress_moist * eps_a

        return lue

    @staticmethod
    def biomass(apar, lue):
        r"""
        Computes the light use efficiency

        Parameters
        ----------
        apar : np.ndarray or float
            apar
            :math:`I_{ra_24,fpar}`
            [MJ/m2]
        lue : np.ndarray or float
            light use efficiency
            :math:`I`
            [gr/MJ]

        Returns
        -------
        biomass : np.ndarray or float
            biomass production
            :math:`I`
            [kg/ha]
        """

        biomass = apar * lue * 10

        return biomass
