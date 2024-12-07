"""Domain routers subcommands."""

from typing import List, Optional

import typer

from cyberfusion.CoreCli._utilities import (
    BOOL_MESSAGE,
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    EMPTY_TO_CLEAR_MESSAGE,
    catch_api_exception,
    confirm_clear,
    console,
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
    """List domain routers."""
    console.print(
        get_support().get_table(objs=get_support().domain_routers, detailed=detailed)
    )


@app.command()
@catch_api_exception
def get(
    domain: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show domain router."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().domain_routers, domain=domain)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def add_firewall_groups(domain: str, firewall_groups_names: List[str]) -> None:
    """Add firewall groups."""
    domain_router = get_object(get_support().domain_routers, domain=domain)

    if domain_router.firewall_groups_ids is None:
        domain_router.firewall_groups_ids = []

    for firewall_group_name in firewall_groups_names:
        firewall_group = get_object(
            get_support().firewall_groups,
            name=firewall_group_name,
            cluster_id=domain_router.cluster_id,
        )

        domain_router.firewall_groups_ids.append(firewall_group.id)

    domain_router.update()


@app.command()
@catch_api_exception
@exit_with_status
def remove_firewall_groups(domain: str, firewall_groups_names: List[str]) -> int:
    """Remove firewall groups."""
    domain_router = get_object(get_support().domain_routers, domain=domain)

    exit_code = 0
    success = False

    if domain_router.firewall_groups_ids is None:
        return exit_code

    for firewall_group_name in firewall_groups_names:
        firewall_group = get_object(
            get_support().firewall_groups,
            name=firewall_group_name,
            cluster_id=domain_router.cluster_id,
        )

        try:
            domain_router.firewall_groups_ids.remove(firewall_group.id)
            success = True
        except ValueError:
            print_warning(
                f"Firewall group '{firewall_group_name}' not found, skipping."
            )
            exit_code = 64

    if not success:
        handle_manual_error("No firewall groups have been removed")

    domain_router.update()

    return exit_code


@app.command()
@catch_api_exception
def update_force_ssl(
    domain: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update force SSL."""
    domain_router = get_object(get_support().domain_routers, domain=domain)

    domain_router.force_ssl = state
    domain_router.update()


@app.command()
@confirm_clear
@catch_api_exception
def update_certificate(
    domain: str,
    certificate_id: Optional[int] = typer.Argument(
        default=None, help=EMPTY_TO_CLEAR_MESSAGE
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update certificate."""
    domain_router = get_object(get_support().domain_routers, domain=domain)

    domain_router.certificate_id = certificate_id
    domain_router.update()


@app.command()
@confirm_clear
@catch_api_exception
def update_node(
    domain: str,
    node_hostname: Optional[str] = typer.Argument(
        default=None, help=EMPTY_TO_CLEAR_MESSAGE
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update node."""
    domain_router = get_object(get_support().domain_routers, domain=domain)

    if node_hostname is not None:
        node = get_object(get_support().nodes, hostname=node_hostname)
        domain_router.node_id = node.id
    else:
        domain_router.node_id = None

    domain_router.update()


@app.command()
@confirm_clear
@catch_api_exception
def update_security_txt_policy(
    domain: str,
    security_txt_policy_id: Optional[int] = typer.Argument(
        default=None, help=EMPTY_TO_CLEAR_MESSAGE
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update security.txt policy."""
    domain_router = get_object(get_support().domain_routers, domain=domain)

    domain_router.security_txt_policy_id = security_txt_policy_id
    domain_router.update()
