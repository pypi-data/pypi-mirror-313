import ee

from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.image_collection import GEEImageCollection
from digitalarztools.pipelines.gee.core.region import GEERegion
from digitalarztools.utils.logger import da_logger


class GEESoilMoisture:
    """
    SMAP information: https://developers.google.com/earth-engine/tutorials/community/smap-soil-moisture
    Datasets: https://developers.google.com/earth-engine/datasets/catalog/NASA_SMAP_SPL4SMGP_007#bands
    """
    region: GEERegion
    gee_region: GEEImage
    band_name: str

    def __init__(self, is_initialized, region: GEERegion, start_date, end_date, how='latest', band="sm_surface"):
        if is_initialized:
            self.band_name = band
            self.region = region
            self.gee_region = self.smap_data_using_gee(region, start_date, end_date, how, band)
        else:
            da_logger.error("Please initialized GEE before further processing")

    @staticmethod
    def smap_data_using_gee(region, start_date=None, end_date=None, how='max', bands=("sm_surface",), no_of_days=5) -> GEEImage:
        """
        https://developers.google.com/earth-engine/datasets/catalog/NASA_SMAP_SPL4SMGP_007#bands
         :param region:
        :param start_date: (YYYY-MM-DD) start
        :param end_date: (YYYY-MM-DD) end
        :param how: choices are 'median', 'max', 'mean', 'first', 'cloud_cover', 'latest', 'oldest'
        :param bands: choices are sm_surface, sm_rootzone,sm_profile etc. see detail in above url
        :param no_of_days: if both start and end date is None pass no_of_days
        :return: GEEImage
        """
        img_collection = (ee.ImageCollection("NASA/SMAP/SPL4SMGP/007")
                          .filterBounds(region.aoi))
        if end_date is None:
            end_date = GEEImageCollection.get_collection_max_date(img_collection)
            date_range = GEEImageCollection.calculate_date_range(no_of_days=no_of_days,end_date=end_date)
        elif start_date is None:
            date_range = GEEImageCollection.calculate_date_range(no_of_days=no_of_days, end_date=end_date)
        else:
            date_range = (start_date, end_date)
        start_date = ee.Date(date_range[0])
        end_date = ee.Date(date_range[1])

        img_collection = img_collection.filterDate(start_date, end_date)
        img_collection = img_collection.select(bands)
        return GEEImage(GEEImageCollection(img_collection).get_image(how))

    def convert_volumetric_fraction_to_mm(self):
        # Set your assumptions

        if self.band_name == "sm_surface":
            root_zone_depth = 50  # Top 5 cm soil layer = 50 mm
        elif self.band_name == "sm_rootzone":
            root_zone_depth = 1000  # Top 100 cm soil layer = 1000 mm
        else:
            root_zone_depth = 0
        if root_zone_depth != 0:
            image = self.gee_region.image
            # # Calculate soil moisture depth in mm (simplified calculation)
            # smd_image = image.multiply(root_zone_depth)
            # Load and prepare soil density image
            soil_density_image = ee.Image(
                "OpenLandMap/SOL/SOL_BULKDENS-FINEEARTH_USDA-4A1H_M_v02"
            )
            soil_density_image = soil_density_image.resample("bilinear").reproject(
                crs=image.projection(), scale=image.projection().nominalScale()
            )
            # Extract soil density values
            soil_density_values = soil_density_image.select("b0")
            # Calculate soil moisture depth with soil density
            particle_density = 2.65  # Assumed value for most mineral soils
            smd_image = image.multiply(root_zone_depth).multiply(
                1 - soil_density_values.divide(particle_density)
            )
            return smd_image
    @staticmethod
    def get_vis_params():
        vis_params = {
            'min': 0.1,  # Minimum value of soil moisture to map
            'max': 0.5,  # Maximum value of soil moisture to map
            'palette': ['blue', 'cyan', 'green', 'yellow', 'red']  # Color gradient for visualization
        }
        return vis_params

    @classmethod
    def get_soil_moisture_url(cls, region: GEERegion,):
        vis_params = cls.get_vis_params()
        sm_img = cls.smap_data_using_gee(region,how='latest')
        # Create a mask for areas with precipitation greater than 10mm.
        mask = sm_img.image.gt(vis_params['min'])

        # Update the precipitation image with the mask.
        masked_img = sm_img.image.updateMask(mask)

        url = GEEImage.get_imgae_url(masked_img, vis_params)
