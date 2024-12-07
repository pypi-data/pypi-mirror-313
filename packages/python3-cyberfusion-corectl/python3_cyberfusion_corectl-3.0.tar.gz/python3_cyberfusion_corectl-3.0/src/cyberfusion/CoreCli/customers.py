"""Customers subcommands."""

import typer
from rich.panel import Panel
from rich.table import Table

from cyberfusion.ClusterSupport.enums import IPAddressFamily
from cyberfusion.CoreCli._utilities import (
    DETAILED_MESSAGE,
    catch_api_exception,
    console,
    get_object,
    get_support,
    wait_for_task,
)

app = typer.Typer()

HELP_PANEL_CUSTOMERS = "Customers"
HELP_PANEL_IP_ADDRESSES = "IP addresses"


@app.command("list", rich_help_panel=HELP_PANEL_CUSTOMERS)
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List customers."""
    console.print(
        get_support().get_table(objs=get_support().customers, detailed=detailed)
    )


@app.command(rich_help_panel=HELP_PANEL_CUSTOMERS)
@catch_api_exception
def get(
    identifier: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show customer."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().customers, identifier=identifier)],
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_IP_ADDRESSES)
@catch_api_exception
def list_ip_addresses_products(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """List IP addresses products."""
    console.print(
        get_support().get_table(
            objs=get_support().customer_ip_addresses_products,
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_IP_ADDRESSES)
@catch_api_exception
def list_ip_addresses(
    identifier: str,
) -> None:
    """List IP addresses."""
    customer = get_object(get_support().customers, identifier=identifier)

    ip_addresses = customer.get_ip_addresses()

    table = Table(
        expand=True,
        show_lines=False,
        show_edge=False,
        box=None,
    )

    for column in [
        "Service Account Group",
        "Service Account Name",
        "IP Address",
        "DNS Name",
        "Default",
    ]:
        table.add_column(column, overflow="fold")

    for service_account_group, service_accounts in ip_addresses.items():
        for service_account_name, ip_addresses in service_accounts.items():
            for ip_address in ip_addresses:
                table.add_row(
                    service_account_group,
                    service_account_name,
                    ip_address["ip_address"],
                    ip_address["dns_name"],
                    str(not ip_address["dns_name"]),
                )

    console.print(Panel(table, title="IP Addresses", title_align="left"))


@app.command(rich_help_panel=HELP_PANEL_IP_ADDRESSES)
@catch_api_exception
def create_ip_address(
    identifier: str,
    service_account_name: str,
    dns_name: str,
    address_family: IPAddressFamily,
) -> None:
    """Create IP address."""
    customer = get_object(get_support().customers, identifier=identifier)

    task_collection = customer.create_ip_address(
        service_account_name=service_account_name,
        dns_name=dns_name,
        address_family=address_family,
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command(rich_help_panel=HELP_PANEL_IP_ADDRESSES)
@catch_api_exception
def delete_ip_address(identifier: str, ip_address: str) -> None:
    """Delete IP address."""
    customer = get_object(get_support().customers, identifier=identifier)

    task_collection = customer.delete_ip_address(ip_address=ip_address)

    wait_for_task(task_collection_uuid=task_collection.uuid)
