import ee

from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.region import GEERegion
from digitalarztools.pipelines.gee.tags.merit import GEEMerit
from digitalarztools.pipelines.gee.tags.modis_daily_data import MODISDailyData


class GEEWater:
    @staticmethod
    def surface_water_using_jrc(band="max_extent", region: GEERegion = None) -> GEEImage:
        """
        https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_4_GlobalSurfaceWater
        recommended bands are max_extent for flood extent and
        occurrence to see how frequent water flow there
        bands are
        name        unit min max description
        occurrence	%	0	100
        The frequency with which water was present.

        change_abs	%	-100	100
        Absolute change in occurrence between two epochs: 1984-1999 vs 2000-2021.

        change_norm	%	-100	100
        Normalized change in occurrence. (epoch1-epoch2)/(epoch1+epoch2) * 100

        seasonality		0	12
        Number of months water is present.

        recurrence	%	0	100
        The frequency with which water returns from year to year.

        transition
        Categorical classification of change between first and last year.

        max_extent
        Binary image containing 1 anywhere water has ever been detected.
        @return:
        """
        dataset = ee.Image('JRC/GSW1_4/GlobalSurfaceWater')
        if region is not None:
            dataset.clip(region.aoi)
        selected_band = dataset.select(band)
        return GEEImage(selected_band)

    @classmethod
    def get_water_mask_jrc(cls, region: GEERegion) -> GEEImage:
        """
        https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_4_GlobalSurfaceWater
        recommended bands are max_extent for flood extent and
        occurrence to see how frequent water flow there
        bands are
        name        unit min max description
        occurrence	%	0	100
        The frequency with which water was present.

        change_abs	%	-100	100
        Absolute change in occurrence between two epochs: 1984-1999 vs 2000-2021.

        change_norm	%	-100	100
        Normalized change in occurrence. (epoch1-epoch2)/(epoch1+epoch2) * 100

        seasonality		0	12
        Number of months water is present.

        recurrence	%	0	100
        The frequency with which water returns from year to year.

        transition
        Categorical classification of change between first and last year.

        max_extent
        Binary image containing 1 anywhere water has ever been detected.
        @return:
        """
        selected_band = cls.surface_water_using_jrc("max_extent", region).image
        mask = selected_band.gt(0)
        masked_band = selected_band.updateMask(mask)
        return masked_band

    @staticmethod
    def get_combined_water_mask(region: GEERegion, date_range, include_merit=True) -> ee.Image:
        water_threshold: float = 0.1
        from digitalarztools.pipelines.gee.tags.sentinel import GEESentinelData
        # Get water masks from Sentinel-2 and MODIS
        # s2_water_masked = GEESentinelData.sentinel2_water_mask(
        #     region, date_range=date_range, water_threshold_s2=water_threshold
        # )  # Ensure single band

        modis_water_masked = MODISDailyData.get_water_masked(
            region, date_range=date_range, water_threshold=water_threshold
        )  # Ensure single band

        jrc_water_masked = GEEWater.get_water_mask_jrc(region)  # Ensure single band

        # Combine water masks from JRC, Sentinel-2, and MODIS
        combined_water_mask = ((jrc_water_masked.unmask(0).Or(
            #     s2_water_masked.unmask(0)
            # ).Or(
            modis_water_masked.unmask(0)
        )))
        if include_merit:
            merit_masked = GEEMerit.get_merit_water_mask(region)

            combined_water_mask = combined_water_mask.Or(
                merit_masked.unmask(0)
            )

        return combined_water_mask
