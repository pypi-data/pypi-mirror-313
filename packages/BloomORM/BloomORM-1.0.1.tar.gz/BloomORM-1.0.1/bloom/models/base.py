import json
from typing import Any
from bloom.models.exceptons import AttrsNotInAnnotations, DataNotFound
from bloom.settings import DATABASES_DIR


class QuerySet:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f"QuerySet <[{self.__annotations__}]>"


class BaseModel:
    id: int

    @classmethod
    def _get_database_data(cls):
        DATABASE = f"{DATABASES_DIR}{cls.__name__}.json"
        try:
            with open(DATABASE, "r") as base:
                existing_data = json.load(base)
        except FileNotFoundError:
            existing_data = []
        return existing_data

    @classmethod
    def create(cls, **kwargs: Any):
        DATABASE = f"{DATABASES_DIR}{cls.__name__}.json"
        existing_data = cls._get_database_data()
        attrs_not_in_annotations = [key for key in kwargs if key not in cls.__annotations__]
        if attrs_not_in_annotations:
            raise AttrsNotInAnnotations(attrs_not_in_annotations)
        else:
            kwargs["id"] = existing_data[-1].get("id") + 1 if existing_data else 1
            existing_data.append(kwargs)
        with open(DATABASE, "w") as base:
            json.dump(existing_data, base, indent=4)

    @classmethod
    def get(cls, data_id: int):
        existing_data = cls._get_database_data()
        for elem in existing_data:
            if elem.get("id") == data_id:
                data = QuerySet(**elem)
                return data
        raise DataNotFound(cls.__name__, data_id)

    @classmethod
    def all(cls):
        return cls._get_database_data()

    @classmethod
    def update(cls, data_id: int, data_update: dict):
        existing_data = cls._get_database_data()
        for elem in existing_data:
            if elem.get("id") == data_id:
                elem.update(data_update)
                return f"message: {cls.__name__}_object({data_id}) update"
        raise DataNotFound(cls.__name__, data_id)

    @classmethod
    def delete(cls, data_id: int):
        existing_data = cls._get_database_data()
        for i in range(len(existing_data)):
            if existing_data[i].get("id") == data_id:
                existing_data.pop(i)
                return f"message: {cls.__name__}_object({data_id}) delete"
        raise DataNotFound(cls.__name__, data_id)

