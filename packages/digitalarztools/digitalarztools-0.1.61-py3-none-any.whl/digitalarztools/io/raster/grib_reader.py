
import cfgrib
import rasterio
from rasterio.transform import from_origin
from rasterio.io import MemoryFile
import xarray as xr
import numpy as np

from digitalarztools.io.raster.rio_raster import RioRaster


class GribReader():
    """
        Use cfgrib to read GRIB files and convert them to an in-memory rasterio dataset.
        Dependencies:
            - cfgrib: For reading GRIB files.
            - rasterio: For working with the raster data.
            - xarray: For handling multi-dimensional arrays.
            - numpy: For data manipulation.
    """

    def __init__(self, file_name: str):
        # Open a GRIB file as an xarray dataset
        self.ds = cfgrib.open_datasets(file_name)[0]
        print(self.ds)

    def get_variable_names(self):
        # Return a list of variable names available in the GRIB file
        return list(self.ds.variables.keys())

    def get_variable_values(self, variable_name: str):
        return self.ds[variable_name].values

    def to_rio_raster(self, variable_name: str) -> RioRaster:
        # Ensure the variable exists in the dataset
        if variable_name not in self.ds:
            raise ValueError(f"Variable '{variable_name}' not found in the dataset.")

        variable_data = self.ds[variable_name]

        # Extract spatial information
        latitude_start = self.ds.latitude.values.max()
        longitude_start = self.ds.longitude.values.min()
        latitudes = self.ds.latitude.values
        longitudes = self.ds.longitude.values
        pixel_height = abs(latitudes[0] - latitudes[1])
        pixel_width = abs(longitudes[0] - longitudes[1])

        # Define metadata for the new raster dataset
        transform = from_origin(longitude_start, latitude_start, pixel_width, pixel_height)
        new_dataset_meta = {
            'driver': 'GTiff',
            'height': variable_data.shape[0],
            'width': variable_data.shape[1],
            'count': 1,
            'dtype': str(variable_data.dtype),
            'crs': '+proj=latlong',
            'transform': transform
        }

        # Use MemoryFile to create an in-memory raster dataset
        with MemoryFile() as memfile:
            with memfile.open(**new_dataset_meta) as dataset:
                dataset.write(variable_data.values, 1)
            # Re-open the MemoryFile as a dataset
            return RioRaster(memfile.open())
