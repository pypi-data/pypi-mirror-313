import json
import os
import traceback
from datetime import datetime, date, timedelta
from typing import Union, List

import ee
import pandas as pd
from geopandas import GeoDataFrame

from tqdm import tqdm

from digitalarztools.adapters.data_manager import DataManager
from digitalarztools.io.file_io import FileIO
from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.region import GEERegion


class GEEImageCollection:
    # image_type: str = None
    img_collection: ee.ImageCollection = None

    # region: GEERegion = None
    # date_rage: tuple = None

    def __init__(self, img_col: ee.ImageCollection):
        self.img_collection = img_col

    @staticmethod
    def get_latest_image_collection(img_collection: ee.ImageCollection, limit: int = -1):
        img_collection = img_collection.sort('system:time_start', False)
        if limit > 0:
            img_collection = img_collection.limit(limit)
        return img_collection

    @classmethod
    def from_tags(cls, image_type: str, date_range: tuple = None, region: Union[GEERegion, dict] = None):
        """
        Parameters
        ----------
        :param image_type:  dataset name or type like 'COPERNICUS/S2_SR' for other check gee documentation
        :param date_range: tuple
            range of date with start and end value like
            ('2021-01-01', '2021-12-31')
            or can be calculated through  time delta
            today = datetime.date.today()
             start_date = today - datetime.timedelta(days=365)
            self.date_range = (start_date.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))
        example:
              s2_collection = ee.ImageCollection('COPERNICUS/S2_SR') \
             .filterDate(start_date, end_date) \
             .filterBounds(fc) \
             .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 10)
        """

        # self.image_type = image_type
        img_collection = ee.ImageCollection(image_type)
        if region is not None:
            region = GEERegion.from_geojson(region) if isinstance(region, dict) else region
            img_collection = img_collection.filterBounds(region.bounds)

        if date_range is not None:
            img_collection = img_collection.filterDate(date_range[0], date_range[1])
        return cls(img_collection)

    def set_region(self, region: Union[GEERegion, dict]):
        region = GEERegion.from_geojson(region) if isinstance(region, dict) else region
        self.img_collection = self.img_collection.filterBounds(region.bounds)

    def set_region_from_poi(self, poi: ee.Geometry.Point, buffer: float):
        self.img_collection = self.img_collection.getRegion(poi, buffer)
        # self.region = GEERegion(region)

    def set_date_range(self, date_range=None, no_of_days=10):
        """
        :param date_range: range of date with start and end value like ('2021-01-01', '2021-12-31')
        :param no_of_days: or no_of_days starting from today
        :return:
        """
        if date_range is None:
            date_range = self.calculate_date_range(no_of_days)
        # self.date_range = date_range
        self.img_collection = self.img_collection.filterDate(date_range[0], date_range[1])

    def select_dataset(self, ds_name: str):
        """
        :param ds_name: dataset name like 'precipitation' in  'UCSB-CHG/CHIRPS/DAILY'
        :return:
        """
        self.img_collection = self.img_collection.select(ds_name)

    def select_bands(self, bands: Union[List, str]) -> 'GEEImageCollection':
        """
        example
            bands = ['B2', 'B3', 'B4', 'B7', 'B8', 'B8A', 'B11', 'B12']
            indices = ['NDVI', 'NDWI', 'NDBI', 'EVI']  additional bands added
            features = ee.List(bands + indices)
        :param bands:
        :return:
        """
        if isinstance(bands, List):
            features = ee.List(bands)
        else:
            features = bands
        new_img_collection = self.img_collection.select(features)
        return GEEImageCollection(new_img_collection)

    def add_bands(self, types: list):
        """
        use to add bands in the image collection
        :param types: list having value "mask_cloud", "NDVI", "NDWI", "NBI", "EVI"
        :return:
        """
        from digitalarztools.pipelines.gee.analysis.indices import GEEIndices
        for t in types:
            t = t.lower()
            if t == "mask_cloud":
                self.img_collection = self.img_collection.map(self.mask_s2_clouds)
            elif t == "ndvi":
                self.img_collection = self.img_collection.map(GEEIndices.add_ndvi)
            elif t == "ndwi":
                self.img_collection = self.img_collection.map(GEEIndices.add_ndwi)
            elif t == "ndbi":
                self.img_collection = self.img_collection.map(GEEIndices.add_ndbi)
            elif t == "evi":
                self.img_collection = self.img_collection.map(GEEIndices.add_evi)

    @staticmethod
    def mask_s2_clouds(image):
        qa = image.select('QA60')
        # Bits 10 and 11 are clouds and cirrus, respectively.
        cloud_bit_mask = int(2 ** 10)
        cirrus_bit_mask = int(2 ** 11)
        # Both flags should be set to zero, indicating clear conditions.
        mask = qa.bitwiseAnd(cloud_bit_mask).eq(0). \
            And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))

        return image.updateMask(mask).divide(10000) \
            .select("B.*") \
            .copyProperties(image, ["system:time_start"])

    def get_collection_size(self):
        size = self.img_collection.size().getInfo()
        return size

    def get_collection_list(self):
        return self.img_collection.toList(self.img_collection.size()).getInfo()

    def get_image_collection(self):
        return self.img_collection

    def enumerate_collection(self) -> (int, GEEImage):
        size = self.img_collection.size().getInfo()
        img_list = ee.List(self.img_collection.toList(self.img_collection.size()))
        for i in range(size):
            yield i, GEEImage(ee.Image(img_list.get(i)))

    def get_image_info_within_poi(self, poi: ee.Geometry.Point, buffer):
        info = self.img_collection.getRegion(poi, buffer).getInfo()
        # pprint.pprint(local_pr[:5])
        return info

    def get_image_info_within_region(self, region: GEERegion):
        info = self.img_collection.getRegion(region.get_aoi()).getInfo()
        return info

    def info_ee_array_to_df(self, region: GEERegion, list_of_bands: list = None) -> pd.DataFrame:
        """
        Transforms client-side ee.Image.getRegion array to pandas.DataFrame.
        :param arr:
        :param list_of_bands:
        :return:
        """
        # img = self.get_image(how='median')
        # gee_image = GEEImage(img)
        try:
            gee_image = GEEImage(self.img_collection.first())

            list_of_bands = gee_image.get_band_names() if list_of_bands is None else list_of_bands
            if len(list_of_bands) != 0:
                min_scale, max_scale = gee_image.get_min_max_scale(list_of_bands)
                # print(min_scale, max_scale)

                arr = self.img_collection.getRegion(geometry=region.aoi, scale=min_scale).getInfo()

                df = pd.DataFrame(arr)

                # Rearrange the header.
                headers = df.iloc[0]
                df = pd.DataFrame(df.values[1:], columns=headers)

                # Convert the data to numeric values.
                for band in list_of_bands:
                    df[band] = pd.to_numeric(df[band], errors="coerce")

                # Convert the time field into a datetime.
                df["datetime"] = pd.to_datetime(df["time"], unit="ms")

                # Keep the columns of interest.
                # df = df[["time", "datetime", *list_of_bands]]

                # The datetime column is defined as index.
                # df = df.set_index("datetime")

                return df
            else:
                return pd.DataFrame()
        except:
            return pd.DataFrame()

    @staticmethod
    def sum_resampler(coll: ee.ImageCollection, freq, unit, scale_factor, band_name):
        """
        This function aims to resample the time scale of an ee.ImageCollection.
        The function returns an ee.ImageCollection with the averaged sum of the
        band on the selected frequency.

        coll: (ee.ImageCollection) only one band can be handled
        freq: (int) corresponds to the resampling frequence
        unit: (str) corresponds to the resampling time unit.
                    must be 'day', 'month' or 'year'
        scale_factor (float): scaling factor used to get our value in the good unit
        band_name (str) name of the output band
        example:
        # Apply the resampling function to the precipitation dataset.
            pr_m = sum_resampler(pr, 1, "month", 1, "pr")
        # Apply the resampling function to the PET dataset.
            pet_m = sum_resampler(pet.select("PET"), 1, "month", 0.0125, "pet")
        # Combine precipitation and evapotranspiration.
            meteo = pr_m.combine(pet_m)

        """
        # Define initial and final dates of the collection.
        firstdate = ee.Date(
            coll.sort("system:time_start", True).first().get("system:time_start")
        )

        lastdate = ee.Date(
            coll.sort("system:time_start", False).first().get("system:time_start")
        )

        # Calculate the time difference between both dates.
        # https://developers.google.com/earth-engine/apidocs/ee-date-difference
        diff_dates = lastdate.difference(firstdate, unit)

        # Define a new time index (for output).
        new_index = ee.List.sequence(0, ee.Number(diff_dates), freq)

        # Define the function that will be applied to our new time index.
        def apply_resampling(date_index):
            # Define the starting date to take into account.
            startdate = firstdate.advance(ee.Number(date_index), unit)

            # Define the ending date to take into account according
            # to the desired frequency.
            enddate = firstdate.advance(ee.Number(date_index).add(freq), unit)

            # Calculate the number of days between starting and ending days.
            diff_days = enddate.difference(startdate, "day")

            # Calculate the composite image.
            image = (
                coll.filterDate(startdate, enddate)
                .mean()
                .multiply(diff_days)
                .multiply(scale_factor)
                .rename(band_name)
            )

            # Return the final image with the appropriate time index.
            return image.set("system:time_start", startdate.millis())

        # Map the function to the new time index.
        res = new_index.map(apply_resampling)

        # Transform the result into an ee.ImageCollection.
        res = ee.ImageCollection(res)

        return res

    def get_latest_image_date(self):
        # Sort the collection by the acquisition date in descending order
        sorted_collection = self.img_collection.sort('system:time_start', False)

        # Get the latest image
        latest_image = sorted_collection.first()
        # Get the acquisition date of the latest image
        latest_date = ee.Date(latest_image.get('system:time_start')).getInfo()
        formatted_date = datetime.utcfromtimestamp(latest_date['value'] / 1000)

        print('Latest acquisition date:', formatted_date.strftime('%Y-%m-%d'))
        return formatted_date

    # Section: Date  Functions

    @staticmethod
    def calculate_date_range(no_of_days=10, end_date=None) -> (str, str):
        """
        Calculates a date range starting 'no_of_days' before the specified (or current) end date.

        Args:
            no_of_days: The number of days prior to the end date to include in the range (default: 10).
            end_date: The ending date of the range. If None, defaults to the current date.

        Returns:
            A tuple containing two strings:
                - The start date in YYYY-MM-DD format.
                - The end date in YYYY-MM-DD format.
        """

        # Handle missing end_date: Use today's date if not provided.
        if end_date is None:
            end_date = date.today()

        # Calculate the start date by subtracting the specified number of days from the end date.
        start_date = end_date - timedelta(days=no_of_days)

        # The commented line was likely meant to find the first day of the current month. It is currently unused.
        # first = today.replace(day=1)

        # Format the start and end dates into YYYY-MM-DD strings.
        date_range = (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

        # Return the calculated date range as a tuple.
        return date_range

    @staticmethod
    def convert_timestamp_to_datetime(timestamp) -> str:
        return GEEImage.convert_timestamp_to_datetime(timestamp)

    @staticmethod
    def get_collection_max_date(img_col: ee.ImageCollection):
        max_timestamp = img_col.aggregate_max('system:time_start')
        # max_timestamp = img_col.first().get('system:time_start')
        # Convert the timestamp to an ee.Date object (server-side)
        max_date = ee.Date(max_timestamp)

        # Format the date as a string (server-side)
        formatted_date = max_date.format('YYYY-MM-dd')
        # return formatted_date.getInfo()
        return datetime.strptime(formatted_date.getInfo(), "%Y-%m-%d").date()

    @staticmethod
    def get_collection_min_date(img_col: ee.ImageCollection):
        min_timestamp = img_col.aggregate_min('system:time_start').getInfo()
        # Convert the timestamp to an ee.Date object (server-side)
        min_date = ee.Date(min_timestamp)

        # Format the date as a string (server-side)
        formatted_date = min_date.format('YYYY-MM-dd')
        return datetime.strptime(formatted_date.getInfo(), "%Y-%m-%d").date()

    @classmethod
    def get_collection_date_range(cls, img_col: ee.ImageCollection) -> (datetime.date, datetime.date):
        max_date = cls.get_collection_max_date(img_col)
        min_date = cls.get_collection_min_date(img_col)
        return (min_date, max_date)

    @staticmethod
    def get_uniques_dates_in_collection(img_col: ee.ImageCollection):
        """
        Extracts a list of unique dates (YYYY-MM-dd) from an Earth Engine ImageCollection.

        Args:
            img_col: The Earth Engine ImageCollection to process.

        Returns:
            ee.List: A list of unique dates in the format YYYY-MM-dd.
        """

        # Step 1: Extract Dates and Set 'date' Property
        # - Apply a function to each image in the collection.
        # - The lambda function sets a new property called 'date' on each image, formatted as 'YYYY-MM-dd'.
        dates = img_col.map(lambda image: ee.Image(image).set('date', image.date().format('YYYY-MM-dd')))

        # Step 2: Select Unique Dates
        # - Use the 'distinct' method to filter the collection based on the unique values of the 'date' property.
        # - This effectively removes any duplicate images with the same date.
        unique_dates_images = dates.distinct('date')

        # Step 3: Aggregate Dates into a List
        # - Extract the 'date' property from each unique image.
        # - Aggregate the dates into a single list.
        unique_dates = unique_dates_images.aggregate_array('date')

        return unique_dates

    def get_ymd_list(self):
        # Inner Function: Processes each image in the collection
        def iter_func(image, newList):
            # Extract the image date as a YYYY-MM-dd string
            date = ee.String(image.date().format("YYYY-MM-dd"))

            # Convert the existing list (newList) to an EE List for manipulation
            newlist = ee.List(newList)

            # Add the current date to the list, sort the list, and return it
            return ee.List(newlist.add(date).sort())

            # Apply the iteration to the image collection

        return self.get_image_collection().iterate(iter_func, ee.List([])).getInfo()

    def get_dates(self) -> List[datetime]:
        """
        Retrieves a list of datetime objects representing the start dates of images in an ImageCollection.

        Returns:
            List: A list of datetime objects, each representing the UTC start date of an image in the ImageCollection.
        """

        # 1. Get start time metadata as a list of milliseconds since epoch
        dates = self.img_collection.aggregate_array('system:time_start')
        dates_milliseconds = dates.getInfo()

        # 2. Convert milliseconds to datetime objects
        # Divide by 1000 to convert milliseconds to seconds, then create datetime objects
        dates = [datetime.utcfromtimestamp(date / 1000) for date in dates_milliseconds]

        return dates

    @staticmethod
    def get_datasets_latest_date(region: GEERegion, tag: str) -> datetime:
        date_range = GEEImageCollection.calculate_date_range()
        img_collection = GEEImageCollection(ee.ImageCollection(tag)
                                            .filterBounds(region.bounds)
                                            .filterDate(date_range[0], date_range[1])
                                            )

        img = img_collection.get_image(how='latest')
        img = img.clip(region.bounds)
        # date = img_collection.get_latest_image_date()
        date = GEEImage.get_image_date(img)
        return date

    # Section: Extract Image from collection

    @staticmethod
    def get_image_ids(collection: ee.ImageCollection):
        def extract_id(image):
            image_id = image.get('system:id')
            # return ee.Feature(None, {'image_id': image_id})
            return image_id

        # Apply the function to each image in the collection
        id_collection = collection.map(extract_id, opt_dropNulls=True)

        # Convert the feature collection to a list of features
        id_list = id_collection.aggregate_array('id').getInfo()
        return id_list

    def get_image(self, how=None) -> ee.Image:
        """
        :param how: choices are 'median', 'max', 'mean', 'first', 'cloud_cover', 'sum' ,'latest'
        :return:
        """
        # if collection.size().getInfo() > 0:
        # image: ee.Image = None
        if how == 'median':
            image = self.img_collection.median()  # .rename(f'median_{name}')
        elif how == "min":
            image = self.img_collection.min()  # .rename(f'min_{name}')
        elif how == "std":
            image = self.img_collection.reduce(ee.Reducer.stdDev())  # .rename(f'std_{name}')
        elif how == 'max':
            image = self.img_collection.max()  # .rename(f'max_{name}')
        elif how == 'mean':
            image = self.img_collection.mean()  # .rename(f'mean_{name}')
        elif how == 'sum':
            image = self.img_collection.sum()  # .rename(f'total_{name}')
        elif how == 'cloud_cover':
            image = self.img_collection.sort('CLOUD_COVER').first()  # .rename(f'least_cloud_{name}')
        elif how == "oldest":
            image = self.img_collection.sort('system:time_start', True).first()  # .rename(f'oldest_{name}')
        else:
            # self.img_collection.sort()
            image = self.img_collection.sort('system:time_start', False).first()  # .rename(f'latest_{name}')
        # ee.Date(image.get('system:time_start')).format('YYYY-MM-dd HH:mm:ss').getInfo()
        # ee.Date(image.get('system:time_end')).format('YYYY-MM-dd HH:mm:ss').getInfo()
        return image

    def get_image_at_index(self, index: int) -> ee.Image:
        """
            img_col.get(0) returns the first image.
            img_col.get(1) returns the second image.
            img_col.get(4) returns the fifth image.
        @param img_col:
        @param index:
        @return:
        issue:

        **the image at the given index is always a fresh Image so any operation done
        like change kelvin to celcius not returented
        **also if band is selected in this case you will again get all bands
        """
        # Sort the collection in descending order
        sorted_img_col = self.img_collection.sort('system:time_start', False)

        # Get the image at the specified index directly from a list
        img = ee.Image(sorted_img_col.toList(index + 1).get(index))  # Get list up to index+1 and then image at index

        return img

    @classmethod
    def get_image_of_date(cls, img_collection, date_range: (datetime, datetime)) -> ee.Image:
        """
        @param img_collection:
        @param date:
        @return:
        """
        start_date = ee.Date(date_range[0].isoformat())
        end_date = ee.Date(date_range[1].isoformat())
        filtered = (img_collection.filterDate(start_date, end_date)
                    .sort('system:time_start', True))
        count = filtered.size().getInfo()
        if count == 1:
            return filtered.first()
        elif count != 1:
            raise Exception(f"More than one image exist in date_range {date_range}")

    @staticmethod
    def get_image_count(img_col) -> int:
        return img_col.size().getInfo()

    @staticmethod
    def get_latest_image_in_collection(image_collection: ee.ImageCollection) -> ee.Image:
        return image_collection.sort('system:time_start', False).first()

    @staticmethod
    def get_oldest_image_in_collection(image_collection: ee.ImageCollection) -> ee.Image:
        return image_collection.sort('system:time_start').first()

    # Section: Collection Combinations, Aggregation and Stats

    @staticmethod
    def convert_hourly_to_daily_collection(img_collection: ee.ImageCollection, how='max') -> ee.ImageCollection:
        """Converts an hourly image collection to a daily collection using a specified statistic.

        Args:
            img_collection: The input hourly image collection.
            how: The statistic to use for aggregation ('max', 'min', 'mean', 'sum', 'median'). Default is 'max'.

        Returns:
            An image collection with one image per day, calculated using the chosen statistic.
        """

        def daily_stats(date):
            day_start = ee.Date(date)
            day_end = day_start.advance(1, 'day')

            daily_collection = img_collection.filterDate(day_start, day_end)

            # Use a dictionary for cleaner reduction logic
            reducers = {
                'max': daily_collection.max(),
                'min': daily_collection.min(),
                'sum': daily_collection.sum(),
                'median': daily_collection.median(),
                'mean': daily_collection.mean()  # Default to mean if 'how' is invalid
            }

            image = reducers.get(how, daily_collection.mean())  # Handle invalid 'how' values
            image = image.set('system:time_start', day_start.millis())  # Use millis for consistency
            return image

        unique_dates = img_collection.aggregate_array('system:time_start').distinct()
        daily_images = ee.ImageCollection(unique_dates.map(daily_stats))
        return daily_images

    @staticmethod
    def convert_daily_to_monthly_collection(img_collection: ee.ImageCollection, how='mean') -> ee.ImageCollection:
        """Converts a daily image collection to a monthly image collection using the specified reduction method.

        Args:
            img_collection: The daily image collection to convert.
            how: The reduction method to use. Choices are 'mean', 'max', 'median', 'sum'.

        Returns:
            The monthly image collection.
        """

        def monthly_stats(month_start_date):
            month_end_date = month_start_date.advance(1, 'month')

            # Find the millisecond timestamp for the start of the NEXT month
            next_month_start_millis = month_end_date.millis()

            monthly_filtered_collection = img_collection.filterDate(month_start_date, month_end_date)

            if how == 'max':
                monthly_image = monthly_filtered_collection.max()
            elif how == 'min':
                monthly_image = monthly_filtered_collection.min()
            elif how == 'sum':
                monthly_image = monthly_filtered_collection.sum()
            elif how == 'median':
                monthly_image = monthly_filtered_collection.median()
            else:  # Default to mean
                monthly_image = monthly_filtered_collection.mean()

            monthly_image = monthly_image.set('system:time_start', month_start_date.millis())
            monthly_image = monthly_image.set('system:time_end', next_month_start_millis - 1)  # 1ms before next month
            return monthly_image

        # Convert dates to start of month, filter, then convert back to ensure correct mapping
        months_collection = img_collection.map(
            lambda img: img.set('system:time_start', ee.Date(img.get('system:time_start')).get('month')))
        unique_months = months_collection.aggregate_array('system:time_start').distinct()
        unique_months_dates = unique_months.map(lambda month: ee.Date(month))

        monthly_images = ee.ImageCollection(unique_months_dates.map(monthly_stats))
        return monthly_images

    @classmethod
    def download_collection(cls, img_coll: ee.ImageCollection, region: GEERegion,
                            folder_path, base_file_name, scale):
        """

        @param img_coll:
        @param region:
        @param folder_path:
        @param base_file_name:
        @param scale:
        @param how: if hourly data how: choices are 'median', 'max', 'mean', 'first', 'cloud_cover', 'sum' ,'latest'
        @return:
        """
        dates = cls(img_coll).get_dates()
        for index, current_date in enumerate(tqdm(dates, desc='Downloading collection')):
            fp = os.path.join(folder_path, f"{base_file_name}_{current_date.strftime('%Y%m%d-%H')}.tif")
            if index == 0 or os.path.exists(fp):
                continue
            previous_date = dates[index - 1]
            print(f"Downloading {os.path.basename(fp)}")

            img = cls.get_image_of_date(img_coll, (previous_date, current_date))
            if img is not None:
                GEEImage(img).download_image(fp, img_region=region, scale=scale, save_metadata=True)

    @staticmethod
    def get_collection_monthly_stats(img_collection: ee.ImageCollection, region: GEERegion, monthly_fp: str,
                                     date_range: tuple = None, band_name: str = None,
                                     scale: int = None, ) -> pd.DataFrame:
        data = []
        if date_range is None:
            date_range = GEEImageCollection.get_collection_date_range(img_collection)
        if band_name is None:
            band_name = img_collection.first().bandNames().getInfo()[0]
        fn, ext = FileIO.get_file_name_ext(monthly_fp)
        monthly_fp_temp = os.path.join(os.path.dirname(monthly_fp), f"{fn}_temp.{ext}")
        # Load existing data from the file if it exists
        print("working on temp file", monthly_fp_temp)
        if os.path.exists(monthly_fp_temp):
            with open(monthly_fp_temp, 'r') as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # Extract the years that are already present in the existing data
        existing_years = {entry['year'] for entry in existing_data}
        is_error = False
        for year in tqdm(range(date_range[0].year, date_range[1].year + 1)):
            # Skip the year if it already exists in the file
            if year in existing_years:
                print(f"Year {year} already exists in the file. Skipping...")
                continue

            for month in range(1, 13):
                try:
                    start_date = date(year, month, 1)
                    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

                    # Filter the image collection for the specified month
                    monthly_collection = GEEImageCollection(
                        img_collection.filterDate(start_date.strftime('%Y-%m-%d'),
                                                  end_date.strftime('%Y-%m-%d')))

                    size = monthly_collection.get_collection_size()
                    if size > 0:
                        gee_image_max = monthly_collection.get_image('max').clip(region.aoi)
                        max_stats = GEEImage.get_image_stats(gee_image_max, scale, reducer="max", bands=[band_name])
                        max_value = max_stats[band_name]['max']
                        gee_image_min = monthly_collection.get_image('min').clip(region.aoi)
                        min_stats = GEEImage.get_image_stats(gee_image_min, scale, reducer="min", bands=[band_name])
                        min_value = min_stats[band_name]['min']
                        gee_image_mean = monthly_collection.get_image('mean').clip(region.aoi)
                        mean_stats = GEEImage.get_image_stats(gee_image_mean, scale, reducer="mean", bands=[band_name])
                        mean_value = mean_stats[band_name]['mean']

                        # Reduce the region to get the min, max, and avg temperature
                        # stats = self.safe_reduce_region_stats(monthly_collection.mean(), self.gee_pipline.region.aoi)

                        data.append({
                            'year': year,
                            'month': month,
                            'min': min_value,
                            'max': max_value,
                            'avg': mean_value
                        })
                except Exception as e:
                    is_error = True
                    traceback.print_exc()
                    print(str(e), year, month)

            # Append the new data for the year to the existing data
            existing_data.extend(data)

            # Save the updated data to the JSON file
            with open(monthly_fp_temp, 'w') as file:
                json.dump(existing_data, file, indent=4)

            # Clear the data list for the next year
            data = []

        # If you want to convert the final data to a DataFrame
        df = pd.DataFrame(existing_data)
        print(df.head())
        if not is_error:
            completed = FileIO.copy_file_content(monthly_fp_temp, monthly_fp)
            if completed:
                os.remove(monthly_fp_temp)
                print(f"Temp deleted successfully.")
        return df
