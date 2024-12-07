"""API users subcommands."""

from typing import List, Optional

import typer

from cyberfusion.ClusterSupport import APIUser, APIUserToCluster
from cyberfusion.Common import generate_random_string
from cyberfusion.CoreCli._utilities import (
    BOOL_MESSAGE,
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    RANDOM_PASSWORD_MESSAGE,
    catch_api_exception,
    console,
    delete_api_object,
    exit_with_status,
    get_api_user_to_cluster_by_multiple,
    get_object,
    get_support,
    handle_manual_error,
    print_warning,
)

app = typer.Typer()

HELP_PANEL_API_USER = "API Users"
HELP_PANEL_API_USER_GRANT = "API User to Clusters"


@app.command("list", rich_help_panel=HELP_PANEL_API_USER)
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List API users."""
    console.print(
        get_support().get_table(
            objs=get_support().api_users,
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_API_USER)
@catch_api_exception
def get(
    username: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show API user."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().api_users, username=username)],
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_API_USER)
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
    customer_identifier: Optional[str] = None,
    is_active: bool = typer.Option(True, "--active/--inactive"),
    is_superuser: bool = typer.Option(False, "--superuser"),
    trusted_ip_networks: Optional[List[str]] = typer.Option(
        None, "--trusted-ip-network"
    ),
) -> None:
    """Create API user."""
    api_user = APIUser(get_support())

    if customer_identifier:
        customer = get_object(get_support().customers, identifier=customer_identifier)
    else:
        customer = None

    if not trusted_ip_networks:
        trusted_ip_networks = None

    api_user.create(
        username=username,
        is_active=is_active,
        is_superuser=is_superuser,
        password=password,
        trusted_ip_networks=trusted_ip_networks,
        customer_id=customer.id if customer else None,
    )

    console.print(
        get_support().get_table(
            objs=[api_user],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_API_USER)
@catch_api_exception
def update_active(
    username: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update is active."""
    api_user = get_object(get_support().api_users, username=username)

    api_user.is_active = state
    api_user.update()


@app.command(rich_help_panel=HELP_PANEL_API_USER)
@catch_api_exception
def update_superuser(
    username: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update is superuser."""
    api_user = get_object(get_support().api_users, username=username)

    api_user.is_superuser = state
    api_user.update()


@app.command(rich_help_panel=HELP_PANEL_API_USER)
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
    api_user = get_object(get_support().api_users, username=username)

    api_user.update(password=password)


@app.command(rich_help_panel=HELP_PANEL_API_USER)
@catch_api_exception
def add_trusted_ip_networks(username: str, trusted_ip_networks: List[str]) -> None:
    """Add trusted IP networks."""
    api_user = get_object(get_support().api_users, username=username)

    api_user.trusted_ip_networks.extend(trusted_ip_networks)
    api_user.update()


@app.command(rich_help_panel=HELP_PANEL_API_USER)
@catch_api_exception
@exit_with_status
def remove_trusted_ip_networks(username: str, trusted_ip_networks: List[str]) -> int:
    """Remove trusted IP networks."""
    api_user = get_object(get_support().api_users, username=username)

    exit_code = 0
    success = False

    for ip_network in trusted_ip_networks:
        try:
            api_user.trusted_ip_networks.remove(ip_network)
            success = True
        except ValueError:
            print_warning(f"Trusted IP network '{ip_network}' not found, skipping.")
            exit_code = 64

    if not success:
        handle_manual_error("No trusted IP networks have been removed")

    api_user.update()

    return exit_code


@app.command(rich_help_panel=HELP_PANEL_API_USER)
@catch_api_exception
def delete(
    username: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete API user."""
    api_user = get_object(get_support().api_users, username=username)

    delete_api_object(obj=api_user, confirm=confirm)


@app.command(rich_help_panel=HELP_PANEL_API_USER_GRANT)
@catch_api_exception
def list_grants(
    api_user_username: Optional[str] = typer.Option(
        None, "--api-user", "-u", help="Filter by API user username"
    ),
    cluster_name: Optional[str] = typer.Option(
        None, "--cluster", "-c", help="Filter by cluster name"
    ),
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """List API users to clusters."""
    args = {}

    if cluster_name is not None:
        args["cluster_id"] = get_object(get_support().clusters, name=cluster_name).id

    if api_user_username is not None:
        args["api_user_id"] = get_object(
            get_support().api_users, username=api_user_username
        ).id

    console.print(
        get_support().get_table(
            objs=get_support().get_api_users_to_clusters(**args),
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_API_USER_GRANT)
@catch_api_exception
def create_grant(api_user_username: str, cluster_name: str) -> None:
    """Create API user to cluster."""
    api_user = get_object(get_support().api_users, username=api_user_username)
    cluster = get_object(get_support().clusters, name=cluster_name)

    api_user_to_cluster = APIUserToCluster(get_support())

    api_user_to_cluster.create(api_user_id=api_user.id, cluster_id=cluster.id)

    console.print(
        get_support().get_table(
            objs=[api_user_to_cluster],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_API_USER_GRANT)
@catch_api_exception
def revoke_grant(
    api_user_username: str,
    cluster_name: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete API user to cluster."""
    api_user_to_cluster = get_api_user_to_cluster_by_multiple(
        api_user_username=api_user_username,
        cluster_name=cluster_name,
    )

    delete_api_object(obj=api_user_to_cluster, confirm=confirm)
