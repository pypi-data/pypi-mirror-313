import importlib
import json
import os
import traceback
from urllib.request import urlopen

import fiona
import geopandas as gp
from geoalchemy2.shape import from_shape
from shapely import wkt

from digitalarztools.io.vector.gpd_vector import GPDVector

fiona.drvsupport.supported_drivers['kml'] = 'rw' # enable KML support which is disabled by default
fiona.drvsupport.supported_drivers['KML'] = 'rw' # enable KML support which is disabled by default
from pathlib import Path

import shapely

from shapely.geometry import shape

from digitalarztools.adapters.db import metadata_obj, DBModel
from digitalarztools.adapters.manager import DBManager
from digitalarztools.pipelines.gmap.models import TblBoundaries, TblLocations, TblPlaces


class GMapPipeline:
    def __init__(self):
        self.search_radius = -1
        self.api_key = os.getenv("g_map_key")
        manager = DBModel.manager()
        self.create_tables(manager)

    @staticmethod
    def create_tables(db_manager: DBManager):
        this_package = __package__
        module = importlib.import_module(f'{this_package}.models')
        tables = [getattr(getattr(module, attr), "__tablename__") for attr, value in vars(module).items() if
                  hasattr(getattr(module, attr), "__tablename__")]
        tables = [table for key, table in metadata_obj.tables.items() if key in tables]

        metadata_obj.create_all(db_manager.get_engine(), tables=tables)
        # print("tables added successfully")

    def fetch_url(self, lat, lon):
        if self.search_radius == -1:
            raise Exception("search radius is not provided")

        location = str(lat) + "," + str(lon)
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + location + "&radius=" + \
              str(self.search_radius) + "&&sensor=false&key=" + self.api_key
        response = urlopen(url)
        data = json.loads(response.read())
        return data

    def fetch_tokentag_url(self, token):
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=" + token + "&sensor=false&key=" + self.api_key
        response = urlopen(url)
        data = json.loads(response.read())
        return data

    def fetch_places_data(self, lat, lon):
        places_data = self.fetch_url(lat, lon)
        self.save_places_data(places_data)
        while True:
            if places_data.get('next_page_token') is not None:
                token = places_data["next_page_token"]
                places_data = self.fetch_tokentag_url(token)
                self.save_places_data(places_data)
            else:
                break
    @staticmethod
    def save_places_data(data):
        print(data)
        if len(data["results"]) > 0:
            for row in data["results"]:
                try:
                    place_id = row["place_id"]
                    geom_obj = row["geometry"]["location"]
                    geom_wkt = "POINT(" + str(geom_obj["lng"]) + " " + str(geom_obj["lat"]) + ")"
                    # geos_geom = GEOSGeometry(geom_wkt)
                    # geos_geom.srid = 4326
                    geom = shapely.wkt.loads(geom_wkt)
                    geom = from_shape(geom, srid=4326)
                    row["geom"] = geom
                    row["place_id"] = place_id
                    print(row)
                    # TblPlaces.objects.update_or_create(place_id=place_id, defaults=row)
                    tbl_place = TblPlaces(**row)
                    tbl_place.save()
                except Exception as e:
                    traceback.print_exc()

    @staticmethod
    def insert_boundary( geom, name, search_radius) -> int or None:
        geom = from_shape(geom, srid=4326)
        boundary = TblBoundaries().query().filter_by(name=name).first()
        if boundary is None:
            boundary = TblBoundaries()
            boundary.name = name
            boundary.geom = geom
            boundary.search_radius = search_radius
            id = boundary.save()
        else:
            id = boundary.id
        return id


    @staticmethod
    def insert_location(lat, lng, geom, boundary_id):
        try:
            geom = from_shape(geom, srid=4326)
            loc = TblLocations.query().filter(TblLocations.geom.same(geom)).first()
            if loc is None:
                loc = TblLocations(geom=geom, lat=lat,lng=lng, boundary_id=boundary_id)
                id = loc.save()
            else:
                id = loc.id
            return id


        except Exception as e:
            return None
    def download_poi(self, gdv: GPDVector, search_radius, boundary_name):
        self.search_radius = search_radius

        if "4326" not in str(gdv.get_crs()):
            gdv.to_crs(epsg=4326)

        minx, miny, maxx, maxy = gdv.extent
        x_increment = self.search_radius * 0.000012
        y_increment = self.search_radius * 0.000012

        polygon = gdv.get_unary_union()
        polygon = shapely.wkb.loads(
            shapely.wkb.dumps(polygon, output_dimension=2))
        boundary_id = self.insert_boundary(polygon, boundary_name, self.search_radius)
        loc_ids = []
        while True:
            if maxy > miny:
                start_x = minx
                while True:
                    if maxx > start_x:
                        point_wkt = "Point(" + str(start_x) + " " + str(miny) + ")"
                        shp_geom = shapely.wkt.loads(point_wkt)
                        if polygon.contains(shp_geom):
                            id = self.insert_location(miny, start_x, shp_geom, boundary_id)
                            loc_ids.append(id)
                        start_x += x_increment
                    else:
                        break
                miny += y_increment
            else:
                break
        # gdf = gp.GeoDataFrame(locations, geometry="geom")
        # gdf["geometry"] = gdf["geom"].apply(wkt.load)
        # gdf.crs = 4326
        print("Location Inserted...")
        print("Total Locations", len(loc_ids))

        # gdf.to_postgis(TblLocations.__tablename__, con=DBModel.get_engine(), if_exists='append')

        locations: list[TblLocations] = list(TblLocations.query().filter_by(is_downloaded=False, boundary_id=boundary_id).all())
        print("location need to download", len(locations))
        download_ids = []
        for row in locations:
            if row.id in loc_ids:
                lat = row.lat
                lng = row.lng
                self.fetch_places_data(lat, lng)
                id = row.id
                download_ids.append(id)
                # TblLocations.objects.update_or_create(id=id, defaults={'is_downloaded': True})
                row.is_downloaded = True
                row.save()
        print("downloaded location",len(download_ids))
