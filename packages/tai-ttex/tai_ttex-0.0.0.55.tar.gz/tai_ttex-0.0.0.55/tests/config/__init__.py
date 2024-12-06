from ttex.config import Config
from .. import dummy_log_handler
from typing import Union


class DummyConfig(Config):
    def __init__(self, a: int, b: Union[Config, str], c=None, d=3):
        self.a = a
        self.b = b
        self.c = c
        self.d = d


class EmptyConfig(Config):
    def __init__(self):
        pass


dict_config = {
    "DummyConfig": {
        "a": "a",
        "b": {
            "DummyConfig": {
                "a": "a2",
                "b": "b2",
            }
        },
        "c": "ConfigFactory",
        "d": "d",
    }
}
