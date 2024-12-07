"""Htpasswd subcommands."""

import typer

from cyberfusion.ClusterSupport.htpasswd_files import HtpasswdFile
from cyberfusion.ClusterSupport.htpasswd_users import HtpasswdUser
from cyberfusion.Common import generate_random_string
from cyberfusion.CoreCli._utilities import (
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    RANDOM_PASSWORD_MESSAGE,
    catch_api_exception,
    console,
    delete_api_object,
    get_object,
    get_support,
)

app = typer.Typer()

HELP_PANEL_HTPASSWD_FILES = "Htpasswd Files"
HELP_PANEL_HTPASSWD_USERS = "Htpasswd Users"


@app.command(rich_help_panel=HELP_PANEL_HTPASSWD_FILES)
@catch_api_exception
def list_files(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """List htpasswd files."""
    console.print(
        get_support().get_table(
            objs=get_support().htpasswd_files,
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_HTPASSWD_USERS)
@catch_api_exception
def list_users(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """List htpasswd users."""
    console.print(
        get_support().get_table(
            objs=get_support().htpasswd_users,
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_HTPASSWD_FILES)
@catch_api_exception
def get_file(
    id_: int = typer.Argument(metavar="id", default=...),
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show htpasswd file."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().htpasswd_files, id_=id_)],
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_HTPASSWD_USERS)
@catch_api_exception
def get_user(
    id_: int = typer.Argument(metavar="id", default=...),
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show htpasswd user."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().htpasswd_users, id_=id_)],
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_HTPASSWD_FILES)
@catch_api_exception
def create_file(
    unix_user_username: str,
) -> None:
    """Create htpasswd file."""
    unix_user_id = get_object(get_support().unix_users, username=unix_user_username).id

    htpasswd_file = HtpasswdFile(get_support())

    htpasswd_file.create(
        unix_user_id=unix_user_id,
    )

    console.print(
        get_support().get_table(
            objs=[htpasswd_file],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_HTPASSWD_USERS)
@catch_api_exception
def create_user(
    username: str = typer.Argument(default=...),
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
    htpasswd_file_id: int = typer.Argument(default=...),
) -> None:
    """Create htpasswd user."""
    htpasswd_user = HtpasswdUser(get_support())

    htpasswd_user.create(
        username=username,
        password=password,
        htpasswd_file_id=htpasswd_file_id,
    )

    console.print(
        get_support().get_table(
            objs=[htpasswd_user],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_HTPASSWD_USERS)
@catch_api_exception
def update_user_password(
    id_: int = typer.Argument(metavar="id", default=...),
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
) -> None:
    """Update htpasswd user password."""
    htpasswd_user = get_object(get_support().htpasswd_users, id_=id_)

    htpasswd_user.password = password
    htpasswd_user.update()


@app.command(rich_help_panel=HELP_PANEL_HTPASSWD_FILES)
@catch_api_exception
def delete_file(
    id_: int = typer.Argument(metavar="id", default=...),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete htpasswd file."""
    htpasswd_file = get_object(get_support().htpasswd_files, id_=id_)

    delete_api_object(obj=htpasswd_file, confirm=confirm)


@app.command(rich_help_panel=HELP_PANEL_HTPASSWD_USERS)
@catch_api_exception
def delete_user(
    id_: int = typer.Argument(metavar="id", default=...),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete htpasswd user."""
    htpasswd_user = get_object(get_support().htpasswd_users, id_=id_)

    delete_api_object(obj=htpasswd_user, confirm=confirm)
