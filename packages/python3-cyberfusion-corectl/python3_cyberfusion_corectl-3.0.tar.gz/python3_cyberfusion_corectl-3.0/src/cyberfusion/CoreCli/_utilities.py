"""Generic utilities."""

import configparser
import inspect
import json
import os
import re
import subprocess
from datetime import datetime, timedelta, timezone
from enum import Enum
from functools import lru_cache, wraps
from http import HTTPStatus
from pathlib import Path
from time import sleep
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)

import plotext
import requests
import typer
from rich.console import Console
from rich.progress import (
    Progress,
    ProgressColumn,
    SpinnerColumn,
    Task,
    TaskID,
    TimeElapsedColumn,
)
from rich.text import Text
from typer.models import ArgumentInfo, OptionInfo

from cyberfusion.ClusterApiCli import (
    METHOD_DELETE,
    METHOD_GET,
    METHOD_PATCH,
    METHOD_POST,
    METHOD_PUT,
    ClusterApiCallException,
)
from cyberfusion.ClusterSupport import ClusterSupport, TimeUnit
from cyberfusion.ClusterSupport._interfaces import APIObjectInterface
from cyberfusion.ClusterSupport.api_users_to_clusters import APIUserToCluster
from cyberfusion.ClusterSupport.cmses import CMS
from cyberfusion.ClusterSupport.databases_usages import DatabaseUsage
from cyberfusion.ClusterSupport.haproxy_listens_to_nodes import (
    HAProxyListenToNode,
)
from cyberfusion.ClusterSupport.mail_accounts_usages import MailAccountUsage
from cyberfusion.ClusterSupport.nodes import NodeGroup
from cyberfusion.ClusterSupport.task_collection_results import (
    TASK_STATES_DEFINITIVE,
    TaskCollectionResult,
    TaskState,
)
from cyberfusion.ClusterSupport.unix_users_usages import UNIXUserUsage
from cyberfusion.ClusterSupport.virtual_hosts import (
    VirtualHostServerSoftwareName,
)
from cyberfusion.Common import convert_bytes_gib

# Set constants

EMPTY_TO_CLEAR_MESSAGE = "Leave empty to clear"
CONFIRM_MESSAGE = "When --confirm is used, no confirmation prompt will be given"
DETAILED_MESSAGE = "Show more information"
RANDOM_PASSWORD_MESSAGE = "Use an empty string for a randomized password"
BOOL_MESSAGE = "[true|false]"

PATH_DIRECTORY_CONFIG_GENERIC = os.path.join(str(Path.home()), ".config")
PATH_DIRECTORY_CONFIG_CLI = os.path.join(PATH_DIRECTORY_CONFIG_GENERIC, "cyberfusion")

PATH_CONFIG_LOCAL = os.path.join(PATH_DIRECTORY_CONFIG_CLI, "cyberfusion.cfg")
PATH_CONFIG_SYSTEM = os.path.join(os.path.sep, "etc", "cyberfusion", "cyberfusion.cfg")
PATH_CONFIG_ENVIRONMENT = os.environ.get("CLUSTER_CONFIG_FILE", None)

console = Console()
err_console = Console(stderr=True)

F = TypeVar("F", bound=Callable[..., Optional[int]])

# Enums


class HttpMethod(str, Enum):
    """Enum for HTTP methods."""

    GET: str = METHOD_GET
    PATCH: str = METHOD_PATCH
    PUT: str = METHOD_PUT
    POST: str = METHOD_POST
    DELETE: str = METHOD_DELETE


# Error handlers


def print_warning(message: str) -> None:
    """Print warning message."""
    typer.secho(f"Warning: {message}", fg="yellow")


def handle_manual_error(message: str) -> None:
    """Handle manually raised error.

    Prints and exits.
    """
    typer.secho(f"Error: {message}", fg="red")

    raise SystemExit(1)


def handle_api_error(obj: ClusterApiCallException) -> None:
    """Handle error from ClusterApiCallException."""
    message = "Error: "

    if obj.status_code in (
        HTTPStatus.BAD_REQUEST,
        HTTPStatus.CONFLICT,
        HTTPStatus.FORBIDDEN,
        HTTPStatus.NOT_FOUND,
        HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        try:
            message += obj.body["detail"]
        except KeyError:
            # Fall back to a generic message. Most likely scenario: 500 was
            # returned because an internal error wasn't handled.

            message += "Unexpected error. Contact support."
    elif obj.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        for error in obj.body["detail"]:
            location = " -> ".join(error["loc"])

            if location == "__root__":  # Doesn't mean anything to the user
                location = "Input"

            message += f"\n{location} is invalid: {error['msg']}"
    else:
        message += "Unexpected error. Contact support."

    typer.secho(message, fg="red")

    raise SystemExit(1)


# Callback options. See main.callback for descriptions.

state: Dict[str, List[str]] = {"clusters_names": []}

# Support


def get_config_file_path() -> Optional[str]:
    """Get config file path."""
    if PATH_CONFIG_ENVIRONMENT:
        return PATH_CONFIG_ENVIRONMENT

    for path in [PATH_CONFIG_LOCAL, PATH_CONFIG_SYSTEM]:
        if not os.path.exists(path):
            continue

        return path

    return None


@lru_cache(maxsize=1)
def get_support(config_file_path: Optional[str] = None) -> ClusterSupport:
    """Get ClusterSupport object.

    This is a singleton for efficiency (uses 'lru_cache' to avoid instantiating
    class in the root of this module, as we only want to create a ClusterSupport
    object when it is needed.
    """
    if not config_file_path:
        config_file_path = get_config_file_path()

    try:
        clusters_ids: Optional[List[int]] = None

        if state["clusters_names"]:
            clusters_ids = []

            accessible_core_api_clusters = ClusterSupport(
                config_file_path=config_file_path
            ).accessible_core_api_clusters.items()

            for cluster_name in state["clusters_names"]:
                found = False

                for (
                    cluster_id,
                    _cluster_name,
                ) in accessible_core_api_clusters:
                    if _cluster_name != cluster_name:
                        continue

                    found = True

                    clusters_ids.append(cluster_id)

                    break

                if not found:
                    print_warning(
                        f"API user has no access to specified cluster with name '{cluster_name}', skipping..."
                    )

            if (
                clusters_ids == []
            ):  # Passing an empty list to ClusterSupport means no limit
                print_warning(
                    "API user does not have access to all specified clusters, operating on all clusters"
                )

        return ClusterSupport(
            config_file_path=config_file_path, cluster_ids=clusters_ids
        )
    except configparser.Error:
        if config_file_path:
            handle_manual_error(
                f"The config file at '{config_file_path}' exists, but could not be read. If you are running this program on a cluster node, make sure that you're running this command as the root user."
            )
        else:
            handle_manual_error(
                f"Could not find config file. Run 'corectl setup' to create config file for the first time. (Tried paths: {PATH_CONFIG_LOCAL}, {PATH_CONFIG_SYSTEM})"
            )
    except ClusterApiCallException as e:
        handle_api_error(e)


# Generic functions


def get_package_version() -> str:
    """Get package version from pipx."""
    return json.loads(
        subprocess.run(
            ["pipx", "list", "--json"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        ).stdout
    )["venvs"]["python3-cyberfusion-corectl"]["metadata"]["main_package"][
        "package_version"
    ]


def print_or_write_contents(contents: str, output_file: Optional[Path]) -> None:
    """Print, or write contents to file."""
    contents = contents.rstrip()

    if output_file:
        output_file.write_text(contents + "\n")  # Add EOF

        return

    console.print(contents)


def get_object(objects: List[APIObjectInterface], **filters: Any) -> APIObjectInterface:
    """Get single object, or error if non-existent."""
    try:
        return get_support()._filter_objects(objects, **filters)[0]
    except IndexError:
        _count = 0

        attributes = ""

        for k, v in filters.items():
            _count += 1

            attributes += f"{k}={v}"

            if _count != len(filters.items()):
                attributes += ", "

        handle_manual_error(f"Object with attributes matching '{attributes}' not found")


def get_cms_by_virtual_host_domain(virtual_host_domain: str) -> CMS:
    """Get CMS by virtual host domain."""
    return get_object(
        get_support().cmses,
        virtual_host_id=get_object(
            get_support().virtual_hosts, domain=virtual_host_domain
        ).id,
    )


def get_haproxy_listen_to_node_by_multiple(
    haproxy_listen_name: str,
    node_hostname: str,
) -> HAProxyListenToNode:
    """Get HAProxy listen to node by HAProxy listen name and node hostname."""
    node = get_object(get_support().nodes, hostname=node_hostname)
    haproxy_listen = get_object(
        get_support().haproxy_listens,
        name=haproxy_listen_name,
        cluster_id=node.cluster.id,
    )

    return get_object(
        get_support().haproxy_listens_to_nodes,
        haproxy_listen_id=haproxy_listen.id,
        node_id=node.id,
    )


def get_api_user_to_cluster_by_multiple(
    api_user_username: str,
    cluster_name: str,
) -> APIUserToCluster:
    """Get API user to cluster by API user username and cluster name."""
    api_user = get_object(get_support().api_users, username=api_user_username)
    cluster = get_object(get_support().clusters, name=cluster_name)

    return get_object(
        get_support().api_users_to_clusters,
        api_user_id=api_user.id,
        cluster_id=cluster.id,
    )


def get_first_found_virtual_host_server_software(
    cluster_id: int,
) -> Optional[VirtualHostServerSoftwareName]:
    """Get first found virtual host server software by nodes groups."""
    nodes = get_support().get_nodes(cluster_id=cluster_id)

    for node in nodes:
        if NodeGroup.NGINX in node.groups:
            return VirtualHostServerSoftwareName.NGINX

        elif NodeGroup.APACHE in node.groups:
            return VirtualHostServerSoftwareName.APACHE

    return VirtualHostServerSoftwareName.APACHE  # Default


def get_usages_timestamp(
    *, hours_before: Optional[int] = None, days_before: Optional[int] = None
) -> Tuple[datetime, TimeUnit]:
    """Get timestamp and time_unit for requesting usages."""

    # Exit if both are set OR neither is set

    if days_before and hours_before or not days_before and not hours_before:
        handle_manual_error("Use either --days-before OR --hours-before")

    timestamp = datetime.utcnow().replace(tzinfo=timezone.utc)
    time_unit = TimeUnit.HOURLY

    if hours_before:
        timestamp = timestamp - timedelta(hours=hours_before)

    if days_before:
        timestamp = timestamp - timedelta(days=days_before)
        time_unit = TimeUnit.DAILY

    return timestamp, time_unit


def get_usages_plot(
    *,
    usages: List[Union[DatabaseUsage, MailAccountUsage, UNIXUserUsage]],
) -> str:
    """Get plot.

    Hourly interval by default.
    """
    if not usages:
        handle_manual_error("No usages found")

    times = [plotext.datetime_to_string(obj.datetime_object) for obj in usages]

    usages = [convert_bytes_gib(obj.usage) for obj in usages]

    plotext.plot(times, usages)

    plotext.clear_color()
    plotext.title("Disk Usage")
    plotext.xlabel("Time")
    plotext.ylabel("GiB")

    return plotext.build()


def apply_environment_variable(
    environment_variables_obj: Dict[str, str],
    environment_variable_string: str,
) -> None:
    """Parse and apply environment variable from string."""
    split_string = environment_variable_string.split("=", 1)

    if len(split_string) < 2:
        handle_manual_error("Invalid format. Use 'key=value'")

    environment_variables_obj[split_string[0]] = split_string[1]


def delete_api_object(
    *,
    obj: APIObjectInterface,
    confirm: bool,
) -> None:
    """Delete API object."""
    console.print(
        "Data of objects (such as virtual hosts and databases) is not deleted on the cluster. Delete the data yourself if needed."
    )

    if not confirm:
        typer.confirm("Are you sure you want to delete this object?", abort=True)

    obj.delete()


def validate_string(
    s: str, *, max_length: int = 253, regex: Optional[str] = None
) -> bool:
    """Validate string using regex.

    When no regex is given, a default will be used and the max length can be set.
    When a custom regex is given, max_length won't work
    """
    if not regex:
        regex = f"^[a-zA-Z0-9-_]{{1,{max_length}}}$"

    return bool(re.fullmatch(re.compile(regex), s))


# Decorators


def confirm_clear(f: F) -> F:
    """Confirm that user wants to clear value."""

    @wraps(f)
    def wrapper(
        confirm: bool,
        *args: tuple,
        **kwargs: dict,
    ) -> None:
        signature = inspect.signature(f)

        for parameter in signature.parameters:
            default = signature.parameters[parameter].default

            if not isinstance(default, ArgumentInfo) and not isinstance(
                default, OptionInfo
            ):
                continue

            if default.help != EMPTY_TO_CLEAR_MESSAGE:
                continue

            if kwargs[parameter] is None:
                if not confirm:
                    typer.confirm(
                        "Are you sure you want to clear the value?", abort=True
                    )

        f(*args, **kwargs)

    return cast(F, wrapper)


def catch_api_exception(f: F) -> F:
    """Catch ClusterApiCallException and handle it."""

    @wraps(f)
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        try:
            f(*args, **kwargs)
        except ClusterApiCallException as e:
            handle_api_error(e)

    return cast(F, wrapper)


def exit_with_status(f: F) -> F:
    """Exit with custom status code."""

    @wraps(f)
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        status = f(*args, **kwargs)

        if status is None:
            return

        raise SystemExit(status)

    return cast(F, wrapper)


# Tasks


class StateColumn(ProgressColumn):
    """Column that shows task state."""

    def render(self, task: Task) -> Text:
        """Render column."""
        return Text(task.fields["state"])


class MessageColumn(ProgressColumn):
    """Column that shows task message."""

    def render(self, task: Task) -> Text:
        """Render column."""
        return Text(task.fields["message"])


def wait_for_task(
    *,
    task_collection_uuid: str,
) -> Optional[bool]:
    """Wait for task_collection to finish.

    Returns True if all tasks were successful.
    """
    TOTAL_STEPS = 1

    console.print(
        f"(To run in background, press CTRL+C. Return with `corectl task-collections results {task_collection_uuid}`.)"
    )

    tasks: Dict[str, TaskID] = {}

    def get_results() -> List[TaskCollectionResult]:
        """Get task collection results."""
        return get_support().task_collection_results(
            task_collection_uuid=task_collection_uuid
        )

    def add_or_update_task(progress: Progress, result: TaskCollectionResult) -> None:
        """Add or update task in progress."""
        data = {
            "state": result.state,
            "message": result.message or "",
        }

        if result.state == TaskState.SUCCESS:
            colour = "green"
        elif result.state in [TaskState.REVOKED, TaskState.FAILURE]:
            colour = "red"
        elif result.state == TaskState.STARTED:
            colour = "yellow"
        else:
            colour = "grey62"

        if result.description in tasks:
            progress.update(
                tasks[result.description],
                description=f"[{colour}]" + result.description,
                **data,
            )
        else:
            tasks[result.description] = progress.add_task(
                f"[{colour}]" + result.description,
                total=TOTAL_STEPS,
                start=False,
                **data,
            )

        if (
            result.state not in TASK_STATES_DEFINITIVE
            and result.state != TaskState.PENDING
        ):
            progress.start_task(tasks[result.description])

        if result.state in TASK_STATES_DEFINITIVE:
            progress.stop_task(tasks[result.description])
            progress.advance(tasks[result.description], advance=TOTAL_STEPS)

    with Progress(
        "[progress.description]{task.description}",
        SpinnerColumn(),
        TimeElapsedColumn(),
        StateColumn(),
        MessageColumn(),
        console=console,
    ) as progress:
        for result in get_results():
            add_or_update_task(progress, result)

        while not progress.finished:
            sleep(2)

            for result in get_results():
                add_or_update_task(progress, result)

    return all(task.state == TaskState.SUCCESS for task in get_results())


# WordPress


def _fetch_wordpress_versions() -> Dict[str, str]:
    """Fetch WordPress versions."""
    response = requests.get("https://api.wordpress.org/core/stable-check/1.0/")
    response.raise_for_status()

    return response.json()


def get_latest_wordpress_version() -> str:
    """Get latest WordPress version."""
    try:
        versions = _fetch_wordpress_versions()
    except requests.exceptions.HTTPError:
        handle_manual_error("Could not fetch latest WordPress version")

    # Return the key with value "latest", throw error when key can't be found

    try:
        return list(versions.keys())[list(versions.values()).index("latest")]
    except ValueError:
        handle_manual_error("Could not fetch latest WordPress version")

    # This return will never be reached, but mypy was complaining

    return ""


class WordPressVersionStatus(Enum):
    """Enum for WordPress version status."""

    INSECURE = "insecure"
    OUTDATED = "outdated"
    LATEST = "latest"


def check_wordpress_version(version: str) -> Optional[WordPressVersionStatus]:
    """Check if wordpress version is outdated or insecure."""
    try:
        versions = _fetch_wordpress_versions()
    except requests.exceptions.HTTPError:
        return None

    try:
        if versions[version] == WordPressVersionStatus.INSECURE.value:
            return WordPressVersionStatus.INSECURE
        elif versions[version] == WordPressVersionStatus.OUTDATED.value:
            return WordPressVersionStatus.OUTDATED
        elif versions[version] == WordPressVersionStatus.LATEST.value:
            return WordPressVersionStatus.LATEST
    except KeyError:
        handle_manual_error("Invalid WordPress version, specify a valid version")

    return None
