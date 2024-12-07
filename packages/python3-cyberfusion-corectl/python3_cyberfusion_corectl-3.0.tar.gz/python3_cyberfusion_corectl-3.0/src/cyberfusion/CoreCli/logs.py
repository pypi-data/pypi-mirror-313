"""Logs subcommands."""

import time
from enum import Enum
from typing import Any, List, Optional, Union

import typer

from cyberfusion.ClusterSupport.logs import AccessLog, ErrorLog, LogMethod
from cyberfusion.CoreCli._utilities import (
    catch_api_exception,
    console,
    err_console,
    get_object,
    get_support,
    handle_manual_error,
)

app = typer.Typer()


@app.command()
@catch_api_exception
def show_access_logs(
    domain: str,
    min_before: Optional[int] = typer.Option(
        default=None, help="Show logs since n minutes ago"
    ),
    limit: int = typer.Option(default=1000, help="Limit to n lines"),
    pager: bool = True,
    status_code: Optional[int] = typer.Option(
        None, "--status-code", "-s", help="Filter by status code"
    ),
    remote_address: Optional[str] = typer.Option(
        None, "--remote-address", "-r", help="Filter by remote address"
    ),
    method: Optional[LogMethod] = typer.Option(
        None, "--method", "-m", help="Filter by HTTP method"
    ),
    uri: Optional[str] = typer.Option(None, "--uri", "-u", help="Filter by URI"),
) -> None:
    """Show access logs in pager."""
    timestamp = None

    if min_before:
        timestamp = time.time() - (min_before * 60)

    access_logs = get_support().access_logs(
        virtual_host_id=get_object(get_support().virtual_hosts, domain=domain).id,
        timestamp=timestamp,
        limit=limit,
    )

    show_logs(
        logs=access_logs,
        pager=pager,
        filters={
            "status_code": status_code,
            "remote_address": remote_address,
            "method": method,
            "uri": uri,
        },
    )


@app.command()
@catch_api_exception
def show_error_logs(
    domain: str,
    min_before: Optional[int] = typer.Option(
        default=None, help="Show logs since n minutes ago"
    ),
    limit: Optional[int] = typer.Option(default=None, help="Limit to n lines"),
    pager: bool = True,
    error_message: Optional[str] = typer.Option(
        None, "--error-message", "-M", help="Filter by error message"
    ),
    remote_address: Optional[str] = typer.Option(
        None, "--remote-address", "-r", help="Filter by remote address"
    ),
    method: Optional[LogMethod] = typer.Option(
        None, "--method", "-m", help="Filter by HTTP method"
    ),
    uri: Optional[str] = typer.Option(None, "--uri", "-u", help="Filter by URI"),
) -> None:
    """Show error logs in pager."""
    timestamp = None

    if min_before:
        timestamp = time.time() - (min_before * 60)

    error_logs = get_support().error_logs(
        virtual_host_id=get_object(get_support().virtual_hosts, domain=domain).id,
        timestamp=timestamp,
        limit=limit,
    )

    show_logs(
        logs=error_logs,
        pager=pager,
        filters={
            "error_message": error_message,
            "remote_address": remote_address,
            "method": method,
            "uri": uri,
        },
    )


@app.command()
@catch_api_exception
def watch_access_logs(
    domain: str,
    interval: float = typer.Option(default=2.0, help="Time in seconds between updates"),
    lines: int = typer.Option(default=10, help="Amount of previous lines to print"),
    status_code: Optional[int] = typer.Option(
        None, "--status-code", "-s", help="Filter by status code"
    ),
    remote_address: Optional[str] = typer.Option(
        None, "--remote-address", "-r", help="Filter by remote address"
    ),
    method: Optional[LogMethod] = typer.Option(
        None, "--method", "-m", help="Filter by HTTP method"
    ),
    uri: Optional[str] = typer.Option(None, "--uri", "-u", help="Filter by URI"),
) -> None:
    """Follow access logs."""
    follow_logs(
        virtual_host_id=get_object(get_support().virtual_hosts, domain=domain).id,
        log_type=LogTypeEnum.ACCESS_LOG,
        lines=lines,
        interval=interval,
        filters={
            "status_code": status_code,
            "remote_address": remote_address,
            "method": method,
            "uri": uri,
        },
    )


@app.command()
@catch_api_exception
def watch_error_logs(
    domain: str,
    interval: float = typer.Option(default=2.0, help="Time in seconds between updates"),
    lines: int = typer.Option(default=10, help="Amount of previous lines to print"),
    error_message: Optional[str] = typer.Option(
        None, "--error-message", "-M", help="Filter by error message"
    ),
    remote_address: Optional[str] = typer.Option(
        None, "--remote-address", "-r", help="Filter by remote address"
    ),
    method: Optional[LogMethod] = typer.Option(
        None, "--method", "-m", help="Filter by HTTP method"
    ),
    uri: Optional[str] = typer.Option(None, "--uri", "-u", help="Filter by URI"),
) -> None:
    """Follow error logs."""
    follow_logs(
        virtual_host_id=get_object(get_support().virtual_hosts, domain=domain).id,
        log_type=LogTypeEnum.ERROR_LOG,
        lines=lines,
        interval=interval,
        filters={
            "error_message": error_message,
            "remote_address": remote_address,
            "method": method,
            "uri": uri,
        },
    )


def show_logs(
    *,
    logs: Union[List[AccessLog], List[ErrorLog]],
    filters: dict[str, Any],
    pager: bool = True,
) -> None:
    """Display logs in pager."""
    if not logs:
        handle_manual_error("No logs found")

    output = "\n".join(line.raw_message for line in logs if _show_line(line, filters))

    if not pager:
        console.print(output)
        return

    with console.pager():
        console.print(output)


class LogTypeEnum(str, Enum):
    """Enum for log types."""

    ACCESS_LOG = "access_logs"
    ERROR_LOG = "error_logs"


def follow_logs(
    *,
    virtual_host_id: int,
    log_type: LogTypeEnum,
    lines: int,
    interval: float,
    filters: dict[str, Any],
) -> None:
    """Follow logs."""
    LIMIT = 1000

    first_run = True

    if log_type == LogTypeEnum.ACCESS_LOG:
        log_getter = get_support().access_logs
        last_entry = AccessLog(get_support())
    elif log_type == LogTypeEnum.ERROR_LOG:
        log_getter = get_support().error_logs
        last_entry = ErrorLog(get_support())

    while True:
        logs = log_getter(
            virtual_host_id=virtual_host_id,
            limit=LIMIT,
        )

        if not logs:
            time.sleep(interval)

            continue

        if first_run:
            # Set index to show last few lines

            index = -lines - 1
            first_run = False
        else:
            # Find previous last entry in new list

            try:
                index = [
                    idx
                    for idx, line in enumerate(logs)
                    if line.timestamp == last_entry.timestamp
                    and line.raw_message == last_entry.raw_message
                ][-1]
            except IndexError:
                # Over 'limit' logs were added since last iteration, so previous
                # entry is no longer returned by API, and is therefore no longer
                # in 'logs'. Reset index to simply output all new entries.

                index = -1

                err_console.print(
                    f"[red]Skipped some logs, as over {LIMIT} logs were added in {interval} seconds[/red]"
                )

        # Start at next entry

        for line in logs[index + 1 :]:
            if not _show_line(line, filters):
                continue

            console.print(line.raw_message)

        last_entry = logs[-1]

        time.sleep(interval)


def _show_line(line: Union[AccessLog, ErrorLog], filters: dict[str, Any]) -> bool:
    """Determine if a log line should be shown."""

    for filter_key in filters:
        # Check if the filter was provided

        if filters[filter_key] is None:
            continue

        # Ensure the line has the attribute to filter on

        if not hasattr(line, filter_key):
            return False

        # Check if the attribute matches the filter

        if getattr(line, filter_key) != filters[filter_key]:
            return False

    # If we didn't determine that something doesn't match, then we assume it matches

    return True
