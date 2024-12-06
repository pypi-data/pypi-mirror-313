from ttex.config import Config, ConfigFactory
from . import DummyConfig, dict_config
import pytest
from logging import Handler
import os
import json


def test_get_val():
    config = Config()
    config.test = 5

    assert config.get("test") == 5
    assert config.get("test2") is None

    # default values
    assert config.get("test", 3) == 5
    assert config.get("test2", 3) == 3


def test_extract_empty():
    config = Config()
    test_config = ConfigFactory.extract(DummyConfig, config)
    assert test_config.a is None
    assert test_config.b is None
    assert test_config.c is None
    assert test_config.d == 3


def test_extract():
    config = Config()
    config.a = "arg"
    config.b = 5
    config.c = "kwarg"
    config.d = 17

    test_config = ConfigFactory.extract(DummyConfig, config)

    for arg in ["a", "b", "c", "d"]:
        assert getattr(test_config, arg) == getattr(config, arg)


def test_exctract_class():
    ex_class = ConfigFactory._extract_attr("ttex.log.handler.WandbHandler")
    assert issubclass(ex_class, Handler)

    with pytest.raises(ValueError) as e:
        # Splitting error
        ConfigFactory._extract_attr("DummyConfig")

    # Test error catching
    with pytest.raises(ValueError) as e:
        # Module import error
        ConfigFactory._extract_attr("WandbHandler")
    assert "Did not recognise" in str(e.value)
    assert "KeyError" in str(e.value)

    with pytest.raises(ValueError) as e:
        # Module import error
        ConfigFactory._extract_attr("tex.WandbHandler")
    assert "Did not recognise" in str(e.value)
    assert "No module named" in str(e.value)

    with pytest.raises(ValueError) as e:
        # class not found
        ConfigFactory._extract_attr("ttex.WandbHandler")
    assert "Did not recognise" in str(e.value)
    assert "has no attribute" in str(e.value)


@pytest.mark.parametrize("mode", ["extract", "dict", "json"])
def test_from_dict(mode):
    if mode == "extract":
        config = ConfigFactory.extract(
            DummyConfig, dict_config["DummyConfig"], context=globals()
        )
    elif mode == "dict":
        config = ConfigFactory.from_dict(dict_config, context=globals())
    else:
        path = "sample_dict.json"
        with open(path, "w") as outfile:
            json.dump(dict_config, outfile)
        config = ConfigFactory.from_file(path, context=globals())

    assert isinstance(config, DummyConfig)
    assert config.a == "a"
    assert isinstance(config.b, DummyConfig)
    assert config.b.a == "a2"
    assert config.c == ConfigFactory

    if mode == "json":
        os.remove(path)


def test_config_dict_format():
    # more than 1 key in config
    with pytest.raises(AssertionError):
        ConfigFactory.from_dict(dict_config["DummyConfig"])
    # Missing definition (not passed in globals)
    with pytest.raises(ValueError):
        ConfigFactory.from_dict(dict_config)
