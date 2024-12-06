from __future__ import annotations

import itertools
from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, ClassVar, cast, overload

import pydash
import yaml
from mm_mongo import MongoCollection
from mm_std import Err, Ok, Result, synchronized, utc_now

from mm_base1.errors import UnregisteredDConfigError
from mm_base1.models import DConfig, DConfigType
from mm_base1.utils import get_registered_attributes


class DC[T: (str, bool, int, float, Decimal)]:
    _counter = itertools.count()

    def __init__(self, value: T, description: str = "", hide: bool = False) -> None:
        self.value: T = value
        self.description = description
        self.hide = hide
        self.order = next(DC._counter)

    @overload
    def __get__(self, obj: None, obj_type: None) -> DC[T]: ...

    @overload
    def __get__(self, obj: object, obj_type: type) -> T: ...

    def __get__(self, obj: object, obj_type: type | None = None) -> T | DC[T]:
        if obj is None:
            return self
        return cast(T, getattr(DConfigService.dconfig_storage, self.key))

    def __set_name__(self, owner: object, name: str) -> None:
        self.key = name

    @staticmethod
    def get_attrs_from_settings(dconfig_settings: DConfigStorage) -> list[DC[T]]:
        attrs: list[DC[T]] = []
        keys = get_registered_attributes(dconfig_settings)
        for key in keys:
            field = getattr(dconfig_settings.__class__, key)
            if isinstance(field, DC):
                attrs.append(field)
        attrs.sort(key=lambda x: x.order)

        return attrs


class DConfigStorage(dict[str, object]):
    descriptions: ClassVar[dict[str, str]] = {}
    types: ClassVar[dict[str, DConfigType]] = {}
    hidden: ClassVar[set[str]] = set()

    def __getattr__(self, item: str) -> object:
        if item not in self:
            raise UnregisteredDConfigError(item)

        return self.get(item, None)

    def get_or_none(self, key: str) -> object | None:
        try:
            return self.get(key)
        except UnregisteredDConfigError:
            return None

    def get_non_hidden_keys(self) -> set[str]:
        return self.keys() - self.hidden

    def get_type(self, key: str) -> DConfigType:
        return self.types[key]


@dataclass
class DConfigInitValue:
    key: str
    order: int
    description: str
    value: str | int | float | bool


class DConfigService:
    dconfig_storage = DConfigStorage()
    dconfig_collection: MongoCollection[DConfig]
    dlog: Callable[[str, object], None]

    @classmethod
    @synchronized
    def init_storage(
        cls,
        dconfig_collection: MongoCollection[DConfig],
        dconfig_settings: DConfigStorage,
        dlog: Callable[[str, object], None],
    ) -> DConfigStorage:
        cls.dconfig_collection = dconfig_collection
        cls.dlog = dlog

        for attr in DC.get_attrs_from_settings(dconfig_settings):
            type_ = cls.get_type(attr.value)
            cls.dconfig_storage.descriptions[attr.key] = attr.description
            cls.dconfig_storage.types[attr.key] = type_
            if attr.hide:
                cls.dconfig_storage.hidden.add(attr.key)

            dv = cls.dconfig_collection.get_or_none(attr.key)
            if dv:
                typed_value_res = cls.get_typed_value(dv.type, dv.value)
                if isinstance(typed_value_res, Ok):
                    cls.dconfig_storage[attr.key] = typed_value_res.ok
                else:
                    cls.dlog("dconfig.get_typed_value", {"error": typed_value_res.err, "attr": attr.key})
            else:  # create rows if not exists
                cls.dconfig_collection.insert_one(
                    DConfig(_id=attr.key, type=type_, value=cls.get_str_value(type_, attr.value)),
                )
                cls.dconfig_storage[attr.key] = attr.value

        # remove rows which not in settings.DCONFIG
        cls.dconfig_collection.delete_many({"_id": {"$nin": get_registered_attributes(dconfig_settings)}})
        return cls.dconfig_storage

    @classmethod
    def update_multiline(cls, key: str, value: str) -> None:
        value = value.replace("\r", "")
        cls.dconfig_collection.update_by_id(key, {"$set": {"value": value, "updated_at": utc_now()}})
        cls.dconfig_storage[key] = value

    @classmethod
    def update(cls, data: dict[str, str]) -> bool:
        result = True
        for key, str_value in data.items():
            if key in cls.dconfig_storage:
                str_value = str_value or ""  # for BOOLEAN type (checkbox)
                str_value = str_value.replace("\r", "")  # for MULTILINE (textarea do it)
                type_value_res = cls.get_typed_value(cls.dconfig_storage.types[key], str_value.strip())
                if isinstance(type_value_res, Ok):
                    cls.dconfig_collection.update_by_id(key, {"$set": {"value": str_value, "updated_at": utc_now()}})
                    cls.dconfig_storage[key] = type_value_res.ok
                else:
                    cls.dlog("dconfig_service_update", {"error": type_value_res.err, "key": key})
                    result = False
            else:
                cls.dlog("dconfig_service_update", {"error": "unknown key", "key": key})
                result = False
        return result

    @classmethod
    def update_dconfig_yaml(cls, yaml_value: str) -> bool | None:
        data = yaml.full_load(yaml_value)
        if isinstance(data, dict):
            return cls.update(data)

    @classmethod
    def export_dconfig_yaml(cls) -> str:
        result = pydash.omit(cls.dconfig_storage, *cls.dconfig_storage.hidden)
        return yaml.dump(result, explicit_end=True, default_style="'", sort_keys=False)

    @staticmethod
    def get_type(value: object) -> DConfigType:
        if isinstance(value, bool):
            return DConfigType.BOOLEAN
        if isinstance(value, str):
            return DConfigType.MULTILINE if "\n" in value else DConfigType.STRING
        if isinstance(value, Decimal):
            return DConfigType.DECIMAL
        if isinstance(value, int):
            return DConfigType.INTEGER
        if isinstance(value, float):
            return DConfigType.FLOAT
        raise ValueError(f"unsupported type: {type(value)}")

    @staticmethod
    def get_typed_value(type_: DConfigType, str_value: str) -> Result[Any]:
        try:
            if type_ == DConfigType.BOOLEAN:
                return Ok(bool(str_value))
            if type_ == DConfigType.INTEGER:
                return Ok(int(str_value))
            if type_ == DConfigType.FLOAT:
                return Ok(float(str_value))
            if type_ == DConfigType.DECIMAL:
                return Ok(Decimal(str_value))
            if type_ == DConfigType.STRING:
                return Ok(str_value)
            if type_ == DConfigType.MULTILINE:
                return Ok(str_value.replace("\r", ""))
            return Err(f"unsupported type: {type_}")
        except Exception as e:
            return Err(str(e))

    @staticmethod
    def get_str_value(type_: DConfigType, value: Any) -> str:
        if type_ is DConfigType.BOOLEAN:
            return "True" if value else ""
        return str(value)
