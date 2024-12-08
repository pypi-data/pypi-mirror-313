from collections import deque

import numpy as np
from matplotlib import pyplot as plt
from pysheds.pgrid import Grid
from pysheds.pview import Raster
from scipy import sparse
from scipy.ndimage import label, maximum_filter


class DEMProcess:

    @staticmethod
    def fill_sink(dem_data: np.ndarray):
        # Label connected components
        labeled_array, num_features = label(dem_data)

        # Find maxima within each label
        maxima = maximum_filter(dem_data, footprint=np.ones((3, 3)), labels=labeled_array)

        # Fill depressions
        filled_dem = np.where(dem_data == maxima, dem_data, maxima)

        return filled_dem

    @staticmethod
    def get_direction_lookup_table() -> dict:
        """
           lookup table
           Encoding        Direction	    Flow Direction (x, y)
           64              North (N)	    (0, -1)
           128             Northeast (NE)	(1, -1)
           1               East (E)	    (1, 0)
           2               Southeast (SE)	(1, 1)
           4               South (S)	    (0, 1)
           8               Southwest (SW)	(-1, 1)
           16              West (W)	    (-1, 0)
           32              Northwest (NW)	(-1, -1)
           0:              river mouth
           -1:             inland depression
           @rtype: dict

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
    def get_inverted_flow_dir():
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
    def flow_direction_d8(cls, dem: np.ndarray):
        """Calculates D8 flow direction from a DEM using a vectorized approach.

        Args:
            dem: A 2D NumPy array representing the Digital Elevation Model.

        Returns:
            A 2D NumPy array of the same shape as the input DEM, where each
            element represents the flow direction code (2, 4, 8, 16, 32, 64, 128) based on the D8 algorithm.
        """

        # Define D8 flow direction codes and corresponding offsets
        directions = cls.get_direction_lookup_table()

        # Create padded arrays for each direction to handle boundaries
        padded_dem = {direction: np.pad(dem, ((1 - offset[0], 1 + offset[0]),
                                              (1 - offset[1], 1 + offset[1])), mode='edge')
                      for direction, offset in directions.items()}

        # Vectorized drop calculation
        drops = np.stack([padded_dem[direction][1:-1, 1:-1] - dem for direction in directions])

        # Get steepest descent direction
        steepest_descent = (2 ** np.argmax(drops, axis=0)).reshape(dem.shape)  # Reshape here!

        # Convert to desired flow direction codes
        flow_dir = np.zeros_like(dem)
        for code, direction in directions.items():  # Corrected loop order

            flow_dir[steepest_descent == code] = code

        return flow_dir

    @classmethod
    def flow_dir_xy(cls, flow_dir) -> (np.ndarray, np.ndarray):

        lookup_table = cls.get_direction_lookup_table()

        # Vectorize lookup using np.vectorize
        vectorized_lookup = np.vectorize(lambda x: lookup_table.get(x, (0, 0)))

        # Apply vectorized lookup to flow direction values
        flow_dir_x, flow_dir_y = vectorized_lookup(flow_dir)

        # Calculate magnitude of flow direction for accumulation (optional)
        # flow_magnitude = np.sqrt(flow_dir_x ** 2 + flow_dir_y ** 2)
        return flow_dir_x, flow_dir_y

    @classmethod
    def invert_flow_direction(cls, flow_dir):
        """
        Inverts flow direction for a flow direction grid encoded with power of two values.
        Each direction is represented by a power of two, and the function maps each direction
        to its opposite.
        """
        # Define a mapping from each direction to its opposite
        invert_map = cls.get_inverted_flow_dir()
        inverted = np.vectorize(invert_map.get)(flow_dir)
        return inverted

    @classmethod
    def calculate_flow_accumulation_d8_recursive(cls, flow_direction):
        """
        Calculate the flow accumulation from flow direction.

        :param flow_direction: A 2D numpy array of flow directions
        :return: A 2D numpy array of flow accumulation
        """
        flow_direction_mapping = cls.get_direction_lookup_table()
        rows, cols = flow_direction.shape
        flow_accumulation = np.zeros(flow_direction.shape)

        def accumulate_flow(r, c):
            """Helper function to recursively accumulate flow"""
            if flow_accumulation[r, c] > 0:
                return flow_accumulation[r, c]

            flow_accumulation[r, c] = 1  # Each cell contributes at least itself

            # Check neighbors in flow direction
            for direction, (dr, dc) in flow_direction_mapping.items():
                rr, cc = r + dr, c + dc
                if 0 <= rr < rows and 0 <= cc < cols and flow_direction[rr, cc] == direction:
                    flow_accumulation[r, c] += accumulate_flow(rr, cc)

            return flow_accumulation[r, c]

        # Calculate flow accumulation for each cell
        for r in range(rows):
            for c in range(cols):
                accumulate_flow(r, c)

        return flow_accumulation

    @classmethod
    def calculate_flow_accumulation_d8(cls, flow_direction):
        rows, cols = flow_direction.shape
        flow_accumulation = np.zeros(flow_direction.shape)
        flow_direction_mapping = cls.get_direction_lookup_table()

        # Initialize queue with all cells
        queue = deque([(r, c) for r in range(rows) for c in range(cols)])

        # Iterate through the queue
        while queue:
            r, c = queue.popleft()
            flow_accumulation[r, c] = 1  # Each cell contributes at least itself

            for direction, (dr, dc) in flow_direction_mapping.items():
                rr, cc = r + dr, c + dc
                if 0 <= rr < rows and 0 <= cc < cols and flow_direction[rr, cc] == direction:
                    flow_accumulation[rr, cc] += flow_accumulation[r, c]
                    queue.append((rr, cc))

        return flow_accumulation

    @staticmethod
    def extract_streams(flow_accumulation, threshold=None, std_multiplier=2):
        """Extracts stream network from flow accumulation based on a threshold.

        Args:
            flow_accumulation: A 2D NumPy array of flow accumulation values.
            threshold: The minimum flow accumulation value to be considered a stream.

        Returns:
            A 2D NumPy array of the same shape as flow_accumulation, where 1 represents
            stream cells and 0 represents non-stream cells.
        """
        if threshold is None:
            # Mask out zero flow accumulation areas
            valid_flow_mask = flow_accumulation > 1
            flow_accumulation_valid = flow_accumulation[valid_flow_mask]

            # Calculate mean and standard deviation of non-zero flow accumulation
            mean = np.mean(flow_accumulation_valid)
            std_dev = np.std(flow_accumulation_valid)

            # Define threshold based on mean + std multiplier
            threshold = mean + std_multiplier * std_dev
        stream_raster = np.where(flow_accumulation >= threshold, 255, 0).astype(np.uint8)
        return stream_raster

    @classmethod
    def delineate_watershed_for_point(cls, flow_dir, pour_point):
        DIRECTION_OFFSETS = cls.get_direction_lookup_table()
        inverted_flow_dir = cls.get_inverted_flow_dir()
        rows, cols = flow_dir.shape
        watershed_mask = np.zeros_like(flow_dir, dtype=bool)
        queue = deque([pour_point])

        while queue:
            r, c = queue.pop()
            if watershed_mask[r, c]:
                continue  # Skip if already processed
            watershed_mask[r, c] = True
            for direction, (dr, dc) in DIRECTION_OFFSETS.items():
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and not watershed_mask[nr, nc]:
                    # Check if the flow direction leads to the current cell
                    if flow_dir[nr, nc] == inverted_flow_dir[direction]:
                        queue.append((nr, nc))

        return watershed_mask

    @staticmethod
    def plot_dem(dem, extent, plot_title, cbar_title = None):
        fig, ax = plt.subplots(figsize=(8, 6))

        # Ensure figure background is transparent
        fig.patch.set_alpha(0)

        # Plot the DEM
        im = ax.imshow(dem, extent=extent, cmap='terrain', zorder=1)

        # Add a colorbar
        cbar = plt.colorbar(im, ax=ax, orientation='vertical', pad=0.01)
        if cbar_title is not None:
            cbar.set_label(cbar_title, rotation=270, labelpad=15)

        # Add grid lines
        ax.grid(zorder=0)

        # Set titles and labels
        ax.set_title(plot_title, size=14)
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        # Adjust layout to fit everything nicely
        plt.tight_layout()

        # Display the plot
        plt.show()

