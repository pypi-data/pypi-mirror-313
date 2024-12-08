import ee
import geopandas as gpd
from pyproj import CRS

from digitalarztools.io.file_io import FileIO
from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.pipelines.gee.core.auth import GEEAuth
from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.region import GEERegion
from digitalarztools.proccessing.operations.geodesy import GeodesyOps


class GEEMerit:
    """
    Merit dataset from https://developers.google.com/earth-engine/datasets/catalog/MERIT_Hydro_v1_0_1#bands
    """

    def __init__(self, fp: str, aoi: gpd.GeoDataFrame = None, utm_reproject:bool = False):
        """
        :param fp: file path of merit data in 4326
        :param aoi: in GeoDataFrame
        """
        self.raster = RioRaster(fp)
        if aoi is not None:
            self.raster.clip_raster(aoi, in_place=True)
        if utm_reproject:
            utm_srid = GeodesyOps.utm_srid_from_extent(*self.raster.get_raster_extent())
            crs = CRS.from_epsg(utm_srid)
            self.raster.reproject_raster(crs, in_place=True)


    @staticmethod
    def download_data(fp: str, region: GEERegion, band = None):
        """
        Download the file
        @param gee_auth: GEEAuth object
        @param fp: file path of merit data in 4326
        @param region: GEERegion object
        """
        dirname = FileIO.mkdirs(fp)

        dataset = ee.Image('MERIT/Hydro/v1_0_1')  # .clip(region.get_aoi())
        if band is not None:
            dataset = dataset.select(band)

        gee_img = GEEImage(dataset)
        gee_img.download_image(fp, region, scale=90, bit_depth=32, within_aoi_only=False)
        print("download complete at ", fp)

    def get_dem(self, output_fp: str = None, resolution_in_meter: int = -1) -> RioRaster:
        """
        dem is at band 1 and height is in meter
        :param output_fp: path of file to same
        """
        dem_arr = self.raster.get_data_array(1)
        dem_raster = self.raster.rio_raster_from_array(dem_arr)
        if resolution_in_meter != -1:
            res = GeodesyOps.meter_2_dd(resolution_in_meter)  if dem_raster.get_crs().is_geographic else resolution_in_meter
            print(res)
            dem_raster.resample_raster_res(res)

        if output_fp is not None:
            dem_raster.save_to_file(output_fp)
        return dem_raster

    def get_direction_raster(self, output_fp: str = None) -> RioRaster:
        """
        direction_raster is at band 2
        Flow Direction (Local Drainage Direction)
                1: east
                2: southeast
                4: south
                8: southwest
                16: west
                32: northwest
                64: north
                128: northeast
                0: river mouth
                -1: inland depression
        :param output_fp: path of file to same
        """
        dem_arr = self.raster.get_data_array(2)
        dem_raster = self.raster.rio_raster_from_array(dem_arr)
        if output_fp is not None:
            dem_raster.save_to_file(output_fp)
        return dem_raster

    def get_river_mouth(self) -> gpd.GeoDataFrame:
        """
        direction_raster is at band 2
        Flow Direction (Local Drainage Direction)
                1: east
                2: southeast
                4: south
                8: southwest
                16: west
                32: northwest
                64: north
                128: northeast
                0: river mouth
                -1: inland depression
        """
        gdf = self.raster.raster_2_vector(2, classes=[0])
        return gdf

    def get_river_channel_width(self, output_fp: str = None) -> RioRaster:
        """
        river channel width is at band 3
        River channel width at the channel centerlines. River channel width is calculated
        by the method described in [Yamazaki et al. 2012, WRR], with some improvements/changes on the algorithm.
        :param output_fp: path of file to same
        """
        dem_arr = self.raster.get_data_array(3)
        dem_raster = self.raster.rio_raster_from_array(dem_arr)
        if output_fp is not None:
            dem_raster.save_to_file(output_fp)
        return dem_raster

    def get_stream_raster(self) -> RioRaster:
        """
        water surface is at band 4
            Land and permanent water

            0: Land
            1: permanent water
        """
        dem_arr = self.raster.get_data_array(4)
        dem_raster = self.raster.rio_raster_from_array(dem_arr)
        return dem_raster

    def get_water_area(self) -> gpd.GeoDataFrame:
        """
        water surface is at band 4
            Land and permanent water

            0: Land
            1: permanent water
        """
        gdf = self.raster.raster_2_vector(4, classes=[1])
        return gdf

    def get_upstream_drainage_area(self, output_fp: str = None) -> RioRaster:
        """
        Upstream drainage area (flow accumulation area) is at band 5
        :param output_fp: path of file to same
        """
        dem_arr = self.raster.get_data_array(5)
        dem_raster = self.raster.rio_raster_from_array(dem_arr)
        if output_fp is not None:
            dem_raster.save_to_file(output_fp)
        return dem_raster

    def get_upstream_drainage_pixel(self, output_fp: str = None) -> RioRaster:
        """
        Upstream drainage pixel (flow accumulation grid).is at band 6
        :param output_fp: path of file to same
        """
        dem_arr = self.raster.get_data_array(6)
        dem_raster = self.raster.rio_raster_from_array(dem_arr)
        if output_fp is not None:
            dem_raster.save_to_file(output_fp)
        return dem_raster

    def get_hydro_adjusted_elev(self, output_fp: str = None)->RioRaster:
        """
        Hydrologically adjusted elevations, also know as "hand" at band 7 (height above the
        nearest drainage). The elevations are adjusted to satisfy the condition
        "downstream is not higher than its upstream" while minimizing the required modifications
        from the original DEM. The elevation above EGM96 geoid is represented in meters,
        and the vertical increment is set to 10cm.
        For detailed method, see [Yamazaki et al., 2012, WRR].
        :param output_fp: path of file to same
        """
        dem_arr = self.raster.get_data_array(7)
        dem_raster = self.raster.rio_raster_from_array(dem_arr)
        if output_fp is not None:
            dem_raster.save_to_file(output_fp)
        return dem_raster

    def get_vis_river_channel_width(self, output_fp: str = None) -> RioRaster:
        """
        Visualization of the river channel width..is at band 8
        :param output_fp: path of file to same
        """
        dem_arr = self.raster.get_data_array(8)
        dem_raster = self.raster.rio_raster_from_array(dem_arr)
        if output_fp is not None:
            dem_raster.save_to_file(output_fp)
        return dem_raster

    @staticmethod
    def get_merit_water_mask(region: GEERegion) -> ee.Image:
        # Load the MERIT Hydro dataset
        dataset = ee.Image('MERIT/Hydro/v1_0_1').clip(region.aoi)

        # Select the 'wth' band (Water bodies)
        selected_band = dataset.select('wth')

        # Create a binary water mask
        mask = selected_band.gt(0)

        # Apply the mask
        masked_band = selected_band.updateMask(mask)

        return masked_band

