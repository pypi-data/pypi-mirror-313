import math

import networkx as nx
import numpy as np
from scipy.signal import convolve2d


class SARAnalysis:
    @staticmethod
    def unwrap_phase_using_goldstein_cut_out(wrapped_phase):
        """
        Unwraps the phase using the Goldstein branch cut method.
        Wrapped Phase: InSAR interferograms represent the phase difference between two SAR images. However, this phase is "wrapped" between -π and π. This wrapping makes it difficult to interpret the true displacement signal.
        Unwrapped Phase: Unwrapping is the process of removing these discontinuities in the wrapped phase to get a continuous phase signal, which is directly proportional to the displacement of the Earth's surface (in the case of ground deformation).
        @param wrapped_phase:
        @return:
        """

        kernel = np.array([[0, 1, 0],
                           [1, 0, 1],
                           [0, 1, 0]])

        # Calculate gradients of the wrapped phase
        phase_dx = convolve2d(wrapped_phase, kernel, mode='same', boundary='wrap')
        phase_dy = convolve2d(wrapped_phase, kernel.T, mode='same', boundary='wrap')

        # Determine the branch cuts
        branch_cuts = np.round((phase_dx + phase_dy) / (2 * np.pi))

        # Integrate the branch cuts to get the unwrapped phase
        unwrapped_phase = wrapped_phase + 2 * np.pi * np.cumsum(np.cumsum(branch_cuts, axis=0), axis=1)

        return unwrapped_phase

    @staticmethod
    def phase_unwrap_using_min_cost_flow(insar_phase):
        """
        phase unwrap using  Minimum Cost Flow
        Example:
            Replace this with your actual InSAR phase data
            insar_phase_data = np.random.rand(5, 5) * 2 * np.pi

            unwrapped_phase_result = phase_unwrap(insar_phase_data)
            print("Unwrapped Phase:")
            print(unwrapped_phase_result)

        """
        # Create a graph
        G = nx.Graph()

        # Add nodes for each pixel in the InSAR phase image
        rows, cols = insar_phase.shape
        for i in range(rows):
            for j in range(cols):
                G.add_node((i, j), phase=insar_phase[i, j])

        # Add source and sink nodes
        G.add_node('source')
        G.add_node('sink')

        # Connect source to all pixels in the first row
        for j in range(cols):
            G.add_edge('source', (0, j), capacity=1, weight=0)

        # Connect all pixels to sink
        for i in range(rows):
            for j in range(cols):
                G.add_edge((i, j), 'sink', capacity=1, weight=0)

                # Connect neighboring pixels with capacity and weight based on phase difference
                if i < rows - 1:
                    phase_diff = insar_phase[i + 1, j] - insar_phase[i, j]
                    weight = np.abs(phase_diff)  # Absolute phase difference as weight
                    G.add_edge((i, j), (i + 1, j), capacity=1, weight=weight)

                if j < cols - 1:
                    phase_diff = insar_phase[i, j + 1] - insar_phase[i, j]
                    weight = np.abs(phase_diff)
                    G.add_edge((i, j), (i, j + 1), capacity=1, weight=weight)

        # Solve the minimum cost flow problem
        flow_dict = nx.min_cost_flow(G, capacity='capacity', weight='weight')

        # Extract the unwrapped phase from the flow result
        unwrapped_phase = np.zeros_like(insar_phase, dtype=float)
        for i in range(rows):
            for j in range(cols):
                unwrapped_phase[i, j] = insar_phase[i, j] + flow_dict[(i, j)]['sink']

        return unwrapped_phase

    @staticmethod
    def surface_deformation(unwrapped_phase_data, wavelength: float, pixel_size: float):
        """
        # Constants
        wavelength: The wavelength of the SAR signal used
        (for Sentinel-1 C-band, t's about 5.6 cm or 0.056 meters.
         For X-band The value of 0.03 meters (3 cm) )
        Sentinel-1: you must use the C-band wavelength of 0.056 meters.
        wavelength = 0.056  # Replace with the actual wavelength of your imaging system
        pixel_size = 0.1  # Replace with the actual pixel size of your images

        """

        # Phase to Displacement Conversion
        displacement_data = (unwrapped_phase_data / (2 * np.pi)) * (wavelength * pixel_size)
        # in google earth engine use
        # displacement_data = unwrapped_phase_data.multiply(wavelength / (4 * math.pi));
        return displacement_data
