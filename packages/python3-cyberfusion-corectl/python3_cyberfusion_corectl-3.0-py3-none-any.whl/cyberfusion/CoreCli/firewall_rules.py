"""Firewall rules subcommands."""

from typing import Optional

import typer

from cyberfusion.ClusterSupport.firewall_rules import (
    FirewallRule,
    FirewallRuleExternalProviderName,
    FirewallRuleServiceName,
)
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
    """List firewall rules."""
    console.print(
        get_support().get_table(
            objs=get_support().firewall_rules,
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get(
    id_: int = typer.Argument(metavar="id", default=...),
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show firewall rule."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().firewall_rules, id_=id_)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create(
    firewall_group_name: Optional[str] = typer.Option(
        None,
        rich_help_panel="Access Source",
    ),
    external_provider_name: Optional[FirewallRuleExternalProviderName] = typer.Option(
        None,
        rich_help_panel="Access Source",
    ),
    service_name: Optional[FirewallRuleServiceName] = typer.Option(
        None,
        rich_help_panel="Access Destination",
    ),
    haproxy_listen_name: Optional[str] = typer.Option(
        None,
        rich_help_panel="Access Destination",
    ),
    port: Optional[int] = typer.Option(
        None,
        rich_help_panel="Access Destination",
    ),
    node_hostname: str = typer.Argument(default=...),
) -> None:
    """Create firewall rule."""
    firewall_rule = FirewallRule(get_support())

    node = get_object(get_support().nodes, hostname=node_hostname)

    firewall_group_id = None

    if firewall_group_name:
        firewall_group_id = get_object(
            get_support().firewall_groups,
            name=firewall_group_name,
            cluster_id=node.cluster_id,
        ).id

    haproxy_listen_id = None

    if haproxy_listen_name:
        haproxy_listen_id = get_object(
            get_support().haproxy_listens,
            name=haproxy_listen_name,
            cluster_id=node.cluster_id,
        ).id

    firewall_rule.create(
        node_id=node.id,
        firewall_group_id=firewall_group_id,
        external_provider_name=external_provider_name,
        service_name=service_name,
        haproxy_listen_id=haproxy_listen_id,
        port=port,
    )

    console.print(
        get_support().get_table(
            objs=[firewall_rule],
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
    """Delete firewall rule."""
    firewall_rule = get_object(get_support().firewall_rules, id_=id_)

    delete_api_object(obj=firewall_rule, confirm=confirm)
