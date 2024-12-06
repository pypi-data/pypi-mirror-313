import importlib.resources

from logging import Logger, getLogger
from inspect import stack
from pathlib import Path
from tomlkit import parse, TOMLDocument

class GConfig():
    """
    ERROR_01
    ERROR_02
    """

    __FILE_NAME__: str = ".genov.toml"
    __VALUE_TODO_STR__: str = "GTodo.str" # The default value in config template
    __VALUE_TODO_FLOAT__: str = "GTodo.float" # The default value in config template

    __ERROR_01__ = "[ERROR_01 - Missing configuration file]"
    __ERROR_02__ = "[ERROR_02 - Incorrect toml file]"
    __ERROR_03__ = "[ERROR_03 - Incorrect Genov configuration file]"

    _obj_logger: Logger = getLogger(__name__)

    _path: Path
    _config: TOMLDocument = None
    _template: TOMLDocument = None

    @property
    def config(self):
        if self._config is None:
            self._config = self._load_config( path = self._path)
            if self._check_config(
                config = self._config.unwrap(),
                template=self._template.unwrap()
            ):
                raise Exception(self.__ERROR_03__)
        return self._config.value

    def __init__(
            self
    ):
        self._path = Path.home().joinpath(GConfig.__FILE_NAME__)
        self._template = self._load_template()

    @staticmethod
    def _load_config(path: Path) -> TOMLDocument:
        if path.is_file() is False:
            raise Exception(GConfig.__ERROR_01__)

        try:
            obj_the_return: TOMLDocument = parse(path.read_text())
        except Exception as an_exception:
            raise Exception(GConfig.__ERROR_02__) from an_exception

        return obj_the_return

    @staticmethod
    def _load_template() -> TOMLDocument:
        try:
            str_the_template: str = (
                importlib.resources.read_text("genov.utils.config", GConfig.__FILE_NAME__))
        except Exception as an_exception:
            raise Exception (
                f"Unexpected error: template toml configuration file could not be read...") from an_exception
        try:
            obj_the_template: TOMLDocument = parse(str_the_template)
        except Exception as an_exception:
            raise Exception (
                f"Unexpected error: template toml configuration file could not be parsed...") from an_exception
        return obj_the_template

    @staticmethod
    def _check_config(
            config: dict,
            template: dict
    ) -> dict|None:
        GConfig._obj_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        dict_the_return: dict = {}

        for sub_key, sub_template in template.items():
            if not sub_key in config:
                dict_the_return[sub_key] = sub_template

            elif isinstance(sub_template, dict):
                if isinstance(config[sub_key], dict):
                    dict_the_sub_return: dict = GConfig._check_config(config[sub_key], sub_template)
                    if dict_the_sub_return:
                        dict_the_return[sub_key] = dict_the_sub_return
                else:
                    dict_the_return[sub_key] = sub_template

            elif sub_template == GConfig.__VALUE_TODO_STR__:
                if not isinstance(config[sub_key], str):
                    dict_the_return[sub_key] = sub_template
            elif sub_template == GConfig.__VALUE_TODO_FLOAT__:
                if not isinstance(config[sub_key], float):
                    dict_the_return[sub_key] = sub_template

        GConfig._obj_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        if dict_the_return:
            return dict_the_return

        return None
