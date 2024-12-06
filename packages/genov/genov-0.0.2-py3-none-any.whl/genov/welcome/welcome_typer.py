import typer
from rich import print
from rich.panel import Panel
from rich.tree import Tree
from rich.console import Console

from genov.welcome.welcome import welcome


app = typer.Typer()

@app.command()
def welcome_typer(name: str):
    """
    Welcome to the Genovation toolbox!
    This command will greet NAME, and return welcome message.
    It experiments the rich library that can be used across other commands.
    """

    # Typer.secho function...
    typer.secho(
        "Welcome",
        blink=True,
        bold=True
    )

    # A panel: fit
    panel = Panel.fit("Just a panel", border_style="red")
    print(panel)

    # Another panel
    print(
        Panel(
            f"[bold red]Welcome![/bold red]\n"
            f"[green]{welcome(name=name)}[/green]\n"
            f"shooting! :boom:"
        )
    )

    # A tree...
    root = Tree("[b green]Rich Tree", highlight=True, hide_root=True)
    node = root.add(":file_folder: Renderables", guide_style="red")
    node.add(":file_folder: [bold yellow]Atomic", guide_style="uu green")
    node.add(":file_folder: [bold magenta]Containers", guide_style="bold magenta" )
    print( Panel(root) )

    # Error...
    err_console = Console(stderr=True)
    err_console.print("Here is something written to standard error")