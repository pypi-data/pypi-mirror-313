from typing import Union

from fastapi import Query
from geoalchemy2 import RasterElement
from rasterio import MemoryFile, DatasetReader, CRS
from sqlalchemy import ResultProxy, Select, func
from sqlalchemy.orm import Session

from digitalarztools.io.raster.rio_raster import RioRaster


class PostGISRaster(RioRaster):
    def __init__(self, src: Union[str, DatasetReader]):
        super().__init__(src)

    @staticmethod
    def from_postgis(qs: Union[str, Query, Select, ResultProxy], col_name: str, session: Session = None):
        """
        Retrieve raster data from a PostGIS column and return a PostGISRaster object.

        @param qs: Can be one of the following:
            - str: Raw SQL query string (e.g., "SELECT * FROM drm_temp_raster LIMIT 1").
            - Query: SQLAlchemy ORM Query object (e.g., session.query(DrmTempRaster).filter(DrmTempRaster.date == today)).
            - Select: SQLAlchemy Core Select object (e.g., select([drm_temp_raster_table]).where(drm_temp_raster_table.c.date == today)).
            - ResultProxy: ResultProxy object from a previous execution (e.g., result of session.execute(text(sql_query))).
        @param col_name: The name of the column containing the raster data.
        @param session: SQLAlchemy Session object (optional if qs is already a ResultProxy).
        @return: PostGISRaster object.
        """
        if isinstance(qs, str):
            result = session.execute(qs).first()
        elif isinstance(qs, ResultProxy):
            result = qs.first()
        elif isinstance(qs, Select):
            result = session.execute(qs).first()
        elif isinstance(qs, Query):
            result = qs.first()
        else:
            raise TypeError("Unsupported query type")

        if not result:
            raise ValueError("Query returned no results")

        # Use the column name dynamically
        raster_entry = result
        raster_data = getattr(raster_entry, col_name)

        # Process the raster data with rasterio
        with MemoryFile(raster_data) as memfile:
            with memfile.open() as dataset:
                return PostGISRaster(dataset)

    @staticmethod
    def from_postgis_raster(raster_element: object, session:Session):
        """
        SELECT ST_AsGDALRaster(rast, 'GTiff') FROM your_table WHERE ...
        or
        obj = session.query(func.ST_AsGDALRaster(DRMTempRaster.raster, 'GTiff').label('raster')).filter(
            DRMTempRaster.dataset == dataset_name,
            # func.date(DRMTempRaster.date) == datetime.today(),
            func.ST_Intersects(DRMTempRaster.envelope, func.ST_GeomFromText(envelope_wkt, 4326))
        ).first()
        # Read the raster data
        raster = PostGISRaster.from_postgis_raster(obj.raster)
        @param raster_data:
        @return:
        """
        # # Assuming raster_element.data is a WKB string starting with '0100'
        # wkb_string = raster_element.data
        # # Convert the WKB string to bytes
        # wkb_bytes = bytes(wkb_string, 'utf-8')

        with MemoryFile(raster_element) as memfile:
            with memfile.open() as dataset:
                raster = RioRaster(dataset)
                print(raster.get_raster_extent())


    @staticmethod
    def to_postgis(raster: Union[RioRaster,str]):
        """
        Convert a RioRaster object into a list of bytes for each band.

        Usage:
            metadata, raster_band = PostGISRaster.to_postgis(rio_raster)

            # Use a parameterized query to insert the data
            query = text('
                INSERT INTO drm_temp_raster (metadata, raster)
                VALUES (:metadata, :raster)
            ')

            session.execute(query, {'metadata': meta_data, 'raster': raster_band})
            session.commit()

        Or:
            metadata, rater_data = PostGISRaster.to_postgis(rio_raster)

            # Create an instance of the model and assign the raster data
            raster_obj = DRMTempRaster(
                dataset=dataset_name,
                raster=rater_data,  # Directly use bands as the raster data
                raster_meta_data=meta_data,
                envelope=from_shape(polygon, srid=4326)
            )

            # Add the object to the session and commit
            session.add(raster_obj)
            session.commit()

        @param raster: RioRaster object containing the dataset to be stored.
        @return: Tuple containing metadata and a list of bytes for each band.
        """

        if isinstance(raster, str):
            raster = RioRaster(raster)
        dataset: DatasetReader = raster.dataset


        meta_data = dataset.profile
        meta_data['crs'] = str(meta_data['crs'])
        raster_data = dataset.read()
        raster_data= func.st_rastfromwkb(raster_data.tobytes())
        return meta_data, raster_data
