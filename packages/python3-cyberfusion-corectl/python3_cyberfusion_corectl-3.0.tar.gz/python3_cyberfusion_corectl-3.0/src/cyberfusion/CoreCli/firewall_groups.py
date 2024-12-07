"""Firewall groups subcommands."""

from typing import List

import typer

from cyberfusion.ClusterSupport.firewall_groups import FirewallGroup
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
def list_(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """List firewall groups."""
    console.print(
        get_support().get_table(objs=get_support().firewall_groups, detailed=detailed)
    )


@app.command()
@catch_api_exception
def get(
    id_: int = typer.Argument(metavar="id", default=...),
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show firewall group."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().firewall_groups, id_=id_)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create(
    name: str,
    ip_networks: List[str],
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create firewall group."""
    firewall_group = FirewallGroup(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    firewall_group.create(name=name, ip_networks=ip_networks, cluster_id=cluster.id)

    console.print(
        get_support().get_table(
            objs=[firewall_group],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def add_ip_networks(
    id_: int = typer.Argument(metavar="id", default=...),
    ip_networks: List[str] = typer.Argument(default=...),
) -> None:
    """Add IP networks."""
    firewall_group = get_object(get_support().firewall_groups, id_=id_)

    firewall_group.ip_networks.extend(ip_networks)
    firewall_group.update()


@app.command()
@catch_api_exception
@exit_with_status
def remove_ip_networks(
    id_: int = typer.Argument(metavar="id", default=...),
    ip_networks: List[str] = typer.Argument(default=...),
) -> int:
    """Remove IP networks."""
    firewall_group = get_object(get_support().firewall_groups, id_=id_)

    exit_code = 0
    success = False

    for ip_network in ip_networks:
        try:
            firewall_group.ip_networks.remove(ip_network)
            success = True
        except ValueError:
            print_warning(f"IP network '{ip_network}' not found, skipping.")
            exit_code = 64

    if not success:
        handle_manual_error("No IP networks have been removed")

    firewall_group.update()

    return exit_code


@app.command()
@catch_api_exception
def delete(
    id_: int = typer.Argument(metavar="id", default=...),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete firewall group."""
    firewall_group = get_object(get_support().firewall_groups, id_=id_)

    delete_api_object(obj=firewall_group, confirm=confirm)
