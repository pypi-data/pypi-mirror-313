"""Basic authentication realms subcommands."""

from typing import Optional

import typer

from cyberfusion.ClusterSupport import BasicAuthenticationRealm
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
    """List basic authentication realms."""
    console.print(
        get_support().get_table(
            objs=get_support().basic_authentication_realms,
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get(
    id_: int = typer.Argument(metavar="id", default=...),
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show basic authentication realm."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().basic_authentication_realms, id_=id_)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create(
    name: str,
    virtual_host_domain: str,
    htpasswd_file_id: int,
    directory_path: Optional[str] = typer.Option(
        default=None, help="Leave blank for entire virtual host document root."
    ),
) -> None:
    """Create basic authentication realm."""
    virtual_host_id = get_object(
        get_support().virtual_hosts, domain=virtual_host_domain
    ).id

    basic_authentication_realm = BasicAuthenticationRealm(get_support())

    basic_authentication_realm.create(
        name=name,
        htpasswd_file_id=htpasswd_file_id,
        virtual_host_id=virtual_host_id,
        directory_path=directory_path,
    )

    console.print(
        get_support().get_table(
            objs=[basic_authentication_realm],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def update_name(
    id_: int = typer.Argument(metavar="id", default=...),
    name: str = typer.Argument(default=...),
) -> None:
    """Update name."""
    basic_authentication_realm = get_object(
        get_support().basic_authentication_realms, id_=id_
    )

    basic_authentication_realm.name = name
    basic_authentication_realm.update()


@app.command()
@catch_api_exception
def update_htpasswd_file(
    id_: int = typer.Argument(metavar="id", default=...),
    htpasswd_file_id: int = typer.Argument(default=...),
) -> None:
    """Update htpasswd file."""
    basic_authentication_realm = get_object(
        get_support().basic_authentication_realms, id_=id_
    )

    basic_authentication_realm.htpasswd_file_id = htpasswd_file_id
    basic_authentication_realm.update()


@app.command()
@catch_api_exception
def delete(
    id_: int = typer.Argument(metavar="id", default=...),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete basic authentication realm."""
    basic_authentication_realm = get_object(
        get_support().basic_authentication_realms, id_=id_
    )

    delete_api_object(obj=basic_authentication_realm, confirm=confirm)
