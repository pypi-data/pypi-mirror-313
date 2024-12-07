"""MariaDB encryption keys subcommands."""

import typer

from cyberfusion.ClusterSupport.mariadb_encryption_keys import (
    MariaDBEncryptionKey,
)
from cyberfusion.CoreCli._utilities import (
    DETAILED_MESSAGE,
    catch_api_exception,
    console,
    get_object,
    get_support,
)

app = typer.Typer()


@app.command("list")
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List MariaDB encryption keys."""
    console.print(
        get_support().get_table(
            objs=get_support().mariadb_encryption_keys, detailed=detailed
        )
    )


@app.command()
@catch_api_exception
def create(
    cluster_name: str,
) -> None:
    """Create MariaDB encryption key."""
    mariadb_encryption_key = MariaDBEncryptionKey(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    mariadb_encryption_key.create(cluster_id=cluster.id)

    console.print(
        get_support().get_table(
            objs=[mariadb_encryption_key],
            detailed=True,
        )
    )
