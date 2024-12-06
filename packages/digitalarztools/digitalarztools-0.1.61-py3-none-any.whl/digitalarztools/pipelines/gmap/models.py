from geoalchemy2 import Geometry

from digitalarztools.adapters.db import DBModel
import sqlalchemy as db


class TblPlaces(DBModel):
    __tablename__ = 'tbl_places'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place_id = db.Column(db.Text, nullable=True)
    business_status = db.Column(db.String(123), nullable=True)
    icon = db.Column(db.Text, nullable=True)
    icon_background_color = db.Column(db.String(255), nullable=True)
    icon_mask_base_uri = db.Column(db.String(255), nullable=True)
    name = db.Column(db.Text, nullable=True)
    opening_hours = db.Column(db.JSON, nullable=True)
    photos = db.Column(db.JSON, nullable=True)
    plus_code = db.Column(db.JSON, nullable=True)
    price_level = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    reference = db.Column(db.String(255), nullable=True)
    scope = db.Column(db.String(255), nullable=True)
    types = db.Column(db.Text, nullable=True)
    user_ratings_total = db.Column(db.Integer, nullable=True)
    vicinity = db.Column(db.Text, nullable=True)
    geom = db.Column(Geometry(geometry_type="GEOMETRY", srid=4326), nullable=True)
    geometry = db.Column(db.JSON, nullable=True)
    permanently_closed = db.Column(db.String(25), nullable=True)


class TblBoundaries(DBModel):
    __tablename__ = 'tbl_boundaries'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500), nullable=True)
    geom = db.Column(Geometry(geometry_type="GEOMETRY", srid=4326), nullable=True)
    search_radius = db.Column(db.Float, nullable=False)
    # is_location_added = db.Column(db.Boolean, default=False)

class TblLocations(DBModel):
    __tablename__ = 'tbl_locations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    boundary_id = db.Column(db.ForeignKey(TblBoundaries.id), nullable=True)
    is_downloaded = db.Column(db.Boolean, default=False)
    geom = db.Column(Geometry("POINT"), nullable=True)
