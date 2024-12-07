"""FPM pools subcommands."""

from typing import Optional

import typer

from cyberfusion.ClusterSupport.fpm_pools import FPMPool
from cyberfusion.Common import generate_random_string
from cyberfusion.CoreCli._utilities import (
    BOOL_MESSAGE,
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    EMPTY_TO_CLEAR_MESSAGE,
    catch_api_exception,
    confirm_clear,
    console,
    delete_api_object,
    get_object,
    get_support,
    wait_for_task,
)

app = typer.Typer()


@app.command("list")
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List FPM pools."""
    console.print(
        get_support().get_table(
            objs=get_support().fpm_pools,
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get(
    name: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show FPM pool."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().fpm_pools, name=name)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create(
    name: str,
    version: str,
    max_children: int,
    max_requests: int = 1000,
    process_idle_timeout: int = 10,
    cpu_limit: Optional[int] = None,
    log_slow_requests_threshold: Optional[int] = None,
    namespaced: bool = typer.Option(False, "--namespaced/--not-namespaced"),
    unix_user_username: str = typer.Argument(default=...),
) -> None:
    """Create FPM pool."""
    fpm_pool = FPMPool(get_support())

    fpm_pool.create(
        name=name,
        unix_user_id=get_object(
            get_support().unix_users, username=unix_user_username
        ).id,
        version=version,
        max_children=max_children,
        max_requests=max_requests,
        process_idle_timeout=process_idle_timeout,
        cpu_limit=cpu_limit,
        log_slow_requests_threshold=log_slow_requests_threshold,
        is_namespaced=namespaced,
    )

    console.print(
        get_support().get_table(
            objs=[fpm_pool],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def update_version(name: str, version: str) -> None:
    """Update version.

    The version of an FPM pool is not changeable. Therefore, this creates a new
    FPM pool, with another ID.
    """

    # Get current FPM pool. We'll use its attributes and delete it afterwards.

    current_fpm_pool = get_object(get_support().fpm_pools, name=name)

    # Set name for new FPM pool. If the name currently ends with the PHP version
    # without a dot, replace it with the new PHP version. Otherwise, add a random
    # string to the end as the name is unique

    current_fpm_pool_version_without_dot = "".join(current_fpm_pool.version.split("."))
    new_fpm_pool_version_without_dot = "".join(version.split("."))

    if current_fpm_pool.name.endswith(current_fpm_pool_version_without_dot):
        new_fpm_pool_name = current_fpm_pool.name.replace(
            current_fpm_pool_version_without_dot,
            new_fpm_pool_version_without_dot,
        )
    else:
        new_fpm_pool_name = (
            f"{current_fpm_pool.name}-{generate_random_string(6).lower()}"
        )

    # Create new FPM pool with the attributes of the old one, but the updated
    # version

    new_fpm_pool = FPMPool(get_support())

    new_fpm_pool.create(
        name=new_fpm_pool_name,
        unix_user_id=current_fpm_pool.unix_user_id,
        version=version,
        max_children=current_fpm_pool.max_children,
        max_requests=current_fpm_pool.max_requests,
        process_idle_timeout=current_fpm_pool.process_idle_timeout,
        cpu_limit=current_fpm_pool.cpu_limit,
        log_slow_requests_threshold=current_fpm_pool.log_slow_requests_threshold,
        is_namespaced=current_fpm_pool.is_namespaced,
    )

    console.print(
        f"Created new FPM pool with name '{new_fpm_pool_name}', PHP version {version}"
    )

    # Update all virtual hosts using the current FPM pool to use the new FPM pool
    # with the updated version

    for virtual_host in get_support().get_virtual_hosts(
        fpm_pool_id=current_fpm_pool.id, cluster_id=current_fpm_pool.cluster_id
    ):
        virtual_host.fpm_pool_id = new_fpm_pool.id
        virtual_host.update()

        console.print(
            f"Updated FPM pool for virtual host with domain '{virtual_host.domain}' from '{current_fpm_pool.name}' to '{new_fpm_pool.name}'"
        )

    # Delete the current FPM pool, as all virtual hosts are now using the new
    # FPM pool with the updated version

    current_fpm_pool.delete()

    console.print(
        f"Deleted old FPM pool with name '{current_fpm_pool.name}', PHP version {current_fpm_pool.version}"
    )


@app.command()
@catch_api_exception
def update_max_children(name: str, max_children: int) -> None:
    """Update max children."""
    fpm_pool = get_object(get_support().fpm_pools, name=name)

    fpm_pool.max_children = max_children
    fpm_pool.update()


@app.command()
@catch_api_exception
def update_max_requests(name: str, max_requests: int) -> None:
    """Update max requests."""
    fpm_pool = get_object(get_support().fpm_pools, name=name)

    fpm_pool.max_requests = max_requests
    fpm_pool.update()


@app.command()
@catch_api_exception
def update_process_idle_timeout(name: str, process_idle_timeout: int) -> None:
    """Update process idle timeout."""
    fpm_pool = get_object(get_support().fpm_pools, name=name)

    fpm_pool.process_idle_timeout = process_idle_timeout
    fpm_pool.update()


@app.command()
@confirm_clear
@catch_api_exception
def update_log_slow_requests_threshold(
    name: str,
    threshold: Optional[int] = typer.Argument(
        default=None, help=EMPTY_TO_CLEAR_MESSAGE
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update log slow requests threshold."""
    fpm_pool = get_object(get_support().fpm_pools, name=name)

    fpm_pool.log_slow_requests_threshold = threshold
    fpm_pool.update()


@app.command()
@confirm_clear
@catch_api_exception
def update_cpu_limit(
    name: str,
    limit: Optional[int] = typer.Argument(default=None, help=EMPTY_TO_CLEAR_MESSAGE),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update CPU limit."""
    fpm_pool = get_object(get_support().fpm_pools, name=name)

    fpm_pool.cpu_limit = limit
    fpm_pool.update()


@app.command()
@catch_api_exception
def update_namespaced(
    name: str, state: bool = typer.Argument(default=..., help=BOOL_MESSAGE)
) -> None:
    """Update is namespaced."""
    fpm_pool = get_object(get_support().fpm_pools, name=name)

    fpm_pool.is_namespaced = state
    fpm_pool.update()


@app.command()
@catch_api_exception
def restart(name: str) -> None:
    """Restart FPM pool."""
    fpm_pool = get_object(get_support().fpm_pools, name=name)

    task_collection = fpm_pool.restart()

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command()
@catch_api_exception
def reload(name: str) -> None:
    """Reload FPM pool."""
    fpm_pool = get_object(get_support().fpm_pools, name=name)

    task_collection = fpm_pool.reload()

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command()
@catch_api_exception
def delete(
    name: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete FPM pool."""
    fpm_pool = get_object(get_support().fpm_pools, name=name)

    delete_api_object(obj=fpm_pool, confirm=confirm)
