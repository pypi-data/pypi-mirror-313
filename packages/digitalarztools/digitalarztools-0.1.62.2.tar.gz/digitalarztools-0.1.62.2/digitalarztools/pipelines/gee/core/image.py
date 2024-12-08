import json
import os
import traceback
from datetime import datetime

import geopandas as gpd
from typing import List, Optional

import ee
import numpy as np
import pandas as pd
import requests
from PIL import Image
from ee.batch import Export
from rasterio import MemoryFile
from shapely.geometry import shape

from digitalarztools.io.file_io import FileIO
from digitalarztools.io.raster.rio_process import RioProcess
from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.io.url_io import UrlIO
from digitalarztools.pipelines.gee.core.region import GEERegion
from tqdm import tqdm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
from io import BytesIO


class GEEImage:
    image: ee.Image

    def __init__(self, img: ee.Image):
        self.image = img
        # self.bands = self.get_image_bands()
        self.bands = None

    @classmethod
    def get_image_by_tag(cls, tag: str) -> 'GEEImage':
        img = ee.Image(tag)
        return cls(img)

    def get_gee_image(self) -> ee.Image:
        return self.image

    def get_gee_id(self):
        return self.image.get('system:index').getInfo()

    def get_band(self, band_name, in_place=False) -> 'GEEImage':
        # nir = self.image.select('B5')
        if in_place:
            self.image = self.image.select(band_name)
        else:
            return GEEImage(self.image.select(band_name))

    def get_band_names(self):
        band_names = self.image.bandNames()
        # print('Band names:', band_names.getInfo())
        return band_names.getInfo()

    def get_min_max_scale(self, band_names: list = None) -> tuple:
        band_names = self.get_image_bands(self.image) if band_names is None else band_names
        min_scale, max_scale = -1, -1
        for band_name in band_names:
            scale = self.get_band_scale(band_name)[1]
            if min_scale == -1 or min_scale > scale:
                min_scale = scale
            if max_scale == -1 or max_scale < scale:
                max_scale = scale

        return min_scale, max_scale

    def get_band_scale(self, band_name: str):
        band_projection = self.image.select(band_name).projection()
        band_scale = band_projection.nominalScale()
        return (band_name, band_scale.getInfo())

    def get_band_projection(self, band_name: str):
        band_projection = self.image.select(band_name).projection()
        # band_scale = band_projection.nominalScale()
        # return (band_name, band_scale.getInfo())
        return band_projection.getInfo()

    def get_image_bands_info(self):
        # band_names = self.image.bandNames()
        # band_info = band_names.getInfo()
        band_info = self.get_image_bands(self.image)
        # print('Band names:', band_info)
        return band_info

    def get_image_metadata(self) -> dict:
        # print(self.image.getInfo())
        # properties = self.image.propertyNames()
        # print('Metadata properties:',
        #       properties.getInfo())  # ee.List of metadata properties
        return self.image.getInfo()

    def get_projection(self, is_info=True):
        # Get projection information from band 1.
        band_name = self.image.bandNames().getInfo()[0]
        # for b_name in band_names:
        #     b1_proj = self.image.select(b_name).projection()
        #     print('{} projection:'.format(b_name), b1_proj.getInfo())  # ee.Projection object

        projection = self.image.select(band_name).projection()
        return projection.getInfo() if is_info else projection

    def get_geo_transform(self, is_info=True):
        projection = self.get_projection(False)
        transform = projection.transform
        return transform.getInfo() if is_info else transform

    def get_crs(self, is_info=True):
        projection = self.get_projection(False)
        crs = projection.crs
        return crs.getInfo() if is_info else crs


    @staticmethod
    def get_image_region(img):
        geometry = img.geometry()

        # Check if the geometry is empty
        if geometry is None:  # or geometry.type().getInfo() == 'GeometryCollection':
            raise Exception("Region is not set for this image")

        # If the image has a geometry then return it
        return geometry

    def get_region(self):
        """Extracts the region of an ee.Image, raising an Exception if not set.

        Returns:
            The extracted ee.Geometry region.

        Raises:
            ValueError: If the image does not have a defined region.
        """
        # Get the geometry (region) of the image
        return self.get_image_region(self.image)

    def get_datatype(self):
        band_name = self.get_band_names()
        # Fetch information about this band
        if len(band_name) == 0:
            band_info = self.image.select(band_name[0]).getInfo()
            return band_info['data_type']

    def get_scale(self, b_name=None):
        # Get scale (in meters) information from band 1.
        if b_name is None:
            band_names = self.image.bandNames().getInfo()
            res = {}
            for b_name in band_names:
                b1_scale = self.image.select(b_name).projection().nominalScale()
                # print('{} scale:'.format(b_name), b1_scale.getInfo())  # ee.Number
                res[b_name] = b1_scale.getInfo()
            return res
        else:
            b1_scale = self.image.select(b_name).projection().nominalScale()
            return b1_scale.getInfo()

    def get_cloude_cover(self):
        # Get a specific metadata property.
        cloudiness = self.image.get('CLOUD_COVER')
        print('CLOUD_COVER:', cloudiness.getInfo())  # ee.Number

    def get_pixel_value(self, lon, lat):
        p = ee.Geometry.Point([lon, lat], 'EPSG:4326')
        band_names = self.image.bandNames().getInfo()
        pixel_info = []
        for b_name in band_names:
            data = self.image.select(b_name).reduceRegion(ee.Reducer.first(), p, 10).get(b_name)
            info = {"band": b_name, "value": ee.Number(data)}
            pixel_info.append(info)

    def get_map_id_dict(self, vis_params):
        map_id_dict = self.image.getMapId(vis_params)
        # print(map_id_dict)
        # print(map_id_dict['tile_fetcher'].url_format)
        return map_id_dict

    def get_map_id(self, vis_params):
        map_id_dict = self.image.getMapId(vis_params)
        res = {
            'mapid': map_id_dict['mapid'],
            'token': map_id_dict['token'],
            'url_format': map_id_dict['tile_fetcher'].url_format,
            'image': map_id_dict['image'].getInfo()
        }
        return res

    def get_url_template(self, vis_params):
        map_id_dict = self.image.getMapId(vis_params)
        return map_id_dict['tile_fetcher'].url_format

    def get_download_url(self, img_name, aoi: ee.Geometry.Polygon, scale=None):
        try:
            # Check if bands are already set, otherwise get them from the image.
            if not self.bands:
                self.bands = self.get_image_bands(self.image)

            # Check if the required bands are present.
            # missing_bands = [band for band in required_bands if band not in self.bands]
            # if missing_bands:
            #     raise ValueError(f"Missing bands in the image: {missing_bands}")

            # Generate download URL if required bands are present.
            url = self.image.getDownloadURL({
                'image': self.image.serialize(),
                'region': aoi,
                'bands': self.bands,
                'name': img_name,
                'scale': scale,
                'format': 'GEO_TIFF'
            })
            return url

        except ee.ee_exception.EEException as e:
            print(f"An Earth Engine error occurred: {e}")
            return None
        except ValueError as e:
            print(f"ValueError: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    # def download_bands(self, fp, region):
    #     meta_data = self.get_image_metadata()
    #     bands = meta_data['bands']
    #     # self.bands = self.get_image_bands()
    #     for index, band in enumerate(bands):
    #         id = band["id"]

    def to_rio_raster(self, img_region: GEERegion, scale=-1,
                      bit_depth=32, no_of_bands=None, delete_folder=True, within_aoi_only=True) -> RioRaster:
        if scale == -1:
            scale = self.get_scale()
            scale = min(scale.values())

        if no_of_bands is None:
            self.bands = self.get_image_bands(self.image)
            no_of_bands = len(self.bands)

        required_tiles = []

        for region, index in img_region.get_tiles(no_of_bands, scale, bit_depth=bit_depth,
                                                  within_aoi_only=within_aoi_only):
            required_tiles.append((region, index))
        try:
            datasets = []
            progress_bar = tqdm(desc="Processing Tiles", unit="tile", total=len(required_tiles))
            for i, (region, index) in enumerate(required_tiles):
                aoi = region.get_aoi()
                url = self.image.getDownloadURL({
                    'scale': scale,
                    'region': aoi,
                    'format': 'GEO_TIFF'
                })
                try:
                    # Download the image as a byte stream
                    response = requests.get(url)
                    response.raise_for_status()  # Raise an error for bad status codes

                    # Use a MemoryFile to read the byte stream with rasterio
                    memfile = MemoryFile(response.content)
                    dataset = memfile.open()
                    datasets.append((memfile, dataset))


                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

                progress_bar.update(1)
            progress_bar.close()

            if datasets:
                try:
                    # Extract the datasets from the tuples
                    dataset_readers = [dataset for memfile, dataset in datasets]

                    raster = RioProcess.mosaic_images(ds_files=dataset_readers)
                    return raster
                except Exception as e:
                    print(f"An unexpected error occurred during merging or saving: {e}")
                finally:
                    # Close all datasets and memory files
                    for memfile, dataset in datasets:
                        dataset.close()
                        memfile.close()
            else:
                print("No datasets were successfully processed.")
        except Exception as e:
            traceback.print_exc()
            print("Not enough memory available to download")
        return RioRaster(None)

    def download_image(self, file_path, img_region: GEERegion, scale=-1,
                       bit_depth=32, no_of_bands=None, delete_folder=True, within_aoi_only=True, save_metadata=True):
        if scale == -1:
            scale = self.get_scale()
            scale = min(scale.values())
        if no_of_bands is None:
            self.bands = self.get_image_bands(self.image)
            no_of_bands = len(self.bands)
        if save_metadata:
            print("saving meta data...")
            meta_data = self.get_image_metadata()
            meta_data_fp = f"{file_path[:-4]}_meta_data.json"
            dirname = FileIO.mkdirs(meta_data_fp)
            with open(meta_data_fp, "w") as f:
                # Serialize the dictionary to a JSON string and write it to the file
                json.dump(meta_data, f)
        print("downloading images...")
        dir_name = os.path.dirname(file_path)
        img_name, img_ext = FileIO.get_file_name_ext(os.path.basename(file_path))
        download_dir_name = os.path.join(dir_name, img_name)
        dirname = FileIO.mkdirs(download_dir_name)

        required_tiles = []

        for region, index in img_region.get_tiles(no_of_bands, scale, bit_depth=bit_depth,
                                                  within_aoi_only=within_aoi_only):
            required_tiles.append((region, index))
            # print(region, index)
        # df = pd.DataFrame(required_tiles)
        # Create a tqdm progress bar for the loop
        progress_bar = tqdm(desc="Processing Tiles", unit="tile", total=len(required_tiles))
        for i, (region, index) in enumerate(required_tiles):
            temp_file_path = os.path.join(download_dir_name, f"r{index[0]}c{index[1]}.tif")
            if not os.path.exists(temp_file_path):
                aoi = region.get_aoi()
                url = self.get_download_url(img_name, aoi=aoi, scale=scale)
                if url is not None:
                    res = UrlIO.download_url(url, temp_file_path)
            # Simulate some processing time
            # time.sleep(0.1)

            # Update the tqdm progress bar
            progress_bar.update(1)
        # Close the tqdm progress bar
        progress_bar.close()
        res = False
        try:
            raster = RioProcess.mosaic_images(download_dir_name)

            raster.save_to_file(file_path)
            if delete_folder:
                FileIO.delete_folder(download_dir_name)
            print('Image downloaded as ', file_path)

            res = True
        except:
            traceback.print_exc()
            res = False
        return res

    def to_geojson(self, scale=None, gee_region: GEERegion = None):
        if scale is None:
            scale = self.get_scale()
        region = gee_region.aoi if gee_region is not None else self.get_region()
        # Reduce the masked image to vectors (polygons).
        first_band_int = self.image.select(0).toInt()
        # Create a new image by combining the cast band with the rest of the image bands.
        image_int = first_band_int.addBands(
            self.image.select(ee.List.sequence(1, self.image.bandNames().size().subtract(1))))

        vector_polygons = image_int.reduceToVectors(
            geometryType='polygon',
            reducer=ee.Reducer.countEvery(),
            geometry=region,
            scale=scale,  # Adjust scale as needed.
            maxPixels=1e13
        )

        # Get the vector polygons as a GeoJSON dictionary.
        return vector_polygons.getInfo()

    def to_gdf(self, scale=None, gee_region: GEERegion = None):
        vector_polygons_geojson = self.to_geojson(scale, gee_region)
        # Create a list to hold the feature geometries and properties.
        features = []

        for feature in vector_polygons_geojson['features']:
            geom = shape(feature['geometry'])
            properties = feature['properties']
            features.append({'geometry': geom, **properties})

        # Create a GeoDataFrame from the features.
        gdf = gpd.GeoDataFrame(features)
        return gdf

    def to_numpy(self, aoi: ee.Geometry.Polygon = None, band_names: List[str] = [], is_r_c_b=True):
        """
        @param aoi:  ee.Geometry.Polygon
        @param band_names: list of band names
        @param is_r_c_b: row x col x band or band x row xcol
        @return:
        """
        image = self.image
        if aoi is None:
            aoi = self.get_region()
        if image.args:
            band_arrs = image.sampleRectangle(region=aoi)
            # Get band names
            if len(band_names) == 0:
                band_names = self.get_band_names()

            bands = []

            # Iterate over each band
            for i, name in enumerate(band_names):
                # name = band_names.get(i).getInfo()
                print('Band name: ', name)

                # Get the band data
                band_arr = band_arrs.get(name)
                np_arr = np.array(band_arr.getInfo())
                print("np_arr", np_arr.shape)

                # Expand the dimensions of the images so they can be concatenated into 3-D.
                np_arr_expanded = np.expand_dims(np_arr, 2)
                print("np_arr_expanded", np_arr_expanded.shape)

                # Append the expanded array to the list
                bands.append(np_arr_expanded)
            if is_r_c_b:
                # Concatenate all the bands along the third dimension
                np_image = np.concatenate(bands, axis=2)
            else:
                # Stack all the bands along the first dimension to get (bands, rows, cols)
                np_image = np.stack(bands, axis=0)
            if len(band_names) == 1:
                # Remove the singleton dimension to get (rows, cols)
                np_image = np.squeeze(np_image, axis=2)
            return np_image

    def export_output(self, name: str, bucket_name: str, region: ee.Geometry.Polygon, description: str = ''):
        # res = Export.image.toDrive(**{
        #     "image": self.output_image,
        #     "description": 'test',
        #     "folder": 'gee_python',
        #     "fileNamePrefix": name,
        #     "scale": 30,
        #     # "maxPixels": 1e13,
        #     "region": self.aoi.bounds().getInfo()['coordinates']
        # })
        # self.gee_image_2_numpy(self.output_image)
        res = Export.image.toCloudStorage(
            image=self.image,
            description=description,
            bucket=bucket_name,
            fileNamePrefix=name,
            scale=30,
            region=region
        )
        res.start()
        while res.status()['state'] not in ['FAILED', 'COMPLETED']:
            print(res.status())
        res_status = res.status()
        if res_status['state'] == 'FAILED':
            print("error:", res_status['error_message'])
        return res_status

    def get_histogram_data(self, band_name, aoi_sub: ee.Geometry.Polygon):
        data = self.image.select(band_name).reduceRegion(
            ee.Reducer.fixedHistogram(0, 0.5, 500), aoi_sub).get(band_name).getInfo()
        return data

    @staticmethod
    def get_histogram(img, region: GEERegion, scale: int, is_info_needed=True):
        histogram = img.reduceRegion(
            reducer=ee.Reducer.histogram(255),  # Adjust bin count as needed
            geometry=region,
            scale=scale,  # Adjust scale to match your imagery resolution
            bestEffort=True
        )
        values, frequencies = None, None
        if is_info_needed:
            histogram_info = histogram.getInfo()
            values = histogram_info['nd']['bucketMeans']
            frequencies = histogram_info['nd']['histogram']

        return histogram, values, frequencies

    def get_statistic(self, band_name, aoi_sub: ee.Geometry.Polygon):
        mean = self.image.select(band_name).reduceRegion(
            ee.Reducer.mean(), aoi_sub).get(band_name).getInfo()
        variance = self.image.select(band_name).reduceRegion(
            ee.Reducer.variance(), aoi_sub).get(band_name).getInfo()

        return mean, variance

    @staticmethod
    def generate_legend_as_bytes(label: str, palette: List[str], min_val: Optional[float] = None,
                                 max_val: Optional[float] = None) -> bytes:
        """
        Generate a color legend as bytes.
        """
        fig = Figure(figsize=(6, 1))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=0.5)

        # Ensure palette colors are in the correct format
        palette = ["#" + val if val[0] != "#" else val for val in palette]

        """
                Generate a color legend as bytes.
                """
        if min_val is not None and max_val is not None:
            # Create gradient color legend with Matplotlib
            fig = Figure(figsize=(6, 1))
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            fig.subplots_adjust(bottom=0.5)

            # Ensure palette colors are in the correct format
            palette = ["#" + val if val[0] != "#" else val for val in palette]

            cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", palette)
            norm = matplotlib.colors.Normalize(vmin=min_val, vmax=max_val)
            cbar = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation='horizontal')

            buf = BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            buf.seek(0)  # Rewind the buffer to the beginning
        else:
            # Create solid color legend with PIL
            width, height = 600, 100  # Define the size of the image
            image = Image.new("RGB", (width, height), palette[0])

            buf = BytesIO()
            image.save(buf, format='PNG')
            buf.seek(0)  # Rewind the buffer to the beginning

        return buf

    @staticmethod
    def convert_timestamp_to_datetime(timestamp) -> str:
        max_date = ee.Date(timestamp)

        # Format the date as a string (server-side)
        formatted_date = max_date.format('YYYY-MM-dd')
        return formatted_date.getInfo()

    @staticmethod
    def get_image_date(img) -> datetime:
        """
        return system time stamp
        """
        # Get the date of the latest image.
        latest_date = ee.Date(img.get('system:time_start')).getInfo()

        # Convert the timestamp to a readable format.
        formatted_date = datetime.utcfromtimestamp(latest_date['value'] / 1000)

        print('Latest acquisition date:', formatted_date.strftime('%Y-%m-%d'))
        return formatted_date

    def get_band_count(self):
        band_names = self.image.bandNames()

        return band_names.size().getInfo()

    @staticmethod
    def get_image_bands(img):
        try:
            return img.bandNames().getInfo()
        except ee.EEException as e:
            print(f"An error occurred while getting band names: {e}")
            return []

    @classmethod
    def get_imgae_url(cls, img, vis_params):
        bands = cls.get_image_bands(img)
        if len(bands) > 0:
            url = img.getMapId(vis_params)
            return url['tile_fetcher'].url_format

    def convert_to_binary_image(self, value, is_gt=True):
        # Create a binary mask where values greater than 1 are set to 1
        img_mask = self.image.gt(value) if is_gt else self.image.lt(value)

        # Apply the mask to the image
        binary_img = self.image.updateMask(img_mask)

        # Convert the masked image to binary (0s and 1s)
        return binary_img.selfMask().unmask(0)

    @staticmethod
    def get_image_stats(image, scale=None, reducer='all', bands=None, aoi=None) -> dict:
        try:
            final_stats = []
            if aoi is None:  # or geometry.type().getInfo() == 'GeometryCollection':
                aoi = image.geometry()
            if bands is None:
                bands = image.bandNames().getInfo()
            reducers = {"min": ee.Reducer.min(), "max": ee.Reducer.max(), "mean": ee.Reducer.mean()}
            for band in bands:
                stats = {"band_name": band}
                if scale is None:
                    scale = image.select(band).projection().nominalScale().getInfo()
                # print("band", band, "scale", scale)
                # Get the minimum value for the band.
                if reducer == 'all':
                    for reducer in reducers:
                        stats[reducer] = image.select(band).reduceRegion(
                            reducer=reducers[reducer],
                            geometry=aoi,
                            scale=scale,
                            maxPixels=1e13,  # Set a higher maxPixels limit
                            # bestEffort=True
                        ).get(band).getInfo()
                else:
                    stats[reducer] = image.select(band).reduceRegion(
                        reducer=reducers[reducer],
                        geometry=aoi,
                        scale=scale,
                        maxPixels=1e13,  # Set a higher maxPixels limit
                        # bestEffort=True
                    ).get(band).getInfo()
                final_stats.append(stats)
            return final_stats
        except Exception as e:
            traceback.print_exc()
            print(str(e))

    def info_ee_array_to_df(self, region: GEERegion, list_of_bands: list = None) -> pd.DataFrame:
        """
        Transforms client-side ee.Image.getRegion array to pandas.DataFrame.

        Args:
            region (GEERegion): The region of interest to fetch data for.
            list_of_bands (list, optional): A list of band names to include.
                                            If None, all bands are used. Defaults to None.

        Returns:
            pd.DataFrame: The DataFrame containing the extracted data,
                          or an empty DataFrame if an error occurs.
        """
        try:
            list_of_bands = self.get_band_names() if list_of_bands is None else list_of_bands

            if list_of_bands:  # Check if list_of_bands is not empty
                min_scale, max_scale = self.get_min_max_scale(list_of_bands)

                # Fetch image data, directly referencing the ee.Image
                arr = self.image.getRegion(geometry=region.aoi, scale=min_scale).getInfo()

                df = pd.DataFrame(arr)
                headers = df.iloc[0]
                df = df.iloc[1:].set_axis(headers, axis=1)  # Concise way to set headers

                # Convert columns to numeric (using errors='coerce' is more robust)
                for band in list_of_bands:
                    df[band] = pd.to_numeric(df[band], errors="coerce")

                # Convert 'time' to datetime (assuming it's in milliseconds)
                df["datetime"] = pd.to_datetime(df["time"], unit="ms")

                # Optional: Reorder columns if desired
                # df = df[["datetime", *list_of_bands]]

                # Optional: Set 'datetime' as index if needed
                # df.set_index("datetime", inplace=True)

                return df

            else:  # Handle the case where there are no bands to process
                return pd.DataFrame()

        except Exception as e:  # Catch specific exceptions for better error handling
            print(f"Error processing Earth Engine data: {e}")
            return pd.DataFrame()

    import geopandas as gpd

    def image_to_gdf(self, region: GEERegion, list_of_bands: list = None, crs: str = "EPSG:4326") -> gpd.GeoDataFrame:
        """
        Converts an Earth Engine Image to a GeoDataFrame.

        Args:
            region (GEERegion): The region of interest to extract data from.
            list_of_bands (list, optional): A list of band names to include.
                                            If None, all bands are used. Defaults to None.
            crs (str, optional): The coordinate reference system for the GeoDataFrame.
                                 Defaults to "EPSG:4326" (WGS84).

        Returns:
            gpd.GeoDataFrame: A GeoDataFrame containing the image data with point geometries, or
                              an empty GeoDataFrame if an error occurs or there's no data.
        """
        try:
            # Fetch data as DataFrame
            df = self.image_to_gdf(region, list_of_bands)

            if df.empty:
                print("No image data found in the specified region.")
                return gpd.GeoDataFrame()  # Return an empty GeoDataFrame if no data

            # Check if longitude and latitude are present
            if 'longitude' not in df.columns or 'latitude' not in df.columns:
                print("Longitude and/or latitude not found in the DataFrame.")
                return gpd.GeoDataFrame()

            # Convert to GeoDataFrame
            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs=crs)

            # Drop unnecessary columns
            gdf = gdf.drop(columns=['longitude', 'latitude'])

            return gdf

        except Exception as e:  # Broad exception handling for demonstration
            print(f"Error converting image to GeoDataFrame: {e}")
            return gpd.GeoDataFrame()

    @classmethod
    def to_assets(cls, img: ee.Image, region:GEERegion, scale:int, description:str, assetId:str):
        """

        @param img:
        @param scale:
        @param description:
        @param assetId:  like 'projects/ee-atherashraf-cloud/assets/heat_waves'
        @return:
        """
        # Define export parameters
        export_params = {
            'image': img,
            'description': description,
            'assetId': assetId,  # Replace with your username and desired asset ID
            'region': region.aoi,
            'scale': scale,
            'maxPixels': 1e18
        }

        # Start the export task
        task = ee.batch.Export.image.toAsset(**export_params)
        task.start()
        cls.wait_for_task(task)

    @staticmethod
    # Function to wait for the export to complete (Google Drive)
    def wait_for_task(task):
        import time
        while task.status()['state'] in ['READY', 'RUNNING']:
            print('Task still running...')
            time.sleep(30)
        print('Task completed:', task.status())