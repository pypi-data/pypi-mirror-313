import copy
from logging import Logger, getLogger
import re
from inspect import stack
from typing import Type, TypeVar

from typer import Context, BadParameter
from rich import print
from rich.panel import Panel
from rich.text import Text

class GContext(dict):

    __ERROR_01__ = "[ERROR_01 - Incorrect alias name]"
    __ERROR_02__ = "[ERROR_02 - Inexistant alias name]"
    __ERROR_03__ = "[ERROR_03 - Incorrect type]"

    _obj_logger: Logger = getLogger(__name__)

    _config: dict = None
    _alias: list[str] = []
    _obj_alias_regex: re.Pattern = re.compile('^[a-z_]+$')

    @property
    def config(self):
        if self._config is None:
            raise Exception(f"Unexpected error: configuration has not been initialized...")
        return self._config

    @config.setter
    def config(self, config: dict):
        if self._config is None:
            self._config = copy.deepcopy(config)
        else:
            raise Exception(f"Unexpected error: configuration was already initialized...")

    def __init__(self):
        super().__init__()

    def __setitem__(self, key, value):
        self._obj_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        # The alias should only contain alpha characters and "_"
        if self._obj_alias_regex.match(key) is None:
            raise Exception(self.__ERROR_01__)

        if key in self:
            self._obj_logger.info(f"Function '{stack()[0].filename} - {stack()[0].function}': alias '{key}' overridden.")

        self._obj_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        dict.__setitem__(self,key, value)

    def alias(self, alias, value) -> any:
        any_the_return: any = self.get(alias, None)
        self[alias] = value
        return any_the_return

    @staticmethod
    def check_alias_name_to_get(ctx_context: Context, str_alias: str) -> str:
        if ctx_context.resilient_parsing:
            return str_alias

        if GContext._obj_alias_regex.match(str_alias) is None:
            text = Text()
            text.append("Error:\n", style="bold blink red")
            text.append(
                f"Alias '{str_alias}' is incorrect, as it does not follow naming convention: '^[a-z_]+$'.")
            print(Panel(text))
            raise BadParameter(GContext.__ERROR_01__)

        _obj_the_obj: GContext = ctx_context.obj

        if str_alias not in _obj_the_obj._alias:
            text = Text()
            text.append("Error:\n", style="bold blink red")
            text.append(
                f"Alias '{str_alias}' does not exist in context.")
            print(Panel(text))
            raise BadParameter(GContext.__ERROR_02__)

        return str_alias

    @staticmethod
    def check_alias_name_to_set(ctx_context: Context, str_alias: str) -> str:
        if ctx_context.resilient_parsing:
            return str_alias

        if GContext._obj_alias_regex.match(str_alias) is None:
            text = Text()
            text.append("Error:\n", style="bold blink red")
            text.append(
                f"Alias '{str_alias}' is incorrect, as it does not follow naming convention: '^[a-z_]+$'.")
            print(Panel(text))
            raise BadParameter(GContext.__ERROR_01__)

        _obj_the_obj: GContext = ctx_context.obj

        if str_alias in _obj_the_obj._alias:
            text = Text()
            text.append("Warning:\n", style="bold orange_red1")
            text.append(
                f"Alias '{str_alias}' already exists in context. It will be overriden.")
            print(Panel(text))

        _obj_the_obj._alias.append(str_alias)

        return str_alias

    T = TypeVar("T")

    @staticmethod
    def get_alias_value(ctx_context: Context, str_alias: str, typ_type: Type[T], b_strict: bool=False) -> T:

        if str_alias not in ctx_context.obj:
            raise Exception(f"Could not find in context alias '{str_alias}' to check...")

        _obj_the_object: any = ctx_context.obj[str_alias]

        if not isinstance( _obj_the_object, typ_type):

            if b_strict:
                text = Text()
                text.append("Error:\n", style="bold blink red")
                text.append(
                    f"Alias '{str_alias}' is of type '{type(_obj_the_object)}', which is not an instance of "
                    f"'{typ_type}'.")
                print(Panel(text))
                raise BadParameter(GContext.__ERROR_03__)

            else:
                text = Text()
                text.append("Warning:\n", style="bold orange_red1")
                text.append(
                    f"Alias '{str_alias}' is of type '{type(_obj_the_object)}', which is not an instance of "
                    f"'{typ_type}'.")
                print(Panel(text))
                return False

        return _obj_the_object
