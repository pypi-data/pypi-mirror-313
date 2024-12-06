import math

import numpy as np
import geopandas as gpd
from pyproj import CRS
from shapely import Point, Polygon, LineString

from digitalarztools.io.raster.rio_raster import RioRaster


class HECRAS:
    @staticmethod
    def calculate_friction_slope(Q, n, A, R):
        """
        Calculate the friction slope using Manning's equation.
        Q: Discharge (m^3/s)
        n: Manning's roughness coefficient
        A: Cross-sectional area (m^2)
        R: Hydraulic radius (m)
        """
        return (Q * n / (A * R ** (2 / 3))) ** 2

    @staticmethod
    def specific_energy(y, Q, g, b):
        """
        Calculate specific energy.
        y: Water depth (m)
        Q: Discharge (m^3/s)
        g: Acceleration due to gravity (m/s^2)
        b: Channel width (m)
        """
        A = y * b
        return y + Q ** 2 / (2 * g * A ** 2)

    @classmethod
    def energy_gradient(cls, A, P, Q, S0, n, g):
        """
        Calculate the energy gradient.
        A: river bed area
        P: wetted perimeter
        Q: Discharge (m^3/s)
        S0: Bed slope
        n: Manning's roughness coefficient
        g: Acceleration due to gravity (m/s^2)
        """
        # A = y * b
        # R = A / (b + 2 * y)
        R = A / P
        Sf = cls.calculate_friction_slope(Q, n, A, R)

        dE_dy = 1 - Q ** 2 / (g * A ** 3)
        dE_dx = (S0 - Sf) / dE_dy

        return dE_dx

    @classmethod
    def steady_flow_solver(cls, A, P, Q, S0, n, dx, y0, g=9.81, max_iter=100, tol=1e-6):
        """
        Solve for the water height y using the finite difference method.
        Steady flow analysis is the Energy Equation, which is derived from Bernoulli’s equation and includes terms for energy losses due to friction and channel changes.
        A: river bed area
        P: wetted perimeter
        Q: Discharge (m^3/s)
        S0: Bed slope
        n: Manning's roughness coefficient
        dx: Spatial step (m)
        y0: Initial guess for water depth (m)
        g: Acceleration due to gravity (m/s^2)
        max_iter: Maximum number of iterations
        tol: Convergence tolerance
        """
        y = y0
        for iteration in range(max_iter):
            dE_dx = cls.energy_gradient(A, P, Q, S0, n, g)

            y_new = y - dx * dE_dx

            if abs(y_new - y) < tol:
                print(f"Converged after {iteration + 1} iterations.")
                break

            y = y_new
        else:
            print("Maximum iterations reached without convergence.")

        return y

    @staticmethod
    def calculate_water_level(initial_bed_area, initial_wetted_perimeter,
                              slope, target_Q, channel_width, channel_height, n=0.027):
        """
        derived from Manning's equation for discharge (Q) in open-channel flow. Manning's equation is commonly used to calculate the discharge based on the channel geometry, hydraulic radius, slope, and Manning's roughness coefficient
        @param initial_bed_area:
        @param initial_wetted_perimeter:
        @param slope:
        @param target_Q:
        @param channel_width:
        @param channel_height:
        @param n : Manning's roughness coefficient'
        @return:
        """

        # Function to calculate discharge based on given height
        def discharge_from_height(h, channel_width, slope, n=0.027):
            # assuming rectangle shape
            A = (channel_width * h) + initial_bed_area
            P = (channel_width + 2 * h) + initial_wetted_perimeter
            R = A / P  # Hydraulic radius
            # n = 0.027  # Manning's roughness coefficient
            return (1.49 / n) * (A * R ** (2 / 3)) * (slope ** (1 / 2))

        step_size = 1 / 3  # 1 foot height
        for h in np.arange(step_size, 100, step_size):  # A large practical limit for height
            discharge = discharge_from_height(h, channel_width, slope, n)
            # print(discharge, target_Q )
            if discharge > target_Q:
                height = h - step_size
                height += channel_height
                return height
        return 0

    @staticmethod
    def interpolate_discharge(q_min, q_max, min_point, max_point, xs_point):
        inv_distance_from_min = 1 / xs_point.distance(min_point)
        inv_distance_from_max = 1 / xs_point.distance(max_point)
        # Sum of all inverse distances
        total_inv_distance = inv_distance_from_min + inv_distance_from_max

        # Normalizing weights
        normalized_weight_min = inv_distance_from_min / total_inv_distance
        normalized_weight_max = inv_distance_from_max / total_inv_distance

        return q_max * normalized_weight_max + q_min * normalized_weight_min


if __name__ == "__main__":
    # Example parameters
    Q = 10  # Discharge (m^3/s)
    b = 5  # Channel width (m)
    S0 = 0.001  # Bed slope
    n = 0.03  # Manning's roughness coefficient
    dx = 100  # Spatial step (m)
    y0 = 2.0  # Initial guess for water depth (m)

    water_depth = HECRAS.steady_flow_solver(Q, b, S0, n, dx, y0)
    print("Calculated water depth:", water_depth)
