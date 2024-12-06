import os.path

from geopandas import GeoDataFrame

from digitalarztools.adapters.data_manager import DataManager
from digitalarztools.io.file_io import FileIO
from digitalarztools.io.raster.band_process import BandProcess
from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.io.vector.gpd_vector import GPDVector


class RioRasterCollection:
    def __init__(self, imagery_folder):
        self.imagery_folder = imagery_folder

    def get_rasters_fp(self):
        fps = FileIO.list_files_in_folder(self.imagery_folder, ext="tif")
        # rasters = [RioRaster(fp) for fp in fps]
        return fps

    def calculates_stats(self, base_name: str, aoi_gdf: GeoDataFrame = None, purpose: str = None) -> DataManager:
        """
        @param base_name:  for datamanager
        @param aoi_gdf:  it should have single geometry if not function will use unary union to combine all
        @param purpose:
        @return:
        """
        dm_base_folder = os.path.join(self.imagery_folder, "raster_stats")
        data_manager = DataManager(dm_base_folder, base_name, purpose)
        union_gdf = GPDVector.get_unary_union_gdf(aoi_gdf)
        geom = union_gdf.geometry.values[0]
        for fp in self.get_rasters_fp():
            raster = RioRaster(fp)
            raster.clip_raster(union_gdf)

            for i in range(raster.get_spectral_resolution()):
                stats = BandProcess.get_summary_data(raster.get_data_array(i + 1))
                stats["file_path"] = os.path.relpath(fp, self.imagery_folder)
                stats["file_name"] = os.path.basename(fp)
                fn, ext = FileIO.get_file_name_ext(fp)
                data_manager.add_record(fn, stats, geom=geom.wkb)
        return data_manager

    def get_stats_data_manager(self, base_name: str):
        dm_base_folder = os.path.join(self.imagery_folder, "raster_stats")
        data_manager = DataManager(dm_base_folder, base_name)
        return data_manager
