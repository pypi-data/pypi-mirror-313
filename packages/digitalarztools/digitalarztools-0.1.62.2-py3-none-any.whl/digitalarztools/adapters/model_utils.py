import importlib

from sqlalchemy import Table, insert

from dafastmap.utils.adapters.db import DBBase
from dafastmap.utils.adapters.manager import GeoDBManager
from settings import DA_APPS


class ModelUtils:
    @staticmethod
    def get_model(model_name):
        for key in DA_APPS:
            if key != "auth":
                module = importlib.import_module(f'{DA_APPS[key]["path"]}.models')
                for a in dir(module):
                    if a.lower() == model_name.lower():
                        cls = getattr(module, a)
                        if cls is not None:
                            return cls

    @classmethod
    def add_model_obj(cls,model_name, row):
        model = cls.get_model(model_name)
        manager: GeoDBManager = model.manager()

        if model is not None:
            stmt = insert(model).values(**row)
            res = manager.execute_ddl(stmt)
            return res

