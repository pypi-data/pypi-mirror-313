"""Custom configs subcommands."""

from pathlib import Path

import typer

from cyberfusion.ClusterSupport.custom_configs import CustomConfig
from cyberfusion.ClusterSupport.virtual_hosts import (
    VirtualHostServerSoftwareName,
)
from cyberfusion.CoreCli._utilities import (
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    catch_api_exception,
    console,
    delete_api_object,
    get_object,
    get_support,
    print_warning,
)

app = typer.Typer()


@app.command("list")
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List custom configs."""
    console.print(
        get_support().get_table(
            objs=get_support().custom_configs,
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get(
    id_: int = typer.Argument(metavar="id", default=...),
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show custom config."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().custom_configs, id_=id_)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get_contents(id_: int = typer.Argument(metavar="id", default=...)) -> None:
    """Show custom config contents."""
    custom_config = get_object(get_support().custom_configs, id_=id_)

    console.print(custom_config.contents)


@app.command()
@catch_api_exception
def create(
    name: str,
    server_software_name: VirtualHostServerSoftwareName,
    contents: Path = typer.Argument(
        default=..., exists=True, dir_okay=False, resolve_path=True
    ),
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create custom config."""
    custom_config = CustomConfig(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    custom_config.create(
        name=name,
        server_software_name=server_software_name,
        contents=contents.read_text(),
        cluster_id=cluster.id,
    )

    console.print(
        get_support().get_table(
            objs=[custom_config],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def update(
    id_: int = typer.Argument(metavar="id", default=...),
    contents: Path = typer.Argument(
        default=..., exists=True, dir_okay=False, resolve_path=True
    ),
) -> None:
    """Overwrite custom config using a file."""
    custom_config = get_object(get_support().custom_configs, id_=id_)

    custom_config.contents = contents.read_text()
    custom_config.update()


@app.command()
@catch_api_exception
def edit(id_: int = typer.Argument(metavar="id", default=...)) -> None:
    """Edit custom config using $EDITOR."""
    custom_config = get_object(get_support().custom_configs, id_=id_)

    custom_config.contents = typer.edit(custom_config.contents)

    if custom_config.contents is None:
        print_warning("No changes have been made")

        return

    custom_config.update()


@app.command()
@catch_api_exception
def delete(
    id_: int = typer.Argument(metavar="id", default=...),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete custom config."""
    custom_config = get_object(get_support().custom_configs, id_=id_)

    delete_api_object(obj=custom_config, confirm=confirm)
