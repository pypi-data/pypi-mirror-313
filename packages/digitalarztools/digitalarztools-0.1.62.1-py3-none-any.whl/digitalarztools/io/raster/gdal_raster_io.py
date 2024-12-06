#
# import osgeo
# import pyproj
# from osgeo import gdal
# from osgeo.osr import SpatialReference
# from pyproj.enums import WktVersion
# import numpy as np
#
# class GDALRasterIO:
#
#     @staticmethod
#     def crs_from_pyproj(proj_crs: pyproj.CRS) -> SpatialReference:
#         osr_crs = SpatialReference()
#         if osgeo.version_info.major < 3:
#             osr_crs.ImportFromWkt(proj_crs.to_wkt(WktVersion.WKT1_GDAL))
#         else:
#             osr_crs.ImportFromWkt(proj_crs.to_wkt())
#         return osr_crs
#
#     @classmethod
#     def write_geotiff(cls, filename, arr, proj_crs: pyproj.CRS = None, geo_transform: np.array = None):
#
#         arr_type = gdal.GDT_Float32 if arr.dtype == np.float32 else gdal.GDT_Int32
#         if len(arr.shape) == 2:
#             bands = 1
#             rows, cols = arr.shape
#         else:
#             bands, rows, cols = arr.shape
#         driver = gdal.GetDriverByName("GTiff")
#         out_ds = driver.Create(filename, cols, rows, bands, arr_type)
#         if proj_crs is not None:
#             out_ds.SetProjection(proj_crs.to_wkt())
#         if geo_transform is not None:
#             gt = [geo_transform[2], geo_transform[0], geo_transform[1], geo_transform[5], geo_transform[3],
#                   geo_transform[4]]
#             out_ds.SetGeoTransform(gt)
#         for b in range(bands):
#             band = out_ds.GetRasterBand(b + 1)
#             d = arr if bands == 1 else arr[b, :, :]
#             cls.write_to_band(band, d)
#
#     @staticmethod
#     def write_to_band(band, data):
#         band.WriteArray(data)
#         band.FlushCache()
#         band.ComputeStatistics(True)
#
#     @classmethod
#     def from_numpy(cls, data, geo_transform, proj_crs):
#         arr_type = gdal.GDT_Float32 if data.dtype == np.float32 else gdal.GDT_Int32
#         driver = gdal.GetDriverByName("MEM")
#         if len(data.shape) == 2:
#             bands = 1
#             rows, cols = data.shape
#         else:
#             bands, rows, cols = data.shape
#         out_ds = driver.Create("in-mem-raster", cols, rows, bands, arr_type)
#         if geo_transform is not None:
#             out_ds.SetGeoTransform([geo_transform[2], geo_transform[0], geo_transform[1],
#                                     geo_transform[5], geo_transform[3], geo_transform[4]])
#         if proj_crs is not None:
#             out_ds.SetProjection(proj_crs.to_wkt())
#         for b in range(bands):
#             band = out_ds.GetRasterBand(b + 1)
#             d = data if bands == 1 else data[b, :, :]
#             cls.write_to_band(band, d)
#         return out_ds
