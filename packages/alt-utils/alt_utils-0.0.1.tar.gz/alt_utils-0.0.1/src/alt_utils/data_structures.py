from dataclasses import dataclass, fields
from typing import Self


@dataclass
class NestedDeserializableDataclass:
    """
    A dataclass that can be generated from a dict. Fields that are NestedDeserializableDataclass
    themselves are properly initialized as well.
    """

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        d = d.copy()
        for field in fields(cls):
            if type(field.type) is not str and issubclass(field.type, NestedDeserializableDataclass):
                d[field.name] = field.type.from_dict(d[field.name])
        return cls(**d)
