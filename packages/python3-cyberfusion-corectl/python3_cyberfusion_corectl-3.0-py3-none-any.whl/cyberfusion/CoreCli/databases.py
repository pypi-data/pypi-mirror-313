"""Databases subcommands."""

from typing import List, Optional

import typer

from cyberfusion.ClusterSupport.database_user_grants import (
    DatabaseUserGrant,
    Privilege,
)
from cyberfusion.ClusterSupport.database_users import (
    DatabaseServerSoftwareName,
    DatabaseUser,
    Host,
)
from cyberfusion.ClusterSupport.databases import Database
from cyberfusion.Common import generate_random_string
from cyberfusion.CoreCli._utilities import (
    BOOL_MESSAGE,
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    RANDOM_PASSWORD_MESSAGE,
    catch_api_exception,
    console,
    delete_api_object,
    exit_with_status,
    get_object,
    get_support,
    get_usages_plot,
    get_usages_timestamp,
    handle_manual_error,
    print_warning,
    wait_for_task,
)

app = typer.Typer()

HELP_PANEL_DATABASES = "Databases"
HELP_PANEL_DATABASE_USERS = "Database Users"
HELP_PANEL_DATABASE_USER_GRANTS = "Database User Grants"


@app.command("list", rich_help_panel=HELP_PANEL_DATABASES)
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List databases."""
    console.print(
        get_support().get_table(
            objs=get_support().databases,
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_DATABASES)
@catch_api_exception
def get(
    name: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show database."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().databases, name=name)],
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_DATABASE_USERS)
@catch_api_exception
def list_users(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """List database users."""
    console.print(
        get_support().get_table(
            objs=get_support().database_users,
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_DATABASE_USERS)
@catch_api_exception
def get_user(
    id_: int = typer.Argument(metavar="id", default=...),
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show database user."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().database_users, id_=id_)],
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_DATABASE_USER_GRANTS)
@catch_api_exception
def list_user_grants(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
    database_user_id: Optional[int] = typer.Argument(default=None),
) -> None:
    """List user grants."""
    console.print(
        get_support().get_table(
            objs=get_support().get_database_user_grants(
                database_user_id=database_user_id
            ),
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_DATABASES)
@catch_api_exception
def usage(
    name: str,
    hours_before: Optional[int] = None,
    days_before: Optional[int] = None,
    amount: Optional[int] = typer.Option(default=None, show_default="All"),
) -> None:
    """Show disk usage graph.

    Using --hours-before OR --days-before is required.
    """
    database = get_object(get_support().databases, name=name)

    timestamp, time_unit = get_usages_timestamp(
        days_before=days_before, hours_before=hours_before
    )

    usages = get_support().database_usages(
        database_id=database.id,
        timestamp=timestamp,
        time_unit=time_unit,
    )[:amount]

    typer.echo(get_usages_plot(usages=usages))


@app.command(rich_help_panel=HELP_PANEL_DATABASES)
@catch_api_exception
def create(
    name: str,
    server_software: DatabaseServerSoftwareName = typer.Argument(
        default=..., case_sensitive=False
    ),
    optimizing_enabled: bool = typer.Option(False, "--optimize/--dont-optimize"),
    backups_enabled: bool = typer.Option(True, "--backup/--dont-backup"),
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create database."""
    database = Database(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    database.create(
        name=name,
        server_software_name=server_software.value,
        optimizing_enabled=optimizing_enabled,
        backups_enabled=backups_enabled,
        cluster_id=cluster.id,
    )

    console.print(
        get_support().get_table(
            objs=[database],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_DATABASE_USERS)
@catch_api_exception
def create_user(
    name: str,
    server_software: DatabaseServerSoftwareName = typer.Argument(
        default=..., case_sensitive=False
    ),
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
    user_grant_database_name: Optional[str] = typer.Option(
        default=None, help="Specify this to give user access to a database"
    ),
    user_grant_table: Optional[str] = typer.Option(
        default=None,
        help="Only works in combination with --user-grant-database, omit for all tables",
    ),
    user_grant_privilege: Privilege = typer.Option(
        default=Privilege.ALL,
        help="Only works in combination with --user-grant-database.",
        show_default="ALL",
        case_sensitive=False,
    ),
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create database user."""
    database_user = DatabaseUser(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    host = Host.ALL

    if server_software == DatabaseServerSoftwareName.POSTGRESQL:
        host = None

    database_user.create(
        name=name,
        host=host,
        password=password,
        server_software_name=server_software.value,
        phpmyadmin_firewall_groups_ids=None,
        cluster_id=cluster.id,
    )

    if user_grant_database_name:
        database_user_grant = DatabaseUserGrant(get_support())

        database_user_grant.create(
            database_id=get_object(
                get_support().databases, name=user_grant_database_name
            ).id,
            database_user_id=database_user.id,
            table_name=user_grant_table,
            privilege_name=user_grant_privilege,
        )

    console.print(
        get_support().get_table(
            objs=[database_user],
            detailed=True,
        )
    )

    if user_grant_database_name:
        console.print(
            get_support().get_table(
                objs=[database_user_grant],
                detailed=True,
            )
        )


@app.command(rich_help_panel=HELP_PANEL_DATABASE_USER_GRANTS)
@catch_api_exception
def create_user_grant(
    database_user_id: int,
    database_name: str,
    table_name: Optional[str] = typer.Argument(
        default=None, help="Leave empty for all tables"
    ),
    user_grant_privilege: Privilege = typer.Option(
        default=Privilege.ALL,
        show_default="ALL",
        case_sensitive=False,
    ),
) -> None:
    """Create database user grant."""
    database_user = get_object(get_support().database_users, id_=database_user_id)
    database = get_object(get_support().databases, name=database_name)

    database_user_grant = DatabaseUserGrant(get_support())

    database_user_grant.create(
        database_id=database.id,
        database_user_id=database_user.id,
        table_name=table_name,
        privilege_name=user_grant_privilege,
    )

    console.print(
        get_support().get_table(
            objs=[database_user_grant],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def create_all(
    name: str,
    user_name: str,
    server_software: DatabaseServerSoftwareName = typer.Argument(
        default=..., case_sensitive=False
    ),
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
    user_grant_privilege: Privilege = typer.Option(
        default=Privilege.ALL,
        show_default="ALL",
        case_sensitive=False,
    ),
    optimizing_enabled: bool = typer.Option(False, "--optimize/--dont-optimize"),
    backups_enabled: bool = typer.Option(True, "--backup/--dont-backup"),
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create database with user and user grant."""
    create_grant = server_software == DatabaseServerSoftwareName.MARIADB

    cluster = get_object(get_support().clusters, name=cluster_name)

    # Prevent a database from being created when the user already exists. There
    # is no need to check for the database itself. If it already exists, the API
    # will return an error on creation

    if get_support().get_database_users(name=user_name, cluster_id=cluster.id):
        handle_manual_error("Database user already exists")

    database = Database(get_support())
    database_user = DatabaseUser(get_support())
    database_user_grant = DatabaseUserGrant(get_support())

    host = Host.ALL

    if server_software == DatabaseServerSoftwareName.POSTGRESQL:
        host = None

    database.create(
        name=name,
        server_software_name=server_software.value,
        cluster_id=cluster.id,
        optimizing_enabled=optimizing_enabled,
        backups_enabled=backups_enabled,
    )

    database_user.create(
        name=user_name,
        host=host,
        password=password,
        server_software_name=server_software.value,
        phpmyadmin_firewall_groups_ids=None,
        cluster_id=cluster.id,
    )

    if create_grant:
        database_user_grant.create(
            database_id=database.id,
            database_user_id=database_user.id,
            table_name=None,
            privilege_name=user_grant_privilege,
        )
    else:
        print_warning(
            "Skipping database user grant. This is only supported on MariaDB servers."
        )

    console.print(
        get_support().get_table(
            objs=[database],
            detailed=True,
        )
    )
    console.print(
        get_support().get_table(
            objs=[database_user],
            detailed=True,
        )
    )

    if create_grant:
        console.print(
            get_support().get_table(
                objs=[database_user_grant],
                detailed=True,
            )
        )


@app.command(rich_help_panel=HELP_PANEL_DATABASE_USERS)
@catch_api_exception
def update_user_password(
    user_id: int,
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
) -> None:
    """Update database user password."""
    database_user = get_object(get_support().database_users, id_=user_id)

    database_user.password = password
    database_user.update()


@app.command(rich_help_panel=HELP_PANEL_DATABASES)
@catch_api_exception
def update_backups(
    name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update backups."""
    database = get_object(get_support().databases, name=name)

    database.backups_enabled = state
    database.update()


@app.command(rich_help_panel=HELP_PANEL_DATABASES)
@catch_api_exception
def update_optimizing(
    name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update optimizing."""
    database = get_object(get_support().databases, name=name)

    if not database.server_software_name == DatabaseServerSoftwareName.MARIADB:
        print_warning("Optimizing is compatible only with the MariaDB server software.")

        return

    database.optimizing_enabled = state
    database.update()


@app.command(rich_help_panel=HELP_PANEL_DATABASES)
@catch_api_exception
def delete(
    name: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete database."""
    database = get_object(get_support().databases, name=name)

    delete_api_object(obj=database, confirm=confirm)


@app.command(rich_help_panel=HELP_PANEL_DATABASE_USERS)
@catch_api_exception
def delete_user(
    id_: int = typer.Argument(metavar="id", default=...),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete database user."""
    database_user = get_object(get_support().database_users, id_=id_)

    delete_api_object(obj=database_user, confirm=confirm)


@app.command(rich_help_panel=HELP_PANEL_DATABASES)
@catch_api_exception
def sync(
    left_database_name: str,
    right_database_name: str,
) -> None:
    """Sync database."""
    left_database = get_object(get_support().databases, name=left_database_name)
    right_database = get_object(get_support().databases, name=right_database_name)

    task_collection = left_database.sync(right_database_id=right_database.id)

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command(rich_help_panel=HELP_PANEL_DATABASES)
@catch_api_exception
def compare(
    left_database_name: str,
    right_database_name: str,
    sort_alphabetically: bool = typer.Option(default=True),
) -> None:
    """Compare databases."""
    left_database = get_object(get_support().databases, name=left_database_name)
    right_database = get_object(get_support().databases, name=right_database_name)

    (
        _identical_tables_names,
        _not_identical_tables_names,
        _only_left_tables_names,
        _only_right_tables_names,
    ) = left_database.get_comparison(right_database_id=right_database.id)

    console.print(
        get_support().get_comparison_table(
            left_column_name="Table",
            left_label=left_database.name,
            right_label=right_database.name,
            identical=_identical_tables_names,
            different=_not_identical_tables_names,
            left_only=_only_left_tables_names,
            right_only=_only_right_tables_names,
            sort_alphabetically=sort_alphabetically,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_DATABASE_USERS)
@catch_api_exception
def add_phpmyadmin_firewall_groups(
    id_: int = typer.Argument(metavar="id", default=...),
    phpmyadmin_firewall_groups_names: List[str] = typer.Argument(default=...),
) -> None:
    """Add phpMyAdmin firewall groups."""
    database_user = get_object(get_support().database_users, id_=id_)

    if database_user.phpmyadmin_firewall_groups_ids is None:
        database_user.phpmyadmin_firewall_groups_ids = []

    for phpmyadmin_firewall_group_name in phpmyadmin_firewall_groups_names:
        firewall_group = get_object(
            get_support().firewall_groups,
            name=phpmyadmin_firewall_group_name,
            cluster_id=database_user.cluster_id,
        )

        database_user.phpmyadmin_firewall_groups_ids.append(firewall_group.id)

    database_user.update()


@app.command(rich_help_panel=HELP_PANEL_DATABASE_USERS)
@catch_api_exception
@exit_with_status
def remove_phpmyadmin_firewall_groups(
    id_: int = typer.Argument(metavar="id", default=...),
    phpmyadmin_firewall_groups_names: List[str] = typer.Argument(default=...),
) -> int:
    """Remove phpMyAdmin firewall groups."""
    database_user = get_object(get_support().database_users, id_=id_)

    exit_code = 0
    success = False

    if database_user.phpmyadmin_firewall_groups_ids is None:
        return exit_code

    for phpmyadmin_firewall_group_name in phpmyadmin_firewall_groups_names:
        firewall_group = get_object(
            get_support().firewall_groups,
            name=phpmyadmin_firewall_group_name,
            cluster_id=database_user.cluster_id,
        )

        try:
            database_user.phpmyadmin_firewall_groups_ids.remove(firewall_group.id)
            success = True
        except ValueError:
            print_warning(
                f"Firewall group '{phpmyadmin_firewall_group_name}' not found, skipping."
            )
            exit_code = 64

    if not success:
        handle_manual_error("No firewall groups have been removed")

    database_user.update()

    return exit_code
