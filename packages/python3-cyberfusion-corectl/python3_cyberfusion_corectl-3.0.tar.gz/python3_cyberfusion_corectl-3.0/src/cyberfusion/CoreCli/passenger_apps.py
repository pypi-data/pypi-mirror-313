"""Passenger apps subcommands."""

import os
from typing import Dict, List, Optional

import typer

from cyberfusion.ClusterSupport.passenger_apps import (
    PassengerApp,
    PassengerEnvironment,
)
from cyberfusion.CoreCli._utilities import (
    BOOL_MESSAGE,
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    EMPTY_TO_CLEAR_MESSAGE,
    apply_environment_variable,
    catch_api_exception,
    confirm_clear,
    console,
    delete_api_object,
    exit_with_status,
    get_object,
    get_support,
    handle_manual_error,
    print_warning,
    wait_for_task,
)

app = typer.Typer()


@app.command("list")
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List Passenger apps."""
    console.print(
        get_support().get_table(
            objs=get_support().passenger_apps,
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get(
    name: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show Passenger app."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().passenger_apps, name=name)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create_nodejs(
    name: str,
    nodejs_version: str,
    startup_file: str,
    environment: PassengerEnvironment = PassengerEnvironment.PRODUCTION.value,
    environment_variables_arg: Optional[List[str]] = typer.Option(
        None,
        "--environment-variable",
        help="Can be used multiple times. Use key=value pairs",
    ),
    max_pool_size: int = 5,
    max_requests: int = 1000,
    pool_idle_time: int = 10,
    cpu_limit: Optional[int] = None,
    namespaced: bool = typer.Option(False, "--namespaced/--not-namespaced"),
    app_root: Optional[str] = typer.Option(
        default=None, help="Default is UNIX user home directory + name"
    ),
    unix_user_username: str = typer.Argument(default=...),
) -> None:
    """Create NodeJS Passenger app."""
    passenger_app = PassengerApp(get_support())

    environment_variables: Dict[str, str] = {}

    if environment_variables_arg:
        for var in environment_variables_arg:
            apply_environment_variable(environment_variables, var)

    unix_user = get_object(get_support().unix_users, username=unix_user_username)

    if not app_root:
        app_root = os.path.join(unix_user.home_directory, name)

    passenger_app.create_nodejs(
        name=name,
        unix_user_id=unix_user.id,
        environment=environment,
        environment_variables=environment_variables,
        max_pool_size=max_pool_size,
        max_requests=max_requests,
        pool_idle_time=pool_idle_time,
        cpu_limit=cpu_limit,
        is_namespaced=namespaced,
        app_root=app_root,
        nodejs_version=nodejs_version,
        startup_file=startup_file,
    )

    console.print(
        get_support().get_table(
            objs=[passenger_app],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def update_environment_variables(name: str, environment_variables: List[str]) -> None:
    """Update environment variables."""
    passenger_app = get_object(get_support().passenger_apps, name=name)

    for var in environment_variables:
        apply_environment_variable(passenger_app.environment_variables, var)

    passenger_app.update()


@app.command()
@catch_api_exception
@exit_with_status
def delete_environment_variables(
    name: str,
    environment_variables: List[str],
    delete_all: bool = typer.Option(False, "--delete-all/--delete-provided"),
    confirm: bool = typer.Option(
        default=False, help="Skip confirmation prompt for delete-all"
    ),
) -> int:
    """Delete environment variables."""
    passenger_app = get_object(get_support().passenger_apps, name=name)

    exit_code = 0

    if delete_all:
        if not confirm:
            typer.confirm(
                "Are you sure you want to delete all environment variables?",
                abort=True,
            )

        passenger_app.environment_variables = {}
    else:
        if not environment_variables:
            handle_manual_error(
                "Use at least 1 environment variable or use --delete-all"
            )

        for var in environment_variables:
            try:
                del passenger_app.environment_variables[var]
            except KeyError:
                print_warning(f"Environment variable '{var}' does not exist, skipping.")
                exit_code = 64

    passenger_app.update()

    return exit_code


@app.command()
@catch_api_exception
def update_max_pool_size(name: str, max_pool_size: int) -> None:
    """Update max pool size."""
    passenger_app = get_object(get_support().passenger_apps, name=name)

    passenger_app.max_pool_size = max_pool_size
    passenger_app.update()


@app.command()
@catch_api_exception
def update_max_requests(name: str, max_requests: int) -> None:
    """Update max requests."""
    passenger_app = get_object(get_support().passenger_apps, name=name)

    passenger_app.max_requests = max_requests
    passenger_app.update()


@app.command()
@catch_api_exception
def update_pool_idle_time(name: str, pool_idle_time: int) -> None:
    """Update pool idle time."""
    passenger_app = get_object(get_support().passenger_apps, name=name)

    passenger_app.pool_idle_time = pool_idle_time
    passenger_app.update()


@app.command()
@catch_api_exception
def update_nodejs_version(name: str, nodejs_version: str) -> None:
    """Update NodeJS version."""
    passenger_app = get_object(get_support().passenger_apps, name=name)

    passenger_app.nodejs_version = nodejs_version
    passenger_app.update()


@app.command()
@catch_api_exception
def update_startup_file(name: str, startup_file: str) -> None:
    """Update startup file."""
    passenger_app = get_object(get_support().passenger_apps, name=name)

    passenger_app.startup_file = startup_file
    passenger_app.update()


@app.command()
@confirm_clear
@catch_api_exception
def update_cpu_limit(
    name: str,
    cpu_limit: Optional[int] = typer.Argument(
        default=None, help=EMPTY_TO_CLEAR_MESSAGE
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update CPU limit."""
    passenger_app = get_object(get_support().passenger_apps, name=name)

    passenger_app.cpu_limit = cpu_limit
    passenger_app.update()


@app.command()
@catch_api_exception
def update_environment(name: str, environment: PassengerEnvironment) -> None:
    """Update environment."""
    passenger_app = get_object(get_support().passenger_apps, name=name)

    passenger_app.environment = environment
    passenger_app.update()


@app.command()
@catch_api_exception
def update_namespaced(
    name: str, state: bool = typer.Argument(default=..., help=BOOL_MESSAGE)
) -> None:
    """Update is namespaced."""
    passenger_app = get_object(get_support().passenger_apps, name=name)

    passenger_app.is_namespaced = state
    passenger_app.update()


@app.command()
@catch_api_exception
def restart(name: str) -> None:
    """Restart Passenger app."""
    passenger_app = get_object(get_support().passenger_apps, name=name)

    task_collection = passenger_app.restart()

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
    """Delete Passenger app.."""
    passenger_app = get_object(get_support().passenger_apps, name=name)

    delete_api_object(obj=passenger_app, confirm=confirm)
