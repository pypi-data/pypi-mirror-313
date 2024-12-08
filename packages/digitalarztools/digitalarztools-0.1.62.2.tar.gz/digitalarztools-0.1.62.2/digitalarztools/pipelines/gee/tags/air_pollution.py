import ee

from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.image_collection import GEEImageCollection
from digitalarztools.pipelines.gee.core.region import GEERegion


class AirPollution():
    @staticmethod
    def get_s5_ch4(region:GEERegion, date_range:tuple) -> GEEImage:
        """
        :param region: GEERegion
        :param date_range: ('YYYY-MM-DD', 'YYYY-MM-DD')
        Mol fraction	1285*	2405*	Column-averaged dry air mixing ratio of methane, as parts-per-billion
        Resolution 1113.2 meters
        :return:
        """
        collection = GEEImageCollection(ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CH4')
                      .select('CH4_column_volume_mixing_ratio_dry_air')
                      .filterDate(date_range[0], date_range[1]))
        gee_image = GEEImage(collection.get_image('mean'))
        return gee_image

    @staticmethod
    def get_s5_so2(region:GEERegion, date_range: tuple) ->GEEImage:
        """
        :param region: GEERegion
        :param date_range: ('YYYY-MM-DD', 'YYYY-MM-DD')
        mol/m^2	-0.4051*	0.2079*	 SO2 vertical column density at ground level, calculated using the DOAS technique.
        Resolution 1113.2 meters
        :return:
        """
        collection = GEEImageCollection(ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_SO2")
                                        .select('SO2_column_number_density')
                                        .filterBounds(region.bounds)
                                        .filterDate(date_range[0], date_range[1]))
        gee_image = GEEImage(collection.get_image('mean'))
        return gee_image

    def get_s5_co(region:GEERegion, date_range: tuple) ->GEEImage:
        """
        :param region: GEERegion
        :param date_range: ('YYYY-MM-DD', 'YYYY-MM-DD')
        mol/m^2	-34.43*	5.71* Vertically integrated CO column density.
        Resolution 1113.2 meters
        :return:
        """
        collection = GEEImageCollection(ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CO")
                                        .select('CO_column_number_density')
                                        .filterBounds(region.bounds)
                                        .filterDate(date_range[0], date_range[1]))
        gee_image = GEEImage(collection.get_image('mean'))
        return gee_image

