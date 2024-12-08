from dataclasses import dataclass, fields, is_dataclass
from typing import Mapping, Self


@dataclass
class NestedDeserializableDataclass:
    """
    A dataclass that can be generated from a dict. Fields that are dataclasses
    themselves are properly initialized as well.
    """

    @classmethod
    def from_dict(cls, d: Mapping) -> Self:
        d = dict(d)
        for field in fields(cls):
            if type(field.type) is not str:
                if issubclass(field.type, NestedDeserializableDataclass):
                    d[field.name] = field.type.from_dict(d[field.name])
                elif is_dataclass(field.type):
                    d[field.name] = field.type(**d[field.name])
        return cls(**d)
