# import os
# import numpy as np
# from uuid import uuid4
# from osgeo import gdal, osr
# from pyproj import Proj, transform
#
# from digitalarztools.io.vector.gpd_vector import GPDVector
#
#
# class GDALRasterDA:
#     dataset = None
#     metadata = {}
#
#     def __init__(self, file, is_s3_storage=False):
#         if isinstance(file, str):
#             if not is_s3_storage:
#                 # self.raster = gdal.Open(file_path, GA_ReadOnly)
#                 self.dataset = gdal.Open(file)
#             # else:
#             #     ct_storage = CT_S3Storage()
#             #     f = ct_storage.open(file, mode='rb')
#             #     mmap_name = "/vsimem/" + uuid4().hex
#             #     gdal.FileFromMemBuffer(mmap_name, f.read())
#             #     self.dataset = gdal.Open(mmap_name)
#         else:
#             self.dataset = file
#         self.set_metadata()
#
#     def get_x_y_value_raster(self) -> (np.ndarray, np.ndarray):
#         """
#         This function retrieves information about the X and Y raster
#         :return: lat and lon raster
#         """
#
#         rows, cols = self.get_img_resolution()
#         geo_t = self.get_geo_transform()
#         X = np.zeros((rows, cols))
#         Y = np.zeros((rows, cols))
#
#         # tim way of doing it
#         for col in np.arange(cols):
#             X[:, col] = geo_t[0] + col * geo_t[1] + geo_t[1] / 2
#             # ULx + col*(E-W pixel spacing) + E-W pixel spacing
#         for row in np.arange(rows):
#             Y[row, :] = geo_t[3] + row * geo_t[5] + geo_t[5] / 2
#             # ULy + row*(N-S pixel spacing) + N-S pixel spacing,
#             # negative as we will be counting from the UL corner
#         return X, Y
#
#         # for i in np.arange(cols):
#         #     for j in np.arange(i, rows):
#         #         Y[j, :] = i * geo_t[3] + j * geo_t[4] + geo_t[5]
#         #         break
#         #     X[:, i] = i * geo_t[0] + j * geo_t[1] + geo_t[2]
#         # return X, Y
#
#     # def get_meta_data(self):
#     #     width = self.dataset.RasterXSize
#     #     height = self.dataset.RasterYSize
#     #     geo_transform = self.dataset.GetGeoTransform()
#     #     scale = [geo_transform[1], geo_transform[5]]
#     #     origin = [geo_transform[0], geo_transform[3]]
#     #     srid = self.get_srid()
#     #     return {width, height, scale, origin, srid}
#
#     def set_metadata(self):
#         self.metadata['rows'] = self.dataset.RasterYSize
#         self.metadata['cols'] = self.dataset.RasterXSize
#         self.metadata['bands'] = self.dataset.RasterCount
#         self.metadata['driver'] = self.dataset.GetDriver().LongName
#         self.metadata['srid'] = self.get_srid()
#         # shifting at 0,3 scaling at 1,5 and skew at 2,4
#         self.metadata['geo_transform'] = self.dataset.GetGeoTransform()
#         self.metadata['extent'] = self.get_raster_extent()
#
#     def get_img_resolution(self):
#         rows = self.dataset.RasterYSize
#         cols = self.dataset.RasterXSize
#         return rows, cols
#
#     def get_geo_transform(self):
#         return self.dataset.GetGeoTransform()
#
#     def get_raster_extent(self):
#         geo_transform = self.dataset.GetGeoTransform()
#         min_x = geo_transform[0]
#         max_y = geo_transform[3]
#         max_x = min_x + geo_transform[1] * self.dataset.RasterXSize
#         max_y = max_y + geo_transform[5] * self.dataset.RasterYSize
#         extent = (min_x, max_y, max_x, max_y)
#         return extent
#
#     def get_image_res(self):
#         width = self.dataset.RasterXSize
#         height = self.dataset.RasterYSize
#         return width, height
#
#     def get_spatial_res(self):
#         geo_transform = self.dataset.GetGeoTransform()
#         scale = [geo_transform[1], geo_transform[5]]
#         return scale
#
#     def get_origin(self):
#         geo_transform = self.dataset.GetGeoTransform()
#         origin = [geo_transform[0], geo_transform[3]]
#         return origin
#
#     def get_projection(self):
#         return self.dataset.GetProjection()
#
#     def get_srid(self):
#         proj = osr.SpatialReference(wkt=self.dataset.GetProjection())
#         srid = proj.GetAttrValue('AUTHORITY', 1)
#         return srid
#
#     def get_envelope(self):
#         extent = self.get_raster_extent()
#         # envelop = Polygon.from_bbox(extent)
#         envelop = GPDVector.extent_2_envelop(*extent, crs=None)
#         return envelop
#
#     def get_gdal_dataset(self):
#         return self.dataset
#
#     def get_path(self):
#         files = self.dataset.GetFileList()
#         return files[0] if len(files) > 0 else None
#
#     def get_no_data_value(self, band_no):
#         band = self.dataset.GetRasterBand(band_no)
#         return band.GetNoDataValue()
#
#     def band_count(self):
#         return self.dataset.RasterCount
#
#     def band_to_numpy_array(self, band_no=1):
#         # band_no starts from 1
#         band = self.dataset.GetRasterBand(band_no)
#         np_array = np.array(band.ReadAsArray())
#         return np_array
#
#     def get_data_type(self):
#         band = self.dataset.GetRasterBand(1)
#         data_type_name = gdal.GetDataTypeByName(band.DataType)
#         return band.DataType, data_type_name
#         # print("Band Type={}".format(gdal.GetDataTypeName(band.DataType)))
#
#     # def plot_rgb_image(self):
#     #     img = np.dstack((b1, b2, b3))
#     #     f = plt.figure()
#     #     plt.imshow(img)
#     #     # plt.savefig('Tiff.png')
#     #     plt.show()
#     #
#     # def plot_single_band(self):
#     #     img = np.dstack((b1, b2, b3))
#     #     f = plt.figure()
#     #     plt.imshow(img)
#     #     plt.savefig('Tiff.png')
#     #     plt.show()
#
#     def make_coincident(self, raster2):
#         scale = raster2.get_spatial_res()
#         des_srid = raster2.get_srid()
#         gdal.Warp('/vsimem/reprojected.vrt', self.dataset, dstSRS='EPSG:' + str(des_srid),
#                   xRes=scale[0], yRes=scale[1])
#         self.dataset = gdal.Open('/vsimem/reprojected.vrt')
#
#     def reproject_raster(self, des_srid):
#         gdal.Warp('/vsimem/reprojected.vrt', self.dataset, dstSRS='EPSG:' + str(des_srid))
#         self.dataset = gdal.Open('/vsimem/reprojected.vrt')
#
#     # def get_extent_after_skip_row_cols(self, skip_rows, skip_cols):
#     #     ulx, lry, lrx, uly = self.get_raster_extent()
#     #     geo_t = self.get_geo_transform()
#     #     y_size, x_size = self.get_img_resolution()
#     #     # Remove a part of image
#     #     nrow_skip = round((skip_rows * y_size) / 2)
#     #     ncol_skip = round((skip_cols * x_size) / 2)
#     #
#     #     # Up to here, all  the projection have been defined, as well as a
#     #     # transformation from the from to the to
#     #     ulx, uly = transform(inProj, outProj, geo_t[0] + nrow_skip * geo_t[1], geo_t[3] + nrow_skip * geo_t[5])
#     #     lrx, lry = transform(inProj, outProj, geo_t[0] + geo_t[1] * (x_size - ncol_skip),
#     #                          geo_t[3] + geo_t[5] * (y_size - nrow_skip))
#
#     def reproject_raster_tim(self, des_srid, in_place=True):
#         src_srid = self.get_srid()
#         osng = osr.SpatialReference()
#         osng.ImportFromEPSG(des_srid)
#         wgs84 = osr.SpatialReference()
#         wgs84.ImportFromEPSG(src_srid)
#         gdal.ReprojectImage(self.dataset, '/vsimem/reprojected.vrt', wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_CubicSpline)
#         if in_place:
#             self.dataset = gdal.Open('/vsimem/reprojected.vrt')
#         else:
#             return gdal.Open('/vsimem/reprojected.vrt')
#
#     def reproject_dataset(self, pixel_spacing, epsg_to, fit_extend=False):
#         """
#         A sample function to reproject and resample a GDAL dataset from within
#         Python. The idea here is to reproject from one system to another, as well
#         as to change the pixel size. The procedure is slightly long-winded, but
#         goes like this:
#
#         1. Set up the two Spatial Reference systems.
#         2. Open the original dataset, and get the geotransform
#         3. Calculate bounds of new geotransform by projecting the UL corners
#         4. Calculate the number of pixels with the new projection & spacing
#         5. Create an in-memory raster dataset
#         6. Perform the projection
#         """
#
#         g = self.dataset
#         # EPSG_code = '326%02d' % UTM_Zone
#         # epsg_to = int(EPSG_code)
#
#         # 2) Define the UK OSNG, see <http://spatialreference.org/ref/epsg/27700/>
#         try:
#             proj = g.GetProjection()
#             Proj_in = proj.split('EPSG","')
#             epsg_from = int((str(Proj_in[-1]).split(']')[0])[0:-1])
#         except:
#             epsg_from = int(4326)  # Get the Geotransform vector:
#         geo_t = self.get_geo_transform()
#         # Vector components:
#         # 0- The Upper Left easting coordinate (i.e., horizontal)
#         # 1- The E-W pixel spacing
#         # 2- The rotation (0 degrees if image is "North Up")
#         # 3- The Upper left northing coordinate (i.e., vertical)
#         # 4- The rotation (0 degrees)
#         # 5- The N-S pixel spacing, negative as it is counted from the UL corner
#         x_size = g.RasterXSize  # Raster xsize
#         y_size = g.RasterYSize  # Raster ysize
#
#         # epsg_to = int(epsg_to)
#
#         # 2) Define the UK OSNG, see <http://spatialreference.org/ref/epsg/27700/>
#         osng = osr.SpatialReference()
#         osng.ImportFromEPSG(epsg_to)
#         wgs84 = osr.SpatialReference()
#         wgs84.ImportFromEPSG(epsg_from)
#
#         inProj = Proj(init='epsg:%d' % epsg_from)
#         outProj = Proj(init='epsg:%d' % epsg_to)
#
#         # Remove a part of image
#         nrow_skip = round((0.06 * y_size) / 2)
#         ncol_skip = round((0.06 * x_size) / 2)
#
#         # Up to here, all  the projection have been defined, as well as a
#         # transformation from the from to the to
#         ulx, uly = transform(inProj, outProj, geo_t[0] + nrow_skip * geo_t[1], geo_t[3] + nrow_skip * geo_t[5])
#         lrx, lry = transform(inProj, outProj, geo_t[0] + geo_t[1] * (x_size - ncol_skip),
#                              geo_t[3] + geo_t[5] * (y_size - nrow_skip))
#
#         # See how using 27700 and WGS84 introduces a z-value!
#         # Now, we create an in-memory raster
#         mem_drv = gdal.GetDriverByName('MEM')
#         # ulx, lry, lrx, uly = extent
#         if fit_extend:
#             ulx = np.ceil(ulx / pixel_spacing) * pixel_spacing + 0.5 * pixel_spacing
#             uly = np.floor(uly / pixel_spacing) * pixel_spacing - 0.5 * pixel_spacing
#             lrx = np.floor(lrx / pixel_spacing) * pixel_spacing - 0.5 * pixel_spacing
#             lry = np.ceil(lry / pixel_spacing) * pixel_spacing + 0.5 * pixel_spacing
#
#         # The size of the raster is given the new projection and pixel spacing
#         # Using the values we calculated above. Also, setting it to store one band
#         # and to use Float32 data type.
#         col = int((lrx - ulx) / pixel_spacing)
#         rows = int((uly - lry) / pixel_spacing)
#
#         # Re-define lr coordinates based on whole number or rows and columns
#         (lrx, lry) = (ulx + col * pixel_spacing, uly -
#                       rows * pixel_spacing)
#
#         dest = mem_drv.Create('', col, rows, 1, gdal.GDT_Float32)
#
#         if dest is None:
#             print('input folder to large for memory, clip input map')
#
#         # Calculate the new geotransform
#
#         new_geo = (ulx, pixel_spacing, geo_t[2], uly, geo_t[4], - pixel_spacing)
#
#         # Set the geotransform
#         dest.SetGeoTransform(new_geo)
#         dest.SetProjection(osng.ExportToWkt())
#
#         # Perform the projection/resampling
#         gdal.ReprojectImage(g, dest, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_CubicSpline)
#
#         return dest, ulx, lry, lrx, uly, epsg_to
#
#     def create_hill_shade(self, temp_file_name):
#         gdal.DEMProcessing('/vsimem/hill_shade.vrt', self.dataset, 'hillshade', format='GTiFF', zFactor=1)
#         hill_shade_raster = gdal.Open('/vsimem/hill_shade.vrt')
#         return hill_shade_raster
#
#     def merge_raster(self, da_raster):
#         # temp_path1 = os.path.join(MEDIA_ROOT, "merge1.tif")
#         # print(temp_path1)
#         # self.save_to_file(temp_path1)
#         # temp_path2 = os.path.join(MEDIA_ROOT, "merge2.tif")
#         # print(temp_path2)
#         # da_raster.save_to_file(temp_path2)
#         # temp_file_path = os.path.join(MEDIA_ROOT, "final_merge_raster.tif")
#         # print(temp_file_path)
#         # file_path = self.create_temporary_file_path("merged", file_extension='tif')
#         file_path = '/vsimem/merged.tif'
#         from osgeo_utils import gdal_merge
#         gdal_merge.main(['', '-o', file_path, self.get_path(), da_raster.get_path()])
#         # merged_raster = gdal.Open('/vsimem/merged.vrt')
#         # merge_command = ["python", 'gdal_merge.py', "-o", file_path, self.get_path(), da_raster.get_path()]
#         # subprocess.call(merge_command, shell=True)
#         # command = "which gdal_merge.py"
#         # command_path = subprocess.check_output(command)
#         # print(command_path)
#         # command = "gdal_merge -o %s %s %s " % (file_path, self.get_path(), da_raster.get_path())
#         # print(command)
#         # output = subprocess.check_output(command)
#         # subprocess.call(command, shell=True)
#         # print(output)
#         merged_raster = GDALRasterDA(file_path, is_s3_storage=False)
#         # os.remove(file_path)
#         return merged_raster
#
#     def save_to_file(self, des_path, file_format="GTiff"):
#         # Open output format driver, see gdal_translate --formats for list
#         # format = "GTiff"
#         driver = gdal.GetDriverByName(file_format)
#         # Output to new format
#         dst_ds = driver.CreateCopy(des_path, self.dataset)
#         # Properly close the datasets to flush to disk
#         dst_ds = None
#
#     # def create_temporary_file_path(self, file_type, file_extension='tif'):
#     #     file_name = Common_Utils.add_timestamp_to_string(file_type)
#     #     file_name = os.path.join(MEDIA_ROOT, '%s.%s' % (file_name, file_extension))
#     #     # print("local:" + file_name)
#     #     return file_name
#
#     # def upload_to_s3_storage(self, file_type, s3_raster_path_name=None):
#     #     file_name = self.create_temporary_file_path(file_type)
#     #     self.save_to_file(file_name)
#     #     ct_storage = CT_S3Storage()
#     #     file = open(file_name, 'rb')
#     #
#     #     ct_storage.save(s3_raster_path_name, file)
#     #     os.remove(file_name)
#
#     def to_numpy_array(self):
#         return self.dataset.ReadAsArray()
#
#     def to_bytes(self):
#         return self.dataset.ReadRaster()
#
#     # def to_GDALRaster(self):
#     #     # GDALRaster(self.dataset.ReadRaster(buf_type='utf-8))
#     #     raster = None
#     #     file_path = self.get_path()
#     #     if file_path: raster = GDALRaster(file_path)
#     #     return raster
