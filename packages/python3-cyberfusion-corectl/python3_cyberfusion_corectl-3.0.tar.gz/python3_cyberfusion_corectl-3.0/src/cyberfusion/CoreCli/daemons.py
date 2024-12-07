"""Daemons subcommands"""

from typing import List

import typer

from cyberfusion.ClusterSupport.daemons import Daemon
from cyberfusion.CoreCli._utilities import (
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    catch_api_exception,
    console,
    delete_api_object,
    exit_with_status,
    get_object,
    get_support,
    handle_manual_error,
    print_warning,
)

app = typer.Typer()


@app.command("list")
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List daemons."""
    console.print(
        get_support().get_table(objs=get_support().daemons, detailed=detailed)
    )


@app.command()
@catch_api_exception
def get(
    name: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show daemon."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().daemons, name=name)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create(
    name: str,
    command: str,
    unix_user_username: str,
    node_hostnames: list[str],
) -> None:
    """Create daemon."""
    daemon = Daemon(get_support())

    nodes_ids = None

    if node_hostnames:
        nodes_ids = [
            get_object(get_support().nodes, hostname=hostname).id
            for hostname in node_hostnames
        ]

    daemon.create(
        name=name,
        command=command,
        nodes_ids=nodes_ids,
        unix_user_id=get_object(
            get_support().unix_users, username=unix_user_username
        ).id,
    )

    console.print(
        get_support().get_table(
            objs=[daemon],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def update_command(
    name: str, command: str = typer.Option(default=..., prompt=True)
) -> None:
    """Update command."""
    daemon = get_object(get_support().daemons, name=name)

    daemon.command = command
    daemon.update()


@app.command()
@catch_api_exception
def add_nodes(name: str, nodes_hostnames: List[str]) -> None:
    """Add nodes."""
    daemon = get_object(get_support().daemons, name=name)

    nodes_ids = []

    for node_hostname in nodes_hostnames:
        nodes_ids.append(get_object(get_support().nodes, hostname=node_hostname).id)

    daemon.nodes_ids.extend(nodes_ids)
    daemon.update()


@app.command()
@catch_api_exception
@exit_with_status
def remove_nodes(name: str, nodes_hostnames: List[str]) -> int:
    """Remove nodes."""
    daemon = get_object(get_support().daemons, name=name)

    exit_code = 0
    success = False

    for node_hostname in nodes_hostnames:
        node = get_object(get_support().nodes, hostname=node_hostname)

        try:
            daemon.nodes_ids.remove(node.id)
            success = True
        except ValueError:
            print_warning(f"Node '{node_hostname}' not found, skipping.")
            exit_code = 64

    if not success:
        handle_manual_error("No nodes have been removed")

    daemon.update()

    return exit_code


@app.command()
@catch_api_exception
def delete(
    name: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete daemon."""
    daemon = get_object(get_support().daemons, name=name)

    delete_api_object(obj=daemon, confirm=confirm)
