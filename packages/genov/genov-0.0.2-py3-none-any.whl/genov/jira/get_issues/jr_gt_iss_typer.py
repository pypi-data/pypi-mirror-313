from logging import Logger, getLogger
from inspect import stack
from typer import Typer, Context, Option, Exit
from typing import Annotated
from genov.utils.context.context import GContext

from pathlib import Path

import pydash
from pandas import DataFrame
from rich.panel import Panel
from rich import print
from rich.text import Text

from genov.jira.get_issues.jr_gt_iss import JiraIssuesGetter

_obj_app = Typer()

@_obj_app.command()
def jira_get_issues_typer(
        ctx_context: Context,
        str_alias: Annotated[
            str,
            Option(
                "--alias", "-a",
                help="The alias for the issues stored in context.",
                metavar="alias",
                callback=GContext.check_alias_name_to_set
            )
        ] = "issues"
):
    """
    The command returns the issues from a Jira instance, and store in context as ALIAS.
    """
    _obj_logger: Logger = getLogger(__name__)
    _obj_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    # We retrieve the parameters from the config file
    _str_the_username: str = pydash.get(ctx_context.obj.config, "jira.api_token.username", None)
    _str_the_password: str = pydash.get(ctx_context.obj.config, "jira.api_token.password", None)
    _str_the_url: str = pydash.get(ctx_context.obj.config, "jira.urls.search", None)

    if any(v is None for v in [_str_the_username, _str_the_password, _str_the_url]):

        text = Text()
        text.append("Error:\n", style="bold blink red")
        text.append(
            f"'genov' commands related to jira rely on an API Token to be configured in the configuration file "
            f"'{Path.home().joinpath(".genov.toml")}', under 'jira > api_token'. This API token is to be retrieved "
            f"from atlassian website [https://id.atlassian.com/manage-profile/security/api-tokens].")
        print(Panel(text))
        raise Exit(code=1)

    _df_the_issues: DataFrame = JiraIssuesGetter(
        str_username=_str_the_username,
        str_password=_str_the_password,
        str_url=_str_the_url
    ).get_issues()

    ctx_context.obj[str_alias] = _df_the_issues

    _obj_logger.debug(_df_the_issues.columns)

    _obj_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
