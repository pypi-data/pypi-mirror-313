import os

from dotenv import load_dotenv
import inspect
from typing import Union, Any

from sqlalchemy import *
from sqlalchemy.orm import *

from digitalarztools.adapters.manager import DBManager, DBParams, DBString

load_dotenv()
metadata_obj = MetaData()


# Base = declarative_base(metadata=metadata_obj)


class DBModel(DeclarativeBase):
    metadata = metadata_obj

    class _Meta:
        db_credentials: DBParams = None

    @classmethod
    def get_session(cls) -> Session:
        return cls.manager().managed_session()

    @classmethod
    def query(
            cls, *entities: [Any], **kwargs: Any
    ) -> Query[Any]:
        """
        Return a new :class:`_query.Query` object corresponding to this
        :class:`_orm.Session`.
        Exampla:
            LayerCategory.query().filter_by(id=3).first()
            LayerCategory.query(LayerCategory.main,LayerCategory.id).filter_by(id=3).first()
            LayerCategory.query().values(LayerCategory.main,LayerCategory.id)
        """
        if len(entities) == 0:
            return cls.manager().managed_session().query(cls)
        else:
            return cls.manager().managed_session().query(*entities)

    @classmethod
    def manager(cls) -> DBManager:
        if cls._Meta.db_credentials is None:
            db_credential = cls.get_db_params()
        else:
            db_credential = cls._Meta.db_credentials
        return DBManager(db_credential)

    @classmethod
    def get_engine(cls) -> Engine:
        return cls.manager().get_engine()

    @classmethod
    def get_db_params(cls):
        engine = os.getenv("engine")
        if engine in ["sqlite"]:
            con_params = os.getenv("file_path")
        else:
            params = {
                "name": os.getenv("name"),
                "host": os.getenv("host"),
                "port": os.getenv("port"),
                "user": os.getenv("user"),
                "password": os.getenv("password")

            }
            con_params = DBString(**params)
        db_credentials: DBParams = DBParams(**{
            "engine": os.getenv("engine"),
            "con_str": con_params
        })

        return db_credentials

    # @classmethod
    # def get_db_key(cls, app_label=None):
    #     if app_label is None:
    #         if hasattr(cls._Meta, "app_label"):
    #             app_label = getattr(cls._Meta, "app_label")
    #         else:
    #             app_label = cls.__module__.split(".")[-2]
    #     return DA_APPS[app_label]["db_key"]

    @classmethod
    def get_fields(cls, skip_fields=None):
        if skip_fields is None:
            skip_fields = []
        attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        col_names = [a[0] for a in attributes if hasattr(a[1], "type") and a[0] not in skip_fields]
        # manager = cls.manager()
        # col_name =  manager.get_table_column_names()
        return col_names

    def save(self):
        manager = self.manager()
        id = None
        with manager.managed_session() as session:
            local_object = session.merge(self)
            session.add(local_object)
            session.commit()
            session.flush()

            id = local_object.id
            session.close()
        return id

    def delete(self, app_label=None):
        manager = self.manager()
        with manager.managed_session() as session:
            local_object = session.merge(self)
            session.delete(local_object)
            session.commit()
            session.flush()
