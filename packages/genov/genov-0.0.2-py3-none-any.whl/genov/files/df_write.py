from logging import Logger, getLogger
from inspect import stack
from pathlib import Path

from rich.console import Console
from rich.table import Table
from typer import Typer, Context, Argument
from typing import Annotated
from genov.utils.context.context import GContext

from pandas import DataFrame

_obj_app = Typer()
_logger: Logger = getLogger(__name__)

@_obj_app.command()
def df_to_stdout(
        ctx_context: Context,
        str_alias: Annotated[
            str,
            Argument(
                help="The alias for the dataframe stored in context to be printed.",
                metavar="alias",
                callback=GContext.check_alias_name_to_get
            )
        ]
):
    """
    The command prints into console the dataframe instance that is stored in context as ALIAS.
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    _df_to_print: DataFrame = GContext.get_alias_value(
        ctx_context=ctx_context, str_alias=str_alias, typ_type=DataFrame, b_strict=True
    )

    console = Console()
    table = Table(str_alias)
    table.add_row(_df_to_print.to_string())
    console.print(table)

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

@_obj_app.command()
def df_to_xlsx(
        ctx_context: Context,
        str_alias: Annotated[
            str,
            Argument(
                help="The alias for the dataframe stored in context to be printed.",
                metavar="alias",
                callback=GContext.check_alias_name_to_get
            )
        ],
        path_file: Annotated[
            Path,
            Argument(
                help="The file to export the dataframe.",
                metavar="file",
                exists=False,
                file_okay=True,
                dir_okay=False,
                writable=True,
                readable=True,
                resolve_path=True,
            )
        ]
):
    """
    Persist the dataframe aliased as ALIAS in the file system as FILE.
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    _df_to_persist: DataFrame = GContext.get_alias_value(
        ctx_context=ctx_context, str_alias=str_alias, typ_type=DataFrame, b_strict=True
    )

    _df_to_persist.to_excel(excel_writer=path_file)
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
