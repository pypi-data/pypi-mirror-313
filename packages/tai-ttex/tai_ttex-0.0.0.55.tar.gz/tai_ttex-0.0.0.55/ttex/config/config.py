"""Config class and ConfigFactory to create one from different sources"""

from abc import ABC
from typing import TypeVar, Type, Union, Dict, Optional
from inspect import signature, Parameter
import importlib
import json


# TODO config with separate levels for keys
class Config(ABC):  # pylint: disable=too-few-public-methods
    """Config to go with a configurable object

    Contains the necessary values required to initialise a configurable object
     as defined by that object's specific config
    """

    def __init__(self, *args, **kwargs):
        """Init a configuration
        Should be overriden by each Config object to specify
        exactly which values are required
        """
        # TODO could add something that auto-adds all the values to the dict
        # TODO consider if this should be a dictionary or a namedtuple or sth

    def get(self, key: str, default=None):
        """Get a specific value from the config dict.
        This might need to be modified for nesting
        Ideally also shouldn't access the dict directly
        """
        return self.__dict__.get(key, default)

    def to_dict(self):
        """
        Convert the config to a dictionary
        """
        raise NotImplementedError


T = TypeVar("T", bound=Config)


class ConfigFactory(ABC):
    """Provides different convenience methods to create a Config Object"""

    @staticmethod
    def _extract_default(param: Parameter):
        """Extract default value from a parameter

        If it has a default, return that - else return None

        Args:
            param (Parameter): The parameter from which the default values
            are to be extracted

        Returns:
            param.default (?): The default value if it exists. Else None

        """
        return param.default if param.default != Parameter.empty else None

    @staticmethod
    def _extract_attr(full_name: str, context: Optional[Dict] = None):
        # Split the string, will throw value error if there is no .
        module_name = None  # type: Optional[str]
        try:
            module_name, class_name = full_name.rsplit(".", 1)
        except ValueError:
            # We do not enforce . - class could already be loaded
            pass
        if module_name:
            # load the module, will raise ImportError if module cannot be loaded
            try:
                m = importlib.import_module(module_name)
            except ImportError as e:
                raise ValueError(f"Did not recognise {full_name}: ImportError {e}")
            # get the class, will raise AttributeError if class cannot be found
            try:
                c = getattr(m, class_name)
            except AttributeError as e:
                raise ValueError(f"Did not recognise {full_name}: AttributeError {e}")
        else:
            # If no module, try loading from globals and context
            if context and full_name in context:
                c = context.get(full_name)
            elif full_name in globals():
                c = globals()[full_name]
            else:
                raise ValueError(
                    f"Did not recognise {full_name}: KeyError Not in context or globals()"
                )
        return c

    @staticmethod
    def extract(
        config_class: Type[T],
        config: Union[Dict, Config],
        context: Optional[Dict] = None,
    ) -> T:
        """Extract Config of config_class from config

        Creates an object of type config_class
         by extracting the relevant values from the config

        Args:
            config_class (Type[T: Config]): They type of config being created
            config (Config/Dict): The config containing the values to be extracted
            context: A dictionary containing the globals() context from where the config is loaded

        Returns:
            sub_config (T:Config): the extracted config of type config_class

        """
        signa = signature(config_class.__init__)
        values = {
            p.name: config.get(p.name, ConfigFactory._extract_default(p))
            for _, p in signa.parameters.items()
            if p.name != "self"
        }
        for k, v in values.items():
            if isinstance(v, str):
                try:
                    # For each string, see if it is an attribute
                    v_attr = ConfigFactory._extract_attr(v, context)
                    values[k] = v_attr
                except ValueError:
                    # not an attribute, just skip
                    continue
            elif isinstance(v, dict) and len(v.keys()) == 1:
                # 1-key dicts might be configs, try converting
                key_class = list(v.keys())[0]
                try:
                    v_attr = ConfigFactory._extract_attr(key_class, context)
                    if issubclass(v_attr, Config):
                        # found a config, process values recursively
                        values[k] = ConfigFactory.extract(v_attr, v[key_class], context)
                except ValueError:
                    continue
        return config_class(**values)

    @staticmethod
    def from_dict(dict_config: Dict, context: Optional[Dict] = None) -> Config:
        """Create config from a dict

        Creates a config by reading the dict and extracting each sub-config.
        Excpected format:
        {
        "ConfigClass": {
            "param1": "param1value",
            "sub_config": {"ConfigClass2": {"param2": "param2value"}},
        }

        The config classes either need to be imported beforehand
        or the full path needs to be specified, i.e. "module.something.ConfigClass"

        Args:
            dict_config (dict): Dict containing the values to put into configs
            context: A dictionary containing the globals() context from where the config is loaded

        Returns:
            config (Config): the extracted Config

        """
        # Check the format is as expected
        # dictionary with 1 key which is config class name
        assert len(dict_config.keys()) == 1
        class_key = list(dict_config.keys())[0]
        try:
            config_class = ConfigFactory._extract_attr(class_key, context)
        except ValueError as e:
            raise ValueError(f"Unexpected config format {e}")

        # Now extract the config
        config = ConfigFactory.extract(config_class, dict_config[class_key], context)
        return config

    @staticmethod
    def from_file(path_to_json_file: str, context: Optional[Dict] = None) -> Config:
        """Create config from a json file

        Creates a config by reading the json file + extracting each sub-config.
        Excpected format:
        {
        "ConfigClass": {
            "param1": "param1value",
            "sub_config": {"ConfigClass2": {"param2": "param2value"}},
        }

        The config classes either need to be imported beforehand
        or the full path needs to be specified, i.e. "module.something.ConfigClass"

        Args:
            path_to_json_file (str): Path to json file containing
                                     the values to be put into the config

        Returns:
            config (Config): the extracted Config

        """
        with open(path_to_json_file, "r") as infile:
            dict_config = json.load(infile)
        return ConfigFactory.from_dict(dict_config, context)
