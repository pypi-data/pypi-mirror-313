"""Nodes subcommands."""

from typing import Any, List, Optional

import typer

from cyberfusion.ClusterSupport.node_add_ons import NodeAddOn
from cyberfusion.ClusterSupport.nodes import Node, NodeGroup
from cyberfusion.CoreCli._utilities import (
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    EMPTY_TO_CLEAR_MESSAGE,
    catch_api_exception,
    confirm_clear,
    console,
    delete_api_object,
    get_object,
    get_support,
    wait_for_task,
)

groups_properties_node_groups = [
    NodeGroup.REDIS,
    NodeGroup.MARIADB,
    NodeGroup.RABBITMQ,
]

app = typer.Typer()

HELP_PANEL_NODES = "Nodes"
HELP_PANEL_NODE_ADD_ONS = "Node Add-Ons"


@app.command("list", rich_help_panel=HELP_PANEL_NODES)
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List nodes."""
    console.print(get_support().get_table(objs=get_support().nodes, detailed=detailed))


@app.command(rich_help_panel=HELP_PANEL_NODES)
@catch_api_exception
def get(
    hostname: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show node."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().nodes, hostname=hostname)],
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_NODES)
@catch_api_exception
def create(
    product: str,
    groups: List[NodeGroup] = typer.Option([], "--group", show_default=False),
    comment: Optional[str] = typer.Option(default=None),
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create node."""
    node = Node(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    groups_properties: dict[NodeGroup, Optional[dict[str, Any]]] = {}

    for group in groups_properties_node_groups:
        if group in groups:
            existing_nodes = get_support().get_nodes(
                cluster_id=cluster.id, groups=group
            )

            groups_properties[group] = {"is_master": len(existing_nodes) == 0}
        else:
            groups_properties[group] = None

    task_collection = node.create(
        groups=groups,
        comment=comment,
        load_balancer_health_checks_groups_pairs={},
        groups_properties=groups_properties,
        cluster_id=cluster.id,
        product=product,
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command(rich_help_panel=HELP_PANEL_NODES)
@catch_api_exception
def add_groups(hostname: str, groups: List[NodeGroup]) -> None:
    """Add groups."""
    node = get_object(get_support().nodes, hostname=hostname)

    groups_properties = node.groups_properties

    for group in groups_properties_node_groups:
        # Skip if the group isn't added, or the node already has this group

        if group not in groups or group in node.groups:
            continue

        existing_nodes = get_support().get_nodes(
            cluster_id=node.cluster_id, groups=group
        )

        groups_properties[group] = {"is_master": len(existing_nodes) == 0}

    node.groups.extend(groups)
    node.groups_properties = groups_properties
    node.update()


@app.command(rich_help_panel=HELP_PANEL_NODES)
@confirm_clear
@catch_api_exception
def update_comment(
    hostname: str,
    comment: Optional[str] = typer.Argument(default=None, help=EMPTY_TO_CLEAR_MESSAGE),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update comment."""
    node = get_object(get_support().nodes, hostname=hostname)

    node.comment = comment
    node.update()


@app.command(rich_help_panel=HELP_PANEL_NODES)
@catch_api_exception
def get_health_checks(
    hostname: str,
) -> None:
    """Get health checks for node."""
    node = get_object(get_support().nodes, hostname=hostname)

    for group in node.load_balancer_health_checks_groups_pairs:
        console.print(
            f"{group}: {', '.join(node.load_balancer_health_checks_groups_pairs[group])}"
        )


@app.command(rich_help_panel=HELP_PANEL_NODES)
@confirm_clear
@catch_api_exception
def set_health_check(
    hostname: str,
    primary_group: NodeGroup,
    additional_groups: List[NodeGroup] = typer.Argument(
        default=None, help=EMPTY_TO_CLEAR_MESSAGE
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Set health check for group."""
    node = get_object(get_support().nodes, hostname=hostname)

    if not additional_groups:
        del node.load_balancer_health_checks_groups_pairs[primary_group]
    else:
        node.load_balancer_health_checks_groups_pairs[primary_group] = additional_groups

    node.update()


@app.command(rich_help_panel=HELP_PANEL_NODES)
@catch_api_exception
def delete(
    hostname: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete node."""
    node = get_object(get_support().nodes, hostname=hostname)

    delete_api_object(obj=node, confirm=confirm)


@app.command(rich_help_panel=HELP_PANEL_NODES)
@catch_api_exception
def xgrade(hostname: str, product_name: str) -> None:
    """Xgrade node."""
    node = get_object(get_support().nodes, hostname=hostname)

    task_collection = node.xgrade(product_name)

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command(rich_help_panel=HELP_PANEL_NODE_ADD_ONS)
@catch_api_exception
def list_add_ons(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """List node add-ons."""
    console.print(
        get_support().get_table(objs=get_support().node_add_ons, detailed=detailed)
    )


@app.command(rich_help_panel=HELP_PANEL_NODE_ADD_ONS)
@catch_api_exception
def get_add_on(
    id_: int = typer.Argument(metavar="id", default=...),
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show node add-on."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().node_add_ons, id_=id_)],
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_NODE_ADD_ONS)
@catch_api_exception
def create_add_on(hostname: str, product_name: str, quantity: int) -> None:
    """Create node add-on."""
    node_add_on = NodeAddOn(get_support())

    node = get_object(get_support().nodes, hostname=hostname)

    task_collection = node_add_on.create(
        node_id=node.id, product=product_name, quantity=quantity
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command(rich_help_panel=HELP_PANEL_NODE_ADD_ONS)
@catch_api_exception
def delete_add_on(
    id_: int = typer.Argument(metavar="id", default=...),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete node add-on."""
    node_add_on = get_object(get_support().node_add_ons, id_=id_)

    delete_api_object(obj=node_add_on, confirm=confirm)


@app.command(rich_help_panel=HELP_PANEL_NODE_ADD_ONS)
@catch_api_exception
def list_add_ons_products(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """List node add-ons products."""
    console.print(
        get_support().get_table(
            objs=get_support().node_add_ons_products, detailed=detailed
        )
    )


@app.command(rich_help_panel=HELP_PANEL_NODES)
@catch_api_exception
def list_products(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """List nodes products."""
    console.print(
        get_support().get_table(objs=get_support().nodes_products, detailed=detailed)
    )
