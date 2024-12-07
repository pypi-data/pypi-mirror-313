"""Crons subcommands."""

from typing import Optional

import typer

from cyberfusion.ClusterSupport.crons import Cron
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
)

app = typer.Typer()


@app.command("list")
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List crons."""
    console.print(get_support().get_table(objs=get_support().crons, detailed=detailed))


@app.command()
@catch_api_exception
def get(
    name: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show cron."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().crons, name=name)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create(
    name: str,
    schedule: str,
    command: str = typer.Option(default=..., prompt=True),
    email_address: Optional[str] = typer.Argument(default=None),
    error_count: int = typer.Argument(default=1),
    random_delay: int = typer.Argument(default=10, metavar="SECONDS"),
    timeout: Optional[int] = typer.Argument(default=None, metavar="SECONDS"),
    locking_enabled: bool = typer.Option(True, "--locking/--no-locking"),
    active: bool = typer.Option(True, "--active/--inactive"),
    unix_user_username: str = typer.Option(default=...),
    node_hostname: Optional[str] = None,
) -> None:
    """Create cron."""
    cron = Cron(get_support())

    node_id = None

    if node_hostname:
        node_id = get_object(get_support().nodes, hostname=node_hostname).id

    cron.create(
        name=name,
        command=command,
        email_address=email_address,
        schedule=schedule,
        unix_user_id=get_object(
            get_support().unix_users, username=unix_user_username
        ).id,
        error_count=error_count,
        random_delay_max_seconds=random_delay,
        timeout_seconds=timeout,
        node_id=node_id,
        locking_enabled=locking_enabled,
        is_active=active,
    )

    console.print(
        get_support().get_table(
            objs=[cron],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def update_locking(
    name: str, state: bool = typer.Argument(default=..., help=BOOL_MESSAGE)
) -> None:
    """Update locking."""
    cron = get_object(get_support().crons, name=name)

    cron.locking_enabled = state
    cron.update()


@app.command()
@catch_api_exception
def update_active(
    name: str, state: bool = typer.Argument(default=..., help=BOOL_MESSAGE)
) -> None:
    """Update is active."""
    cron = get_object(get_support().crons, name=name)

    cron.is_active = state
    cron.update()


@app.command()
@catch_api_exception
def update_command(
    name: str, command: str = typer.Option(default=..., prompt=True)
) -> None:
    """Update command."""
    cron = get_object(get_support().crons, name=name)

    cron.command = command
    cron.update()


@app.command()
@catch_api_exception
def update_email_address(name: str, email_address: str) -> None:
    """Update email address."""
    cron = get_object(get_support().crons, name=name)

    cron.email_address = email_address
    cron.update()


@app.command()
@catch_api_exception
def update_schedule(name: str, schedule: str) -> None:
    """Update schedule."""
    cron = get_object(get_support().crons, name=name)

    cron.schedule = schedule
    cron.update()


@app.command()
@catch_api_exception
def update_error_count(name: str, error_count: int) -> None:
    """Update error count."""
    cron = get_object(get_support().crons, name=name)

    cron.error_count = error_count
    cron.update()


@app.command()
@catch_api_exception
def update_random_delay(name: str, max_seconds: int) -> None:
    """Update random delay."""
    cron = get_object(get_support().crons, name=name)

    cron.random_delay_max_seconds = max_seconds
    cron.update()


@app.command()
@confirm_clear
@catch_api_exception
def update_timeout(
    name: str,
    seconds: Optional[int] = typer.Argument(default=None, help=EMPTY_TO_CLEAR_MESSAGE),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update timeout."""
    cron = get_object(get_support().crons, name=name)

    cron.timeout_seconds = seconds
    cron.update()


@app.command()
@catch_api_exception
def delete(
    name: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete cron."""
    cron = get_object(get_support().crons, name=name)

    delete_api_object(obj=cron, confirm=confirm)
