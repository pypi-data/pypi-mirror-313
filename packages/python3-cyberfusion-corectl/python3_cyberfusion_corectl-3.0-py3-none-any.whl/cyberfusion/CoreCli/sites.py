"""Sites subcommands."""

import typer

from cyberfusion.CoreCli._utilities import (
    catch_api_exception,
    console,
    get_support,
)

app = typer.Typer()


@app.command("list")
@catch_api_exception
def list_() -> None:
    """List sites."""
    console.print(get_support().get_table(objs=get_support().sites))
