import math
import os

import pandas as pd
import rasterio
import numpy as np
from tqdm import tqdm

from digitalarztools.io.raster.rio_process import RioProcess
from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.io.vector.gpd_vector import GPDVector
from digitalarztools.proccessing.analysis.dem_analysis import DEMAnalysis


class SurfaceRunoff:
    """"
    Surface Runoff: For most applications, focus on the upper 0-30 cm layer.
    This layer will typically give a good indication of the soil's runoff potential,
    especially in response to short-duration, high-intensity rainfall.
    """

    def __init__(self):
        self.soil_texture_df = self.get_soil_texture_df()

    @staticmethod
    def get_soil_texture_df() -> pd.DataFrame:
        return pd.DataFrame({
            'HSG': ['A', 'A', 'B', 'B', 'C', 'C', 'C', 'D', 'D', 'D'],
            'Soil_Texture': ['Sand', 'Loamy Sand', 'Sandy Loam', 'Loam',
                             'Sandy Clay Loam', 'Clay Loam', 'Silty Clay Loam',
                             'Sandy Clay', 'Silty Clay', 'Clay'],
            # Minimum and maximum percentage of sand in the soil texture class
            'Sand_min': [85, 70, 50, 30, 45, 20, 0, 45, 0, 0],
            'Sand_max': [100, 85, 70, 50, 60, 45, 20, 100, 45, 45],
            # Minimum and maximum percentage of silt in the soil texture class
            'Silt_min': [0, 0, 0, 30, 0, 0, 40, 0, 40, 0],
            'Silt_max': [15, 30, 50, 50, 30, 50, 60, 20, 60, 40],
            # Minimum and maximum percentage of clay in the soil texture class
            'Clay_min': [0, 0, 10, 10, 27, 27, 27, 35, 40, 40],
            'Clay_max': [10, 20, 27, 27, 35, 40, 40, 100, 100, 100],
            # Comments for each soil texture classification
            'Comments': [
                'High infiltration, very low runoff potential (sandy soils).',
                'High infiltration, low runoff potential (loamy sand).',
                'Moderate infiltration, moderate runoff potential (sandy loam).',
                'Moderate infiltration, moderate runoff potential (loam).',
                'Slow infiltration, moderately high runoff potential (sandy clay loam).',
                'Slow infiltration, moderately high runoff potential (clay loam).',
                'Slow infiltration, moderately high runoff potential (silty clay loam).',
                'Very slow infiltration, high runoff potential (sandy clay).',
                'Very slow infiltration, high runoff potential (silty clay).',
                'Very slow infiltration, high runoff potential (clay).'
            ]
        })

    def classify_soil_texture(self, sand, silt, clay):
        """
        Classifies soil texture into Hydrologic Soil Groups (HSG) based on the
        percentages of sand, silt, and clay using a predefined DataFrame.
        """
        sand = math.floor(sand)
        silt = math.floor(silt)
        clay = math.floor(clay)
        condition = (
                (self.soil_texture_df['Sand_min'] <= sand) & (self.soil_texture_df['Sand_max'] >= sand) &
                (self.soil_texture_df['Silt_min'] <= silt) & (self.soil_texture_df['Silt_max'] >= silt) &
                (self.soil_texture_df['Clay_min'] <= clay) & (self.soil_texture_df['Clay_max'] >= clay)
        )

        result = self.soil_texture_df[condition]

        if not result.empty:
            return result.iloc[0]['HSG']
        else:
            closest_match = self.soil_texture_df.apply(
                lambda row: abs(row['Sand_min'] + row['Sand_max']) / 2 - sand +
                            abs(row['Silt_min'] + row['Silt_max']) / 2 - silt +
                            abs(row['Clay_min'] + row['Clay_max']) / 2 - clay,
                axis=1
            ).idxmin()

            closest_hsg = self.soil_texture_df.iloc[closest_match]['HSG']
            return closest_hsg

    # Calculate slope from DEM
    # @staticmethod
    # def calculate_slope(dem, pixel_size):
    #     # Simple slope calculation using central difference method
    #     dzdx = np.gradient(dem, axis=1) / pixel_size
    #     dzdy = np.gradient(dem, axis=0) / pixel_size
    #     slope = np.sqrt(dzdx ** 2 + dzdy ** 2) * 100  # Slope in percentage
    #     return slope

    # Define Runoff Coefficient based on Hydrologic Soil Group and slope
    @staticmethod
    def runoff_coefficient(soil_group, slope, om):
        # Base Coefficient by Soil Group
        base_coefficient = {
            'A': 0.20,
            'B': 0.40,
            'C': 0.60,
            'D': 0.80
        }

        # Adjust based on slope
        slope_factor = 1 + (slope / 100) * 0.05  # 0.05 increase per 10% slope

        # Adjust based on OM
        if om > 5:
            om_factor = 0.90  # Reduce coefficient by 10% for high OM
        else:
            om_factor = 1.00  # No change for low OM

        val = base_coefficient[soil_group] * slope_factor * om_factor
        return val

    def calculate_runoff_coefficient(self, sand: RioRaster, silt: RioRaster, clay: RioRaster, bulk_density: RioRaster,
                                     om: RioRaster, dem: RioRaster, temp_dir: str):
        aoi_gdf = sand.get_envelop()

        zxy_gdf = GPDVector.get_zxy_tiles(aoi_gdf, zoom=9)
        zxy_gdf.to_crs(sand.get_crs())
        # Open rasters and read data

        for index, row in tqdm(zxy_gdf.iterrows(), total=zxy_gdf.shape[0]):
            temp_file = os.path.join(temp_dir, f"{row['z']}_{row['x']}_{row['y']}.tif")
            if not os.path.exists(temp_file):
                aoi_gdf = GPDVector.row_to_gdf(row, columns=['geometry'], geom_col='geometry', crs=zxy_gdf.crs)
                sand_clip = sand.clip_raster(aoi_gdf, in_place=False)
                silt_clip = silt.clip_raster(aoi_gdf, in_place=False)
                clay_clip = clay.clip_raster(aoi_gdf, in_place=False)
                om_clip = om.clip_raster(aoi_gdf, in_place=False)
                dem_clip = dem.clip_raster(aoi_gdf, in_place=False)
                height, width = om_clip.get_img_resolution()
                dem_clip.resample_raster(width,height)
                sand_chunk = sand_clip.get_data_array(1)
                silt_chunk = silt_clip.get_data_array(1)
                clay_chunk = clay_clip.get_data_array(1)
                # bulk_density_data = bulk_density.get_data_array(1)
                om_chunk = om_clip.get_data_array(1)
                dem_data = dem_clip.get_data_array(1)
                res = dem.get_spatial_resolution()
                unit = dem.get_unit()
                centroid = aoi_gdf.unary_union.centroid
                z = DEMAnalysis.get_z_factor("m", unit="dd", lat=centroid.y)
                # Calculate slope
                slope_chunk = DEMAnalysis.calculate_slope_in_percent(dem_data, res, z)
                # print(f"sand_chunk shape: {sand_chunk.shape}")
                # print(f"silt_chunk shape: {silt_chunk.shape}")
                # print(f"clay_chunk shape: {clay_chunk.shape}")
                # print(f"slope_chunk shape: {slope_chunk.shape}")
                # print(f"om_chunk shape: {om_chunk.shape}")
                # print(f"dem_chunk shape: {dem_data.shape}")

                # Calculate runoff coefficient for each pixel
                # runoff_coeff = np.zeros(sand_data.shape, dtype=np.float32)

                # Apply vectorized operations on the chunk
                soil_group_chunk = np.vectorize(self.classify_soil_texture)(
                    sand_chunk, silt_chunk, clay_chunk
                )
                # print(soil_group_chunk)
                runoff_coeff = np.vectorize(self.runoff_coefficient)(
                    soil_group_chunk, slope_chunk, om_chunk
                )

                ro_ras = sand_clip.rio_raster_from_array(runoff_coeff)
                ro_ras.save_to_file(temp_file)
        raster = RioProcess.mosaic_images(temp_dir)
        return raster
        # Define a chunk size
        # chunk_size = 500
        # soil_texture_df = cls.get_soil_texture_df()
        # Process in chunks with progress bar
        # for i in tqdm(range(0, sand_data.shape[0], chunk_size), desc="Processing in chunks"):
        #     end_i = min(i + chunk_size, sand_data.shape[0])
        #     for j in range(0, sand_data.shape[1], chunk_size):
        #         end_j = min(j + chunk_size, sand_data.shape[1])
        #
        #         # Slice the chunks
        #         sand_chunk = sand_data[i:end_i, j:end_j]
        #         silt_chunk = silt_data[i:end_i, j:end_j]
        #         clay_chunk = clay_data[i:end_i, j:end_j]
        #         slope_chunk = slope_data[i:end_i, j:end_j]
        #         om_chunk = om_data[i:end_i, j:end_j]

        #
        # # Store results back in the original array
        # runoff_coeff[i:end_i, j:end_j] = runoff_coeff_chunk

        return runoff_coeff

    @staticmethod
    def calculate_runoff_potential(soil_moisture_path, field_capacity_path, precipitation_path, et0_path,
                                   runoff_coefficient_path, output_path, soil_layer_depth_mm=30):
        # Open the raster files
        with rasterio.open(soil_moisture_path) as soil_moisture_src, \
                rasterio.open(field_capacity_path) as field_capacity_src, \
                rasterio.open(precipitation_path) as precipitation_src, \
                rasterio.open(et0_path) as et0_src, \
                rasterio.open(runoff_coefficient_path) as runoff_coefficient_src:
            # Read the raster data as numpy arrays
            soil_moisture = soil_moisture_src.read(1)  # Fractional values
            field_capacity = field_capacity_src.read(1)  # Fractional values
            precipitation = precipitation_src.read(1)  # mm
            et0 = et0_src.read(1)  # mm
            runoff_coefficient = runoff_coefficient_src.read(1)  # Fractional values (0 to 1)

            # Convert fractional soil moisture and field capacity to depth in mm
            soil_moisture_depth = soil_moisture * soil_layer_depth_mm
            field_capacity_depth = field_capacity * soil_layer_depth_mm

            # Calculate soil water surplus (positive values indicate potential runoff)
            soil_water_surplus = soil_moisture_depth - field_capacity_depth

            # Calculate excess precipitation (precipitation minus ET0)
            excess_precipitation = precipitation - et0

            # Calculate runoff potential before applying the runoff coefficient
            runoff_potential_raw = soil_water_surplus + excess_precipitation

            # Apply the runoff coefficient to modulate the runoff potential
            runoff_potential = runoff_potential_raw * runoff_coefficient

            # Masking out invalid values (e.g., negative runoff potential)
            runoff_potential[runoff_potential < 0] = 0

            # Write the runoff potential to a new raster
            with rasterio.open(
                    output_path,
                    'w',
                    driver='GTiff',
                    height=soil_moisture_src.height,
                    width=soil_moisture_src.width,
                    count=1,
                    dtype=runoff_potential.dtype,
                    crs=soil_moisture_src.crs,
                    transform=soil_moisture_src.transform,
            ) as dest:
                dest.write(runoff_potential, 1)

        print(f"Runoff potential raster saved to {output_path}")


if __name__ == "__main__":
    # Paths to raster files
    sand_raster = 'path_to_sand_raster.tif'
    silt_raster = 'path_to_silt_raster.tif'
    clay_raster = 'path_to_clay_raster.tif'
    bulk_density_raster = 'path_to_bulk_density_raster.tif'
    om_raster = 'path_to_om_raster.tif'
    dem_raster = 'path_to_dem_raster.tif'

    # Calculate the runoff coefficient raster
    runoff_coefficient_raster = SurfaceRunoff.calculate_runoff_coefficient(sand_raster, silt_raster, clay_raster,
                                                                           bulk_density_raster,
                                                                           om_raster, dem_raster)

    # Optionally, save the output as a new raster file
    output_raster_path = 'runoff_coefficient.tif'
    with rasterio.open(dem_raster) as src:
        meta = src.meta.copy()
        meta.update(dtype=rasterio.float32)

        with rasterio.open(output_raster_path, 'w', **meta) as dst:
            dst.write(runoff_coefficient_raster, 1)

    # Paths to your raster files
    soil_moisture_path = 'path/to/soil_moisture.tif'
    field_capacity_path = 'path/to/field_capacity.tif'
    precipitation_path = 'path/to/precipitation.tif'
    et0_path = 'path/to/et0.tif'
    runoff_coefficient_path = 'path/to/runoff_coefficient.tif'
    output_path = 'path/to/runoff_potential.tif'

    # Calculate and save the runoff potential raster
    SurfaceRunoff.calculate_runoff_potential(soil_moisture_path, field_capacity_path, precipitation_path, et0_path,
                                             runoff_coefficient_path, output_path)
