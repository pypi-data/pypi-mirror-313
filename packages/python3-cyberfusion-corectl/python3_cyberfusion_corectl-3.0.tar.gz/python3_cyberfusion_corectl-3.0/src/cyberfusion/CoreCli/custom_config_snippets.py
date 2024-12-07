"""Custom config snippets subcommands."""

from pathlib import Path

import typer

from cyberfusion.ClusterSupport.custom_config_snippets import (
    CustomConfigSnippet,
    CustomConfigSnippetTemplateName,
)
from cyberfusion.ClusterSupport.virtual_hosts import (
    VirtualHostServerSoftwareName,
)
from cyberfusion.CoreCli._utilities import (
    BOOL_MESSAGE,
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
    """List custom config snippets."""
    console.print(
        get_support().get_table(
            objs=get_support().custom_config_snippets,
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get(
    id_: int = typer.Argument(metavar="id", default=...),
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show custom config snippet."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().custom_config_snippets, id_=id_)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get_contents(id_: int = typer.Argument(metavar="id", default=...)) -> None:
    """Show custom config snippet contents."""
    custom_config_snippet = get_object(get_support().custom_config_snippets, id_=id_)

    console.print(custom_config_snippet.contents)


@app.command()
@catch_api_exception
def create_from_file(
    name: str,
    server_software_name: VirtualHostServerSoftwareName,
    contents: Path = typer.Argument(
        default=..., exists=True, dir_okay=False, resolve_path=True
    ),
    default: bool = False,
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create custom config snippet from file."""
    custom_config_snippet = CustomConfigSnippet(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    custom_config_snippet.create(
        name=name,
        server_software_name=server_software_name,
        is_default=default,
        contents=contents.read_text(),
        cluster_id=cluster.id,
    )

    console.print(
        get_support().get_table(
            objs=[custom_config_snippet],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def create_from_template(
    name: str,
    server_software_name: VirtualHostServerSoftwareName,
    template_name: CustomConfigSnippetTemplateName,
    default: bool = False,
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create custom config snippet from template."""
    custom_config_snippet = CustomConfigSnippet(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    custom_config_snippet.create(
        name=name,
        server_software_name=server_software_name,
        is_default=default,
        template_name=template_name,
        cluster_id=cluster.id,
    )

    console.print(
        get_support().get_table(
            objs=[custom_config_snippet],
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
    """Overwrite custom config snippet using a file."""
    custom_config_snippet = get_object(get_support().custom_config_snippets, id_=id_)

    custom_config_snippet.contents = contents.read_text()
    custom_config_snippet.update()


@app.command()
@catch_api_exception
def edit(id_: int = typer.Argument(metavar="id", default=...)) -> None:
    """Edit custom config snippet using $EDITOR."""
    custom_config_snippet = get_object(get_support().custom_config_snippets, id_=id_)

    custom_config_snippet.contents = typer.edit(custom_config_snippet.contents)

    if custom_config_snippet.contents is None:
        print_warning("No changes have been made")

        return

    custom_config_snippet.update()


@app.command()
@catch_api_exception
def update_is_default(
    id_: int = typer.Argument(metavar="id", default=...),
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update is default."""
    custom_config_snippet = get_object(get_support().custom_config_snippets, id_=id_)

    custom_config_snippet.is_default = state
    custom_config_snippet.update()


@app.command()
@catch_api_exception
def delete(
    id_: int = typer.Argument(metavar="id", default=...),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete custom config snippet."""
    custom_config_snippet = get_object(get_support().custom_config_snippets, id_=id_)

    delete_api_object(obj=custom_config_snippet, confirm=confirm)
