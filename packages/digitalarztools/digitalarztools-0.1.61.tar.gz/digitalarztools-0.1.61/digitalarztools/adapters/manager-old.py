import json
import os.path
import traceback
import geopandas as gpd
from sqlite3 import Error
from urllib import parse
from typing import Union

from dotenv import load_dotenv
from pydantic import BaseModel
from shapely import wkt, wkb
from sqlalchemy import Engine, create_engine, select, func, Connection, Table, MetaData, Column, Integer, String, \
    inspect, text
from sqlalchemy.orm import Session

load_dotenv()


class DBString(BaseModel):
    host: str
    user: str
    password: str
    name: str
    port: str


class DBParams:
    engine: str  # postgresql,sqlite
    con_str: Union[str, DBString]  # either provide file_path or DBString

    def __init__(self, engine: str, con_str: Union[dict, DBString]):
        self.engine = engine
        self.con_str = DBString(**con_str) if isinstance(con_str, dict) else con_str


class DBManager:
    engine: Engine

    def __init__(self, db_info: Union[DBParams, Engine]):
        if isinstance(db_info, Engine):
            self.engine: Engine = db_info
        else:
            self.engine: Engine = self.create_sql_alchemy_engine(db_info)
        if self.engine is None:
            raise Exception("Enable to create sql alchemy engine")

    def get_engine(self):
        return self.engine

    def get_session(self):
        return Session(self.engine)

    @classmethod
    def for_sqlite3(cls, db_fp: str) -> 'DBManager':
        """ create a database connection to a SQLite database """
        engine: Engine = cls.create_sql_alchemy_engine(DBParams(**{"engine": "sqlite", "con_params": db_fp}))
        if not os.path.exists(db_fp):
            conn: Connection = None
            try:
                # listen(engine, 'connect', load_spatialite)
                conn = engine.connect()
                conn.execute(".load mod_spatialite.dylib")
                conn.execute(select([func.InitSpatialMetaData()]))
            #     conn = sqlite3.connect(db_fp)
            #     print(sqlite3.version)
            #     engine = create_engine(f"sqlite:////{db_fp}")
            #     return cls(engine)
            except Error as e:
                print(e)
            finally:
                if conn:
                    conn.close()
        return cls(engine)

    def get_query_data(self, query):
        with Session(self.engine) as session:
            rs = session.execute(text(query))
            return rs.fetchall()

    @staticmethod
    def create_sql_alchemy_engine(config: DBParams) -> Engine:
        try:
            if config.engine in ["sqlite"]:
                db_string = f'{config.engine}:///{config.con_str}'
            else:
                params = config.con_str
                db_string = f'{config.engine}://{params.user}:{parse.quote(params.password)}@{params.host}:{params.port}/{params.name}'
            return create_engine(db_string, echo=True)
        except Exception as e:
            # da_logger.error()
            traceback.print_exc()

    @classmethod
    def create_postgres_engine(cls, db_str: Union[DBString, dict]):
        if isinstance(db_str, dict):
            db_str = DBString(**db_str)
        params = DBParams(engine='postgresql+psycopg2', con_str=db_str)
        return cls.create_sql_alchemy_engine(params)


class GeoDBManager(DBManager):

    @staticmethod
    def get_geometry_cols(table: Table) -> list:
        geom_cols = [col for col in list(table.columns) if 'geometry' in str(col.type)]
        return geom_cols

    async def get_tile_envelop(self, x, y, z) -> gpd.GeoDataFrame:
        query = f"SELECT ST_AsText( ST_TileEnvelope({z}, {x}, {y}));"
        res = await self.execute_query_as_one(query)
        polygon = wkt.loads(res)
        # gdf = gpd.GeoDataFrame({"geometry": [polygon]}, geometry='geometry', crs='EPSG:3857')
        return polygon

    def get_geom_col_srid(self, tbl, geom_col):
        res = self.get_session().query(tbl.c[geom_col].st_srid()).first()
        return res[0] if len(res) > 0 else 0

    @staticmethod
    def data_to_gdf(data, geom_col, srid=0, is_postgis_geom=True):
        gdf = gpd.GeoDataFrame(data)
        gdf = gdf.dropna(axis=0)
        if is_postgis_geom:
            gdf["geom"] = gdf[geom_col].apply(lambda x: wkb.loads(x, hex=True))
        else:
            gdf["geom"] = gdf[geom_col].apply(lambda x: wkt.loads(str(x)))
        if geom_col != "geom":
            gdf = gdf.drop(geom_col, axis=1)
        gdf = gdf.set_geometry("geom")
        if srid != 0:
            gdf.crs = srid
        return gdf

    def table_to_gdf(self, tbl: Union[Table, str], geom_col="geom", limit=-1):
        if isinstance(tbl, str):
            tbl = self.get_sqlalchemy_table(tbl)
        # geom_cols = self.get_geometry_cols(tbl)
        data = self.get_all_data(tbl, limit)
        # geom_col = geom_cols[0]
        srid = self.get_geom_col_srid(tbl, geom_col)
        return self.data_to_gdf(data, geom_col, srid)

    def execute_query_as_gdf(self, query, srid, geom_col='geom', is_postgis_geom=True):
        data = self.get_query_data(query)
        if data and len(data) > 0:
            return self.data_to_gdf(data, geom_col, srid, is_postgis_geom)
        return gpd.GeoDataFrame()

    def execute_as_geojson(self, query, geom_field='geom') -> dict:
        if self.engine.engine.name == "postgres":
            statement = f"SELECT jsonb_build_object(" \
                        f"'type',     'FeatureCollection', " \
                        f"'features', jsonb_agg(feature)) " \
                        f"FROM ( " \
                        f"SELECT jsonb_build_object( " \
                        f"'type', 'Feature', " \
                        f"'geometry',   ST_AsGeoJSON({geom_field})::jsonb," \
                        f"'properties', to_jsonb(row) - 'geom' -'geometry' - '{geom_field}'" \
                        f") AS feature " \
                        f"FROM ({query}) row) features"
            with self.engine.connect() as con:
                rs = con.exec_driver_sql(statement)
                if rs.returns_rows:
                    res = rs.first()
                    return res[0]
        else:
            gdf = self.execute_query_as_gdf(query)
            return json.loads(gdf.to_json())

    def execute_as_mvt(self, table_name, z, x, y, g_col="geom", pk_cols=",oid", cols=",river_name"):
        """
        :param table_name:
        :param z:
        :param x:
        :param y:
        :param g_col:
        :param pk_cols:
        :param cols:
        :return:
        example
        WITH mvtgeom AS
            (
              SELECT ST_AsMVTGeom(geom, ST_TileEnvelope(12, 513, 412), extent => 4096, buffer => 64) AS geom, name, description
              FROM points_of_interest
              WHERE geom && ST_TileEnvelope(12, 513, 412, margin => (64.0 / 4096))
            )
            SELECT ST_AsMVT(mvtgeom.*)
            FROM mvtgeom;
        """
        query = f"WITH mvtgeom AS(" \
                f"SELECT ST_AsMVTGeom({g_col}, ST_TileEnvelope({z}, {x}, {y}), " \
                f"extent => 4096, buffer => 64) as geom {pk_cols} {cols} " \
                f"from {table_name} " \
                f" WHERE geom && ST_TileEnvelope({z}, {x}, {y}, margin => (64.0 / 4096))" \
                f") SELECT ST_AsMVT(mvtgeom.*) FROM mvtgeom"
        print(query)
        mvt = self.execute_query_as_one(query)
        mvt_bytes = bytes(mvt)
        return mvt_bytes

    def create_xyz_cache_table(self, table_name: str):
        meta_data = MetaData()
        xyz_table = Table(table_name, meta_data,
                          Column('id', Integer, primary_key=True, autoincrement=True),
                          Column('x', Integer),
                          Column('y', Integer),
                          Column('z', Integer),
                          Column('mvt', String))
        meta_data.create_all(self.engine)
        return xyz_table

    def get_spatial_table_names(self) -> list:
        inspector = inspect(self.engine)
        schema = 'public'
        table_names = []
        for table_name in inspector.get_table_names(schema=schema):
            table = self.get_sqlalchemy_table(table_name)
            geom_cols = self.get_geometry_cols(table)
            if len(geom_cols) > 0:
                table_names.append(table_name)
        return table_names
