import ee

from digitalarztools.pipelines.gee.core.auth import GEEAuth
from digitalarztools.pipelines.gee.core.region import GEERegion


class GEEWaterAnalysis():
    @staticmethod
    def curve_number_surface(gee_auth: GEEAuth, roi):
        if gee_auth.is_initialized:
            # # Define the region of interest (adjust coordinates as needed)
            # roi = ee.Geometry.Rectangle([
            #     [-122.45, 37.74],
            #     [-122.40, 37.80]
            # ])

            # Load land use/land cover data (adjust to your dataset)
            lu = ee.ImageCollection('USGS/NLCD_RELEASES/2019_REL/NLCD').first()

            # Load soil data (adjust to your dataset)
            soil = ee.Image('USDA/NATSGO_CONUS_SOIL_PROPERTIES/2019')

            # Define a function to calculate Curve Number based on LU and soil group
            def calculateCN(luImage, soilImage):
                # Extract land use/cover class
                luClass = luImage.select('landcover')

                # Extract soil hydrologic group
                soilGroup = soilImage.select('hydgrp')

                # Create a dictionary to map LU classes and soil groups to CN values
                cnTable = {
                    '11': {'A': 77, 'B': 85, 'C': 90, 'D': 92},  # Open Water
                    '12': {'A': 70, 'B': 79, 'C': 84, 'D': 87},  # Perennial Ice/Snow
                    '21': {'A': 39, 'B': 61, 'C': 74, 'D': 80},  # Developed, Open Space
                    '22': {'A': 68, 'B': 79, 'C': 86, 'D': 89},  # Developed, Low Intensity
                    '23': {'A': 79, 'B': 84, 'C': 88, 'D': 90},  # Developed, Medium Intensity
                    '24': {'A': 89, 'B': 92, 'C': 94, 'D': 95},  # Developed, High Intensity
                    '31': {'A': 30, 'B': 58, 'C': 71, 'D': 78},  # Barren Land (Rock/Sand/Clay)
                    '41': {'A': 39, 'B': 61, 'C': 74, 'D': 80},  # Deciduous Forest
                    '42': {'A': 45, 'B': 66, 'C': 77, 'D': 83},  # Evergreen Forest
                    '43': {'A': 36, 'B': 55, 'C': 69, 'D': 75},  # Mixed Forest
                    '51': {'A': 55, 'B': 70, 'C': 77, 'D': 81},  # Dwarf Scrub
                    '52': {'A': 34, 'B': 51, 'C': 65, 'D': 72},  # Shrub/Scrub
                    '71': {'A': 49, 'B': 69, 'C': 79, 'D': 84},  # Grassland/Herbaceous
                    '72': {'A': 30, 'B': 58, 'C': 71, 'D': 78},  # Sedge/Herbaceous
                    '73': {'A': 45, 'B': 66, 'C': 77, 'D': 83},  # Lichens
                    '74': {'A': 25, 'B': 50, 'C': 63, 'D': 70},  # Moss
                    '81': {'A': 68, 'B': 79, 'C': 86, 'D': 89},  # Pasture/Hay
                    '82': {'A': 61, 'B': 75, 'C': 83, 'D': 87},  # Cultivated Crops
                    '90': {'A': 30, 'B': 55, 'C': 68, 'D': 74},  # Woody Wetlands
                    '95': {'A': 77, 'B': 85, 'C': 90, 'D': 92}  # Emergent Herbaceous Wetlands
                }

                # Use a look-up table to get CN values based on LU and soil
                cn = luClass.map(lambda c: soilGroup.map(
                    lambda s: cnTable[c.format()]['A'] if s == 1 else  # Hydgrp A
                    cnTable[c.format()]['B'] if s == 2 else  # Hydgrp B
                    cnTable[c.format()]['C'] if s == 3 else  # Hydgrp C
                    cnTable[c.format()]['D']  # Hydgrp D
                ))

                return cn.rename('cn')

            # Calculate Curve Number image
            cnImage = calculateCN(lu, soil)

            return cnImage
        else:
            print("Error: Please initialize Google Earth Engine")


    @staticmethod
    def get_water_level_using_change_detection_sentinel_1(region: GEERegion, water_mask: ee.Image,
                                                          before_date_range: tuple, after_date_range: tuple):
        """"
        @param region:
        @param water_mask: ee.Image
        @param before_date_range: range of date with start and end
        @param after_date_range: range of date with start and end
             (start_date.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))
        """
        # if date_range is None:
        #     date_range = GEEImageCollection.get_date_range(no_of_days=90)
        # Load Sentinel-1 SAR data
        polarization = 'VV'
        sentinel1_collection = (ee.ImageCollection('COPERNICUS/S1_GRD')
                                .filterBounds(region.bounds)
                                # .filterDate(date_range[0], date_range[1])
                                .filter(ee.Filter.listContains('transmitterReceiverPolarisation', polarization))
                                .filter(ee.Filter.eq('instrumentMode', 'IW'))
                                # .sort('system:time_start', False)  # Sort descending to get latest first
                                .select(polarization))
        after_collection = sentinel1_collection.filterDate(after_date_range[0], after_date_range[1])
        before_collection = sentinel1_collection.filterDate(before_date_range[0], before_date_range[1])

        # Calculate the median image for each time period
        before_img = before_collection.sum()
        after_img = after_collection.sum()

        # Calibration Factor (needs to be determined through empirical analysis)
        # multiply this factor will convert db of back scattering into meter
        # For indus basin  save assumption is
        # 0.03 to -0.10 meters per dB: This range suggests that for every 1 dB increase in backscatter,
        # you might expect a decrease in water level between 3 and 10 centimeters.
        calibration_factor = 0.07  # replace with your calibrated value)

        # Load a DEM (replace with your DEM source)
        dem = ee.Image('USGS/SRTMGL1_003');

        # Calculate the difference in backscatter, adding a small constant (e.g., 0.01)
        epsilon = 0.01
        difference_image = after_img.subtract(before_img).add(epsilon)

        # Calibration and Conversion Function
        def db_to_meters(img, calibration_factor,dem):
            """Converts backscatter difference (dB) to estimated water level (m)."""
            linear_power_ratio = ee.Image(10).pow(img.divide(10))  # dB to linear power
            water_level_change = linear_power_ratio.subtract(1).multiply(calibration_factor)
            return water_level_change.add(dem)  # Add DEM to get absolute water level

        # Calculate the difference and apply the calibration function
        masked_difference = difference_image.updateMask(water_mask)
        estimated_water_level_change = db_to_meters(masked_difference, calibration_factor, dem)


        return estimated_water_level_change