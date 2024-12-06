from logging import Logger, getLogger, basicConfig
from inspect import stack

from typing import Annotated
from typer import Typer, Context, Option
from rich import print
from rich.panel import Panel

from genov.utils.config.config import GConfig
from genov.utils.context.context import GContext

# The commands
from genov.welcome.welcome_typer import welcome_typer
from genov.jira.get_issues.jr_gt_iss_typer import jira_get_issues_typer
from genov.files.df_write import df_to_stdout, df_to_xlsx

# We instantiate the typer application
_obj_genov = Typer(
    chain=True,             # To chain commands
    no_args_is_help=True    # when no parameter, help is displayed
)

# We register the commands here.
_obj_genov.command("welcome")(welcome_typer)
_obj_genov.command("jr-gt-iss")(jira_get_issues_typer)
_obj_genov.command("df-to-stdout")(df_to_stdout)
_obj_genov.command("df-to-xlsx")(df_to_xlsx)

## We add a callback
@_obj_genov.callback()
def main(
        ctx_context: Context,
        b_verbose: Annotated[
            bool,
            Option(
                "--verbose/--no-verbose",
                "-v",
                help="Level of logging verbosity: INFO (--verbose), WARNING (default) or ERROR (--no-verbose).",
                show_default="WARNING"
            )
        ] = None
):
    """
    Genov tool box, the application with all the commands you need in your day-to-day work at Genovation.

    Use the VERBOSE parameter to set the level of logs you need, and let you guide by the HELP.
    """

    _obj_logger: Logger = getLogger(__name__)
    _str_log_msg: str

    _obj_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    if b_verbose is True:
        _str_log_msg = f"[bold red]Logging: DEBUG[/bold red]"
        basicConfig(level="DEBUG")
    elif b_verbose is False:
        _str_log_msg = f"[bold blue]Logging: ERROR[/bold blue]"
        basicConfig(level="ERROR")
    else:
        _str_log_msg = f"[bold orange]Logging: WARNING[/bold orange]"
        basicConfig(level="WARNING")

    print(
        Panel(
            f"{_str_log_msg}\n"
            f"Welcome to the Genovation toolbox!")
    )

    # We load the configuration
    obj_the_config: GConfig = GConfig()
    try:
        dict_the_config: dict = obj_the_config.config
    except Exception as an_exception:
        raise Exception("Configuration file is incorrect! Run cfg_check to get the issues to fix.") from an_exception

    # Ensure that ctx_context.obj exists and is an instance of genov.utils.context.Context
    # This is effectively the context, that is shared across commands
    if not ctx_context.obj:
         _obj_logger.debug(f"We call function ctx_context.ensure_object(genov.utils.context.context.Context)")
         ctx_context.ensure_object(GContext)

    ctx_context.obj.config = dict_the_config

    _obj_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

if __name__ == '__main__':
    _obj_genov()