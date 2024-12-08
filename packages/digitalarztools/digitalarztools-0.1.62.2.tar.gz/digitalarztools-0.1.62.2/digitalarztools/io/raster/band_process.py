import enum
import math
from time import time
from typing import List

import geopandas as gpd

import numpy as np
import pandas as pd
import scipy
from rasterio.features import rasterize
from scipy.ndimage import generic_filter
from scipy.spatial import KDTree
from shapely import LineString, Point
from shapely.geometry.polygon import orient, Polygon
from skimage import measure

from digitalarztools.utils.logger import da_logger


class SummaryData():
    sum = lambda x: np.nansum(x)


class BandProcess:
    def __init__(self, data: np.ndarray):
        self.data = data

    @staticmethod
    @staticmethod
    def gap_filling(data: np.ndarray, no_data_value, method=1) -> np.ndarray:
        """
        This function fills the no data gaps in a numpy array

        Keyword arguments:
        data -- numpy array
        no_data_value -- Value that must be filled
        method -- The interpolation method to use (default is 1)
        """
        try:
            # fill the no data values
            if no_data_value is np.nan:
                mask = ~(np.isnan(data))
            else:
                mask = ~(data == no_data_value)

            xx, yy = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))
            xym = np.vstack((np.ravel(xx[mask]), np.ravel(yy[mask]))).T
            data0 = np.ravel(data[:, :][mask])
            data_end = None

            if method == 1:
                interp0 = scipy.interpolate.NearestNDInterpolator(xym, data0)
                data_end = interp0(np.ravel(xx), np.ravel(yy)).reshape(xx.shape)

            if method == 2:
                interp0 = scipy.interpolate.LinearNDInterpolator(xym, data0)
                data_end = interp0(np.ravel(xx), np.ravel(yy)).reshape(xx.shape)

            return data_end
        except Exception as e:
            da_logger.warning(f"Failed in gap filling due to: {str(e)}")
            return data

    @staticmethod
    def create_buffer(Data_In: np.ndarray, Buffer_area=2):
        """
        This function creates a 3D array which is used to apply the moving window
        :param Data_In:
        :param Buffer_area:
        :return:
        """
        # A block of 2 times Buffer_area + 1 will be 1 if there is the pixel in the middle is 1
        Data_Out = np.empty((len(Data_In), len(Data_In[1])))
        Data_Out[:, :] = Data_In
        for ypixel in range(0, Buffer_area + 1):

            for xpixel in range(1, Buffer_area + 1):

                if ypixel == 0:
                    for xpixel in range(1, Buffer_area + 1):
                        Data_Out[:, 0:-xpixel] += Data_In[:, xpixel:]
                        Data_Out[:, xpixel:] += Data_In[:, :-xpixel]

                    for ypixel in range(1, Buffer_area + 1):
                        Data_Out[ypixel:, :] += Data_In[:-ypixel, :]
                        Data_Out[0:-ypixel, :] += Data_In[ypixel:, :]

                else:
                    Data_Out[0:-xpixel, ypixel:] += Data_In[xpixel:, :-ypixel]
                    Data_Out[xpixel:, ypixel:] += Data_In[:-xpixel, :-ypixel]
                    Data_Out[0:-xpixel, 0:-ypixel] += Data_In[xpixel:, ypixel:]
                    Data_Out[xpixel:, 0:-ypixel] += Data_In[:-xpixel, ypixel:]

        Data_Out[Data_Out > 0.1] = 1
        Data_Out[Data_Out <= 0.1] = 0

        return (Data_Out)

    @staticmethod
    def get_summary_data(data: np.ndarray, nodata=None, ignore_negative_values=True, ignore_values: list = []):
        data = data.astype(np.float64)  # Convert data to float64 for NaN compatibility

        # Handle nodata values
        if nodata is not None:
            data[data == nodata] = np.nan  # Convert nodata values to NaN

        # Handle specified ignore values
        for value in ignore_values:
            data[data == value] = np.nan  # Convert specified ignore values to NaN

        # Ignore negative values if required
        if ignore_negative_values:
            data[data <= 0] = np.nan  # Convert all non-positive values to NaN

        # Ensure there are valid data points before computing statistics
        if np.isnan(data).all():
            return {
                "mean": np.nan, "median": np.nan, "std": np.nan,
                "min": np.nan, "q25": np.nan, "q75": np.nan, "max": np.nan, "sum": np.nan
            }

        # Compute statistics while ignoring NaN values
        mean_val = np.nanmean(data)  # Calculate mean, ignoring NaN
        min_val = np.nanmin(data)  # Calculate min, ignoring NaN
        max_val = np.nanmax(data)  # Calculate max, ignoring NaN
        std_val = np.nanstd(data)  # Calculate standard deviation, ignoring NaN
        q25_val = np.nanquantile(data, 0.25)  # 25th percentile, ignoring NaN
        median_val = np.nanquantile(data, 0.5)  # Median, ignoring NaN
        q75_val = np.nanquantile(data, 0.75)  # 75th percentile, ignoring NaN
        total_sum = np.nansum(data)  # Sum, ignoring NaN

        return {
            "mean": mean_val, "median": median_val, "std": std_val,
            "min": min_val, "q25": q25_val, "q75": q75_val, "max": max_val, "sum": total_sum
        }

    @classmethod
    def get_value_area_data(cls, data: np.ndarray, no_data, spatial_res_in_meter : tuple, values=None) -> list:
        """
        @param data:
        @param no_data:
        @param spatial_res_in_meter: (res_x, res_y)
        @param values:
        @return:
        """
        value_count = cls.get_value_count_data(data, no_data, values)
        value_area = []
        area =  spatial_res_in_meter[0]/1000 * spatial_res_in_meter[1]/1000 if len(spatial_res_in_meter) == 2 else spatial_res_in_meter/1000
        # print(area)
        for index, v in enumerate(value_count):
            value = v['value']
            value_area.append({"value": value, "area": v["count"] * area, "unit":"sq. km"})
        return value_area

    @staticmethod
    def get_value_count_data(data: np.ndarray, no_data, values=None) -> list:
        """
        :param data: np.ndarray  like data = raster.get_data_array(band_no)
        :param no_data: no_data = raster.get_nodata_value()
        :param values:
        :return: value and count if res is provide than area in meter
        """
        if no_data is not None and 'float' in str(data.dtype):
            data[data == no_data] = np.nan
        # data[data == no_data] = np.nan
        if values is None:
            if "float" in str(data.dtype):
                data[data == no_data] = np.nan
                min_value = math.ceil(np.nanquantile(data, 0.25))
                max_value = math.ceil(np.nanquantile(data, 0.75))
                prev_val = None
                for v in range(min_value, max_value):
                    if v in [min_value, max_value]:
                        values.append((v,))
                    else:
                        values.append((prev_val, v))
                    prev_val = v

            else:
                values = np.unique(data)
                values = values[values != no_data]
        else:
            if "float" in str(data.dtype) and not isinstance(values[0], tuple):
                val = [float(v) for v in values]
                values = []
                for i in range(len(val)):
                    if i == 0 or i == len(val) - 1:
                        values.append((val[i],))
                    else:
                        values.append((val[i - 1], val[i]))

        output = []
        for idx, v in enumerate(values):
            if isinstance(v, tuple):
                if len(v) == 1 and idx == 0:
                    count = np.count_nonzero(data <= v[0])
                    key = f"<= {v[0]}"
                elif len(v) == 1 and idx != 0:
                    count = np.count_nonzero(data >= v[0])
                    key = f">= {v[0]}"
                else:
                    count = np.count_nonzero((data > v[0]) & (data <= v[1]))
                    key = " - ".join(map(str, v))
                # output[key] = count * (res_in_meter[0] * res_in_meter[1])
                # output.append({"value": " - ".join(map(str, v)), "count": count })
            else:
                v = float(v) if isinstance(v, str) else v
                count = np.count_nonzero(data == v)
                key = str(v)
            # output[key] = count
            o = {"value": key, "count": count}
            # if labels is not None:
            #     o["label"] = labels[idx]
            output.append(o)
        return output

    @staticmethod
    def get_boolean_raster(data: np.ndarray, pixel_value: list):
        con = None
        for v in pixel_value:
            con = data == v if con is None else np.logical_or(con, data == v)
        res = np.where(con, 1, 0)
        res = res.astype(np.uint8)
        return res

    @staticmethod
    def create_distance_raster(data: np.ndarray, pixel_value, pixel_size_in_km=1):
        boolean_data = BandProcess.get_boolean_raster(data, pixel_value)
        dist_array = np.empty(boolean_data.shape, dtype=float)
        try:
            print("calculating distance raster")
            tree = KDTree(data=np.array(np.where(boolean_data == 1)).T, leafsize=64)
            t_start = time()
            for cur_index, val in np.ndenumerate(boolean_data):
                min_dist, min_index = tree.query([cur_index])
                if len(min_dist) > 0 and len(min_index) > 0:
                    min_dist = min_dist[0]
                    min_index = tree.data[min_index[0]]
                    # dist = math.sqrt(math.pow((cur_index[0] - min_index[0]),2)+math.pow((cur_index[1] - min_index[1]),2))
                    # print(min_dist, dist)
                    # if self.affine is not None:
                    #     if cur_index[1] == min_index[1]:
                    #         # columns are same meaning nearest is either vertical or self.
                    #         # no correction needed, just convert to km
                    #         dd_min_dist = min_dist * self.pixel_size
                    #         km_min_dist = dd_min_dist * 111.321
                    #
                    #     else:
                    #         km_min_dist = calc_haversine_distance(
                    #             convert_index_to_coords(cur_index, self.affine),
                    #             convert_index_to_coords(min_index, self.affine),
                    #         )
                    #
                    #     val = km_min_dist * 1000
                    #
                    # else:
                    # val = min_dist
                    dist_array[cur_index[0]][cur_index[1]] = min_dist * pixel_size_in_km
            e_time = time()
            print("Distance calc run time: {0} seconds".format(round(time() - t_start, 4)))
        except Exception as e:
            print(str(e))
        return dist_array

    @staticmethod
    def stretch_data(normalize_data: np.ndarray, stretch_range=[0, 255]):
        """
        stretch normalize data between stretch range. in future the stretch will based on dtype range
        :param normalize_data: use min_max, logarithmic, and exponential normalization
        :param stretch_range: list of min and max range
        :return:
        """
        max_stretch_val = stretch_range[1] - stretch_range[0]
        data = stretch_range[0] + (normalize_data * max_stretch_val)

        return data

    @staticmethod
    def logarithmic_normalization(data: np.ndarray, no_data: float, is_inverse: bool = False):
        """
        Normalize data between 0 and 1 using logarithmic stretch
        :param data:
        :param no_data:
        :param is_inverse:
        :return:
        """
        if 'float' not in str(data.dtype):
            data = data.astype(np.float32)
        if no_data is not None:
            data[data == no_data] = np.nan

        # data[data == no_data] = 0
        # data[data <= 30] = 0

        max_val = np.nanmax(data)
        # min_val = np.nanmin(data)
        c = 1 / np.log(1 + max_val)
        data = c * np.log(1 + data)
        if is_inverse:
            data = 1 - data
        # stetch between specified range
        # max_stretch_val = stretch_range[1] - stretch_range[0]
        # data = stretch_range[0] + (data * max_stretch_val)

        if no_data is not None:
            data = np.nan_to_num(data, nan=no_data)
        # if dtype is not None:
        #     data = data.astype(dtype)
        return data

    @staticmethod
    def min_max_normalization(data: np.ndarray, no_data, is_inverse: bool = False) -> np.ndarray:
        """
         Normalize data between 0 and 1 using min-max stretch
        :param data:
        :param no_data:
        :param is_inverse:
        :return:
        """
        if 'float' not in str(data.dtype):
            data = data.astype(np.float32)
        if no_data is not None:
            data[data == no_data] = np.nan
        min_val = np.nanmin(data)
        max_val = np.nanmax(data)
        # stretch from zero to 1
        data = (data - min_val) / (max_val - min_val)
        if is_inverse:
            data = 1 - data

        # stetch between specified range
        # max_stretch_val = stretch_range[1] - stretch_range[0]
        # data = stretch_range[0] + (data * max_stretch_val)

        if no_data is not None:
            data = np.nan_to_num(data, nan=no_data)
        # if dtype is not None:
        #     data = data.astype(dtype)
        return data

    @staticmethod
    def mask_data(band_data: np.ndarray, ignore_values: List[float]):
        """
        Mask the ignore values in the band data.

        :param band_data: The array of raster data to mask.
        :param ignore_values: A list of float values to ignore (mask out).
        :return: A masked array where the ignore values are masked.
        """
        # Mask the ignore values
        mask = np.isin(band_data, ignore_values)
        masked_data = np.ma.masked_array(band_data, mask=mask)
        return masked_data

    @staticmethod
    def majority_filter(input_array, neighborhood_size=(3, 3)):
        def majority_operation(window):
            values, counts = np.unique(window, return_counts=True)
            return values[np.argmax(counts)]

        filtered_array = generic_filter(input_array, majority_operation, size=neighborhood_size)
        return filtered_array

    @staticmethod
    def remove_single_pixel_noise(data):
        labeled_image, num_labels = measure.label(data, connectivity=2, return_num=True)
        for label in range(1, num_labels + 1):
            label_mask = labeled_image == label
            if np.sum(label_mask) == 1:
                data[label_mask] = 0  # Set isolated pixel to 0 (or any other desired value)
        return data

    @staticmethod
    def reclassify_band(img_arr: np.array, thresholds: dict, nodata=0) -> np.array:
        """
        img_arr: must be as row, col
        :param thresholds:
            example:  {
                    "water": (('lt', 0.015), 4),
                    "built-up": ((0.015, 0.02), 1),
                    "barren": ((0.07, 0.27), 2),
                    "vegetation": (('gt', 0.27), 3)
                }

        """
        if img_arr.ndim > 2:
            img_arr = np.squeeze(img_arr)
        res = np.empty(img_arr.shape)
        res[:] = nodata
        for key in thresholds:
            if thresholds[key][0][0] == 'lt':
                res = np.where(img_arr <= thresholds[key][0][1], thresholds[key][1], res)
            elif thresholds[key][0][0] == 'gt':
                res = np.where(img_arr >= thresholds[key][0][1], thresholds[key][1], res)
            else:
                con = np.logical_and(img_arr >= thresholds[key][0][0], img_arr <= thresholds[key][0][1])
                res = np.where(con, thresholds[key][1], res)
        return res.astype(np.uint8)

    @staticmethod
    def raster_2_polygon(band_data: np.ndarray, classes: list = [], crs=0, tolerance=0) -> gpd.GeoDataFrame:
        # gdf = gpd.GeoDataFrame(columns=['class', 'geometry'], crs = crs)
        if len(classes) == 0:
            classes = np.unique(band_data)
            print("Classes:", classes)
        final_polygons = []
        for class_value in classes:
            # Create a binary mask for the current class
            binary_mask = (band_data == class_value).astype(np.uint8)

            # Find contours
            contours = measure.find_contours(binary_mask, 0.5)

            # Convert contours to polygons
            polygons = [Polygon(contour[:, ::-1]) for contour in contours if
                        len(contour) > 2]  # Reverse to get (x, y) from (row, col)

            # Orient polygons correctly and remove duplicates
            polygons = [orient(polygon) for polygon in polygons]
            if tolerance != 0:
                polygons = [polygon.simplify(tolerance) for polygon in polygons]
            final_polygons = final_polygons + [{'class': class_value, 'geometry': polygon} for polygon in polygons]
            # for polygon in  polygons:
            #     gdf = gdf.append({'class': class_value, 'geometry': polygon}, ignore_index=True)
        gdf = gpd.GeoDataFrame(data=final_polygons, columns=['class', 'geometry'], crs=crs)
        return gdf

    @staticmethod
    def raster_2_polyline(band_data: np.ndarray, classes: list = [], crs=0, tolerance=0) -> gpd.GeoDataFrame:
        if len(classes) == 0:
            classes = np.unique(band_data)
            print("Classes:", classes)
        final_geom = []
        for class_value in classes:
            # Create a binary mask for the current class
            binary_mask = (band_data == class_value).astype(np.uint8)

            # Find contours
            contours = measure.find_contours(binary_mask, 0.5)

            # Convert contours to polygons
            lines = [LineString(contour[:, ::-1]) for contour in contours if len(contour) > 1]

            if tolerance != 0:
                lines = [line.simplify(tolerance) for line in lines]
            final_geom = final_geom + [{'class': class_value, 'geometry': line} for line in lines]

        gdf = gpd.GeoDataFrame(data=final_geom, columns=['class', 'geometry'], crs=crs)
        return gdf

    @staticmethod
    def raster_2_points(band_data: np.ndarray, classes: list = [], crs=0) -> gpd.GeoDataFrame:
        if len(classes) == 0:
            classes = np.unique(band_data)
        all_points = []
        # Get indices of non-zero elements
        for class_value in classes:
            indices = np.argwhere(band_data == class_value)
            # Create a list of points with class information
            points = [Point(j, i) for i, j in indices]

            all_points = all_points + [{'class': class_value, 'geometry': point} for point in points]

        gdf = gpd.GeoDataFrame(data=all_points, columns=['class', 'geometry'], crs=crs)
        return gdf

    @staticmethod
    def generate_aoi_mask(aoi_gdf: gpd.GeoDataFrame, out_shape: tuple, transform):
        """
        Generates a binary mask from a GeoDataFrame based on the shape and transform of a flow accumulation array.

        Args:
        aoi_gdf (GeoDataFrame): The area of interest as a GeoDataFrame.
        flow_acc_shape (tuple): The shape of the flow accumulation array (height, width).
        flow_acc_transform (Affine): The affine transform matrix from the flow accumulation raster.

        Returns:
        numpy.ndarray: A binary mask with the same dimensions as the flow accumulation array.
        """
        # Rasterize the GeoDataFrame
        mask = rasterize(
            [(geom, 1) for geom in aoi_gdf.geometry],
            out_shape=out_shape,
            fill=0,  # Fill value for 'out' array
            transform=transform,
            all_touched=True,  # Include all pixels that are touched by geometries
            dtype=np.uint8
        )

        return mask

    @staticmethod
    def apply_aoi_mask(band_data: np.ndarray, aoi_mask: np.ndarray, no_data_value) -> np.ndarray:
        band_data[aoi_mask == 0] = no_data_value
        return band_data

    @staticmethod
    def get_indices_coordinates(mask: np.ndarray, geotransform, shape: tuple):
        i, j = np.indices(shape)
        # Get the coordinates where the mask is True
        i_masked = i[mask]
        j_masked = j[mask]

        x_coords = geotransform[0] + j_masked * geotransform[1] + i_masked * geotransform[2]
        y_coords = geotransform[3] + j_masked * geotransform[4] + i_masked * geotransform[5]
        return x_coords, y_coords
