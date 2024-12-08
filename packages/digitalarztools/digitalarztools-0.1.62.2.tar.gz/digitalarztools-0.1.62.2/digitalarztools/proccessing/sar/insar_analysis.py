import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ee

from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.image_collection import GEEImageCollection
from digitalarztools.pipelines.gee.core.region import GEERegion


class InSARAnalysis:
    """

        Interferometric Synthetic Aperture Radar (InSAR) is a specialized technique used in radar remote sensing to measure ground surface deformation. InSAR relies on the interference patterns created by combining two or more radar images of the same area, acquired at different times. This technique is particularly useful for monitoring subtle changes in the Earth's surface, such as subsidence, uplift, and other deformations.

        Here's a basic overview of how InSAR works:

        Data Acquisition:

        SAR images are acquired by radar satellites at different times. Typically, two images are taken from slightly different positions in space during two separate passes.
        Interferogram Generation:

        The two SAR images are compared pixel by pixel, and the phase difference between the two images is calculated. This results in an interferogram, which is essentially an image of the phase changes on the ground between the two acquisition times.
        Phase Unwrapping:

        The interferogram contains phase information, but this information is "wrapped" because phase values are confined to a specific range (usually between -π and π). Phase unwrapping is the process of removing these wraps to obtain the true phase values.
        Surface Deformation Measurement:

        Once the phase unwrapping is complete, the resulting data can be used to measure ground surface deformation. Each full wrap of phase corresponds to a certain distance, often referred to as the "wavelength" of the radar signal.
        Generation of Deformation Maps:

        The unwrapped phase information is then converted into deformation maps, which represent the changes in the Earth's surface. Positive and negative values on these maps indicate uplift and subsidence, respectively.

        Note: In the context of interferometric analysis with Sentinel-1 data,
                the terms "master" and "slave" images are often used to represent
                two images acquired at different times.
                The "master" image is typically the reference image, and the
                "slave" image is the image acquired later in time.
    """

    @staticmethod
    def create_interferogram_using_gee(region: GEERegion, date_range: tuple) -> GEEImage:
        """
        date_range = ('2020-01-01', '2020-04-01')
        The "master" image is typically the reference image, and the "slave" image is the image acquired later in time.
            Map = geemap.Map()
            Map.centerObject(geometry, 8)
            Map.addLayer(master_terrain, {'min': -25, 'max': 5, 'bands': ['VV'], 'palette': ['black', 'blue', 'white']},
                         'Master Image')
            Map.addLayer(slave_terrain, {'min': -25, 'max': 5, 'bands': ['VV'], 'palette': ['black', 'blue', 'white']},
                         'Slave Image')
            Map.addLayer(interferogram, {'min': 0, 'max': 2, 'palette': ['black', 'blue', 'white']},
                         'Interferogram')
            Map.addLayerControl()
        """

        # Load Sentinel-1 GRD data
        sentinel1 = (ee.ImageCollection('COPERNICUS/S1_GRD')
                     .filterBounds(region.bounds)
                     .filterDate(date_range[0], date_range[1])
                     .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
                     .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
                     .filter(ee.Filter.eq('instrumentMode', 'IW'))
                     .sort('system:time_start'))

        # Get a list of images within the date range
        image_list = sentinel1.toList(sentinel1.size())

        # Get the master and slave images from the list
        master_image = ee.Image(ee.List(image_list).get(0))
        slave_image = ee.Image(ee.List(image_list).get(1))

        # Apply processing steps (speckle filtering, terrain correction, etc.) if needed
        master_filtered = master_image.select(['VV', 'VH']).focal_median()
        slave_filtered = slave_image.select(['VV', 'VH']).focal_median()

        # Specify the DEM (Digital Elevation Model) for terrain correction
        dem = ee.Image("USGS/SRTMGL1_003")

        # Terrain correction formula
        def terrain_correction(image):
            return image.select(['VV', 'VH']).subtract(ee.Image.constant(90.0)).subtract(dem)

        # Apply terrain correction
        master_terrain = terrain_correction(master_filtered)
        slave_terrain = terrain_correction(slave_filtered)

        # Generate interferogram
        interferogram = slave_terrain.divide(master_terrain)
        return GEEImage(interferogram)



    @staticmethod
    def create_interferogram(master_sar: RioRaster, slave_sar: RioRaster):
        slave_sar.make_coincident_with(master_sar)
        # Get data arrays
        master_data = master_sar.get_data_array(1)
        slave_data = slave_sar.get_data_array(1)

        # Compute interferogram (phase difference)
        interferogram = np.angle(np.exp(1j * (master_data - slave_data)))

        interferogram_raster = master_sar.rio_raster_from_array(interferogram)
        return interferogram_raster

    @staticmethod
    def phase_unwrap(insar_phase):
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
        wavelength = 0.03  # Replace with the actual wavelength of your imaging system
        pixel_size = 0.1  # Replace with the actual pixel size of your images

        """

        # Phase to Displacement Conversion
        displacement_data = (unwrapped_phase_data / (2 * np.pi)) * (wavelength * pixel_size)

        return displacement_data

    @staticmethod
    def display_insar(unwrapped_phase_data, displacement_data):
        # Visualization
        plt.figure(figsize=(8, 6))

        # Display the unwrapped phase map
        plt.subplot(2, 1, 1)
        plt.imshow(unwrapped_phase_data, cmap='jet', aspect='auto')
        plt.colorbar()
        plt.title('Unwrapped Phase Map')

        # Display the corresponding displacement map
        plt.subplot(2, 1, 2)
        plt.imshow(displacement_data, cmap='viridis', aspect='auto')
        plt.colorbar(label='Displacement (meters)')
        plt.title('Displacement Map')

        plt.tight_layout()
        plt.show()
