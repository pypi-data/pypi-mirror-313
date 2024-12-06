import ee

from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.image_collection import GEEImageCollection
from digitalarztools.pipelines.gee.core.region import GEERegion


class GEESurfaceRunoff:
    @classmethod
    def surface_runoff_from_era5_daily(cls, region: GEERegion, no_of_days=7, end_date=None, mask_threshold=0):
        date_range = GEEImageCollection.calculate_date_range(no_of_days * 10, end_date)
        img_collection = (ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
                          .select("surface_runoff_sum")
                          .filterDate(date_range[0], date_range[1])
                          .filterBounds(region.aoi)
                          .sort('system:time_start', False).limit(no_of_days))

        # Calculate the 16-day total precipitation. and multiply by 1000 to convert m into mm
        surface_runoff = img_collection.max().multiply(1000).rename('total_precipitation')

        # Create a mask for areas with precipitation greater than 10mm.
        mask = surface_runoff.gt(mask_threshold)

        # Update the precipitation image with the mask.
        masked_img = surface_runoff.updateMask(mask)

        return masked_img

    @classmethod
    def get_vis_parameters(cls):
        vis_parameter = {
            'min': 0.5,
            'max': 2,
            'palette':['#0000FF', '#00FFFF', '#FFFF00', '#FFA500', '#FF0000']  # ['blue', 'cyan', 'yellow', 'orange', 'red']
        }
        return vis_parameter

    @classmethod
    def get_surface_runoff_url(cls, region: GEERegion, end_date=None, no_of_days=7):
        # masked_img = cls.get_accumulated_precipitation_from_chirps2(region, no_of_days=no_of_days, end_date=end_date,
        #                                                             mask_threshold=5)
        vis_params = cls.get_vis_parameters()

        masked_img = cls.surface_runoff_from_era5_daily(region=region, no_of_days=no_of_days,
                                                        end_date=end_date,mask_threshold=vis_params['min'])
        url = GEEImage.get_imgae_url(masked_img, vis_params)
        print(url)
        return url
