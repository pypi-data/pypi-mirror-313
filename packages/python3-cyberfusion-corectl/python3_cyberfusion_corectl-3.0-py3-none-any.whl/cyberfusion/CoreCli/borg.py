"""Borg subcommands."""

import os
import webbrowser
from http import HTTPStatus
from typing import Optional

import typer

from cyberfusion.ClusterApiCli import ClusterApiCallException
from cyberfusion.ClusterSupport.borg_archives import BorgArchive
from cyberfusion.ClusterSupport.borg_repositories import BorgRepository
from cyberfusion.ClusterSupport.clusters import Cluster, ClusterGroup
from cyberfusion.ClusterSupport.nodes import Node
from cyberfusion.ClusterSupport.ssh_keys import SSHKey
from cyberfusion.ClusterSupport.unix_users import ShellPath, UNIXUser
from cyberfusion.Common import generate_random_string
from cyberfusion.CoreCli._utilities import (
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    RANDOM_PASSWORD_MESSAGE,
    catch_api_exception,
    console,
    delete_api_object,
    get_object,
    get_support,
    handle_api_error,
    handle_manual_error,
    wait_for_task,
)

_imported_cryptography = True

try:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
except ImportError:
    _imported_cryptography = False

app = typer.Typer()

CHARACTER_AT = "@"

HELP_PANEL_BORG_REPOSITORIES = "Borg Repositories"
HELP_PANEL_BORG_ARCHIVES = "Borg Archives"


@app.command(rich_help_panel=HELP_PANEL_BORG_REPOSITORIES)
@catch_api_exception
def list_repositories(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """List Borg repositories."""
    console.print(
        get_support().get_table(
            objs=get_support().borg_repositories,
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_BORG_REPOSITORIES)
@catch_api_exception
def get_repository(
    name: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show Borg repository."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().borg_repositories, name=name)],
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_BORG_ARCHIVES)
@catch_api_exception
def list_archives(borg_repository_name: str) -> None:
    """List Borg archives."""
    borg_repository = get_object(
        get_support().borg_repositories, name=borg_repository_name
    )

    console.print("Fetching archives. This may take up to several minutes.")
    console.print(
        get_support().get_table(
            objs=get_support().get_borg_archives(borg_repository_id=borg_repository.id),
        )
    )


@app.command(rich_help_panel=HELP_PANEL_BORG_ARCHIVES)
@catch_api_exception
def get_archive(
    name: str,
) -> None:
    """Show Borg archive."""
    console.print("Fetching archive. This may take up to several minutes.")
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().borg_archives, name=name)]
        )
    )


@app.command(rich_help_panel=HELP_PANEL_BORG_ARCHIVES)
@catch_api_exception
def list_archive_contents(name: str, path: Optional[str] = None) -> None:
    """List Borg archive contents."""
    borg_archive = get_object(get_support().borg_archives, name=name)

    console.print("Fetching archive contents. This may take up to several minutes.")
    console.print(
        get_support().get_table(
            objs=get_support().borg_archive_contents(
                borg_archive_id=borg_archive.id, path=path
            )
        )
    )


@app.command(rich_help_panel=HELP_PANEL_BORG_REPOSITORIES)
@catch_api_exception
def create_unix_user_repository(
    name: str,
    borg_client_unix_user_username: str = typer.Option(
        default=..., prompt="UNIX user to back up"
    ),
    keep_hourly: int = typer.Option(default=1, prompt=True),
    keep_daily: int = typer.Option(default=1, prompt=True),
    keep_weekly: int = typer.Option(default=1, prompt=True),
    keep_monthly: int = typer.Option(default=1, prompt=True),
    keep_yearly: int = typer.Option(default=1, prompt=True),
    passphrase: str = typer.Option(
        default=generate_random_string,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
        prompt=True,
    ),
    borg_server_cluster_name: Optional[str] = typer.Option(
        "",
        "--borg-server-cluster",
        help="Use '@' to auto-detect",
        prompt="Borg server cluster (leave empty to auto-detect)",
    ),
    borg_server_node_hostname: Optional[str] = typer.Option(
        "",
        "--borg-server-node",
        help="Use '@' to auto-detect",
        prompt="Borg server node (leave empty to auto-detect)",
    ),
    borg_server_unix_user_username: Optional[str] = typer.Option(
        "",
        "--borg-server-unix-user",
        show_default=False,
        help="UNIX user on the Borg server. Will be created if given user does not exist.",
        prompt="Borg server UNIX user (will be created if left empty or if given user does not exist)",
    ),
    borg_client_ssh_key_name: Optional[str] = typer.Option(
        "",
        "--borg-client-ssh-key",
        help="SSH private key with access to Borg server UNIX user. Will be created if given key does not exist.",
        prompt="Borg client SSH private key (will be created if left empty or if given key does not exist)",
    ),
    add_public_key: bool = typer.Option(
        True,
        "--add-public-key/--dont-add-public-key",
        help="Get public key from private key and add to Borg server.",
        prompt="Add public key to Borg server?",
    ),
) -> None:
    """Create UNIX user Borg repository.

    When not passing all the options, the command will work interactively
    """
    if not _imported_cryptography:
        handle_manual_error(
            "CLI is missing dependencies for Borg. See README for how to install them."
        )

    # Make sure repository does not already exist

    if get_support().get_borg_repositories(name=name):
        handle_manual_error(
            "This Borg repository already exists. Delete or update the existing object"
        )

    borg_client_unix_user = get_object(
        get_support().unix_users, username=borg_client_unix_user_username
    )
    borg_client_cluster = get_object(
        get_support().clusters, id_=borg_client_unix_user.cluster_id
    )

    # Get Borg server cluster

    borg_server_cluster = get_borg_server_cluster(name=borg_server_cluster_name)

    # Get Borg server node

    borg_server_node = get_borg_server_node(
        hostname=borg_server_node_hostname,
        borg_server_cluster_id=borg_server_cluster.id,
    )

    # Get or create UNIX user

    if not borg_server_unix_user_username:
        borg_server_unix_user_username = name

    borg_server_unix_user = get_or_create_borg_server_unix_user(
        username=borg_server_unix_user_username,
        borg_server_cluster=borg_server_cluster,
    )

    # Get or create SSH private key

    borg_client_ssh_key = get_or_create_borg_client_ssh_private_key(
        name=borg_client_ssh_key_name,
        borg_client_unix_user=borg_client_unix_user,
        borg_server_unix_user=borg_server_unix_user,
    )

    # Create SSH public key

    if add_public_key:
        borg_server_ssh_key_name = f"{borg_server_unix_user.username}-borg-client-{borg_client_cluster.id}-{borg_client_unix_user.username}"
        borg_server_ssh_public_key = get_public_key_from_private_key(
            private_key=borg_client_ssh_key.private_key
        )

        get_or_create_borg_server_ssh_public_key(
            name=borg_server_ssh_key_name,
            borg_server_unix_user_id=borg_server_unix_user.id,
            borg_server_cluster_id=borg_server_cluster.id,
            public_key=borg_server_ssh_public_key,
        )

    create_repository(
        name=name,
        passphrase=passphrase,
        keep_hourly=keep_hourly,
        keep_daily=keep_daily,
        keep_weekly=keep_weekly,
        keep_monthly=keep_monthly,
        keep_yearly=keep_yearly,
        borg_client_cluster_id=borg_client_cluster.id,
        borg_client_ssh_key=borg_client_ssh_key,
        borg_client_unix_user_id=borg_client_unix_user.id,
        borg_server_cluster_id=borg_server_cluster.id,
        borg_server_node_hostname=borg_server_node.hostname,
        borg_server_unix_user=borg_server_unix_user,
    )


@app.command(rich_help_panel=HELP_PANEL_BORG_REPOSITORIES)
@catch_api_exception
def create_database_repository(
    name: str,
    keep_hourly: int = typer.Option(default=1, prompt=True),
    keep_daily: int = typer.Option(default=1, prompt=True),
    keep_weekly: int = typer.Option(default=1, prompt=True),
    keep_monthly: int = typer.Option(default=1, prompt=True),
    keep_yearly: int = typer.Option(default=1, prompt=True),
    passphrase: str = typer.Option(
        default=generate_random_string,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
        prompt=True,
    ),
    borg_client_cluster_name: Optional[str] = typer.Option(
        "", "--borg-client-cluster", prompt="Borg client cluster"
    ),
    borg_server_cluster_name: Optional[str] = typer.Option(
        "",
        "--borg-server-cluster",
        help="Use '@' to auto-detect",
        prompt="Borg server cluster (leave empty to auto-detect)",
    ),
    borg_server_node_name: Optional[str] = typer.Option(
        "",
        "--borg-server-node",
        help="Use '@' to auto-detect",
        prompt="Borg server node (leave empty to auto-detect)",
    ),
    borg_server_unix_user_username: Optional[str] = typer.Option(
        "",
        "--borg-server-unix-user",
        show_default=False,
        help="UNIX user on the Borg server. Will be created if given user does not exist.",
        prompt="Borg server UNIX user (will be created if left empty or if given user does not exist)",
    ),
    add_public_key: bool = typer.Option(
        True,
        "--add-public-key/--dont-add-public-key",
        prompt="Add public key to Borg server?",
        help="Get Borg client public key and add to Borg server.",
    ),
) -> None:
    """Create database Borg repository."""

    # Make sure Borg repository does not exist

    if get_support().get_borg_repositories(name=name):
        handle_manual_error(
            "This Borg repository already exists. Delete or update the existing object"
        )

    borg_client_cluster = get_object(
        get_support().clusters, name=borg_client_cluster_name
    )

    # Get Borg server cluster

    borg_server_cluster = get_borg_server_cluster(name=borg_server_cluster_name)

    # Get Borg server node

    borg_server_node = get_borg_server_node(
        hostname=borg_server_node_name,
        borg_server_cluster_id=borg_server_cluster.id,
    )

    # Get or create UNIX user

    if not borg_server_unix_user_username:
        borg_server_unix_user_username = name

    borg_server_unix_user = get_or_create_borg_server_unix_user(
        username=borg_server_unix_user_username,
        borg_server_cluster=borg_server_cluster,
    )

    # Create SSH public key

    if add_public_key:
        borg_server_ssh_key_name = (
            f"{borg_server_unix_user.username}-borg-client-{borg_client_cluster.id}"
        )
        borg_server_ssh_public_key = (
            borg_client_cluster.get_borg_public_ssh_key() + "\n"
        )

        get_or_create_borg_server_ssh_public_key(
            name=borg_server_ssh_key_name,
            borg_server_unix_user_id=borg_server_unix_user.id,
            borg_server_cluster_id=borg_server_cluster.id,
            public_key=borg_server_ssh_public_key,
        )

    create_repository(
        name=name,
        passphrase=passphrase,
        keep_hourly=keep_hourly,
        keep_daily=keep_daily,
        keep_weekly=keep_weekly,
        keep_monthly=keep_monthly,
        keep_yearly=keep_yearly,
        borg_client_cluster_id=borg_client_cluster.id,
        borg_client_ssh_key=None,
        borg_client_unix_user_id=None,
        borg_server_cluster_id=borg_server_cluster.id,
        borg_server_node_hostname=borg_server_node.hostname,
        borg_server_unix_user=borg_server_unix_user,
    )


def get_borg_server_cluster(
    name: Optional[str],
) -> Cluster:
    """Get Borg server cluster."""

    # If name is '@', the cluster should be automatically chosen

    if name and name != CHARACTER_AT:
        return get_object(get_support().clusters, name=name)

    borg_server_cluster: Optional[Cluster] = None

    for cluster in get_support().clusters:
        if ClusterGroup.BORG_SERVER not in cluster.groups:
            continue

        if borg_server_cluster is not None:
            handle_manual_error(
                "Multiple Borg server clusters found. Specify one with --borg-server-cluster"
            )

        borg_server_cluster = cluster

    if not borg_server_cluster:
        handle_manual_error(
            "Could not find Borg server cluster. Specify one with --borg-server-cluster"
        )

    return borg_server_cluster


def get_borg_server_node(hostname: Optional[str], borg_server_cluster_id: int) -> Node:
    """Get Borg server node."""

    # If name is '@', the cluster should be automatically chosen

    if hostname and hostname != CHARACTER_AT:
        return get_object(
            get_support().nodes,
            hostname=hostname,
            cluster_id=borg_server_cluster_id,
        )

    borg_nodes = get_support().get_nodes(cluster_id=borg_server_cluster_id)

    if len(borg_nodes) != 1:
        handle_manual_error(
            "Multiple nodes found on Borg server cluster. Specify one with --borg-server-node"
        )

    return borg_nodes[0]


def get_or_create_borg_server_unix_user(
    *, username: str, borg_server_cluster: Cluster
) -> UNIXUser:
    """Get or create UNIX user for Borg server."""

    # Use existing UNIX user if possible

    unix_users = get_support().get_unix_users(
        username=username, cluster_id=borg_server_cluster.id
    )

    if unix_users:
        console.print(f"Using existing Borg server UNIX user: {unix_users[0].username}")

        return unix_users[0]

    unix_user = UNIXUser(get_support())

    try:
        unix_user.create(
            username=username,
            password=generate_random_string(),
            shell_path=ShellPath.BASH,
            record_usage_files=False,
            default_php_version=None,
            default_nodejs_version=None,
            virtual_hosts_directory=None,
            mail_domains_directory=None,
            borg_repositories_directory=os.path.join(
                borg_server_cluster.unix_users_home_directory, username
            ),
            description=None,
            cluster_id=borg_server_cluster.id,
        )
    except ClusterApiCallException as e:
        if e.status_code == HTTPStatus.CONFLICT:
            handle_manual_error(
                f"UNIX user with name {username} already exists. Delete or specify it."
            )
        else:
            handle_api_error(e)

    console.print(f"Borg server UNIX user created: {username}")

    return unix_user


def get_or_create_borg_client_ssh_private_key(
    *,
    name: Optional[str],
    borg_client_unix_user: UNIXUser,
    borg_server_unix_user: UNIXUser,
) -> SSHKey:
    """Get or create SSH private key for Borg client."""
    private_key = (
        rsa.generate_private_key(public_exponent=65537, key_size=4096)
        .private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        .decode()
    )

    if not name:
        name = f"{borg_client_unix_user.cluster_id}-{borg_client_unix_user.username}-borg-server-{borg_server_unix_user.username}"

    try:
        ssh_keys = get_support().get_ssh_keys(
            name=name, cluster_id=borg_client_unix_user.cluster_id
        )

        if ssh_keys:
            console.print(
                f"Using existing Borg client SSH private key: {ssh_keys[0].name}"
            )
            return ssh_keys[0]

        ssh_key = SSHKey(get_support())

        ssh_key.create_private(
            name=name,
            private_key=private_key,
            unix_user_id=borg_client_unix_user.id,
        )
    except ClusterApiCallException as e:
        if e.status_code == HTTPStatus.CONFLICT:
            handle_manual_error(
                f"Borg client SSH key with name {name} already exists. Delete or specify it."
            )
        else:
            handle_api_error(e)

    console.print(f"Borg client SSH private key created: {ssh_key.name}")

    return ssh_key


def get_or_create_borg_server_ssh_public_key(
    *,
    name: str,
    borg_server_unix_user_id: int,
    borg_server_cluster_id: int,
    public_key: str,
) -> SSHKey:
    """Get or create SSH public key for Borg server."""
    ssh_keys = get_support().get_ssh_keys(name=name, cluster_id=borg_server_cluster_id)

    if ssh_keys:
        if (
            ssh_keys[0].public_key == public_key
            and ssh_keys[0].unix_user_id == borg_server_unix_user_id
        ):
            console.print(
                f"Using existing Borg server SSH public key: {ssh_keys[0].name}"
            )

            return ssh_keys[0]
        else:
            handle_manual_error(
                f"SSH key with name '{name}' already exists, but can't be used. Delete it or skip adding public key"
            )

    ssh_key = SSHKey(get_support())
    ssh_key.create_public(
        name=name, public_key=public_key, unix_user_id=borg_server_unix_user_id
    )

    console.print(f"Borg server SSH public key created: {ssh_key.name}")

    return ssh_key


def get_public_key_from_private_key(
    *,
    private_key: str,
) -> str:
    """Get SSH public key from private key."""
    public_key = (
        serialization.load_pem_private_key(data=private_key.encode(), password=None)
        .public_key()
        .public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH,
        )
    )

    return public_key.decode() + "\n"


def create_repository(
    *,
    name: str,
    passphrase: str,
    keep_hourly: Optional[int],
    keep_daily: Optional[int],
    keep_weekly: Optional[int],
    keep_monthly: Optional[int],
    keep_yearly: Optional[int],
    borg_client_cluster_id: int,
    borg_client_unix_user_id: Optional[int],
    borg_client_ssh_key: Optional[SSHKey],
    borg_server_cluster_id: int,
    borg_server_node_hostname: str,
    borg_server_unix_user: UNIXUser,
) -> BorgRepository:
    """Create Borg repository."""
    identity_file_path = None

    if borg_client_ssh_key:
        if not borg_client_ssh_key.private_key:
            handle_manual_error(
                f"SSH key '{borg_client_ssh_key.name}' is not a private key."
            )

        identity_file_path = borg_client_ssh_key.identity_file_path

    remote_path = os.path.join(borg_server_unix_user.borg_repositories_directory, name)

    # Make sure keep_* is not 0

    if not keep_hourly:
        keep_hourly = None

    if not keep_daily:
        keep_daily = None

    if not keep_weekly:
        keep_weekly = None

    if not keep_monthly:
        keep_monthly = None

    if not keep_yearly:
        keep_yearly = None

    borg_repository = BorgRepository(get_support())

    borg_repository.create(
        name=name,
        passphrase=passphrase,
        keep_hourly=keep_hourly,
        keep_daily=keep_daily,
        keep_weekly=keep_weekly,
        keep_monthly=keep_monthly,
        keep_yearly=keep_yearly,
        remote_host=borg_server_node_hostname,
        remote_path=remote_path,
        remote_username=borg_server_unix_user.username,
        identity_file_path=identity_file_path,
        unix_user_id=borg_client_unix_user_id,
        cluster_id=borg_client_cluster_id,
    )

    console.print(
        get_support().get_table(
            objs=[borg_repository],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_BORG_ARCHIVES)
@catch_api_exception
def create_unix_user_archive(name: str, borg_repository_name: str) -> None:
    """Create Borg archive for UNIX user."""
    borg_archive = BorgArchive(get_support())
    borg_repository = get_object(
        get_support().borg_repositories, name=borg_repository_name
    )

    if not borg_repository.unix_user_id:
        handle_manual_error(
            "Trying to create UNIX user archive, but specified Borg repository does not belong to UNIX user. Specify Borg repository that belongs to UNIX user"
        )

    task_collection = borg_archive.create_unix_user(
        name=name,
        borg_repository_id=borg_repository.id,
        unix_user_id=borg_repository.unix_user_id,
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command(rich_help_panel=HELP_PANEL_BORG_ARCHIVES)
@catch_api_exception
def create_database_archive(
    name: str, borg_repository_name: str, database_name: str
) -> None:
    """Create Borg archive for database."""
    borg_archive = BorgArchive(get_support())
    borg_repository = get_object(
        get_support().borg_repositories, name=borg_repository_name
    )

    if borg_repository.unix_user_id:
        handle_manual_error(
            "Trying to create database archive, but specified Borg repository belongs to UNIX user. Specify Borg repository that does not belong to UNIX user"
        )

    task_collection = borg_archive.create_database(
        name=name,
        borg_repository_id=borg_repository.id,
        database_id=get_object(get_support().databases, name=database_name).id,
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command(rich_help_panel=HELP_PANEL_BORG_REPOSITORIES)
@catch_api_exception
def update_repository_backup_count(
    name: str,
    keep_hourly: Optional[int],
    keep_daily: Optional[int],
    keep_weekly: Optional[int],
    keep_monthly: Optional[int],
    keep_yearly: Optional[int],
) -> None:
    """Update Borg repository keep_*."""
    borg_repository = get_object(get_support().borg_repositories, name=name)

    # Make sure keep_* is not 0

    if not keep_hourly:
        keep_hourly = None

    if not keep_daily:
        keep_daily = None

    if not keep_weekly:
        keep_weekly = None

    if not keep_monthly:
        keep_monthly = None

    if not keep_yearly:
        keep_yearly = None

    borg_repository.keep_hourly = keep_hourly
    borg_repository.keep_daily = keep_daily
    borg_repository.keep_weekly = keep_weekly
    borg_repository.keep_monthly = keep_monthly
    borg_repository.keep_yearly = keep_yearly

    borg_repository.update()


@app.command(rich_help_panel=HELP_PANEL_BORG_REPOSITORIES)
@catch_api_exception
def update_repository_borg_client_ssh_key(
    name: str, borg_client_ssh_key_name: str, add_public_key: bool
) -> None:
    """Update Borg repository client SSH key.

    This command does not delete current SSH keys from the API.
    """
    if not _imported_cryptography:
        handle_manual_error(
            "CLI is missing dependencies for Borg. See README for how to install them."
        )

    borg_repository = get_object(get_support().borg_repositories, name=name)

    if borg_repository.unix_user_id is None:
        handle_manual_error("SSH key can not be updated on database repository")

    borg_client_ssh_key = get_object(
        get_support().ssh_keys, name=borg_client_ssh_key_name
    )
    borg_client_unix_user = get_object(
        get_support().unix_users, id_=borg_repository.unix_user_id
    )

    if not borg_client_ssh_key.private_key:
        handle_manual_error(
            f"SSH key '{borg_client_ssh_key.name}' does not have a private key."
        )

    borg_repository.identity_file_path = borg_client_ssh_key.identity_file_path
    borg_repository.update()

    console.print("Note: SSH keys won't get removed from the API")

    if add_public_key:
        borg_server_node = get_object(
            get_support().nodes,
            hostname=borg_repository.remote_host,
            cluster_id=None,
        )
        borg_server_unix_user = get_object(
            get_support().unix_users,
            username=borg_repository.remote_username,
        )
        borg_server_ssh_key_name = f"{borg_server_unix_user.username}-borg-client-{borg_client_unix_user.cluster_id}-{borg_client_unix_user.username}"
        borg_server_ssh_public_key = get_public_key_from_private_key(
            private_key=borg_client_ssh_key.private_key
        )

        get_or_create_borg_server_ssh_public_key(
            name=borg_server_ssh_key_name,
            borg_server_unix_user_id=borg_server_unix_user.id,
            borg_server_cluster_id=borg_server_node.cluster_id,
            public_key=borg_server_ssh_public_key,
        )


@app.command(rich_help_panel=HELP_PANEL_BORG_REPOSITORIES)
@catch_api_exception
def prune_repository(name: str) -> None:
    """Prune Borg repository."""
    borg_repository = get_object(get_support().borg_repositories, name=name)

    task_collection = borg_repository.prune()

    wait_for_task(
        task_collection_uuid=task_collection.uuid,
    )


@app.command(rich_help_panel=HELP_PANEL_BORG_REPOSITORIES)
@catch_api_exception
def check_repository(name: str) -> None:
    """Check Borg repository."""
    borg_repository = get_object(get_support().borg_repositories, name=name)

    task_collection = borg_repository.check()

    wait_for_task(
        task_collection_uuid=task_collection.uuid,
    )


@app.command(rich_help_panel=HELP_PANEL_BORG_ARCHIVES)
@catch_api_exception
def download_archive(name: str, path: str = typer.Argument(default=None)) -> None:
    """Get one-time download link."""
    borg_archive = get_object(get_support().borg_archives, name=name)

    task_collection = borg_archive.download(path=path)

    success = wait_for_task(
        task_collection_uuid=task_collection.uuid,
    )

    if not success:
        return

    url = [
        task_collection_result
        for task_collection_result in get_support().task_collection_results(
            task_collection_uuid=task_collection.uuid
        )
        if task_collection_result.description == "Create URL to get object"
    ][0].message
    webbrowser.open(url)


@app.command(rich_help_panel=HELP_PANEL_BORG_ARCHIVES)
@catch_api_exception
def restore_archive(name: str, path: str = typer.Argument(default=None)) -> None:
    """Restore Borg archive."""
    borg_archive = get_object(get_support().borg_archives, name=name)

    task_collection = borg_archive.restore(path=path)

    wait_for_task(
        task_collection_uuid=task_collection.uuid,
    )


@app.command(rich_help_panel=HELP_PANEL_BORG_REPOSITORIES)
@catch_api_exception
def delete_repository(
    name: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete Borg repository."""
    borg_repository = get_object(get_support().borg_repositories, name=name)

    delete_api_object(obj=borg_repository, confirm=confirm)
