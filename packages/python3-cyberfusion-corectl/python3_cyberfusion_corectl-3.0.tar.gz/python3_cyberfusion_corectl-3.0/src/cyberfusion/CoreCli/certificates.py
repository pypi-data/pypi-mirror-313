"""Certificates subcommands."""

from pathlib import Path
from typing import Optional

import typer

from cyberfusion.ClusterSupport.certificates import Certificate
from cyberfusion.CoreCli._utilities import (
    CONFIRM_MESSAGE,
    catch_api_exception,
    console,
    delete_api_object,
    get_object,
    get_support,
    print_or_write_contents,
)

app = typer.Typer()


@app.command("list")
@catch_api_exception
def list_() -> None:
    """List certificates."""
    console.print(get_support().get_table(objs=get_support().certificates))


@app.command()
@catch_api_exception
def get_common_names(id_: int = typer.Argument(metavar="id", default=...)) -> None:
    """Show common names."""
    certificate = get_object(get_support().certificates, id_=id_)

    for common_name in certificate.common_names:
        console.print(f"- {common_name}")


@app.command("get-certificate")
@catch_api_exception
def get_certificate_(
    id_: int = typer.Argument(metavar="id", default=...),
    output_file: Optional[Path] = typer.Option(
        default=None,
        writable=True,
        resolve_path=True,
        help="When a file is given, output will be written to file instead of stdout",
    ),
) -> None:
    """Show certificate."""
    certificate = get_object(get_support().certificates, id_=id_)

    print_or_write_contents(certificate.certificate, output_file)


@app.command()
@catch_api_exception
def get_ca_chain(
    id_: int = typer.Argument(metavar="id", default=...),
    output_file: Optional[Path] = typer.Option(
        default=None,
        writable=True,
        resolve_path=True,
        help="When a file is given, output will be written to file instead of stdout",
    ),
) -> None:
    """Show CA chain."""
    certificate = get_object(get_support().certificates, id_=id_)

    print_or_write_contents(certificate.ca_chain, output_file)


@app.command()
@catch_api_exception
def get_private_key(
    id_: int = typer.Argument(metavar="id", default=...),
    output_file: Path = typer.Argument(
        default=..., writable=True, dir_okay=False, resolve_path=True
    ),
) -> None:
    """Save private key to file."""
    certificate = get_object(get_support().certificates, id_=id_)

    print_or_write_contents(certificate.private_key, output_file)


@app.command()
@catch_api_exception
def create(
    certificate_file: Path = typer.Argument(
        default=..., exists=True, dir_okay=False, resolve_path=True
    ),
    private_key_file: Path = typer.Argument(
        default=..., exists=True, dir_okay=False, resolve_path=True
    ),
    ca_chain_file: Path = typer.Argument(
        default=..., exists=True, dir_okay=False, resolve_path=True
    ),
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create certificate."""
    certificate = Certificate(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    certificate.create(
        certificate=certificate_file.read_text(),
        ca_chain=ca_chain_file.read_text(),
        private_key=private_key_file.read_text(),
        cluster_id=cluster.id,
    )

    console.print(
        get_support().get_table(
            objs=[certificate],
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
    """Delete certificate."""
    delete_api_object(
        obj=get_object(get_support().certificates, id_=id_), confirm=confirm
    )
