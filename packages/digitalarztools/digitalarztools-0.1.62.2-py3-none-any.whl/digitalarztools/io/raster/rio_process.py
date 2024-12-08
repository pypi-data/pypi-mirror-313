import os
import geopandas as gpd
from pathlib import Path

import numpy as np
import rasterio
from rasterio import DatasetReader, MemoryFile, Env
from rasterio.merge import merge
from shapely.geometry import box
from skimage import color
from skimage.transform import rescale
from osgeo import gdal

from digitalarztools.io.file_io import FileIO
from digitalarztools.io.raster.band_process import BandProcess
from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.io.vector.gpd_vector import GPDVector


class RioProcess:
    def __init__(self):
        pass

    @staticmethod
    def read_raster_ds(img_folder: str):
        ds_files: [DatasetReader] = []
        path = Path(img_folder)
        issues_folder = os.path.join(img_folder, "issue_in_files")
        FileIO.mkdirs(issues_folder)
        FileIO.get_file_count(img_folder)
        # test = [str(p) for p in path.iterdir() if p.suffix == ".tif"]
        # ds_files = []
        for p in path.iterdir():
            if p.suffix == ".tif":
                try:
                    ds_files.append(RioRaster(str(p)).get_dataset())
                except Exception as e:
                    print(str(e))
                    FileIO.mvFile(str(p), issues_folder)
        return ds_files

    @staticmethod
    def filter_images_by_aoi_gdal(img_folder, aoi_gdf):
        """Filters the raster images that intersect the AOI using GDAL."""
        relevant_images = []

        for img_file in os.listdir(img_folder):
            if img_file.endswith('.tif'):
                img_path = os.path.join(img_folder, img_file)

                # Open the raster dataset
                raster_ds = gdal.Open(img_path)
                if raster_ds is None:
                    print(f"Failed to open {img_file}")
                    continue

                # Get the bounding box (georeference extent) of the raster
                transform = raster_ds.GetGeoTransform()
                x_min = transform[0]
                x_max = x_min + (raster_ds.RasterXSize * transform[1])
                y_min = transform[3] + (raster_ds.RasterYSize * transform[5])
                y_max = transform[3]
                raster_bbox = box(x_min, y_min, x_max, y_max)

                # Check if raster bounding box intersects with AOI
                if aoi_gdf.unary_union.intersects(raster_bbox):
                    relevant_images.append(img_path)

        return relevant_images

    @classmethod
    def mosaic_images_gdal(cls, input_folder, output_file, aoi_gdf: gpd.GeoDataFrame):

        # Collect all .tif files in the folder
        # input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.tif')]
        input_files = cls.filter_images_by_aoi_gdal(input_folder, aoi_gdf)
        # Open all the input files
        vrt_options = gdal.BuildVRTOptions(resampleAlg='bilinear')  # Customize resampling method if needed
        vrt = gdal.BuildVRT('/vsimem/temp.vrt', input_files, options=vrt_options)  # Create virtual raster

        # Translate the virtual raster to GeoTIFF
        gdal.Translate(output_file, vrt)

        # Clean up the virtual file
        gdal.Unlink('/vsimem/temp.vrt')

        print(f'Mosaic saved to {output_file}')

    @classmethod
    def mosaic_images(cls, img_folder: str = None, ds_files: [DatasetReader] = []) -> RioRaster:
        is_limit_changed = False
        if img_folder is not None:
            count =  FileIO.get_file_count(img_folder)
            soft, hard = FileIO.get_file_reading_limit()
            # print("soft", soft, "hard", hard)
            if count > soft:
                if count * 2 < hard:
                    """
                    default limit is  soft: 12544 hard:9223372036854775807
                    """
                    FileIO.set_file_reading_limit(count * 2)
                    is_limit_changed = True
                else:
                    raise IOError(f"you are trying to read {count} files. Cannot read more than {hard} files.")
            ds_files = cls.read_raster_ds(img_folder)
            # problem_files.append(str(p))
        if len(ds_files) > 0:
            with Env(CHECK_DISK_FREE_SPACE=False):
                mosaic, out_trans = merge(ds_files)
                crs = ds_files[0].crs
                raster = RioRaster.raster_from_array(mosaic, crs=crs, g_transform=out_trans)
            if is_limit_changed:
                FileIO.set_file_reading_limit(soft)
            return raster

    @staticmethod
    def classify_ndwi(rio_raster, band=8) -> np.ndarray:
        classes = {
            "vegetation": (('lt', 0.1), 3),
            "built-up": ((-0.1, 0.4), 1),
            "water": (('gt', 0.4), 4),
        }
        img_arr = rio_raster.get_data_array(band)
        res = rio_raster.reclassify_raster(img_arr, classes)
        return res.astype(np.uint8)

    # @staticmethod
    # def classify_based_on_ranges(img_arr: np.ndarray, classes: dict):
    #     res = np.empty(img_arr.shape)
    #     res[:] = np.NaN
    #     for key in classes:
    #         if classes[key][0][0] == 'lt':
    #             res = np.where(img_arr <= classes[key][0][1], classes[key][1], res)
    #         elif classes[key][0][0] == 'gt':
    #             res = np.where(img_arr >= classes[key][0][1], classes[key][1], res)
    #         else:
    #             con = np.logical_and(img_arr >= classes[key][0][0], img_arr <= classes[key][0][1])
    #             res = np.where(con, classes[key][1], res)
    #     return res

    @staticmethod
    def classify_ndwi(rio_raster: RioRaster, band=1) -> np.ndarray:
        classes = {
            "vegetation": (('lt', 0.1), 3),
            "built-up": ((-0.1, 0.4), 1),
            "water": (('gt', 0.4), 4),
        }
        img_arr = rio_raster.get_data_array(band)
        res = BandProcess.reclassify_band(img_arr, classes)
        return res.astype(np.uint8)

    @staticmethod
    def classify_ndvi(rio_raster: RioRaster, band=1) -> np.ndarray:
        classes = {
            "water": (('lt', 0.015), 4),
            "built-up": ((0.015, 0.02), 1),
            "barren": ((0.07, 0.27), 2),
            "vegetation": (('gt', 0.27), 3)
        }
        print("no of bands", rio_raster.get_spectral_resolution())
        img_arr = rio_raster.get_data_array(band)
        res = BandProcess.reclassify_band(img_arr, classes)
        return res.astype(np.uint8)

    @classmethod
    def combine_indices(cls, rio_raster):
        # values = np.unique(pc_classification)
        # for val in values:
        ndvi_classification = cls.classify_ndvi(rio_raster, 7)
        ndwi_classification = cls.classify_ndwi(rio_raster, 8)
        x = np.where(ndwi_classification == 1, ndwi_classification, ndvi_classification)
        x = np.where(ndwi_classification == 4, ndwi_classification, x)
        return x

    @classmethod
    def split_2_tiles(cls, raster: RioRaster, des_path: str, tile_width, tile_height, des_crs=None):
        FileIO.mkdirs(des_path)
        tile: RioRaster
        # tile_width, tile_height = 5000, 5000
        # nodata_value = self.raster.get_nodata_value()
        for tile, col_off, row_off in raster.get_tiles(tile_width, tile_height):
            if des_crs:
                tile.reproject_raster(des_crs)
            des_tile = os.path.join(des_path, f'tile_{int(col_off / tile_width)}_{int(row_off / tile_height)}.tif')
            tile.save_to_file(des_tile)
            print(f"saved at {des_tile}")
        cls.generate_index_map(des_path)

    @staticmethod
    def generate_index_map(tile_path):
        crs = None
        envelopes, col_index, row_index, file_name = [], [], [], []
        file_list = FileIO.list_files_in_folder(tile_path, ext='tif')
        for fp in file_list:
            raster = RioRaster(fp)
            if not crs:
                crs = raster.get_crs()
            e = box(*raster.get_raster_extent())
            envelopes.append(e)
            name_parts = FileIO.get_file_name_ext(fp)[0].split("_")
            col_index.append(name_parts[1])
            row_index.append(name_parts[1])
            file_name.append(os.path.basename(fp))
        gdf = gpd.GeoDataFrame({"file_name": file_name, "row_index": row_index, "col_index": col_index},
                               geometry=envelopes, crs=crs)
        gdp_vector = GPDVector(gdf)
        index_des = f"{tile_path}/index_map.gpkg"
        gdp_vector.to_gpkg(index_des, layer="index_map")
        print(f"saved at {index_des}")

    @staticmethod
    def min_max_stretch(raster: RioRaster, band: tuple) -> np.ndarray:
        """
        adjust only for single band like (1,) needd to update for more than one band
        :param raster:
        :param band:
        :return:
        """
        data = raster.get_data_array(band=band)
        data = data.astype(np.float32)
        data[data == raster.get_nodata_value()] = np.nan
        min_val = np.nanmin(data)
        max_val = np.nanmax(data)
        data = (data - min_val) / (max_val - min_val) * 255
        data = data.astype(np.uint8)
        return data

    @classmethod
    def stack_bands(cls, file_list: list, get_band_name=None) -> RioRaster:
        """
        :param file_list: file of bands as tif file
        :param get_band_name: get file info based on sensor (for landsat)
        must have band_name
        :return:  in memory RioRaster
        """
        # Read metadata of first file
        with rasterio.open(file_list[0]) as src0:
            meta = src0.meta

        # Update meta to reflect the number of layers
        meta.update(count=len(file_list))

        # Read each layer and write it to stack
        memfile = MemoryFile()
        dataset = memfile.open(**meta)
        descriptions = []
        for bid, layer in enumerate(file_list, start=1):
            with rasterio.open(layer) as src1:
                dataset.write_band(bid, src1.read(1))
                if get_band_name:
                    name = get_band_name(os.path.basename(layer))
                    descriptions.append(name)
                    dataset.set_band_description(bid, descriptions[-1])
        if len(descriptions) == len(file_list):
            dataset.descriptions = tuple(descriptions)

        dataset.close()

        dataset = memfile.open()  # Reopen as DatasetReader
        # dir_name, file_name = self.get_file_name()
        new_raster = RioRaster(dataset)

        return new_raster

    @classmethod
    def pansharpend(cls, ms_raster: RioRaster, pan_raster: RioRaster,
                    method: str = 'browley', W: float = 0.1) -> RioRaster:
        """
        https://www.kaggle.com/code/resolut/panchromatic-sharpening/notebook
        :param ms_raster: multi spectral raster
        :param pan_raster: pan raster
        :param method: hsv, simple_browley, sample_mean
        :param W:
        :return: RioRaster
        """
        p_band, p_row, p_col = pan_raster.get_data_shape()
        ms_band, ms_row, ms_col = ms_raster.get_data_shape()

        rgbn = ms_raster.get_data_array()
        rgbn = np.moveaxis(rgbn, 0, 2)

        rgbn_scaled = np.empty((p_row, p_col, ms_band))

        for i in range(4):
            rgbn_scaled[:, :, i] = rescale(rgbn[:, :, i], ((p_row / ms_row), (p_col / ms_col)))
        pan = pan_raster.get_data_array(1)
        R = rgbn_scaled[:, :, 0]
        G = rgbn_scaled[:, :, 1]
        B = rgbn_scaled[:, :, 2]
        I = rgbn_scaled[:, :, 3]
        image = None

        if method == 'simple_browley':
            all_in = R + G + B
            # prod = np.multiply(all_in, pan)
            r = np.multiply(R, pan / all_in)[:, :, np.newaxis]
            g = np.multiply(G, pan / all_in)[:, :, np.newaxis]
            b = np.multiply(B, pan / all_in)[:, :, np.newaxis]
            image = np.concatenate([r, g, b], axis=2)
        if method == 'sample_mean':
            r = 0.5 * (R + pan)[:, :, np.newaxis]
            g = 0.5 * (G + pan)[:, :, np.newaxis]
            b = 0.5 * (B + pan)[:, :, np.newaxis]
            image = np.concatenate([r, g, b], axis=2)
        if method == 'esri':
            ADJ = pan - rgbn_scaled.mean(axis=2)
            r = (R + ADJ)[:, :, np.newaxis]
            g = (G + ADJ)[:, :, np.newaxis]
            b = (B + ADJ)[:, :, np.newaxis]
            i = (I + ADJ)[:, :, np.newaxis]

            image = np.concatenate([r, g, b, i], axis=2)

        if method == 'browley':
            a = (pan - W * I)
            b = (W * R + W * G + W * B)
            DNF = np.divide(a, b, out=np.zeros_like(a), where=b != 0)
            r = (R * DNF)[:, :, np.newaxis]
            g = (G * DNF)[:, :, np.newaxis]
            b = (B * DNF)[:, :, np.newaxis]
            i = (I * DNF)[:, :, np.newaxis]
            image = np.concatenate([r, g, b, i], axis=2)
        if method == 'hsv':
            hsv = color.rgb2hsv(rgbn_scaled[:, :, :3])
            hsv[:, :, 2] = pan - I * W
            image = color.hsv2rgb(hsv)
        if image is not None:
            image = np.moveaxis(image, 2, 0)
            return RioRaster.raster_from_array(image,
                                               g_transform=ms_raster.get_geo_transform(),
                                               crs=ms_raster.get_crs(),
                                               nodata_value=ms_raster.get_nodata_value())
        return None
