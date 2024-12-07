"""Redis instances subcommands."""

import typer

from cyberfusion.ClusterSupport.redis_instances import (
    EvictionPolicy,
    RedisInstance,
)
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
)

app = typer.Typer()


@app.command("list")
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List Redis instances."""
    console.print(
        get_support().get_table(
            objs=get_support().redis_instances,
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get(
    name: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show Redis instance."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().redis_instances, name=name)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create(
    name: str,
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
    memory_limit: int = typer.Option(default=100, help="In MB"),
    max_databases: int = typer.Option(default=16),
    eviction_policy: EvictionPolicy = typer.Option(
        default=EvictionPolicy.VOLATILE_LRU.value
    ),
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create Redis instance."""
    redis_instance = RedisInstance(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    redis_instance.create(
        name=name,
        password=password,
        memory_limit=memory_limit,
        max_databases=max_databases,
        eviction_policy=eviction_policy,
        cluster_id=cluster.id,
    )

    console.print(
        get_support().get_table(
            objs=[redis_instance],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def update_password(
    name: str,
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
) -> None:
    """Update password."""
    redis_instance = get_object(get_support().redis_instances, name=name)

    redis_instance.password = password
    redis_instance.update()


@app.command()
@catch_api_exception
def update_memory_limit(
    name: str,
    memory_limit: int = typer.Argument(default=..., help="In MB"),
) -> None:
    """Update memory limit."""
    redis_instance = get_object(get_support().redis_instances, name=name)

    redis_instance.memory_limit = memory_limit
    redis_instance.update()


@app.command()
@catch_api_exception
def update_max_databases(
    name: str,
    max_databases: int = typer.Argument(default=...),
) -> None:
    """Update max databases."""
    redis_instance = get_object(get_support().redis_instances, name=name)

    redis_instance.max_databases = max_databases
    redis_instance.update()


@app.command()
@catch_api_exception
def update_eviction_policy(
    name: str,
    eviction_policy: EvictionPolicy = typer.Argument(default=...),
) -> None:
    """Update eviction policy."""
    redis_instance = get_object(get_support().redis_instances, name=name)

    redis_instance.eviction_policy = eviction_policy
    redis_instance.update()


@app.command()
@catch_api_exception
def delete(
    name: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete Redis instance."""
    redis_instance = get_object(get_support().redis_instances, name=name)

    delete_api_object(obj=redis_instance, confirm=confirm)
