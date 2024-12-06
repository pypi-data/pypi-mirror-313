import numpy as np


class LeafAnalysis:
    @staticmethod
    def vegetation_cover(ndvi, nd_min=0.125, nd_max=0.8, vc_pow=0.7):
        r"""
        Computes vegetation cover based on NDVI

        math ::
            c_{veg} =
            \begin{cases}
            \begin{array}{cc}
            0 & I_{NDVI}\leq I_{NDVI,min}\\
            1-\left(\frac{I_{NDVI,max}-I_{NDVI}}{I_{NDVI,max}-I_{NDVI,min}}\right)^
            {a} & I_{NDVI,min}<I_{NDVI}<I_{NDVI,max}\\
            1 & I_{NDVI}\geq I_{NDVI,max}
            \end{array}\end{cases}

        Parameters
        ----------
        ndvi : np.ndarray or float
            Normalized Difference Vegetation Index
            :math:`I_{NDVI}`
            [-]
        nd_min : np.ndarray or float
            NDVI value where vegetation cover is 0
            :math:`I_{NDVI,min}`
            [-]
        nd_max : np.ndarray or float
            NDVI value where vegetation cover is 1
            :math:`I_{NDVI,max}`
            [-]
        vc_pow : np.ndarray or float
            Exponential power used in vegetation cover function
            :math:`a`
            [-]

        Returns
        -------
        vc : np.ndarray or float
            vegetation cover
            :math:`c_{veg}`
            [-]

        Examples
        --------
            LeafAnalysis.vegetation_cover(0.1, nd_min=0.2)

            LeafAnalysis.vegetation_cover(0.5)

            LeafAnalysis.vegetation_cover(0.85)


            plot:: pyplots/leaf/plot_vegetation_cover.py

        """

        res = np.array([])
        if np.isscalar(ndvi):

            if ndvi <= nd_min:
                res = 0
            if (ndvi > nd_min) & (ndvi < nd_max):
                res = 1 - ((nd_max - ndvi) / (nd_max - nd_min)) ** vc_pow
            if ndvi >= nd_max:
                res = 1

        else:

            # Create empty array
            res = np.ones(ndvi.shape) * np.nan

            # fill in array
            res[ndvi <= nd_min] = 0
            res[np.logical_and(ndvi > nd_min, ndvi < nd_max)] = 1 - (
                    (nd_max - ndvi[np.logical_and(ndvi > nd_min, ndvi < nd_max)]) / (nd_max - nd_min)) ** vc_pow
            res[ndvi >= nd_max] = 1

        return res

    @classmethod
    def leaf_area_index(cls, vc, vc_min=0.0, vc_max=None, lai_pow=-0.45):
        """
        Computes leaf area index based on vegetation cover. It is based on the
        Kustas formulation of LAI vs NDVI.

        Parameters
        ----------
        vc : np.ndarray or float
            vegetation cover
            :math:`c_{veg}`
            [-]
        vc_min : np.ndarray or float
            vegetation cover where LAI is 0
            :math:`c_{veg,min}`
            [-]
        vc_max : np.ndarray or float
            vegetation cover at maximum LAI
            :math:`c_{veg,max}`
            [-]
        lai_pow : np.ndarray or float
            exponential factor used in LAI function
            :math:`b`
            [-]

        Returns
        -------
        lai : np.ndarray or float
            leaf area index
            :math:`I_{lai}`
            [-]

        Examples
        --------
        LeafAnalysis.leaf_area_index(0.0)
        0
        LeafAnalysis.leaf_area_index(0.5)
        1.5403270679109895
        LeafAnalysis.leaf_area_index(1.0)
        7.6304274331264414

            plot:: pyplots/leaf/plot_leaf_area_index.py

        """
        res = np.array([])
        if vc_max is None:
            vc_max = cls.vegetation_cover(0.795)

        if np.isscalar(vc):
            if vc <= vc_min:
                res = 0
            if (vc > vc_min) & (vc < vc_max):
                res = np.log(-(vc - 1)) / lai_pow
            if vc >= vc_max:
                res = np.log(-(vc_max - 1)) / lai_pow

        else:
            # Create empty array
            res = np.ones(vc.shape) * np.nan

            # fill in array
            res[vc <= vc_min] = 0
            res[np.logical_and(vc > vc_min, vc < vc_max)] = np.log(
                -(vc[np.logical_and(vc > vc_min, vc < vc_max)] - 1)) / lai_pow
            res[vc >= vc_max] = np.log(-(vc_max - 1)) / lai_pow

        return res

    @staticmethod
    def effective_leaf_area_index(lai):
        r"""
        Computes effective leaf area index, this describes the leaf area which
        actively participates in transpiration. It is based on the actual leaf
        area index and an extinction function. So with a higher leaf area index the
        effective leaf area index is a smaller percentage of the total leaf area
        index.

        math ::
            I_{lai,eff}=\frac{I_{lai}}{0.3I_{lai}+1.2}

        Parameters
        ----------
        lai : np.ndarray or float
            Leaf area index
            :math:`I_{lai}`
            [-]

        Returns
        -------
        lai_eff : np.ndarray or float
            effective leaf area index
            :math:`I_{lai,eff}`
            [-]

        Examples
        --------
        LeafAnalysis.effective_leaf_area_index(3.0)
        1.4285714285714288
        LeafAnalysis.effective_leaf_area_index(5.0)
        1.8518518518518516


        """
        lai_eff = lai / ((0.3 * lai) + 1.2)
        return lai_eff

    @staticmethod
    def fpar(vc, ndvi):
        r"""
        Computes the fpar

        Parameters
        ----------
        vc : np.ndarray or float
            vegetation cover
            :math:`c_{veg}`
            [-]
        ndvi : np.ndarray or float
            Normalized Difference Vegetation Index
            :math:`I_{NDVI}`
            [-]

        Returns
        -------
        fpar : np.ndarray or float
            fpar
            :math:`I_{vc,ndvi}`
            [-]

        """
        fpar = 0.925 * vc
        fpar[ndvi < 0.1] = 0.0

        return fpar

    @staticmethod
    def apar(ra_24, fpar):
        r"""
        Computes the Aborbed Photosynthetical Active Radiation

        Parameters
        ----------
        ra_24 : np.ndarray or float
            daily solar radiation
            :math:`S^{\downarrow}`
            [Wm-2]
        fpar : np.ndarray or float
            fpar
            :math:`I_{vc,ndvi}`
            [-]

        Returns
        -------
        apar : np.ndarray or float
            apar
            :math:`I_{ra_24,fpar}`
            [MJ/m2]

        """
        par = 0.48 * ra_24 * 0.0864
        apar = par * fpar

        return apar
