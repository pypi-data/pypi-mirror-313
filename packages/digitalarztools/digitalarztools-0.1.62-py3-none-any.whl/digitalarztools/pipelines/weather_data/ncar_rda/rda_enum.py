# Define ENUM types using SQLAlchemy
from enum import Enum
# from sqlalchemy.types import Enum


# Python enum definitions
class RDAFormat(Enum):
    grib = "grib"
    netcdf = "netcdf"
    csv = "csv"
    NONE = None  # If you want to support a 'None' option, consider handling it differently in the database.


class RDAStatus(Enum):
    Deleted = "Deleted"
    Queued = "Queued"
    Purged = "Purged"
    Error = "Error"
    Completed = "Completed"
