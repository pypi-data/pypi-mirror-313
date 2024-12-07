"""HAProxy listens subcommands."""

from typing import Optional

import typer

from cyberfusion.ClusterSupport import HAProxyListen, HAProxyListenToNode
from cyberfusion.ClusterSupport.nodes import NodeGroup
from cyberfusion.CoreCli._utilities import (
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    catch_api_exception,
    console,
    delete_api_object,
    get_haproxy_listen_to_node_by_multiple,
    get_object,
    get_support,
)

app = typer.Typer()

HELP_PANEL_HAPROXY_LISTENS = "HAProxy Listens"
HELP_PANEL_HAPROXY_LISTENS_TO_NODES = "HAProxy Listens to Nodes"


@app.command("list", rich_help_panel=HELP_PANEL_HAPROXY_LISTENS)
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List HAProxy listens."""
    console.print(
        get_support().get_table(
            objs=get_support().haproxy_listens,
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_HAPROXY_LISTENS)
@catch_api_exception
def get(
    name: str,
) -> None:
    """Show HAProxy listen."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().haproxy_listens, name=name)]
        )
    )


@app.command(rich_help_panel=HELP_PANEL_HAPROXY_LISTENS)
@catch_api_exception
def create(
    name: str,
    nodes_group: NodeGroup,
    destination_cluster_name: str,
    port: Optional[int] = None,
    socket_path: Optional[str] = None,
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create HAProxy listen."""
    haproxy_listen = HAProxyListen(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)
    destination_cluster = get_object(
        get_support().clusters, name=destination_cluster_name
    )

    haproxy_listen.create(
        name=name,
        nodes_group=nodes_group,
        port=port,
        socket_path=socket_path,
        destination_cluster_id=destination_cluster.id,
        cluster_id=cluster.id,
    )

    console.print(
        get_support().get_table(
            objs=[haproxy_listen],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_HAPROXY_LISTENS)
@catch_api_exception
def delete(
    name: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete HAProxy listen."""
    haproxy_listen = get_object(get_support().haproxy_listens, name=name)

    delete_api_object(obj=haproxy_listen, confirm=confirm)


@app.command(rich_help_panel=HELP_PANEL_HAPROXY_LISTENS_TO_NODES)
@catch_api_exception
def list_nodes(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
    haproxy_listen_name: Optional[str] = typer.Option(
        None, "--haproxy-listen", "-l", help="Filter by HAProxy listen name"
    ),
    node_hostname: Optional[str] = typer.Option(
        None, "--node", "-n", help="Filter by node hostname"
    ),
) -> None:
    """List HAProxy listens to nodes."""
    args: dict = {}

    node = None

    if node_hostname:
        node = get_object(get_support().nodes, hostname=node_hostname)

        args["node_id"] = node.id

    if haproxy_listen_name:
        haproxy_listen = get_object(
            get_support().haproxy_listens,
            name=haproxy_listen_name,
            cluster_id=node.cluster_id if node else None,
        )

        args["haproxy_listen_id"] = haproxy_listen.id

    console.print(
        get_support().get_table(
            objs=get_support().get_haproxy_listens_to_nodes(**args),
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_HAPROXY_LISTENS_TO_NODES)
@catch_api_exception
def create_node(
    haproxy_listen_name: str,
    node_hostname: str,
) -> None:
    """Create HAProxy listen to node."""
    haproxy_listen_to_node = HAProxyListenToNode(get_support())

    node = get_object(get_support().nodes, hostname=node_hostname)
    haproxy_listen = get_object(
        get_support().haproxy_listens,
        name=haproxy_listen_name,
        cluster_id=node.cluster.id,
    )

    haproxy_listen_to_node.create(haproxy_listen_id=haproxy_listen.id, node_id=node.id)

    console.print(
        get_support().get_table(
            objs=[haproxy_listen_to_node],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_HAPROXY_LISTENS_TO_NODES)
@catch_api_exception
def delete_node(
    haproxy_listen_name: str,
    node_hostname: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete HAProxy listen to node."""
    haproxy_listen_to_node = get_haproxy_listen_to_node_by_multiple(
        haproxy_listen_name=haproxy_listen_name,
        node_hostname=node_hostname,
    )

    delete_api_object(obj=haproxy_listen_to_node, confirm=confirm)
