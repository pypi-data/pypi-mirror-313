from __future__ import annotations

import dataclasses
from datetime import datetime, date, time
from enum import Enum
from types import NoneType
from typing import get_type_hints, get_origin, get_args, Union

import orjson
from dataclasses import dataclass
from holytools.abstract.serialization.serializable import Serializable

castable_classes = ['Decimal', 'UUID', 'Path', 'Enum', 'str', 'int', 'float', 'bool']
converters = {
    datetime: datetime.fromisoformat,
    date: date.fromisoformat,
    time: time.fromisoformat,
}
elementary_type_names : list[str] = castable_classes + [cls.__name__ for cls in converters.keys()]

# -------------------------------------------

@dataclass
class JsonDataclass(Serializable):
    """Can serialize dataclasses with following attributes:
    - Basic serializable types: holytools.abstract.Serializable, int, float, bool, str, int, Path, UUID, Decimal, datetime, date, time
    - Lists, tuples or dicts of basic serializable types"""
    def __init__(self, *args, **kwargs):
        _, __ = args, kwargs
        if not dataclasses.is_dataclass(self):
            raise TypeError(f'{self.__class__} must be a dataclass to be Jsonifyable')

    def to_str(self) -> str:
        defined_fields = set([f.name for f in dataclasses.fields(self) if f.init])
        json_dict = {attr: get_entry(obj=value) for attr, value in self.__dict__.items() if attr in defined_fields}
        return orjson.dumps(json_dict).decode("utf-8")

    @classmethod
    def from_str(cls, json_str: str):
        json_dict = orjson.loads(json_str)
        if not dataclasses.is_dataclass(cls):
            raise TypeError(f'{cls} is not a dataclass. from_json can only be used with dataclasses')
        type_hints = get_type_hints(cls)
        init_dict = {}
        for key, value in json_dict.items():
            dtype = type_hints.get(key)
            if TypeAnalzer.is_optional(dtype) and value is None:
                init_dict[key] = None
                continue
            if dtype is None:
                continue

            dtype = TypeAnalzer.strip_nonetype(dtype)
            origin = get_origin(dtype)
            if origin == list:
                item_type = TypeAnalzer.get_inner_types(dtype)[0]
                restored_value = [make(cls=item_type, s=x) for x in value]
            elif origin == tuple:
                item_types = TypeAnalzer.get_inner_types(dtype)
                restored_value = tuple([make(cls=item_type, s=s) for item_type, s in zip(item_types, value)])
            elif origin == dict:
                key_type, value_type = TypeAnalzer.get_inner_types(dtype)
                key_list = [make(cls=key_type, s=x) for x in value[0]]
                value_list = [make(cls=value_type, s=x) for x in value[1]]
                restored_value = {key: value for key, value in zip(key_list, value_list)}
            else:
                restored_value = make(cls=dtype, s=value)
            init_dict[key] = restored_value

        return cls(**init_dict)


def get_entry(obj):
    if isinstance(obj, Serializable):
        entry = obj.to_str()
    elif isinstance(obj, Enum):
        entry = obj.value
    elif isinstance(obj, dict):
        key_list = [get_entry(k) for k in obj.keys()]
        value_list = [get_entry(v) for v in obj.values()]
        entry = (key_list, value_list)
    elif isinstance(obj, list):
        entry = [get_entry(x) for x in obj]
    elif isinstance(obj, tuple):
        entry = tuple([get_entry(x) for x in obj])
    elif isinstance(obj, float) and obj != obj:
        entry = 'nan'
    else:
        entry = obj
    return entry


def make(cls, s : str):
    if cls in converters:
        instance = converters[cls](s)
    elif cls.__name__ in castable_classes:
        instance = cls(s)
    elif issubclass(cls, Enum):
        instance =  cls(s)
    elif get_origin(cls) == dict:
        instance = orjson.loads(s)
    elif issubclass(cls, Serializable):
        instance = cls.from_str(s)
    else:
        raise TypeError(f'Unsupported type {cls}')
    return instance
        


class TypeAnalzer:
    @staticmethod
    def is_optional(dtype):
        origin = get_origin(dtype)
        if origin is Union:
            return NoneType in get_args(dtype)
        else:
            return False

    # noinspection DuplicatedCode
    @staticmethod
    def strip_nonetype(dtype : type) -> type:
        origin = get_origin(dtype)
        if origin is Union:
            types = get_args(dtype)
            not_none_types = [t for t in types if not t is NoneType]
            if len(not_none_types) == 1:
                core_type = not_none_types[0]
            else:
                raise ValueError(f'Union dtype {dtype} has more than one core dtype')
        else:
            core_type = dtype
        return core_type
    
    @staticmethod
    def get_inner_types(dtype : type) -> tuple:
        inner_dtypes = get_args(dtype)
        return inner_dtypes


if __name__ == "__main__":
    a = make(cls=float, s='4')
    print(a)