import enum
from datetime import datetime, timedelta

import ee

from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.image_collection import GEEImageCollection
from digitalarztools.pipelines.gee.core.region import GEERegion
from digitalarztools.pipelines.gee.tags.water import GEEWater
from digitalarztools.proccessing.operations.thresholds import calculate_otsu_threshold


class GEESentinelTag(enum.Enum):
    SENTINEL1 = 'COPERNICUS/S1_GRD'
    SENTINEL2 = 'COPERNICUS/S2'
    SENTINEL2_SURFACE_REFLECTANCE = "COPERNICUS/S2_SR_HARMONIZED"
    SENTINEL2_TOA = 'COPERNICUS/S2_HARMONIZED'
    SENTINEL3 = "COPERNICUS/S3/OLCI"
    SENTINEL5_CH4 = "COPERNICUS/S5P/OFFL/L3_CH4"


class GEESentinelData:

    @staticmethod
    def get_sentinel_image_collection(region: GEERegion, tag: GEESentinelTag, is_water_related_study=True) -> GEEImageCollection:
        coll =  ee.ImageCollection(tag.value).filterBounds(region.bounds)
        if tag==GEESentinelTag.SENTINEL1 and  is_water_related_study:
            coll = coll.filter(ee.Filter.eq('instrumentMode', 'IW'))
        return GEEImageCollection(coll)

    @classmethod
    def get_latest_dates(cls, dataset_tag: GEESentinelTag , region: GEERegion, delta_in_days=10 ) -> (
            str, str):
        # Calculate the date range for the latest 10 days
        if dataset_tag is None:
            end_date = datetime.now()
        else:
            ee_img_coll = cls.get_sentinel_image_collection(region, dataset_tag)
            end_date = GEEImageCollection.get_collection_max_date(ee_img_coll.img_collection)
        start_date = end_date - timedelta(days=delta_in_days)

        # Convert dates to strings formatted as required by the Earth Engine API
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    @staticmethod
    def sentinel1_water_mask(region: GEERegion, date_range: tuple, water_masked_s2=None):
        """
        Identifies water bodies using Sentinel-1 SAR data for a specified region and date range.

        @param region: GEERegion object containing the region of interest and bounds.
        @param date_range: Tuple of start and end dates like ('2021-01-01', '2021-12-31').
        @param water_masked_s2: Optional water mask from Sentinel-2 or another source to refine the result.
        @return: Masked water bodies layer clipped to the region of interest.
        """
        polarization = 'VV'

        # Load Sentinel-1 SAR data
        sentinel1_coll = ee.ImageCollection(GEESentinelTag.SENTINEL1.value) \
            .filterBounds(region.bounds) \
            .filterDate(date_range[0], date_range[1])\
            .filter(ee.Filter.eq('instrumentMode', 'IW'))
            # .filter(ee.Filter.eq('resolution_meters', 10)) \
            # .filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING')) \
        sentinel1_coll = sentinel1_coll.select(polarization)

        # Ensure the collection has images
        if sentinel1_coll.size().getInfo() == 0:
            raise ValueError("No Sentinel-1 images available for the specified date range and region.")

        # Compute the median of the image collection
        median = sentinel1_coll.median()

        # Set the default threshold value
        s1_water_threshold = -16  # Adjust threshold for local conditions if needed

        # Calculate water threshold using a provided water mask if available
        if water_masked_s2 is not None:
            masked_s1 = median.updateMask(water_masked_s2)
            stats = masked_s1.reduceRegion(
                reducer=ee.Reducer.mean(),  # Mean value of the masked Sentinel-1 image
                geometry=region.bounds,
                scale=100,
                maxPixels=1e13
            )

            # Attempt to fetch the computed mean from Earth Engine
            try:
                s1_water_threshold = stats.get(polarization).getInfo()
            except Exception as e:
                print(f"Error fetching threshold from Sentinel-1 data: {e}")
                raise

        # Print the determined threshold for water detection
        print(f"Threshold for water detection: {s1_water_threshold}")

        # Apply the threshold to identify water bodies
        water = median.lt(s1_water_threshold)

        # Mask the water layer and clip it to the region of interest (AOI)
        water_masked = water.updateMask(water).clip(region.aoi)

        return water_masked

    @staticmethod
    def sentinel2_water_mask(region: GEERegion, date_range: tuple, water_threshold_s2: float = 0.1) -> ee.Image:
        """
           @param region:
           @param date_range: range of date with start and end value like ('2021-01-01', '2021-12-31')
           @param water_threshold: should be less than 0.5 as indices is between 0 - 1
           @return:
         """
        # Load and process Sentinel-2 optical data
        sentinel2 = ee.ImageCollection(GEESentinelTag.SENTINEL2.value) \
            .filterBounds(region.bounds) \
            .filterDate(date_range[0], date_range[1]) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .select(['B3', 'B11'])  # Green and SWIR bands for MNDWI
        # .select(['B3', 'B8'])  # Green and NIR bands for NDWI

        # Compute the median of the Sentinel-2 image collection
        median_s2 = sentinel2.median()

        # Calculate NDWI (Normalized Difference Water Index)
        # ndwi = median_s2.normalizedDifference(['B3', 'B8'])
        # Calculate MNDWI (Modified Normalized Difference Water Index)
        mndwi = median_s2.normalizedDifference(['B3', 'B11'])

        # histogram, values, frequencies = GEEImage.get_histogram(mndwi, region.bounds, 10)

        # Calculate Otsu threshold
        # water_threshold_s2 = calculate_otsu_threshold(values, frequencies)
        # print("otsu threshold", otsu_threshold)

        # Apply a threshold to identify water bodies in Sentinel-2
        # water_threshold_s2 = 0.01  # Adjust threshold for local conditions
        # water_s2 = ndwi.gt(water_threshold_s2)
        water_mask = mndwi.gt(water_threshold_s2)

        # Mask the water layer to only include the AOI
        water_masked_s2 = mndwi.updateMask(water_mask).clip(region.aoi)

        return water_masked_s2

    @staticmethod
    def get_water_mask_vis_params():
        return {'palette': ['#0000cc']}

    @staticmethod
    def get_water_level_vis_params():
        # ['sky blue', 'dark blue', 'mahroon']
        return {'min': -1, 'max': 1, 'palette': ['#87CEEB', '#0000cc', '#800000']}

    @classmethod
    def combined_water_mask(cls, region: GEERegion, date_range: tuple = None):
        """
        @param region:
        @param date_range: range of date with start and end value like ('2021-01-01', '2021-12-31')
        @return:
        """
        water_masked_s2 = cls.sentinel2_water_mask(region, date_range)
        water_masked_s1 = cls.sentinel1_water_mask(region, date_range, water_masked_s2)

        # Combine water masks from Sentinel-1 and Sentinel-2
        combined_water = water_masked_s1.unmask(0).Or(water_masked_s2.unmask(0))
        return combined_water.updateMask(combined_water)

    @classmethod
    def get_water_mask_url(cls, region: GEERegion, date_range: tuple = None):
        """
        @param region:
        @param date_range: range of date with start and end value like ('2021-01-01', '2021-12-31')
        @return:
        """
        if date_range is None:
            date_range = GEEImageCollection.calculate_date_range(20)

        # water_masked = cls.sentinel2_water_mask(region, date_range)
        water_masked = cls.combined_water_mask(region, date_range)
        vis_params = cls.get_water_mask_vis_params()
        url = water_masked.getMapId(vis_params)
        return url['tile_fetcher'].url_format

    @staticmethod
    def get_water_level_using_change_detection_sentinel_1(region: GEERegion, water_mask: ee.Image,
                                                          before_date_range: tuple,
                                                          after_date_range: tuple,
                                                          calibration_factor: float = None) -> ee.Image:
        """
        Detect water level changes using Sentinel-1 SAR data and a water mask.

        @param region: GEERegion defining the area of interest.
        @param water_mask: ee.Image representing the water bodies mask.
        @param before_date_range: Tuple with start and end date for the pre-event period.
        @param after_date_range: Tuple with start and end date for the post-event period.
        @param calibration_factor: The conversion factor to relate dB to meters (if None, conversion is not applied).
            Calibration Factor (needs to be determined through empirical analysis)
            multiply this factor will convert db of back scattering into meter
            For indus basin
            Studies in similar regions often suggest that the relationship
            between dB changes and water level changes can vary widely.
            A general rule of thumb for flat, less vegetated areas might
            be around 0.03 meters per dB, while more complex terrain
            might require a calibration factor of up to 0.10 meters per dB.

        @return: ee.Image representing water level changes (in millimeters if conversion is applied).
        """

        polarization = 'VV'
        sentinel1_collection = (ee.ImageCollection('COPERNICUS/S1_GRD')
                                .filterBounds(region.bounds)
                                .filter(ee.Filter.listContains('transmitterReceiverPolarisation', polarization))
                                .filter(ee.Filter.eq('instrumentMode', 'IW'))
                                .select(polarization))

        after_collection = sentinel1_collection.filterDate(after_date_range[0], after_date_range[1])
        before_collection = sentinel1_collection.filterDate(before_date_range[0], before_date_range[1])

        # Calculate the sum for each period
        before_img = before_collection.sum()
        after_img = after_collection.sum()


        # Calculate the difference in backscatter, adding a small constant (e.g., 0.01)
        epsilon = 0.01
        difference_image = after_img.subtract(before_img).add(epsilon)

        if calibration_factor is not None:
            """
            Apply Linear Scale Conversion
            Linear scale=pow(10,10/dB_value)
            Physical change(meters) =Linear scale × Calibration factor
            """

            # db_to_mm_img = difference_image.expression(
            #     '1000 * (10 ** (diffImage / 10)) * calibFactor',
            #     {
            #         'diffImage': difference_image,
            #         'calibFactor': calibration_factor
            #     }
            # )
            """
            Direct Conversion Using Calibration Factor
            Physical change(meters) =Linear scale × Calibration factor
            """

            db_to_mm_img = difference_image.multiply(calibration_factor).multiply(1000)
            db_to_mm_img = db_to_mm_img.abs()
            return db_to_mm_img.updateMask(water_mask)
        else:
            # Return the difference image without conversion
            return difference_image.updateMask(water_mask)

    @classmethod
    def get_water_level_image(cls, region: GEERegion, end_date: datetime = None, include_merit=False,
                              water_mask=True, calibration_factor: float = None) -> ee.Image:
        """
        @param region:
        @param end_date:
        @param include_merit:
        @param water_mask:
        @param calibration_factor: from 0.03 to 0.10 to convert db to meter
        @return: ee.Image
        """
        if end_date is None:
            end_date = datetime.today()
        after_date_range = GEEImageCollection.calculate_date_range(20, end_date=end_date)
        before_end_date = datetime.strptime(after_date_range[0], '%Y-%m-%d')
        before_date_range = GEEImageCollection.calculate_date_range(20, end_date=before_end_date)
        # date_range = (before_date_range[0], after_date_range[1])

        # water_masked = cls.sentinel2_water_mask(region, before_date_range)
        # water_masked = cls.combined_water_mask(region, date_range)
        # water_masked = GEEWater.get_water_mask_jrc(region)
        if water_mask:
            water_masked = GEEWater.get_combined_water_mask(region, before_date_range, include_merit)
        else:
            water_masked = ee.Image(1)
        water_level_change_image = cls.get_water_level_using_change_detection_sentinel_1(region, water_masked,
                                                                                         before_date_range,
                                                                                         after_date_range,
                                                                                         calibration_factor=calibration_factor)
        water_level_change_image.clip(region.aoi)
        return water_level_change_image

    @classmethod
    def get_water_level_url(cls, region: GEERegion, end_date: datetime = None):
        """
        @param region:
        @param end_date:
        @return:
        """
        water_level_change_image = cls.get_water_level_image(region)
        vis_params = cls.get_water_level_vis_params()
        url = water_level_change_image.getMapId(vis_params)
        return url['tile_fetcher'].url_format

    @classmethod
    def get_latest_date(cls, region: GEERegion, sen_tag: GEESentinelTag = GEESentinelTag.SENTINEL1):
        date_range = GEEImageCollection.calculate_date_range()
        img_collection = GEEImageCollection(ee.ImageCollection(sen_tag.value)
                                            .filterBounds(region.bounds)
                                            .filterDate(date_range[0], date_range[1])
                                            )

        img = img_collection.get_image(how='latest')
        img = img.clip(region.bounds)
        # date = img_collection.get_latest_image_date()
        date = GEEImage.get_image_date(img)
        return date
