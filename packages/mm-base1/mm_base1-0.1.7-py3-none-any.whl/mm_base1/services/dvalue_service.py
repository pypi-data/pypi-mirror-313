from __future__ import annotations

import base64
import itertools
import pickle  # nosec
from typing import ClassVar, cast, overload

import yaml
from mm_mongo import MongoCollection
from mm_std import synchronized, utc_now

from mm_base1.errors import UnregisteredDValueError
from mm_base1.models import DValue
from mm_base1.utils import get_registered_attributes


class DV[T]:
    _counter = itertools.count()

    def __init__(self, value: T, description: str = "", persistent: bool = True) -> None:
        self.value = value
        self.description = description
        self.persistent = persistent
        self.order = next(DV._counter)

    @overload
    def __get__(self, obj: None, obj_type: None) -> DV[T]: ...

    @overload
    def __get__(self, obj: object, obj_type: type) -> T: ...

    def __get__(self, obj: object | None, obj_type: type | None = None) -> T | DV[T]:
        if obj is None:
            return self
        return cast(T, getattr(DValueService.dvalue_storage, self.key))

    def __set__(self, instance: object, value: T) -> None:
        setattr(DValueService.dvalue_storage, self.key, value)

    def __set_name__(self, owner: object, name: str) -> None:
        self.key = name

    @staticmethod
    def get_attrs_from_settings(dvalue_settings: DValueStorage) -> list[DV[T]]:
        attrs: list[DV[T]] = []
        for key in get_registered_attributes(dvalue_settings):
            field = getattr(dvalue_settings.__class__, key)
            if isinstance(field, DV):
                attrs.append(field)
        attrs.sort(key=lambda x: x.order)
        return attrs


class DValueStorage(dict[str, object]):
    persistent: ClassVar[dict[str, bool]] = {}
    descriptions: ClassVar[dict[str, str]] = {}

    def __getattr__(self, item: str) -> object:
        if item not in self:
            raise UnregisteredDValueError(item)
        return self.get(item)

    def __setattr__(self, key: str, value: object) -> None:
        if key not in self:
            raise UnregisteredDValueError(key)
        if DValueStorage.persistent[key]:
            DValueService.update_persistent_value(key, value)
        self[key] = value

    def init_value(self, key: str, value: object, description: str, persistent: bool) -> None:
        DValueStorage.persistent[key] = persistent
        DValueStorage.descriptions[key] = description
        self[key] = value
        if persistent:
            DValueService.init_persistent_value(key, value)


class DValueService:
    dvalue_storage = DValueStorage()
    dvalue_collection: MongoCollection[DValue]

    @classmethod
    @synchronized
    def init_storage(cls, dvalue_collection: MongoCollection[DValue], dvalue_settings: DValueStorage) -> DValueStorage:
        cls.dvalue_collection = dvalue_collection
        persistent_keys = []
        # attrs: list[DV[T]] = DV.get_attrs_from_settings(dvalue_settings)

        for attr in DV.get_attrs_from_settings(dvalue_settings):  # type: ignore[var-annotated]
            value = attr.value
            # get value from db if exists
            if attr.persistent:
                persistent_keys.append(attr.key)
                dvalue_from_db = cls.dvalue_collection.get_or_none(attr.key)
                if dvalue_from_db:
                    value = cls.decode_value(dvalue_from_db.value)
            cls.dvalue_storage.init_value(attr.key, value, attr.description, attr.persistent)

        # remove rows which not in persistent_keys
        cls.dvalue_collection.delete_many({"_id": {"$nin": persistent_keys}})
        return cls.dvalue_storage

    @classmethod
    def get_dvalues_yaml(cls) -> str:
        return yaml.dump(cls.dvalue_storage.copy(), explicit_end=True, default_style="'")

    @classmethod
    def get_dvalue_yaml_value(cls, key: str) -> str:
        return yaml.dump(getattr(cls.dvalue_storage, key), explicit_end=True, default_style="'")

    @classmethod
    def set_dvalue_yaml_value(cls, key: str, yaml_value: str, multiline_string: bool) -> None:
        value = yaml_value.replace("\r", "") if multiline_string else yaml.full_load(yaml_value)
        setattr(cls.dvalue_storage, key, value)

    @classmethod
    def set_dvalue_yaml_values(cls, yaml_values: str) -> None:
        for key, value in yaml.full_load(yaml_values).items():
            setattr(cls.dvalue_storage, key, value)

    @classmethod
    def init_persistent_value(cls, key: str, value: object) -> None:
        if not cls.dvalue_collection.exists({"_id": key}):
            cls.dvalue_collection.insert_one(DValue(_id=key, value=cls.encode_value(value)))
        else:
            cls.update_persistent_value(key, value)

    @classmethod
    def update_persistent_value(cls, key: str, value: object) -> None:
        cls.dvalue_collection.update_by_id(key, {"$set": {"value": cls.encode_value(value), "updated_at": utc_now()}})

    @staticmethod
    def encode_value(value: object) -> str:
        return base64.b64encode(pickle.dumps(value)).decode("utf-8")

    @staticmethod
    def decode_value(value: str) -> object:
        return pickle.loads(base64.b64decode(value))  # nosec
