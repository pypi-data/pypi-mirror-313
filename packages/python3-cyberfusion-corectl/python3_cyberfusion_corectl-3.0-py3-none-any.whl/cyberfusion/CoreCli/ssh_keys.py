"""SSH keys subcommands."""

from pathlib import Path
from typing import Optional

import typer

from cyberfusion.ClusterSupport.root_ssh_keys import RootSSHKey
from cyberfusion.ClusterSupport.ssh_keys import SSHKey
from cyberfusion.CoreCli._utilities import (
    CONFIRM_MESSAGE,
    catch_api_exception,
    console,
    delete_api_object,
    get_object,
    get_support,
    handle_manual_error,
    print_or_write_contents,
)

app = typer.Typer()

HELP_PANEL_SSH_KEYS = "SSH Keys"
HELP_PANEL_ROOT_SSH_KEYS = "Root SSH Keys"


@app.command("list", rich_help_panel=HELP_PANEL_SSH_KEYS)
@catch_api_exception
def list_() -> None:
    """List SSH keys."""
    console.print(get_support().get_table(objs=get_support().ssh_keys))


@app.command(rich_help_panel=HELP_PANEL_ROOT_SSH_KEYS)
@catch_api_exception
def list_root() -> None:
    """List SSH keys for root."""
    console.print(
        get_support().get_table(
            objs=get_support().root_ssh_keys,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_SSH_KEYS)
@catch_api_exception
def get_public_key(
    name: str,
    output_file: Optional[Path] = typer.Option(
        default=None,
        writable=True,
        resolve_path=True,
        help="When a file is given, output will be written to file instead of stdout",
    ),
) -> None:
    """Show public key."""
    public_key = get_object(get_support().ssh_keys, name=name).public_key

    if not public_key:
        handle_manual_error("This SSH key does not have a public key")

    print_or_write_contents(public_key, output_file)


@app.command(rich_help_panel=HELP_PANEL_ROOT_SSH_KEYS)
@catch_api_exception
def get_root_public_key(
    name: str,
    output_file: Optional[Path] = typer.Option(
        default=None,
        writable=True,
        resolve_path=True,
        help="When a file is given, output will be written to file instead of stdout",
    ),
) -> None:
    """Show public key for root."""
    public_key = get_object(get_support().root_ssh_keys, name=name).public_key

    if not public_key:
        handle_manual_error("This SSH key does not have a public key")

    print_or_write_contents(public_key, output_file)


@app.command(rich_help_panel=HELP_PANEL_SSH_KEYS)
@catch_api_exception
def get_private_key(
    name: str,
    output_file: Path = typer.Argument(
        default=..., writable=True, dir_okay=False, resolve_path=True
    ),
) -> None:
    """Save private key to file."""
    private_key = get_object(get_support().ssh_keys, name=name).private_key

    if not private_key:
        handle_manual_error("This SSH key does not have a private key")

    print_or_write_contents(private_key, output_file)


@app.command(rich_help_panel=HELP_PANEL_ROOT_SSH_KEYS)
@catch_api_exception
def get_root_private_key(
    name: str,
    output_file: Path = typer.Argument(
        default=..., writable=True, dir_okay=False, resolve_path=True
    ),
) -> None:
    """Save private key for root to file."""
    private_key = get_object(get_support().root_ssh_keys, name=name).private_key

    if not private_key:
        handle_manual_error("This SSH key does not have a private key")

    print_or_write_contents(private_key, output_file)


@app.command(rich_help_panel=HELP_PANEL_SSH_KEYS)
@catch_api_exception
def create_public_key(
    name: str,
    public_key_file: Path = typer.Argument(
        default=..., exists=True, dir_okay=False, resolve_path=True
    ),
    unix_user_username: str = typer.Argument(default=...),
) -> None:
    """Create public key."""
    unix_user_id = get_object(get_support().unix_users, username=unix_user_username).id

    ssh_key = SSHKey(get_support())

    ssh_key.create_public(
        name=name,
        public_key=public_key_file.read_text(),
        unix_user_id=unix_user_id,
    )

    console.print(
        get_support().get_table(
            objs=[ssh_key],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_ROOT_SSH_KEYS)
@catch_api_exception
def create_root_public_key(
    name: str,
    public_key_file: Path = typer.Argument(
        default=..., exists=True, dir_okay=False, resolve_path=True
    ),
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create public key for root."""
    root_ssh_key = RootSSHKey(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    root_ssh_key.create_public(
        name=name,
        public_key=public_key_file.read_text(),
        cluster_id=cluster.id,
    )

    console.print(
        get_support().get_table(
            objs=[root_ssh_key],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_SSH_KEYS)
@catch_api_exception
def create_private_key(
    name: str,
    private_key_file: Path = typer.Argument(
        default=..., exists=True, dir_okay=False, resolve_path=True
    ),
    unix_user_username: str = typer.Argument(default=...),
) -> None:
    """Create private key."""
    unix_user_id = get_object(get_support().unix_users, username=unix_user_username).id

    ssh_key = SSHKey(get_support())

    ssh_key.create_private(
        name=name,
        private_key=private_key_file.read_text(),
        unix_user_id=unix_user_id,
    )

    console.print(
        get_support().get_table(
            objs=[ssh_key],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_ROOT_SSH_KEYS)
@catch_api_exception
def create_root_private_key(
    name: str,
    private_key_file: Path = typer.Argument(
        default=..., exists=True, dir_okay=False, resolve_path=True
    ),
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create private key for root."""
    root_ssh_key = RootSSHKey(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    root_ssh_key.create_private(
        name=name,
        private_key=private_key_file.read_text(),
        cluster_id=cluster.id,
    )

    console.print(
        get_support().get_table(
            objs=[root_ssh_key],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_SSH_KEYS)
@catch_api_exception
def delete(
    name: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete SSH key."""
    delete_api_object(
        obj=get_object(get_support().ssh_keys, name=name), confirm=confirm
    )


@app.command(rich_help_panel=HELP_PANEL_ROOT_SSH_KEYS)
@catch_api_exception
def delete_root(
    name: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete SSH key for root."""
    delete_api_object(
        obj=get_object(get_support().root_ssh_keys, name=name), confirm=confirm
    )
