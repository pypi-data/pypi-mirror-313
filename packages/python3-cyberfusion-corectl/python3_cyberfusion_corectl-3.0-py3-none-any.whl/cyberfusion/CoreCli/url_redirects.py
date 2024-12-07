"""URL redirects subcommmands."""

from enum import Enum
from typing import Optional

import typer

from cyberfusion.ClusterSupport.url_redirects import URLRedirect
from cyberfusion.CoreCli._utilities import (
    BOOL_MESSAGE,
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    catch_api_exception,
    console,
    delete_api_object,
    get_object,
    get_support,
    handle_manual_error,
)

app = typer.Typer()


def get_url_redirects_by_domain_or_server_alias(
    domain_or_server_alias: str,
) -> Optional[URLRedirect]:
    """Get URL redirects by domain or server alias."""
    by_domain = get_support()._filter_objects(
        get_support().url_redirects, domain=domain_or_server_alias
    )
    by_server_alias = get_support()._filter_objects(
        get_support().url_redirects, server_aliases=domain_or_server_alias
    )

    return by_domain or by_server_alias or None


def get_url_redirect(domain_or_server_alias: str) -> URLRedirect:
    """Get URL redirect by domain or server alias."""
    url_redirects = get_url_redirects_by_domain_or_server_alias(domain_or_server_alias)

    if url_redirects:
        return url_redirects[0]

    handle_manual_error(f"Object '{domain_or_server_alias}' not found")


class StatusCode(str, Enum):
    """Enum for status codes.

    Copy of ClusterSupport.url_redirects.StatusCode with string types, as Typer
    does not support other Enum types.
    """

    MOVED_PERMANENTLY: str = "301"
    FOUND: str = "302"
    SEE_OTHER: str = "303"
    TEMPORARY_REDIRECT: str = "307"
    PERMANENT_REDIRECT: str = "308"


@app.command("list")
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List URL redirects."""
    console.print(
        get_support().get_table(
            objs=get_support().url_redirects,
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get(
    domain: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show URL redirect."""
    console.print(
        get_support().get_table(
            objs=[get_url_redirect(domain)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create(
    domain: str,
    destination_url: str,
    add_www: bool = typer.Option(False, "--add-www/--dont-add-www"),
    status_code: StatusCode = StatusCode.FOUND,
    keep_query_parameters: bool = typer.Option(
        True, "--keep-query-parameters/--drop-query-parameters"
    ),
    keep_path: bool = typer.Option(True, "--keep-path/--drop-path"),
    description: Optional[str] = None,
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create URL redirect."""
    url_redirect = URLRedirect(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    server_aliases = []

    if add_www:
        server_aliases.append(f"www.{domain}")

    url_redirect.create(
        domain=domain,
        server_aliases=server_aliases,
        destination_url=destination_url,
        status_code=int(status_code.value),
        keep_query_parameters=keep_query_parameters,
        keep_path=keep_path,
        description=description,
        cluster_id=cluster.id,
    )

    console.print(
        get_support().get_table(
            objs=[url_redirect],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def update_keep_query_parameters(
    domain: str, state: bool = typer.Argument(default=..., help=BOOL_MESSAGE)
) -> None:
    """Update keep query parameters."""
    url_redirect = get_url_redirect(domain)

    url_redirect.keep_query_parameters = state
    url_redirect.update()


@app.command()
@catch_api_exception
def update_keep_path(
    domain: str, state: bool = typer.Argument(default=..., help=BOOL_MESSAGE)
) -> None:
    """Update keep path."""
    url_redirect = get_url_redirect(domain)

    url_redirect.keep_path = state
    url_redirect.update()


@app.command()
@catch_api_exception
def add_server_alias(domain: str, server_alias: str) -> None:
    """Add server alias."""
    url_redirect = get_url_redirect(domain)

    url_redirect.server_aliases.append(server_alias)
    url_redirect.update()


@app.command()
@catch_api_exception
def remove_server_alias(domain: str, server_alias: str) -> None:
    """Remove server alias."""
    url_redirect = get_url_redirect(domain)

    try:
        url_redirect.server_aliases.remove(server_alias)
    except ValueError:
        handle_manual_error(f"Server alias '{server_alias}' not found")

    url_redirect.update()


@app.command()
@catch_api_exception
def update_destination_url(domain: str, destination_url: str) -> None:
    """Update destination URL."""
    url_redirect = get_url_redirect(domain)

    url_redirect.destination_url = destination_url
    url_redirect.update()


@app.command()
@catch_api_exception
def update_status_code(domain: str, status_code: int) -> None:
    """Update status code."""
    url_redirect = get_url_redirect(domain)

    url_redirect.status_code = status_code
    url_redirect.update()


@app.command()
@catch_api_exception
def update_description(domain: str, description: str) -> None:
    """Update description."""
    url_redirect = get_url_redirect(domain)

    url_redirect.description = description
    url_redirect.update()


@app.command()
@catch_api_exception
def delete(
    domain: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete URL redirect."""
    url_redirect = get_url_redirect(domain)

    delete_api_object(obj=url_redirect, confirm=confirm)
