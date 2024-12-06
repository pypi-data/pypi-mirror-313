import ee

from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.region import GEERegion


class GEESoilAnalysis:
    """
    Analaysis using OpenLand Map
    https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_SAND-WFRACTION_USDA-3A1A1A_M_v02
    """
    @staticmethod
    def calculate_field_capacity(region: GEERegion) ->GEEImage:
        """"
        Calculate field capacity using the Saxton and Rawls (2006) formula
        FC=0.7919+0.001691⋅C−0.29619⋅S−0.000001491⋅(Si^2)+0.0000821⋅(C^2)+0.02427⋅(1/S )+0.01113⋅log(Si)

        where:
            FC is the soil field capacity (volumetric water content, m³/m³).
            S is the sand content (fraction).
            Si is the silt content (fraction).
            C is the clay content (fraction)
        """
        aoi = region.get_aoi()

        # Load the OpenLandMap soil texture datasets for sand, silt, and clay
        # Load the correct OpenLandMap datasets for sand and clay
        sand = ee.Image('OpenLandMap/SOL/SOL_SAND-WFRACTION_USDA-3A1A1A_M/v02').select('mean').clip(aoi)
        clay = ee.Image('OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02').select('mean').clip(aoi)

        # silt = ee.Image('OpenLandMap/SOL/SOL_TEXTURE-SILT_USDA-3A1A1B_M/v02').select('b0').clip(aoi)
        # Calculate silt as the remaining fraction, handling voids
        silt = ee.Image(100).subtract(sand.add(clay)).max(0)

        # Convert percentages to fractions
        sand_frac = sand.divide(100)
        silt_frac = silt.divide(100)
        clay_frac = clay.divide(100)
        # Calculate field capacity using the Saxton and Rawls (2006) formula
        field_capacity = (
            ee.Image(0.7919)
            .add(clay_frac.multiply(0.001691))
            .subtract(sand_frac.multiply(0.29619))
            .subtract(silt_frac.pow(2).multiply(0.000001491))
            .add(clay_frac.pow(2).multiply(0.0000821))
            .add(sand_frac.pow(-1).multiply(0.02427))
            .add(silt_frac.log().multiply(0.01113))
        )
        return GEEImage(field_capacity)

