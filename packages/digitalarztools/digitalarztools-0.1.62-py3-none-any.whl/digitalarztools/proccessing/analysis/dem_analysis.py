from typing import Union, Tuple, Dict, Literal

import pandas as pd
import geopandas as gpd
from collections import deque
import numpy as np
from matplotlib import pyplot as plt
from pyproj import CRS
from scipy.ndimage import label, maximum_filter

from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.proccessing.operations.geodesy import GeodesyOps


class DEMAnalysis:
    def __init__(self, dem: Union[RioRaster, str], aoi: gpd.GeoDataFrame = None, srid: int = 0):
        """
        Initialize the DEMAnalysis class.

        :param dem: DEM input, either a file path to a DEM or a RioRaster object.
        :param aoi: Optional GeoDataFrame to clip the DEM to an area of interest.
        :param srid: Spatial reference ID for reprojecting the DEM.
                     0 means no change, 1 means change to UTM projection based on extent,
                     any other value is treated as the SRID for reprojection.
        """
        self.dem = RioRaster(dem) if isinstance(dem, str) else dem

        if aoi is not None:
            self.dem.clip_raster(aoi, in_place=True)
        if srid > 0:
            if srid == 1:
                srid = GeodesyOps.utm_srid_from_extent(*self.dem.get_raster_extent())
            crs = CRS.from_epsg(srid)
            self.dem.reproject_raster(crs, in_place=True)

    def get_data_array(self) -> np.ndarray:
        return self.dem.get_data_array(1)


    @staticmethod
    def get_z_factor(z_in: Literal["m", "ft"], unit: Literal["degree", "dd", "dms", "m", "ft"],
                     lat: float = None) -> float:
        """
        Get the Z-factor for converting vertical units.

        :param z_in: Desired vertical unit, either "m" for meters or "ft" for feet.
        :param unit: Unit of the DEM, either "dd" for decimal degrees, "dms" for degrees, minutes, seconds, "m" for meters, or "ft" for feet.
        :param lat: Latitude required if the DEM units are in degrees (dd or dms).
        :return: Z-factor for unit conversion.
        :raises Exception: If latitude is not provided when DEM units are in degrees.
        """
        z = 1
        if unit in ["dd", "dms"]:
            if lat is None:
                raise Exception("Latitude can't be null if raster units are in dd or dms")
            df = pd.DataFrame({
                "latitude": [0, 10, 20, 30, 40, 50, 60, 70, 80],
                "z_meter": [0.00000898, 0.00000912, 0.00000956, 0.00001036, 0.00001171, 0.00001395,
                            0.00001792, 0.00002619, 0.00005156],
                "z_feet": [0.00000273, 0.00000278, 0.00000291, 0.00000316, 0.00000357, 0.00000425,
                           0.00000546, 0.00000798, 0.00001571]
            })
            lat = round(lat / 10) * 10
            row = df.loc[df.latitude == lat]
            z = row.z_meter.values[0] if z_in == "m" else row.z_feet.values[0]
        elif unit == "ft" and z_in == "m":
            z = 3.28
        elif unit == "m" and z_in == "ft":
            z = 0.3048
        return z

    @staticmethod
    def get_rad_2_degree() -> float:
        """
        Convert radians to degrees.

        :return: Conversion factor from radians to degrees.
        """
        return 180.0 / np.pi

    @staticmethod
    def get_degree_2_radian() -> float:
        """
        Convert degrees to radians.

        :return: Conversion factor from degrees to radians.
        """
        return np.pi / 180

    def get_gradient(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate the gradient of the DEM.

        :return: Gradient in x and y directions as NumPy arrays.
        """
        res_x, res_y = self.dem.get_spatial_resolution()
        elevation_data = self.dem.get_data_array(1) * self.get_z_factor()
        return np.gradient(elevation_data, res_x, res_y)

    @staticmethod
    def calculate_slope_in_percent(dem: np.ndarray, res: (float, float), z: float = 1):
        # Simple slope calculation using central difference method
        dzdx = np.gradient(dem, axis=1) / res[0] * z
        dzdy = np.gradient(dem, axis=0) / res[1] * z
        slope = np.sqrt(dzdx ** 2 + dzdy ** 2) * 100  # Slope in percentage
        return slope

    def get_slope_data(self, gradient_x: np.ndarray = None, gradient_y: np.ndarray = None) -> np.ndarray:
        """
        Calculate slope from gradient data.

        :param gradient_x: Optional gradient in x direction.
        :param gradient_y: Optional gradient in y direction.
        :return: Slope data as a NumPy array.
        """
        if gradient_x is None or gradient_y is None:
            gradient_x, gradient_y = self.get_gradient()

        hypotenuse_array = np.hypot(gradient_x, gradient_y)
        slope = np.arctan(hypotenuse_array) * self.get_rad_2_degree()
        return slope

    def get_aspect_data(self, gradient_x: np.ndarray = None, gradient_y: np.ndarray = None) -> np.ndarray:
        """
        Calculate aspect from gradient data.

        :param gradient_x: Optional gradient in x direction.
        :param gradient_y: Optional gradient in y direction.
        :return: Aspect data as a NumPy array.
        """
        if gradient_x is None or gradient_y is None:
            gradient_x, gradient_y = self.get_gradient()
        res_x, res_y = self.dem.get_spatial_resolution()
        aspect = np.arctan2(gradient_y / res_y, -gradient_x / res_x) * self.get_rad_2_degree()
        aspect = 180 + aspect
        return aspect

    def calculate_slope_aspect_raster(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate both slope and aspect rasters.

        :return: Tuple containing slope and aspect rasters as NumPy arrays.
        """
        gradient_x, gradient_y = self.get_gradient()
        slope_raster = self.get_slope_data(gradient_x, gradient_y)
        aspect_raster = self.get_aspect_data(gradient_x, gradient_y)
        return slope_raster, aspect_raster

    @staticmethod
    def fill_sink(dem_data: np.ndarray) -> np.ndarray:
        """
        Fill sinks in DEM data using connected component labeling and maximum filter.

        :param dem_data: Input DEM data as a NumPy array.
        :return: Sink-filled DEM data as a NumPy array.
        """
        labeled_array, num_features = label(dem_data)
        maxima = maximum_filter(dem_data, footprint=np.ones((3, 3)), labels=labeled_array)
        filled_dem = np.where(dem_data == maxima, dem_data, maxima)
        return filled_dem

    @staticmethod
    def get_direction_lookup_table() -> Dict[int, Tuple[int, int]]:
        """
        Get lookup table for D8 flow direction encoding.

        :return: Dictionary mapping flow direction codes to (x, y) offsets.
        """
        return {
            128: (1, 1),  # Northeast
            64: (0, 1),  # North
            32: (-1, 1),  # Northwest
            16: (-1, 0),  # West
            8: (-1, -1),  # Southwest
            4: (0, -1),  # South
            2: (1, -1),  # Southeast
            1: (1, 0)  # East
        }

    @staticmethod
    def get_inverted_flow_dir() -> Dict[int, int]:
        """
        Get inverted flow direction lookup table.

        :return: Dictionary mapping each direction to its opposite.
        """
        return {
            64: 4,  # North to South
            128: 8,  # Northeast to Southwest
            1: 16,  # East to West
            2: 32,  # Southeast to Northwest
            4: 64,  # South to North
            8: 128,  # Southwest to Northeast
            16: 1,  # West to East
            32: 2,  # Northwest to Southeast
            0: 0  # No flow remains no flow
        }

    @classmethod
    def flow_direction_d8(cls, dem: np.ndarray) -> np.ndarray:
        """
        Calculate D8 flow direction from a DEM.

        :param dem: Input DEM as a 2D NumPy array.
        :return: Flow direction as a 2D NumPy array.
        """
        directions = cls.get_direction_lookup_table()
        padded_dem = {direction: np.pad(dem, ((1 - offset[0], 1 + offset[0]),
                                              (1 - offset[1], 1 + offset[1])), mode='edge')
                      for direction, offset in directions.items()}
        drops = np.stack([padded_dem[direction][1:-1, 1:-1] - dem for direction in directions])
        steepest_descent = (2 ** np.argmax(drops, axis=0)).reshape(dem.shape)
        flow_dir = np.zeros_like(dem)
        for code, direction in directions.items():
            flow_dir[steepest_descent == code] = code
        return flow_dir

    @classmethod
    def flow_dir_xy(cls, flow_dir: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convert flow direction to x and y components.

        :param flow_dir: Flow direction as a 2D NumPy array.
        :return: Tuple of x and y components as 2D NumPy arrays.
        """
        lookup_table = cls.get_direction_lookup_table()
        vectorized_lookup = np.vectorize(lambda x: lookup_table.get(x, (0, 0)))
        flow_dir_x, flow_dir_y = vectorized_lookup(flow_dir)
        return flow_dir_x, flow_dir_y

    @classmethod
    def invert_flow_direction(cls, flow_dir: np.ndarray) -> np.ndarray:
        """
        Invert flow direction grid.

        :param flow_dir: Flow direction as a 2D NumPy array.
        :return: Inverted flow direction as a 2D NumPy array.
        """
        invert_map = cls.get_inverted_flow_dir()
        inverted = np.vectorize(invert_map.get)(flow_dir)
        return inverted

    @classmethod
    def calculate_flow_accumulation_d8_recursive(cls, flow_direction: np.ndarray) -> np.ndarray:
        """
        Recursively calculate flow accumulation from flow direction.

        :param flow_direction: Flow direction as a 2D NumPy array.
        :return: Flow accumulation as a 2D NumPy array.
        """
        flow_direction_mapping = cls.get_direction_lookup_table()
        rows, cols = flow_direction.shape
        flow_accumulation = np.zeros(flow_direction.shape)

        def accumulate_flow(r, c):
            if flow_accumulation[r, c] > 0:
                return flow_accumulation[r, c]
            flow_accumulation[r, c] = 1
            for direction, (dr, dc) in flow_direction_mapping.items():
                rr, cc = r + dr, c + dc
                if 0 <= rr < rows and 0 <= cc < cols and flow_direction[rr, cc] == direction:
                    flow_accumulation[r, c] += accumulate_flow(rr, cc)
            return flow_accumulation[r, c]

        for r in range(rows):
            for c in range(cols):
                accumulate_flow(r, c)

        return flow_accumulation

    @classmethod
    def calculate_flow_accumulation_d8(cls, flow_direction: np.ndarray) -> np.ndarray:
        """
        Calculate flow accumulation from flow direction using a queue-based approach.

        :param flow_direction: Flow direction as a 2D NumPy array.
        :return: Flow accumulation as a 2D NumPy array.
        """
        rows, cols = flow_direction.shape
        flow_accumulation = np.zeros(flow_direction.shape)
        flow_direction_mapping = cls.get_direction_lookup_table()
        queue = deque([(r, c) for r in range(rows) for c in range(cols)])

        while queue:
            r, c = queue.popleft()
            flow_accumulation[r, c] = 1
            for direction, (dr, dc) in flow_direction_mapping.items():
                rr, cc = r + dr, c + dc
                if 0 <= rr < rows and 0 <= cc < cols and flow_direction[rr, cc] == direction:
                    flow_accumulation[rr, cc] += flow_accumulation[r, c]
                    queue.append((rr, cc))

        return flow_accumulation

    @staticmethod
    def extract_streams(flow_accumulation: np.ndarray, threshold: float = None,
                        std_multiplier: float = 2) -> np.ndarray:
        """
        Extract stream network from flow accumulation.

        :param flow_accumulation: Flow accumulation as a 2D NumPy array.
        :param threshold: Minimum flow accumulation to consider as stream.
        :param std_multiplier: Multiplier for standard deviation to define threshold.
        :return: Stream network as a 2D NumPy array.
        """
        if threshold is None:
            valid_flow_mask = flow_accumulation > 1
            flow_accumulation_valid = flow_accumulation[valid_flow_mask]
            mean = np.mean(flow_accumulation_valid)
            std_dev = np.std(flow_accumulation_valid)
            threshold = mean + std_multiplier * std_dev
        stream_raster = np.where(flow_accumulation >= threshold, 255, 0).astype(np.uint8)
        return stream_raster

    @classmethod
    def delineate_watershed_for_point(cls, flow_dir: np.ndarray, pour_point: Tuple[int, int]) -> np.ndarray:
        """
        Delineate watershed area for a given pour point.

        :param flow_dir: Flow direction as a 2D NumPy array.
        :param pour_point: Tuple representing the coordinates of the pour point.
        :return: Watershed mask as a 2D NumPy array.
        """
        direction_offsets = cls.get_direction_lookup_table()
        inverted_flow_dir = cls.get_inverted_flow_dir()
        rows, cols = flow_dir.shape
        watershed_mask = np.zeros_like(flow_dir, dtype=bool)
        queue = deque([pour_point])

        while queue:
            r, c = queue.pop()
            if watershed_mask[r, c]:
                continue
            watershed_mask[r, c] = True
            for direction, (dr, dc) in direction_offsets.items():
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and not watershed_mask[nr, nc]:
                    if flow_dir[nr, nc] == inverted_flow_dir[direction]:
                        queue.append((nr, nc))

        return watershed_mask

    @staticmethod
    def plot_dem(dem: np.ndarray, extent: Tuple[float, float, float, float], plot_title: str, cbar_title: str = None):
        """
        Plot DEM data.

        :param dem: DEM data as a 2D NumPy array.
        :param extent: Tuple representing the extent of the plot (xmin, xmax, ymin, ymax).
        :param plot_title: Title of the plot.
        :param cbar_title: Optional title for the colorbar.
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_alpha(0)
        im = ax.imshow(dem, extent=extent, cmap='terrain', zorder=1)
        cbar = plt.colorbar(im, ax=ax, orientation='vertical', pad=0.01)
        if cbar_title is not None:
            cbar.set_label(cbar_title, rotation=270, labelpad=15)
        ax.grid(zorder=0)
        ax.set_title(plot_title, size=14)
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        plt.tight_layout()
        plt.show()
