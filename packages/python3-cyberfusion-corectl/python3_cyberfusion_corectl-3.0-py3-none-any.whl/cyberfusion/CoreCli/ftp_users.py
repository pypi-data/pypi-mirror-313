"""FTP users subcommands."""

import os
from typing import Optional

import typer

from cyberfusion.ClusterSupport.ftp_users import FTPUser
from cyberfusion.ClusterSupport.nodes import NodeGroup
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


@app.command("list")
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List FTP users."""
    console.print(
        get_support().get_table(
            objs=get_support().ftp_users,
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get(
    username: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show FTP user."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().ftp_users, username=username)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create(
    username: str,
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
    directory_path_relative: str = typer.Option(
        "",
        "--directory-path",
        help="Relative to UNIX user home directory",
    ),
    unix_user_name: str = typer.Argument(default=...),
) -> None:
    """Create FTP user."""
    ftp_user = FTPUser(get_support())

    unix_user = get_object(get_support().unix_users, username=unix_user_name)
    directory_path = os.path.join(unix_user.home_directory, directory_path_relative)

    ftp_user.create(
        username=username,
        password=password,
        unix_user_id=unix_user.id,
        directory_path=directory_path,
    )

    console.print(
        get_support().get_table(
            objs=[ftp_user],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def create_temporary(
    unix_user_name: str,
    node_hostname: Optional[str] = typer.Argument(
        default=None,
        help="Default is first found node with ProFTPD group",
    ),
) -> None:
    """Create temporary FTP user."""
    ftp_user = FTPUser(get_support())

    unix_user = get_object(get_support().unix_users, username=unix_user_name)

    if node_hostname is None:
        node = get_object(
            get_support().nodes,
            cluster_id=unix_user.cluster_id,
            groups=NodeGroup.PROFTPD,
        )
    else:
        node = get_object(get_support().nodes, hostname=node_hostname)

    username, password, file_manager_url = ftp_user.create_temporary(
        unix_user_id=unix_user.id, node_id=node.id
    )

    console.print(f"Node             : [yellow]{node.hostname}")
    console.print(f"Username         : [yellow]{username}")
    console.print(f"Password         : [yellow]{password}")
    console.print(f"File manager URL : [yellow]{file_manager_url}")


@app.command()
@catch_api_exception
def update_password(
    username: str,
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
) -> None:
    """Update password."""
    ftp_user = get_object(get_support().ftp_users, username=username)

    ftp_user.password = password
    ftp_user.update()


@app.command()
@catch_api_exception
def update_directory_path(
    username: str,
    directory_path_relative: str = typer.Argument(
        metavar="id", default=..., help="Relative to UNIX user home directory"
    ),
) -> None:
    """Update directory path."""
    ftp_user = get_object(get_support().ftp_users, username=username)

    directory_path = os.path.join(
        ftp_user.unix_user.home_directory, directory_path_relative
    )

    ftp_user.directory_path = directory_path
    ftp_user.update()


@app.command()
@catch_api_exception
def delete(
    username: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete FTP user."""
    ftp_user = get_object(get_support().ftp_users, username=username)

    delete_api_object(obj=ftp_user, confirm=confirm)
