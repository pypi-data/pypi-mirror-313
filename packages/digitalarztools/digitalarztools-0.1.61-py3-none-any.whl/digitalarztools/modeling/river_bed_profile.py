import math

import geopandas as gpd
from typing import List

import numpy as np
from shapely import Polygon, LineString, Point

from digitalarztools.io.raster.rio_raster import RioRaster


class RiverBedProfileCalculator:
    def __init__(self, cords_z: List[List[float]]):
        self.coords_z = cords_z

    def calculate_bed_length(self) -> float:
        p1 = Point(self.coords_z[0])
        p2 = Point(self.coords_z[-1])
        # Calculate the horizontal distance between the points
        return p1.distance(p2)

    def calculate_bed_slope(self) -> float:
        """
        The bed slope as a ratio is calculated using the formula:
        Δh is the change in elevation, and
        Δx is the horizontal distance. This ratio indicates the steepness of the slope.
        @return:
        """
        p1 = Point(self.coords_z[0])
        p2 = Point(self.coords_z[-1])
        # Calculate the change in elevation
        delta_h = p1.z - p2.z

        # Calculate the horizontal distance between the points

        delta_x = p1.distance(p2)

        # Calculate the bed slope
        bed_slope = delta_h / delta_x
        return bed_slope

    def calculate_spatial_steps(self) -> float:
        spatial_steps = []
        for index, coords in enumerate(self.coords_z):
            if index > 0:
                p1 = Point(self.coords_z[index - 1])
                p2 = Point(self.coords_z[index])
                spatial_steps.append(p1.distance(p2))
        return float(np.mean(spatial_steps))


class CrossSectionProfileCalculator:
    def __init__(self, cords_z: List[List[float]]):
        """
        @param cords_z:  [[x1,y1,z1]], [x2,y2,z2], [x3,y3,z3], [x4,y4,z4]]
        """
        self.coords_z = cords_z

    @classmethod
    def calculate_cross_section_profile(cls, dem_raster: RioRaster, line: gpd.GeoDataFrame) -> 'RiverBedProfile':
        """
           Sample elevation values from a DEM along a line.

           Parameters:
           dem_path (str): Path to the DEM file.
           line (shapely.geometry.LineString): LineString object representing the cross-section line.
           num_samples (int): Number of sample points along the line.
       """
        dem_epsg = dem_raster.get_crs().to_epsg()
        if line.crs.to_epsg() != dem_epsg:
            line.to_crs(epsg=dem_epsg, inplace=True)
        num_samples = math.ceil(
            line[line.geometry.name].values[0].length / dem_raster.get_spatial_resolution(in_meter=True)[0])
        points = [line.interpolate(float(i) / num_samples, normalized=True).values[0] for i in range(num_samples + 1)]
        coords = [[point.x, point.y] for point in points]
        elevations = np.array([val[0] for val in dem_raster.dataset.sample(coords)])
        coords_z = [[point.x, point.y, elevations[index]] for index, point in enumerate(points)]
        return cls(coords_z)

    def to_polyline_z(self) -> LineString:
        return LineString(self.coords_z)

    @staticmethod
    def to_coords_xz(coord_z):
        return [[xyz[0], xyz[2]] for xyz in coord_z]

    def calculate_bed_area(self) -> float:
        coords_xz = self.to_coords_xz(self.coords_z)
        coords_xz += [coords_xz[0]]
        return float(Polygon(coords_xz).area)

    def calculate_wetted_perimeter(self) -> float:
        coords_xz = self.to_coords_xz(self.coords_z)
        return float(LineString(coords_xz).length)

    def calculate_channel_width(self) -> float:
        width = Point(self.coords_z[0]).distance(Point(self.coords_z[-1]))
        return float(width)

    def calculate_elevation_stats(self) -> dict:
        z = np.array([coord[2] for coord in self.coords_z])
        return {"mean": float(np.mean(z)), "min": float(np.min(z)), "max": float(np.max(z)),
                "median": float(np.median(z)), "std": float(np.std(z))}

    def calculate_channel_depth(self):
        z = [coord[2] for coord in self.coords_z]
        min_z = np.min(z)
        max_z = np.max(z)
        return float(max_z - min_z)

    def calculate_centroid(self) -> List[float]:
        point = LineString(self.coords_z).centroid
        # Compute the average Z-coordinate
        avg_z = sum(coord[2] for coord in self.coords_z) / len(self.coords_z)
        return [float(point.x), float(point.y), float(avg_z)]

    @staticmethod
    def calculate_hydraulic_radius(A: float, P: float) -> float:
        """
        @param A: Area of cross section
        @param P: Wetted perimeter of cross section
        @return:
        """
        return float(A / P)
