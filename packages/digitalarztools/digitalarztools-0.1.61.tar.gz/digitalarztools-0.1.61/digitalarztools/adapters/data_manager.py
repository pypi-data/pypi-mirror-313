import os
import sqlite3
import json
from datetime import date, datetime
from typing import Optional, Union

import geopandas as gpd
import pandas as pd
import pyproj
# from pandas.core.internals import DataManager

from shapely import wkb
from shapely.geometry.base import BaseGeometry
from shapely.ops import transform

from digitalarztools.io.file_io import FileIO


class DataManager:
    def __init__(self, folder_path: str, base_name: str, purpose: str = None):
        if not base_name.startswith("da_"):
            base_name = "da_" + base_name
        if not base_name.endswith(".db"):
            base_name = base_name + ".db"
        self.db_path = os.path.join(folder_path, base_name)
        FileIO.mkdirs(self.db_path)
        self.metadata_file = os.path.join(folder_path, f"da_{base_name}_metadata.json")
        self.metadata = {
            "field_name": [],
            "geom_field_name": "",
            "record_count": 0,
            "purpose": purpose,
            "additional_cols": []
        }
        self.table_name = "records"
        self._initialize_db()
        self._load_metadata()

    @classmethod
    def from_file_path(cls, file_path: str) -> 'DataManager':
        dir = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        return cls(dir, base_name)

    def get_database_file_path(self):
        return self.db_path

    def get_metadata_file_path(self):
        return self.metadata_file

    def _initialize_db(self):
        # Initialize the SQLite database and create the table if it doesn't exist
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                key TEXT UNIQUE,
                data JSON,
                geom BLOB
            )
        ''')
        self.conn.commit()

    def _load_metadata(self):
        # Load metadata from the JSON file
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as file:
                self.metadata = json.load(file)

    def _save_metadata(self):
        # Save metadata to the JSON file
        with open(self.metadata_file, 'w') as file:
            json.dump(self.metadata, file, indent=4)

    @staticmethod
    def default_serializer(obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    @staticmethod
    def ensure_srid_4326(geom: BaseGeometry, original_crs) -> BaseGeometry:
        """
        Ensures the geometry is in SRID 4326. If not, reprojects it.

        Parameters:
        ----------
        geom : BaseGeometry
            The Shapely geometry object.

        original_crs

        Returns:
        -------
        BaseGeometry
            The geometry reprojected to SRID 4326, if necessary.
        """
        if geom is not None:
            # Define the target CRS (SRID 4326)
            target_crs = pyproj.CRS.from_epsg(4326)

            # Only transform if the current CRS is different from 4326
            if original_crs != target_crs:
                project = pyproj.Transformer.from_crs(original_crs, target_crs, always_xy=True).transform
                geom = transform(project, geom)

        return geom

    def add_record(self, key: str, record: dict,
                   geom: Optional[BaseGeometry] = None, geom_crs=None) -> bool:
        """geom must be in 4326"""
        """
        Adds a record to the database table with optional geometric data.

        Parameters:
        ----------
        key : str
            A unique identifier for the record. This is used as the primary key in the database.

        record : dict
            A dictionary containing the data to be serialized into JSON format and stored in the database.

        geom : Optional[Union[BaseGeometry, bytes, bytearray, memoryview]]
            The geometric data associated with the record. It can be:
            - A Shapely geometry object (e.g., Point, Polygon) which will be converted to WKB.
            - A bytes-like object representing the WKB of a geometry.
            - None if there is no geometric data to store.

        Returns:
        -------
        bool
            True if the record was successfully added, False if a record with the same key already exists.
        """
        try:
            # Serialize the record dictionary to a JSON string
            record_json = json.dumps(record, default=self.default_serializer)

            # Handle the geometric data based on its type

            # Convert Shapely geometry to WKB
            if geom_crs is not None:
                geom = self.ensure_srid_4326(geom, geom_crs)
            if geom is not None:
                geom = sqlite3.Binary(geom.wkb)

            # Construct and execute the SQL query to insert the data into the database
            query = f'INSERT INTO {self.table_name} (key, data, geom) VALUES (?, ?, ?)'
            self.cursor.execute(query, (key, record_json, geom))

            # Update metadata with field names and increment record count
            self.metadata['field_name'] = list(record.keys())
            self.metadata['record_count'] += 1

            # Commit the changes to the database
            self.conn.commit()

            # Save the metadata
            self._save_metadata()

            # Return True indicating success
            return True

        except sqlite3.IntegrityError:
            # Handle the case where a record with the same key already exists
            print(f"Record with key '{key}' already exists.")
            return False

        except Exception as e:
            # Catch any other exceptions and print the error message
            print(f"An error occurred: {e}")
            return False

    def delete_record(self, key: str) -> bool:
        """
        Deletes a record from the database table based on the key.

        Parameters:
        ----------
        key : str
            The unique identifier for the record to be deleted.

        Returns:
        -------
        bool
            True if the record was successfully deleted, False if the record with the given key does not exist.
        """
        try:
            # Construct and execute the SQL query to delete the record
            query = f'DELETE FROM {self.table_name} WHERE key = ?'
            self.cursor.execute(query, (key,))

            # Check if any rows were affected by the deletion
            if self.cursor.rowcount == 0:
                # If no rows were affected, the record with the given key does not exist
                print(f"Record with key '{key}' does not exist.")
                return False

            # Commit the changes to the database
            self.conn.commit()

            # Update metadata and save it (e.g., decrement record count)
            self.metadata['record_count'] -= 1
            self._save_metadata()

            # Return True indicating success
            return True

        except Exception as e:
            # Catch any exceptions and print the error message
            print(f"An error occurred while deleting the record: {e}")
            return False

    def update_record(self, key: str, record: dict,
                      geom: Optional[BaseGeometry] = None, geom_crs=None) -> bool:
        """
        Updates an existing record in the database table with new data and optional geometric data.

        Parameters:
        ----------
        key : str
            The unique identifier for the record to be updated. This is used to locate the specific record in the database.

        record : dict
            A dictionary containing the new data to be serialized into JSON format and stored in the database.

        geom : Optional[Union[BaseGeometry, bytes, bytearray, memoryview]]
            The new geometric data associated with the record. It can be:
            - A Shapely geometry object (e.g., Point, Polygon) which will be converted to WKB.
            - A bytes-like object representing the WKB of a geometry.
            - None if there is no geometric data to update.

        Returns:
        -------
        bool
            True if the record was successfully updated, False if the record with the given key does not exist.
        """
        try:
            # Serialize the record dictionary to a JSON string
            record_json = json.dumps(record, default=self.default_serializer)

            # Convert Shapely geometry to WKB
            if geom_crs is not None:
                geom = self.ensure_srid_4326(geom, geom_crs)
            if geom is not None:
                geom = sqlite3.Binary(geom.wkb)

            # Construct and execute the SQL query to update the existing record in the database
            query = f'UPDATE {self.table_name} SET data = ?, geom = ? WHERE key = ?'
            self.cursor.execute(query, (record_json, geom, key))

            # Check if any rows were affected by the update
            if self.cursor.rowcount == 0:
                # If no rows were affected, the record with the given key does not exist
                print(f"Record with key '{key}' does not exist.")
                return False

            # Commit the changes to the database
            self.conn.commit()

            # Return True indicating success
            return True

        except Exception as e:
            # Catch any exceptions and print the error message
            print(f"An error occurred: {e}")
            return False

    def get_record(self, key: str):
        query = f'SELECT data, geom FROM {self.table_name} WHERE key = ?'
        self.cursor.execute(query, (key,))
        result = self.cursor.fetchone()
        if result:
            record = json.loads(result[0])
            geom = gpd.GeoSeries.from_wkb(result[1]) if result[1] is not None else None
            return record, geom
        return None, None

    def record_exists(self, key: str):
        query = f'SELECT 1 FROM {self.table_name} WHERE key = ?'
        self.cursor.execute(query, (key,))
        return self.cursor.fetchone() is not None

    def get_metadata(self):
        return self.metadata

    def get_data_as_df(self, query: str = None) -> pd.DataFrame:
        """
        Fetches data from the database and returns it as a DataFrame.

        Parameters:
        ----------
        query : str, optional
            An SQL query string to fetch specific data from the database.
            If not provided, the function will fetch all records.

        Returns:
        -------
        pd.DataFrame
            A DataFrame containing the fetched records.
        """
        if query is None:
            # Prepare the list of columns to fetch
            columns_to_select = ['key', 'data']

            # Add additional columns from metadata to the selection list
            if "additional_cols" in self.metadata:
                columns_to_select.extend(self.metadata["additional_cols"])

            # Build the SQL query with the necessary columns
            columns_str = ', '.join(columns_to_select)
            query = f'SELECT {columns_str} FROM {self.table_name}'

        # Execute the query
        self.cursor.execute(query)

        # Fetch the data and get the column names from the query
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        # Process the fetched rows
        records = []
        for row in rows:
            record_dict = {}
            for col_name, col_value in zip(column_names, row):
                if isinstance(col_value, str):
                    try:
                        # Attempt to load JSON data
                        json_data = json.loads(col_value)
                        if isinstance(json_data, dict):
                            record_dict.update(json_data)  # Merge JSON data if it’s a dictionary
                        else:
                            record_dict[col_name] = json_data  # Add non-dict JSON data as-is
                    except json.JSONDecodeError:
                        record_dict[col_name] = col_value  # Add string as-is if not JSON
                elif isinstance(col_value, (date, datetime)) or 'date' in col_name:
                    # Convert date or datetime objects to ISO format string
                    record_dict[col_name] = col_value.isoformat()
                else:
                    record_dict[col_name] = col_value  # Add other data types as they are
            records.append(record_dict)

        # Convert records to a DataFrame
        df = pd.DataFrame(records)
        for col in df.columns:
            if "date" in col.lower():  # Check for 'date' or 'at' in column name
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df

    def get_data_as_gdf(self, query: str = None) -> gpd.GeoDataFrame:
        """
        Fetches data from the database, including geometry, and returns it as a GeoDataFrame.

        Parameters:
        ----------
        query : str, optional
            An SQL query string to fetch specific data from the database.
            If not provided, the function will fetch all records with non-null geometry.

        Returns:
        -------
        gpd.GeoDataFrame
            A GeoDataFrame containing the fetched records and their associated geometries.
        """
        if query is None:
            # Prepare the list of columns to fetch
            columns_to_select = ['key', 'data', 'geom']

            # Add additional columns from metadata to the selection list
            if "additional_cols" in self.metadata:
                columns_to_select.extend(self.metadata["additional_cols"])

            # Build the SQL query with the necessary columns
            columns_str = ', '.join(columns_to_select)
            query = f'SELECT {columns_str} FROM {self.table_name} WHERE geom IS NOT NULL'

        # Fetch the data as a DataFrame
        df = self.get_data_as_df(query=query)
        if not df.empty:
            df['geom'] = df['geom'].apply(lambda x: wkb.loads(x))
            # Add the geometry to the DataFrame and create a GeoDataFrame
            gdf = gpd.GeoDataFrame(df, geometry='geom', crs='EPSG:4326')  # Replace with appropriate CRS
            # gdf.drop('geom', axis=1, inplace=True)
            return gdf
        return gpd.GeoDataFrame()

    def add_column(self, column_name: str, data_type: str, default_value=None):
        """
        Add a new column to the table if it doesn't already exist.

        @param column_name: Name of the new column.
        @param data_type: Type of the new column like
             TEXT, INTEGER, BLOB
             DATE (YYYY-MM-DD), TIME (hh:mm:ss) and TIMESTAMP (YYYY-MM-DD hh:mm:ss)
        @param default_value: Default value for the new column.
        """
        try:
            # Check if the column already exists
            self.cursor.execute(f"PRAGMA table_info({self.table_name})")
            columns = [info[1] for info in self.cursor.fetchall()]
            if column_name in columns:
                print(f"Column '{column_name}' already exists. Skipping addition.")
                return

            # Construct the SQL statement for adding a new column with a default value
            sql = f'ALTER TABLE {self.table_name} ADD COLUMN {column_name} {data_type}'
            if default_value is not None:
                sql += f' DEFAULT {default_value}'

            # Execute the SQL statement to add the column
            self.cursor.execute(sql)

            # Check if 'additional_cols' exists in metadata, if not, initialize it
            if "additional_cols" not in self.metadata:
                self.metadata["additional_cols"] = []

            # Update metadata with the new column
            if column_name not in self.metadata["additional_cols"]:
                self.metadata["additional_cols"].append(column_name)
            self._save_metadata()

            # Commit the changes to the database
            self.conn.commit()
            print(f"Added column '{column_name}' to the records table with default value '{default_value}'.")

        except sqlite3.OperationalError as e:
            print(f"Error adding column '{column_name}': {e}")

    def update_column(self, key: str, column_name: str, value):
        try:
            # Update the specified column for the given key
            query = f'UPDATE {self.table_name} SET {column_name} = ? WHERE key = ?'
            self.cursor.execute(query, (value, key))
            if self.cursor.rowcount == 0:
                print(f"Record with key '{key}' does not exist.")
                return False
            self.conn.commit()
            print(f"Updated column '{column_name}' for key '{key}' with value '{value}'.")
            return True
        except sqlite3.OperationalError as e:
            print(f"Error updating column '{column_name}' for key '{key}': {e}")
            return False

    def close(self):
        self.conn.close()

    def get_gdf_list_under_aoi(self, aoi_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        # Fetch the data as a GeoDataFrame
        gdf = self.get_data_as_gdf()
        if not gdf.empty:
            # Ensure both GeoDataFrames have the same CRS
            if gdf.crs != aoi_gdf.crs:
                aoi_gdf = aoi_gdf.to_crs(gdf.crs)

            # Perform the overlay and include the 'key' column
            aoi_gdf = aoi_gdf[[aoi_gdf.geometry.name]]
            result_gdf = gpd.sjoin(gdf, aoi_gdf, how='inner', predicate='intersects')
            return result_gdf
        return gpd.GeoDataFrame()