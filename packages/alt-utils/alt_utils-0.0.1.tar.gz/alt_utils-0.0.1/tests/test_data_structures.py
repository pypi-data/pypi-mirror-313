import unittest
from dataclasses import dataclass

from src.alt_utils import NestedDeserializableDataclass


@dataclass
class DatabaseConfig(NestedDeserializableDataclass):
    db: str
    user: str
    password: str
    host: str
    port: int = 5432


@dataclass
class Config(NestedDeserializableDataclass):
    database: DatabaseConfig
    misc: str


class TestDataStructures(unittest.TestCase):
    def test_ndd(self):
        config_dict = {
            "database": {"db": "dbname", "user": "username", "host": "hostname", "password": "rosebud"},
            "misc": "something",
        }
        config_gen = Config.from_dict(config_dict)
        config_manual = Config(
            database=DatabaseConfig(db="dbname", user="username", host="hostname", password="rosebud", port=5432),
            misc="something",
        )
        self.assertEqual(config_gen, config_manual)
