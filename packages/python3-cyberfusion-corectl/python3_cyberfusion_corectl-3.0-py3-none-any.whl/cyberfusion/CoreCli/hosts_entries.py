"""Hosts entries subcommands."""

import typer

from cyberfusion.ClusterSupport.hosts_entries import HostsEntry
from cyberfusion.CoreCli._utilities import (
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
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
    """List hosts entries."""
    console.print(
        get_support().get_table(objs=get_support().hosts_entries, detailed=detailed)
    )


@app.command()
@catch_api_exception
def get(
    id_: int = typer.Argument(metavar="id", default=...),
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show hosts entry."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().hosts_entries, id_=id_)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create(host_name: str, cluster_name: str, node_hostname: str) -> None:
    """Create hosts entry."""
    hosts_entry = HostsEntry(get_support())

    node = get_object(get_support().nodes, hostname=node_hostname)
    cluster = get_object(get_support().clusters, name=cluster_name)

    hosts_entry.create(host_name=host_name, cluster_id=cluster.id, node_id=node.id)

    console.print(
        get_support().get_table(
            objs=[hosts_entry],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def delete(
    id_: int = typer.Argument(metavar="id", default=...),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete hosts entry."""
    hosts_entry = get_object(get_support().hosts_entries, id_=id_)

    delete_api_object(obj=hosts_entry, confirm=confirm)
