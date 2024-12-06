import json
import os.path
import pandas as pd

import ee
import geopandas as gpd
from pyproj import CRS
from shapely.geometry import shape
from tqdm import tqdm

from digitalarztools.adapters.data_manager import DataManager
from digitalarztools.io.file_io import FileIO
from digitalarztools.io.vector.gpd_vector import GPDVector
from digitalarztools.pipelines.gee.core.region import GEERegion


class GEEFeatureCollection():
    fc: ee.FeatureCollection = None
    region: GEERegion = None

    def __init__(self, fc: ee.FeatureCollection, region: GEERegion = None):
        self.fc = fc
        if region is not None:
            self.region = region
            self.fc.filterBounds(region.get_aoi())


    def filter_bounds(self, region: GEERegion):
        self.region = region
        self.fc.filterBounds(region.get_aoi())

    def get_feature_list(self, bounds: ee.Geometry.Rectangle):
        # roi = ee.Geometry.Rectangle(bounds)  # Replace with actual coordinates
        fc = self.fc.filterBounds(bounds)
        # Get the feature collection as a list of dictionaries
        features_list = fc.getInfo()['features']
        return features_list

    def download_feature_zxy_tiles(self, aoi_gdf: gpd.GeoDataFrame,  base_folder : str, initial_zoom: int):
        tile_fp = os.path.join(base_folder, f"tile_{initial_zoom}.gpkg")
        FileIO.mkdirs(tile_fp)
        if not os.path.exists(tile_fp):
            tiles_gdf = GPDVector.get_zxy_tiles(aoi_gdf, initial_zoom)
            tiles_gdf.to_file(tile_fp, driver='GPKG')
        else:
            tiles_gdf = gpd.read_file(tile_fp, driver='GPKG')
        base_name = 'gee_building_data'
        fc_data_folder = os.path.join(base_folder, f"gee_building_data_z{initial_zoom}")

        data_manager = DataManager(folder_path=fc_data_folder, base_name=base_name,
                                   purpose="GOOGLE_Research_open-buildings_v3_polygons")
        for index, tile in tiles_gdf.iterrows():
            key = f"{base_name}_{tile.z}_{tile.x}_{tile.y}"
            fp = os.path.join(fc_data_folder, f"{key}.gpkg")
            record = {"x": tile.x, "y": tile.y, "z": tile.z}
            temp_folder = None
            if not data_manager.record_exists(key):
                tqdm.write(f"Processing tile {index} of {len(tiles_gdf)}")
                combined_gdf = gpd.GeoDataFrame()  # Empty GeoDataFrame to collect buildings

                try:
                    # Fetch buildings using Google Earth Engine (GEE)
                    gee_region = GEERegion.from_shapely_polygon(tile.geometry)
                    # gdf = GEELandUseLandCover.get_google_buildings(gee_region)
                    features_list = self.get_feature_list(gee_region.bounds)
                    combined_gdf = GPDVector.from_geojson(features_list, crs=CRS.from_epsg(4326))
                    # if not gdf.empty:
                    #     combined_gdf = pd.concat([combined_gdf, gdf], ignore_index=True)

                except ee.ee_exception.EEException as e:
                    tqdm.write(f"Error in tile {index} ({key}): {str(e)}")

                    # Reduce zoom level by 2 and try again
                    # new_zoom = 11
                    temp_folder = os.path.join(fc_data_folder, f'temp_{tile.z}_{tile.x}_{tile.y}')
                    FileIO.mkdirs(temp_folder)

                    self.retry_download_at_lower_zoom(tile, initial_zoom + 2, temp_folder)
                    combined_gdf = GPDVector.combine_files(temp_folder)
                    print("combined_gdf", combined_gdf.shape)

                # If the combined GeoDataFrame has buildings, save the results

                if not combined_gdf.empty:
                    combined_gdf = gpd.GeoDataFrame(combined_gdf, geometry='geometry', crs="EPSG:4326")
                    combined_gdf.to_file(fp, driver='GPKG', layer="buildings")
                    if temp_folder is not None:
                        print("Deleting temp folder", temp_folder)
                        FileIO.delete_folder(temp_folder)

                    record["is_empty"] = False
                    record["no_of_buildings"] = combined_gdf.shape[0]
                else:
                    record["is_empty"] = True
                    record["no_of_buildings"] = 0

                # Add record for the tile
                data_manager.add_record(key, record=record, geom=tile.geometry)
            else:
                tqdm.write(f"Tile {index} ({key}) already processed, skipping.")

        try:
            features_list = self.get_feature_list(self.region.bounds)
            gdf = GPDVector.from_geojson(features_list, crs=CRS.from_epsg(4326))
        except ee.ee_exception.EEException as e:
            tqdm.write(f"Error in tile {index} ({key}): {str(e)}")

    def retry_download_at_lower_zoom(self, tile, zoom, temp_folder):
        """
        Recursive function to handle reducing zoom level by 2 and combining data.
        """

        # exp_aoi_gdf = GPDVector.row_to_gdf(tile, PakDistricts.columns, crs="EPSG:4326", geom_col='geometry')
        exp_aoi_gdf = GPDVector.convert_tile_zxy_to_gdf(tile.x, tile.y, tile.z)
        new_tiles_gdf = GPDVector.get_zxy_tiles(aoi_gdf=exp_aoi_gdf, zoom=zoom)
        # Process new tiles at the lower zoom level
        for new_index, new_tile in tqdm(new_tiles_gdf.iterrows(), total=len(new_tiles_gdf),
                                        desc=f"Processing zoom {zoom} tiles"):
            try:
                temp_fp = os.path.join(temp_folder, f"{new_tile.x}_{new_tile.y}_{new_tile.z}.gpkg")
                if not os.path.exists(temp_fp):
                    # if show_size:
                    #     print("size", combined_gdf.shape)
                    gee_region = GEERegion.from_shapely_polygon(new_tile.geometry)
                    # building_gdf = GEELandUseLandCover.get_google_buildings(gee_region)
                    features_list = self.get_feature_list(gee_region.bounds)
                    building_gdf = GPDVector.from_geojson(features_list, crs=CRS.from_epsg(4326))
                    if not building_gdf.empty:
                        tqdm.write(f"Writing temp file at: {temp_fp}")
                        tqdm.write(f"size: {building_gdf.shape}")
                        building_gdf.to_file(temp_fp, driver='GPKG')
                else:
                    print("temp file already exist", {temp_fp})

            except ee.ee_exception.EEException as e:
                tqdm.write(f"Error in new tile at zoom {zoom}: {str(e)}")
                self.retry_download_at_lower_zoom(new_tile, zoom + 1, temp_folder)


    def download_feature_collection(self, fp: str):
        if self.region is not None:
            region_gdv = self.region.aoi_gdv

            dir_name = FileIO.mkdirs(fp)
            # print(index_map.head())
            # for index, geometry in enumerate(index_map.geometry):
            temp_dir = os.path.join(dir_name, "temp")
            temp_dir = FileIO.mkdirs(temp_dir)
            index_map_fp = os.path.join(dir_name, "index_map.gpkg")
            if os.path.exists(index_map_fp):
                index_map = GPDVector.from_gpkg(index_map_fp)
            else:
                index_map = GPDVector(region_gdv.create_index_map(1000))
                index_map.to_file(index_map_fp, driver='GPKG')
            for index, row in tqdm(index_map.iterrows(),
                                   total=index_map.shape[0],
                                   desc='Downloading features'):
                fp = os.path.join(temp_dir, f"r{row.row}_c{row.col}.gpkg")
                if not os.path.exists(fp):
                    # print(index)
                    roi = ee.Geometry.Rectangle(row.geometry.bounds)  # Replace with actual coordinates

                    fc = self.fc.filterBounds(roi)
                    # Get the feature collection as a list of dictionaries
                    features_list = fc.getInfo()['features']

                    # Extract geometries from the features
                    # geometries = [shape(feature['geometry']) for feature in features_list]

                    # Create a GeoDataFrame
                    # gdf = gpd.GeoDataFrame(features_list)
                    # gdf['geometry'] = gdf.geometry.apply(lambda g: shape(g))
                    # gdf.geometry = gdf['geometry']
                    # gdf.crs = 'EPSG:4326'

                    gdf = GPDVector.from_geojson(features_list)
                    # print(gdv.head())

                    gdf.to_file(fp, driver='GPKG')
            # # gdv.to_file()
            GPDVector.combine_files(temp_dir, output_fp=fp)
        else:
            print("please specify region....")

    def get_fc(self):
        return self.fc

    @classmethod
    def from_shapefile(cls, shp_path):
        gdf = gpd.read_file(shp_path)
        if gdf.crs != 'EPSG:4326':
            gdf = gdf.to_crs('EPSG:4326')
        geojson = json.loads(gdf.to_json())
        return cls.from_geojson(geojson)

    @classmethod
    def from_gee_tag(cls, tags):
        return ee.FeatureCollection(tags)

    @classmethod
    def from_geojson(cls, geojson: dict, proj='EPSG:4326'):
        ee_features = []
        for feature in geojson['features']:
            geom = ee.Geometry(feature["geometry"], opt_proj=proj)
            ee_features.append(ee.Feature(geom, feature['properties']))
        obj = cls()
        obj.fc = ee.FeatureCollection(ee_features)
        return obj

    def getInfo(self):
        return self.fc.getInfo()

    def getMapId(self):
        return self.fc.getMapId()

    @staticmethod
    def get_max_value(feature_collection, property_name):
        features = feature_collection['features']
        max = max(feature['properties'][f'{property_name}_max'] for feature in features)
        return max


