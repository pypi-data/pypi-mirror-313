"""UNIX users subcommands."""

import os
from typing import List, Optional

import typer

from cyberfusion.ClusterSupport.clusters import ClusterGroup
from cyberfusion.ClusterSupport.unix_users import ShellPath, UNIXUser
from cyberfusion.Common import generate_random_string
from cyberfusion.CoreCli._utilities import (
    BOOL_MESSAGE,
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    EMPTY_TO_CLEAR_MESSAGE,
    RANDOM_PASSWORD_MESSAGE,
    catch_api_exception,
    confirm_clear,
    console,
    delete_api_object,
    get_object,
    get_support,
    get_usages_plot,
    get_usages_timestamp,
)

app = typer.Typer()


@app.command("list")
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List UNIX users."""
    console.print(
        get_support().get_table(
            objs=get_support().unix_users,
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get(
    username: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show UNIX user."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().unix_users, username=username)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def usage(
    username: str,
    hours_before: Optional[int] = None,
    days_before: Optional[int] = None,
    amount: Optional[int] = typer.Option(default=None, show_default="All"),
) -> None:
    """Show disk usage graph.

    Using --hours-before OR --days-before is required.
    """
    unix_user = get_object(get_support().unix_users, username=username)

    timestamp, time_unit = get_usages_timestamp(
        days_before=days_before, hours_before=hours_before
    )

    usages = get_support().unix_user_usages(
        unix_user_id=unix_user.id, timestamp=timestamp, time_unit=time_unit
    )[:amount]

    typer.echo(get_usages_plot(usages=usages))


@app.command()
@catch_api_exception
def create(
    username: str,
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
    shell_path: ShellPath = ShellPath.BASH,
    record_usage_files: bool = typer.Option(
        False,
        "--record-usage-files/--dont-record-usage-files",
        help="Record individual file sizes",
    ),
    default_php_version: Optional[str] = None,
    default_nodejs_version: Optional[str] = None,
    virtual_hosts_subdirectory: str = typer.Option(default="", show_default=False),
    mail_domains_subdirectory: str = typer.Option(default="", show_default=False),
    borg_repositories_subdirectory: str = typer.Option(default="", show_default=False),
    description: Optional[str] = None,
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create UNIX user."""
    unix_user = UNIXUser(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    home_directory = os.path.join(cluster.unix_users_home_directory, username)

    unix_user.create(
        username=username,
        password=password,
        shell_path=shell_path,
        record_usage_files=record_usage_files,
        default_php_version=default_php_version,
        default_nodejs_version=default_nodejs_version,
        virtual_hosts_directory=(
            os.path.join(home_directory, virtual_hosts_subdirectory)
            if ClusterGroup.WEB in cluster.groups
            else None
        ),
        mail_domains_directory=(
            os.path.join(home_directory, mail_domains_subdirectory)
            if ClusterGroup.MAIL in cluster.groups
            else None
        ),
        borg_repositories_directory=(
            os.path.join(home_directory, borg_repositories_subdirectory)
            if ClusterGroup.BORG_SERVER in cluster.groups
            else None
        ),
        description=description,
        cluster_id=cluster.id,
    )

    console.print(
        get_support().get_table(
            objs=[unix_user],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def update_password(
    username: str,
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
) -> None:
    """Update password."""
    unix_user = get_object(get_support().unix_users, username=username)

    unix_user.password = password
    unix_user.update()


@app.command()
@catch_api_exception
def update_shell_path(username: str, shell_path: ShellPath) -> None:
    """Update shell path."""
    unix_user = get_object(get_support().unix_users, username=username)

    unix_user.shell_path = shell_path
    unix_user.update()


@app.command()
@confirm_clear
@catch_api_exception
def update_default_php_version(
    username: str,
    version: Optional[str] = typer.Argument(default=None, help=EMPTY_TO_CLEAR_MESSAGE),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update default PHP version."""
    unix_user = get_object(get_support().unix_users, username=username)

    unix_user.default_php_version = version
    unix_user.update()


@app.command()
@confirm_clear
@catch_api_exception
def update_default_nodejs_version(
    username: str,
    version: Optional[str] = typer.Argument(default=None, help=EMPTY_TO_CLEAR_MESSAGE),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update default NodeJS version."""
    unix_user = get_object(get_support().unix_users, username=username)

    unix_user.default_nodejs_version = version
    unix_user.update()


@app.command()
@confirm_clear
@catch_api_exception
def update_description(
    username: str,
    description: Optional[str] = typer.Argument(
        default=None, help=EMPTY_TO_CLEAR_MESSAGE
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update description."""
    unix_user = get_object(get_support().unix_users, username=username)

    unix_user.description = description
    unix_user.update()


@app.command()
@catch_api_exception
def update_record_usage_files(
    username: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update record usage files."""
    unix_user = get_object(get_support().unix_users, username=username)

    unix_user.record_usage_files = state
    unix_user.update()


@app.command()
@catch_api_exception
def delete(
    username: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete UNIX user."""
    unix_user = get_object(get_support().unix_users, username=username)

    delete_api_object(obj=unix_user, confirm=confirm)


def _flatten_comparison_dict(paths: dict, pwd: str = "") -> List:
    """Flatten the comparison dictionary to a list."""
    result = []

    for path_component in paths:
        path = pwd + (
            "" if path_component == os.path.sep else os.path.sep + path_component
        )

        has_children = isinstance(paths[path_component], dict)

        if has_children:
            result.extend(
                _flatten_comparison_dict(
                    paths[path_component],
                    pwd=path,
                )
            )
        else:
            result.append(path)

    return result


def _clean_comparison_path(
    paths: dict, home_directory: str, add_trailing_slash: bool = False
) -> List[str]:
    """Standardize paths by removing home directory and adding a trailing slash for directories."""
    return [
        os.path.relpath(path, home_directory)
        + (os.path.sep if add_trailing_slash else "")
        for path in _flatten_comparison_dict(paths)
    ]


@app.command()
@catch_api_exception
def compare(
    left_unix_user_username: str,
    right_unix_user_username: str,
    sort_alphabetically: bool = typer.Option(default=True),
) -> None:
    """Compare UNIX users."""
    left_unix_user = get_object(
        get_support().unix_users, username=left_unix_user_username
    )
    right_unix_user = get_object(
        get_support().unix_users, username=right_unix_user_username
    )

    (
        _not_identical_paths,
        _only_left_files_paths,
        _only_right_files_paths,
        _only_left_directories_paths,
        _only_right_directories_paths,
    ) = left_unix_user.get_comparison(right_unix_user_id=right_unix_user.id)

    # not_identical_paths

    not_identical_paths = _clean_comparison_path(
        _not_identical_paths,
        home_directory=left_unix_user.home_directory,
    )

    # only_left_files_paths

    only_left_paths = _clean_comparison_path(
        _only_left_files_paths,
        home_directory=left_unix_user.home_directory,
    )

    # only_left_directories_paths

    only_left_paths.extend(
        _clean_comparison_path(
            _only_left_directories_paths,
            home_directory=left_unix_user.home_directory,
            add_trailing_slash=True,
        )
    )

    # only_right_files_paths

    only_right_paths = _clean_comparison_path(
        _only_right_files_paths,
        home_directory=right_unix_user.home_directory,
    )

    # only_right_directories_paths

    only_right_paths.extend(
        _clean_comparison_path(
            _only_right_directories_paths,
            home_directory=right_unix_user.home_directory,
            add_trailing_slash=True,
        )
    )

    console.print(
        get_support().get_comparison_table(
            left_label=left_unix_user.username,
            right_label=right_unix_user.username,
            identical=[],
            different=not_identical_paths,
            left_only=only_left_paths,
            right_only=only_right_paths,
            sort_alphabetically=sort_alphabetically,
        )
    )
