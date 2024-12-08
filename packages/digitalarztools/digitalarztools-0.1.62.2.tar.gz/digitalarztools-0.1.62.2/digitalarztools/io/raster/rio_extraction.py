import os

from digitalarztools.pipelines.gee.core.feature_collection import GEEFeatureCollection
from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.image_collection import GEEImageCollection
from digitalarztools.pipelines.gee.core.region import GEERegion
from digitalarztools.io.raster.rio_raster import RioRaster


class RioExtraction:
    @staticmethod
    def get_gee_s2_ndvi_image(file_path: str, aoi_path: str, date_range: tuple,
                              dataset_name: str = 's2', spatial_res: int = None):
        """
        :param file_path:
        :param aoi_path:
        :param date_range: tuple
            range of date with start and end value like ('2021-01-01', '2021-12-31')
            example:
                start_date, end_date = DateUtils.get_date_range(no_of_days=180)
                date_range = (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        :param dataset_name: str
            key of datasets consist of s2, ls
        :param spatial_res:
        :return:
        """
        datasets = {
            "s2": {"name": 'COPERNICUS/S2_SR', "spatial_res": 10}
        }
        if spatial_res is None:
            spatial_res = datasets[dataset_name]["spatial_res"]
        if not os.path.exists(file_path):

            gee_fc = GEEFeatureCollection.from_shapefile(aoi_path)
            gee_region = GEERegion.from_feature_collection(gee_fc.fc)
            gee_img_collection = GEEImageCollection(gee_region,
                                                    datasets[dataset_name]["name"],
                                                    date_range=date_range)
            gee_img_collection.add_bands(['mask_cloud', 'NDVI'])
            gee_img_collection.select_bands(['NDVI'])
            ndvi = gee_img_collection.get_image(how='max')
            # ndvi = GEEIndices.get_ndvi(img)
            gee_img = GEEImage(ndvi)
            gee_img.download_image(file_path, scale=spatial_res, img_region=gee_region)
            return RioRaster(file_path)

        else:
            return RioRaster(file_path)
