"""Clusters subcommands."""

from typing import List, Optional

import typer
from rich.panel import Panel
from rich.table import Table

from cyberfusion.ClusterSupport import Cluster
from cyberfusion.ClusterSupport.clusters import (
    ClusterGroup,
    HTTPRetryCondition,
    MeilisearchEnvironment,
    PHPExtension,
    UNIXUserHomeDirectory,
)
from cyberfusion.ClusterSupport.enums import IPAddressFamily
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

HELP_PANEL_SHOW = "Show cluster"
HELP_PANEL_UPDATE = "Update cluster"
HELP_PANEL_IP_ADDRESSES = "IP addresses"

ERROR_MISSING_HTTP_RETRY_PROPERTIES = "Cluster does not have HTTP retry properties. This usually means the cluster does not have compatible groups."


@app.command("list")
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List clusters."""
    console.print(
        get_support().get_table(objs=get_support().clusters, detailed=detailed)
    )


@app.command(rich_help_panel=HELP_PANEL_SHOW)
@catch_api_exception
def get(
    cluster_name: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show cluster."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().clusters, name=cluster_name)],
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_SHOW)
@catch_api_exception
def get_borg_ssh_key(
    cluster_name: str,
) -> None:
    """Show Borg SSH key."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    console.print(cluster.get_borg_public_ssh_key())


@app.command()
@catch_api_exception
def create(
    customer_identifier: Optional[str] = typer.Option(
        default=None, help="Do not set unless superuser"
    ),
    groups: List[ClusterGroup] = typer.Option([], "--group", show_default=False),
    description: str = typer.Option(default=...),
    site_name: str = typer.Option(default=...),
    kernelcare_license_key: Optional[str] = typer.Option(default=None),
    unix_users_home_directory: Optional[UNIXUserHomeDirectory] = typer.Option(
        default=None, help="Groups: Web, Mail, Borg Server", show_default=False
    ),
    sync_toolkit_enabled: bool = typer.Option(
        False, "--with-sync-toolkit", help="Groups: Web, Database"
    ),
    php_versions: List[str] = typer.Option(
        [], "--php-version", rich_help_panel="Group: Web (PHP)"
    ),
    custom_php_modules_names: List[PHPExtension] = typer.Option(
        [], "--custom-php-module-name", rich_help_panel="Group: Web (PHP)"
    ),
    php_ioncube_enabled: bool = typer.Option(
        False, "--with-php-ioncube", rich_help_panel="Group: Web (PHP)"
    ),
    php_sessions_spread_enabled: bool = typer.Option(
        False, "--with-php-sessions-spread", rich_help_panel="Group: Web (PHP)"
    ),
    nodejs_version: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Web (NodeJS)"
    ),
    nodejs_versions: List[str] = typer.Option(
        [], "--nodejs-version", rich_help_panel="Group: Web (NodeJS)"
    ),
    wordpress_toolkit_enabled: bool = typer.Option(
        False, "--with-wordpress-toolkit", rich_help_panel="Group: Web"
    ),
    bubblewrap_toolkit_enabled: bool = typer.Option(
        False, "--with-bubblewrap-toolkit", rich_help_panel="Group: Web"
    ),
    mariadb_version: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (MariaDB)"
    ),
    mariadb_cluster_name: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (MariaDB)"
    ),
    mariadb_backup_interval: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database (MariaDB)"
    ),
    postgresql_version: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database (PostgreSQL)"
    ),
    postgresql_backup_interval: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database (PostgreSQL)"
    ),
    redis_password: Optional[str] = typer.Option(
        default=generate_random_string,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
        rich_help_panel="Group: Database (Redis)",
    ),
    redis_memory_limit: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database (Redis)"
    ),
    database_toolkit_enabled: bool = typer.Option(
        False, "--with-database-toolkit", rich_help_panel="Group: Database"
    ),
    automatic_borg_repositories_prune_enabled: bool = typer.Option(
        False,
        "--with-automatic-borg-repositories-prune",
        rich_help_panel="Group: Borg Client",
    ),
    grafana_domain: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (Grafana)"
    ),
    singlestore_studio_domain: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (SingleStore)"
    ),
    singlestore_api_domain: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (SingleStore)"
    ),
    singlestore_license_key: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (SingleStore)"
    ),
    singlestore_root_password: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (SingleStore)"
    ),
    metabase_domain: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (Metabase)"
    ),
    metabase_database_password: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (Metabase)"
    ),
    kibana_domain: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (Kibana)"
    ),
    rabbitmq_management_domain: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (RabbitMQ)"
    ),
    rabbitmq_admin_password: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (RabbitMQ)"
    ),
    rabbitmq_erlang_cookie: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (RabbitMQ)"
    ),
    new_relic_mariadb_password: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (New Relic)"
    ),
    new_relic_apm_license_key: Optional[str] = typer.Option(default=None),
    new_relic_infrastructure_license_key: Optional[str] = typer.Option(default=None),
    mariadb_backup_local_retention: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database (MariaDB)"
    ),
    postgresql_backup_local_retention: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database (PostgreSQL)"
    ),
    meilisearch_backup_local_retention: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database (Meilisearch)"
    ),
    elasticsearch_default_users_password: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (Elasticsearch)"
    ),
    meilisearch_master_key: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database (Meilisearch)"
    ),
    meilisearch_backup_interval: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database (Meilisearch)"
    ),
    meilisearch_environment: Optional[MeilisearchEnvironment] = typer.Option(
        default=None, rich_help_panel="Group: Database (Meilisearch)"
    ),
    automatic_upgrades_enabled: bool = False,
    firewall_rules_external_providers_enabled: bool = False,
) -> None:
    """Create cluster."""
    cluster = Cluster(get_support())

    site = get_object(get_support().sites, name=site_name)

    if customer_identifier:
        if not get_support().is_superuser:
            handle_manual_error("Customer team code must be unset when not superuser")

        customer_id = get_object(
            get_support().customers, identifier=customer_identifier
        ).id
    else:
        if get_support().is_superuser:
            handle_manual_error("Customer team code must be set when superuser")

        customer_id = get_support().customer_id

    if ClusterGroup.DB not in groups:
        redis_password = None  # Reset default value

    http_retry_properties: Optional[dict] = None

    if ClusterGroup.WEB in groups or ClusterGroup.REDIRECT in groups:
        http_retry_properties = {
            "tries_amount": None,
            "tries_failover_amount": None,
            "conditions": [],
        }

    task_collection = cluster.create(
        customer_id=customer_id,
        site_id=site.id,
        groups=groups,
        description=description,
        kernelcare_license_key=kernelcare_license_key,
        unix_users_home_directory=unix_users_home_directory,
        sync_toolkit_enabled=sync_toolkit_enabled,
        php_versions=php_versions,
        custom_php_modules_names=custom_php_modules_names,
        php_ioncube_enabled=php_ioncube_enabled,
        php_sessions_spread_enabled=php_sessions_spread_enabled,
        nodejs_version=nodejs_version,
        nodejs_versions=nodejs_versions,
        wordpress_toolkit_enabled=wordpress_toolkit_enabled,
        bubblewrap_toolkit_enabled=bubblewrap_toolkit_enabled,
        mariadb_version=mariadb_version,
        mariadb_cluster_name=mariadb_cluster_name,
        mariadb_backup_interval=mariadb_backup_interval,
        postgresql_version=postgresql_version,
        postgresql_backup_interval=postgresql_backup_interval,
        grafana_domain=grafana_domain,
        singlestore_studio_domain=singlestore_studio_domain,
        singlestore_api_domain=singlestore_api_domain,
        singlestore_license_key=singlestore_license_key,
        singlestore_root_password=singlestore_root_password,
        metabase_domain=metabase_domain,
        metabase_database_password=metabase_database_password,
        kibana_domain=kibana_domain,
        rabbitmq_management_domain=rabbitmq_management_domain,
        rabbitmq_admin_password=rabbitmq_admin_password,
        rabbitmq_erlang_cookie=rabbitmq_erlang_cookie,
        automatic_upgrades_enabled=automatic_upgrades_enabled,
        firewall_rules_external_providers_enabled=firewall_rules_external_providers_enabled,
        new_relic_mariadb_password=new_relic_mariadb_password,
        new_relic_apm_license_key=new_relic_apm_license_key,
        new_relic_infrastructure_license_key=new_relic_infrastructure_license_key,
        mariadb_backup_local_retention=mariadb_backup_local_retention,
        postgresql_backup_local_retention=postgresql_backup_local_retention,
        meilisearch_backup_local_retention=meilisearch_backup_local_retention,
        elasticsearch_default_users_password=elasticsearch_default_users_password,
        redis_password=redis_password,
        redis_memory_limit=redis_memory_limit,
        database_toolkit_enabled=database_toolkit_enabled,
        automatic_borg_repositories_prune_enabled=automatic_borg_repositories_prune_enabled,
        http_retry_properties=http_retry_properties,
        meilisearch_master_key=meilisearch_master_key,
        meilisearch_backup_interval=meilisearch_backup_interval,
        meilisearch_environment=meilisearch_environment,
        php_settings={},
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def add_groups(cluster_name: str, groups: List[ClusterGroup]) -> None:
    """Add groups."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.groups.extend(groups)
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_description(cluster_name: str, description: str) -> None:
    """Update description."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.description = description
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@confirm_clear
@catch_api_exception
def update_kernelcare_license_key(
    cluster_name: str,
    kernelcare_license_key: Optional[str] = typer.Argument(
        default=..., help=EMPTY_TO_CLEAR_MESSAGE
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update KernelCare license key."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.kernelcare_license_key = kernelcare_license_key
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def add_php_versions(cluster_name: str, php_versions: List[str]) -> None:
    """Add PHP versions."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.php_versions.extend(php_versions)
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
@exit_with_status
def remove_php_versions(cluster_name: str, php_versions: List[str]) -> int:
    """Remove PHP versions."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    exit_code = 0
    success = False

    for php_version in php_versions:
        try:
            cluster.php_versions.remove(php_version)
            success = True
        except ValueError:
            print_warning(f"PHP version '{php_version}' not found, skipping.")
            exit_code = 64

    if not success:
        handle_manual_error("No PHP versions have been removed")

    cluster.update()

    return exit_code


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@confirm_clear
@catch_api_exception
def update_php_setting(
    cluster_name: str,
    key: str,
    value: Optional[str] = typer.Argument(
        default=None,
        help=EMPTY_TO_CLEAR_MESSAGE,
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update PHP setting."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    if key not in cluster.php_settings:
        handle_manual_error(
            "Specified PHP setting does not exist. See the API documentation for available settings."
        )

    cluster.php_settings[key] = value
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_http_retry_tries_failover_amount(
    cluster_name: str, tries_failover_amount: int
) -> None:
    """Update HTTP retry tries failover amount."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    if not cluster.http_retry_properties:
        handle_manual_error(ERROR_MISSING_HTTP_RETRY_PROPERTIES)

    cluster.http_retry_properties["tries_failover_amount"] = tries_failover_amount

    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_http_retry_tries_amount(cluster_name: str, tries_amount: int) -> None:
    """Update HTTP retry tries amount.

    If no conditions are set yet, sane defaults are set.
    """
    cluster = get_object(get_support().clusters, name=cluster_name)

    if not cluster.http_retry_properties:
        handle_manual_error(ERROR_MISSING_HTTP_RETRY_PROPERTIES)

    cluster.http_retry_properties["tries_amount"] = tries_amount

    if not cluster.http_retry_properties[
        "conditions"
    ]:  # Can't set tries_amount without conditions
        cluster.http_retry_properties["conditions"] = [
            HTTPRetryCondition.CONNECTION_FAILURE,
            HTTPRetryCondition.EMPTY_RESPONSE,
            HTTPRetryCondition.JUNK_RESPONSE,
            HTTPRetryCondition.RESPONSE_TIMEOUT,
            HTTPRetryCondition.ZERO_RTT_REJECTED,
            HTTPRetryCondition.HTTP_STATUS_500,
            HTTPRetryCondition.HTTP_STATUS_502,
            HTTPRetryCondition.HTTP_STATUS_503,
            HTTPRetryCondition.HTTP_STATUS_504,
        ]

    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def add_http_retry_conditions(
    cluster_name: str, conditions: List[HTTPRetryCondition]
) -> None:
    """Add NodeJS versions."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    if not cluster.http_retry_properties:
        handle_manual_error(ERROR_MISSING_HTTP_RETRY_PROPERTIES)

    cluster.http_retry_properties["conditions"].extend(conditions)
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
@exit_with_status
def remove_http_retry_conditions(
    cluster_name: str, conditions: List[HTTPRetryCondition]
) -> int:
    """Remove HTTP retry properties conditions."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    if not cluster.http_retry_properties:
        handle_manual_error(ERROR_MISSING_HTTP_RETRY_PROPERTIES)

    exit_code = 0
    success = False

    for condition in conditions:
        try:
            cluster.http_retry_properties["conditions"].remove(condition)
            success = True
        except ValueError:
            print_warning(f"HTTP retry condition '{condition}' not found, skipping.")
            exit_code = 64

    if not success:
        handle_manual_error("No HTTP retry conditions have been removed")

    cluster.update()

    return exit_code


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def add_custom_php_modules(
    cluster_name: str, custom_php_modules_names: List[PHPExtension]
) -> None:
    """Add custom PHP modules."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.custom_php_modules_names.extend(custom_php_modules_names)
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_php_ioncube(
    cluster_name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update PHP ionCube."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.php_ioncube_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_php_session_spread(
    cluster_name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update PHP session spread."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.php_sessions_spread_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_nodejs_version(
    cluster_name: str,
    nodejs_version: int,
) -> None:
    """Update NodeJS version."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.nodejs_version = nodejs_version
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def add_nodejs_versions(cluster_name: str, nodejs_versions: List[str]) -> None:
    """Add NodeJS versions."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.nodejs_versions.extend(nodejs_versions)
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
@exit_with_status
def remove_nodejs_versions(cluster_name: str, nodejs_versions: List[str]) -> int:
    """Remove NodeJS versions."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    exit_code = 0
    success = False

    for nodejs_version in nodejs_versions:
        try:
            cluster.nodejs_versions.remove(nodejs_version)
            success = True
        except ValueError:
            print_warning(f"NodeJS version '{nodejs_version}' not found, skipping.")
            exit_code = 64

    if not success:
        handle_manual_error("No NodeJS versions have been removed")

    cluster.update()

    return exit_code


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_wordpress_toolkit(
    cluster_name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update WordPress toolkit."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.wordpress_toolkit_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_automatic_borg_repositories_prune(
    cluster_name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update automatic Borg repositories prune."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.automatic_borg_repositories_prune_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_sync_toolkit(
    cluster_name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update sync toolkit."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.sync_toolkit_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_bubblewrap_toolkit(
    cluster_name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update Bubblewrap toolkit."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.bubblewrap_toolkit_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_mariadb_version(
    cluster_name: str,
    mariadb_version: str,
) -> None:
    """Update MariaDB version."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.mariadb_version = mariadb_version
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_mariadb_cluster_name(cluster_name: str, mariadb_cluster_name: str) -> None:
    """Update MariaDB cluster name."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.mariadb_cluster_name = mariadb_cluster_name
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_mariadb_backup_interval(
    cluster_name: str,
    mariadb_backup_interval: int,
) -> None:
    """Update MariaDB backup interval."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.mariadb_backup_interval = mariadb_backup_interval
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_postgresql_version(
    cluster_name: str,
    postgresql_version: str,
) -> None:
    """Update PostgreSQL version."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.postgresql_version = postgresql_version
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_postgresql_backup_interval(
    cluster_name: str,
    postgresql_backup_interval: int,
) -> None:
    """Update PostgreSQL backup interval."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.postgresql_backup_interval = postgresql_backup_interval
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_redis_memory_limit(
    cluster_name: str,
    redis_memory_limit: int,
) -> None:
    """Update Redis memory limit."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.redis_memory_limit = redis_memory_limit
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_redis_password(
    cluster_name: str,
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
) -> None:
    """Update Redis password."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.redis_password = password
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_database_toolkit(
    cluster_name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update database toolkit."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.database_toolkit_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_grafana_domain(
    cluster_name: str,
    grafana_domain: str,
) -> None:
    """Update Grafana domain."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.grafana_domain = grafana_domain
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_singlestore_studio_domain(
    cluster_name: str,
    singlestore_studio_domain: str,
) -> None:
    """Update SingleStore studio domain."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.singlestore_studio_domain = singlestore_studio_domain
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_singlestore_api_domain(
    cluster_name: str,
    singlestore_api_domain: str,
) -> None:
    """Update SingleStore API domain."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.singlestore_api_domain = singlestore_api_domain
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_singlestore_license_key(
    cluster_name: str,
    singlestore_license_key: str,
) -> None:
    """Update SingleStore license key."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.singlestore_license_key = singlestore_license_key
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_singlestore_root_password(
    cluster_name: str,
    singlestore_root_password: str,
) -> None:
    """Update SingleStore root password."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.singlestore_root_password = singlestore_root_password
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_metabase_domain(
    cluster_name: str,
    metabase_domain: str,
) -> None:
    """Update Metabase domain."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.metabase_domain = metabase_domain
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_metabase_database_password(
    cluster_name: str,
    metabase_database_password: str,
) -> None:
    """Update Metabase database password."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.metabase_database_password = metabase_database_password
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_kibana_domain(
    cluster_name: str,
    kibana_domain: str,
) -> None:
    """Update Kibana domain."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.kibana_domain = kibana_domain
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_rabbitmq_management_domain(
    cluster_name: str,
    rabbitmq_management_domain: str,
) -> None:
    """Update RabbitMQ management domain."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.rabbitmq_management_domain = rabbitmq_management_domain
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_rabbitmq_admin_password(
    cluster_name: str,
    rabbitmq_admin_password: str,
) -> None:
    """Update RabbitMQ admin password."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.rabbitmq_admin_password = rabbitmq_admin_password
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_rabbitmq_erlang_cookie(
    cluster_name: str,
    rabbitmq_erlang_cookie: str,
) -> None:
    """Update RabbitMQ Erlang cookie."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.rabbitmq_erlang_cookie = rabbitmq_erlang_cookie
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_new_relic_mariadb_password(
    cluster_name: str,
    new_relic_mariadb_password: str,
) -> None:
    """Update New Relic MariaDB password."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.new_relic_mariadb_password = new_relic_mariadb_password
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_new_relic_apm_license_key(
    cluster_name: str,
    new_relic_apm_license_key: str,
) -> None:
    """Update New Relic APM license key."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.new_relic_apm_license_key = new_relic_apm_license_key
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_new_relic_infrastructure_license_key(
    cluster_name: str,
    new_relic_infrastructure_license_key: str,
) -> None:
    """Update New Relic infrastructure license key."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.new_relic_infrastructure_license_key = new_relic_infrastructure_license_key
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_mariadb_backup_local_retention(
    cluster_name: str,
    mariadb_backup_local_retention: int,
) -> None:
    """Update MariaDB backup local retention."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.mariadb_backup_local_retention = mariadb_backup_local_retention
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_postgresql_backup_local_retention(
    cluster_name: str,
    postgresql_backup_local_retention: int,
) -> None:
    """Update PostgreSQL backup local retention."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.postgresql_backup_local_retention = postgresql_backup_local_retention
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_meilisearch_backup_local_retention(
    cluster_name: str,
    meilisearch_backup_local_retention: int,
) -> None:
    """Update Meilisearch backup local retention."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.meilisearch_backup_local_retention = meilisearch_backup_local_retention
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_elasticsearch_default_users_password(
    cluster_name: str,
    elasticsearch_default_users_password: str,
) -> None:
    """Update Elasticearch default users password."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.elasticsearch_default_users_password = elasticsearch_default_users_password
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_automatic_upgrades(
    cluster_name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update automatic upgrades."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.automatic_upgrades_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_firewall_rules_external_providers(
    cluster_name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update firewall rules external providers."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.firewall_rules_external_providers_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_meilisearch_master_key(
    cluster_name: str,
    meilisearch_master_key: str,
) -> None:
    """Update Meilisearch master key."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.meilisearch_master_key = meilisearch_master_key
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_meilisearch_environment(
    cluster_name: str,
    meilisearch_environment: MeilisearchEnvironment,
) -> None:
    """Update Meilisearch environment."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.meilisearch_environment = meilisearch_environment
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_meilisearch_backup_interval(
    cluster_name: str,
    meilisearch_backup_interval: int,
) -> None:
    """Update Meilisearch backup interval."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    cluster.meilisearch_backup_interval = meilisearch_backup_interval
    cluster.update()


@app.command()
@catch_api_exception
def delete(
    cluster_name: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete cluster."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    delete_api_object(obj=cluster, confirm=confirm)


@app.command(rich_help_panel=HELP_PANEL_SHOW)
@catch_api_exception
def unix_users_home_directories_usages(
    cluster_name: str,
    hours_before: Optional[int] = None,
    days_before: Optional[int] = None,
    amount: Optional[int] = typer.Option(default=None, show_default="All"),
) -> None:
    """Show UNIX users home directory usages.

    Using --hours-before OR --days-before is required.
    """
    cluster = get_object(get_support().clusters, name=cluster_name)

    timestamp, time_unit = get_usages_timestamp(
        days_before=days_before, hours_before=hours_before
    )

    usages = get_support().unix_users_home_directory_usages(
        cluster_id=cluster.id, timestamp=timestamp, time_unit=time_unit
    )[:amount]

    typer.echo(get_usages_plot(usages=usages))


@app.command(rich_help_panel=HELP_PANEL_SHOW)
@catch_api_exception
def get_common_properties() -> None:
    """Get clusters common properties."""
    cluster = Cluster(get_support())

    groups = {
        "IMAP": {
            "imap_hostname": "Hostname",
            "imap_port": "Port",
            "imap_encryption": "Encryption",
        },
        "POP3": {
            "pop3_hostname": "Hostname",
            "pop3_port": "Port",
            "pop3_encryption": "Encryption",
        },
        "SMTP": {
            "smtp_hostname": "Hostname",
            "smtp_port": "Port",
            "smtp_encryption": "Encryption",
        },
        "Databases": {"phpmyadmin_url": "phpMyAdmin URL"},
    }

    properties = cluster.get_common_properties()
    matched_properties = []

    for group in groups:
        table = Table(
            expand=True,
            show_lines=False,
            show_edge=False,
            box=None,
            show_header=False,
        )

        for key in groups[group]:
            table.add_row(groups[group][key], str(properties[key]))
            matched_properties.append(key)

        console.print(Panel(table, title=group, title_align="left"))

    unmatched_properties = [k for k in properties.keys() if k not in matched_properties]

    if len(unmatched_properties) > 0:
        table = Table(
            expand=True,
            show_lines=False,
            show_edge=False,
            box=None,
            show_header=False,
        )

        for key in unmatched_properties:
            table.add_row(key, str(properties[key]))

        console.print(Panel(table, title="Other", title_align="left"))


@app.command(rich_help_panel=HELP_PANEL_SHOW)
@catch_api_exception
def get_properties(cluster_name: str) -> None:
    """Get cluster properties."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    panels = {}

    panels["Generic"] = {
        "kernelcare_license_key": "KernelCare License Key",
        "automatic_upgrades_enabled": "Automatic Upgrades",
        "firewall_rules_external_providers_enabled": "Firewall Rules External Providers",
        "new_relic_infrastructure_license_key": "New Relic Infrastructure License Key",
        "new_relic_apm_license_key": "New Relic APM License Key",
    }

    if (
        ClusterGroup.WEB in cluster.groups
        or ClusterGroup.MAIL in cluster.groups
        or ClusterGroup.BORG_SERVER in cluster.groups
    ):
        panels["Groups: Web, Mail, Borg Server"] = {
            "unix_users_home_directory": "UNIX Users Home Directory"
        }

    if ClusterGroup.WEB in cluster.groups:
        panels["Group: Web"] = {
            "http_retry_properties": "HTTP Retry Properties",
            "wordpress_toolkit_enabled": "WordPress Toolkit",
            "bubblewrap_toolkit_enabled": "Bubblewrap Toolkit",
        }
        panels["Group: Web (PHP)"] = {
            "php_versions": "Versions",
            "custom_php_modules_names": "Custom Modules",
            "php_settings": "Settings",
            "php_ioncube_enabled": "ionCube Enabled",
            "php_sessions_spread_enabled": "Session Spreading",
        }
        panels["Group: Web (NodeJS)"] = {
            "nodejs_version": "Version",
            "nodejs_versions": "Versions",
        }

    if ClusterGroup.DB in cluster.groups:
        panels["Group: Database (New Relic)"] = {
            "new_relic_mariadb_password": "MariaDB Password"
        }
        panels["Group: Database (MariaDB)"] = {
            "mariadb_version": "Version",
            "mariadb_cluster_name": "Cluster Name",
            "mariadb_backup_interval": "Backup Interval",
            "mariadb_backup_local_retention": "Local Backup Retention",
        }
        panels["Group: Database (PostgreSQL)"] = {
            "postgresql_version": "Version",
            "postgresql_backup_interval": "Backup Interval",
            "postgresql_backup_local_retention": "Local Backup Retention",
        }
        panels["Group: Database (Redis)"] = {
            "redis_password": "Password",
            "redis_memory_limit": "Memory Limit",
        }
        panels["Group: Database"] = {"database_toolkit_enabled": "Database Toolkit"}
        panels["Group: Database (Meilisearch)"] = {
            "meilisearch_backup_interval": "Backup Interval",
            "meilisearch_backup_local_retention": "Local Backup Retention",
            "meilisearch_master_key": "Master Key",
            "meilisearch_environment": "Environment",
        }
        panels["Group: Database (Grafana)"] = {"grafana_domain": "Domain"}
        panels["Group: Database (SingleStore)"] = {
            "singlestore_studio_domain": "Studio Domain",
            "singlestore_api_domain": "API Domain",
            "singlestore_license_key": "License Key",
            "singlestore_root_password": "Root Password",
        }
        panels["Group: Database (Elasticsearch)"] = {
            "elasticsearch_default_users_password": "Default Users Password"
        }
        panels["Group: Database (RabbitMQ)"] = {
            "rabbitmq_erlang_cookie": "Erlang Cookie",
            "rabbitmq_admin_password": "Admin Password",
            "rabbitmq_management_domain": "Management Domain",
        }
        panels["Group: Database (Metabase)"] = {
            "metabase_domain": "Domain",
            "metabase_database_password": "Database Password",
        }
        panels["Group: Database (Kibana)"] = {"kibana_domain": "Domain"}
    if ClusterGroup.BORG_CLIENT in cluster.groups:
        panels["Group: Borg Client"] = {
            "automatic_borg_repositories_prune_enabled": "Automatic Borg Repositories Prune"
        }

    if ClusterGroup.WEB in cluster.groups or ClusterGroup.DB in cluster.groups:
        panels["Groups: Web, Database"] = {"sync_toolkit_enabled": "Sync Toolkit"}

    for title, attributes in panels.items():
        table = Table(
            expand=True,
            show_lines=False,
            show_edge=False,
            box=None,
            show_header=False,
        )

        for attribute, name in attributes.items():
            value = getattr(cluster, attribute)

            if isinstance(value, dict):
                _value = []

                for k, v in value.items():
                    _value.append(f"{k}: {v}")

                value = "\n".join(_value)
            elif isinstance(value, list):
                value = "\n".join(value)
            else:
                if value is None:
                    value = "None"
                else:
                    value = str(value)

            table.add_row(name, value)

        console.print(Panel(table, title=title, title_align="left"))


@app.command(rich_help_panel=HELP_PANEL_IP_ADDRESSES)
@catch_api_exception
def list_ip_addresses_products(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """List IP addresses products."""
    console.print(
        get_support().get_table(
            objs=get_support().cluster_ip_addresses_products, detailed=detailed
        )
    )


@app.command(rich_help_panel=HELP_PANEL_IP_ADDRESSES)
@catch_api_exception
def list_ip_addresses(cluster_name: str) -> None:
    """List IP addresses."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    ip_addresses = cluster.get_ip_addresses()

    table = Table(
        expand=True,
        show_lines=False,
        show_edge=False,
        box=None,
    )

    for column in [
        "Service Account Group",
        "Service Account Name",
        "IP Address",
        "DNS Name",
        "Default",
    ]:
        table.add_column(column, overflow="fold")

    for service_account_group, service_accounts in ip_addresses.items():
        for service_account_name, ip_addresses in service_accounts.items():
            for ip_address in ip_addresses:
                table.add_row(
                    service_account_group,
                    service_account_name,
                    ip_address["ip_address"],
                    ip_address["dns_name"],
                    str(not ip_address["dns_name"]),
                )

    console.print(Panel(table, title="IP Addresses", title_align="left"))


@app.command(rich_help_panel=HELP_PANEL_IP_ADDRESSES)
@catch_api_exception
def create_ip_address(
    cluster_name: str,
    service_account_name: str,
    dns_name: str,
    address_family: IPAddressFamily,
) -> None:
    """Create IP address."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    task_collection = cluster.create_ip_address(
        service_account_name=service_account_name,
        dns_name=dns_name,
        address_family=address_family,
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command(rich_help_panel=HELP_PANEL_IP_ADDRESSES)
@catch_api_exception
def delete_ip_address(cluster_name: str, ip_address: str) -> None:
    """Delete IP address."""
    cluster = get_object(get_support().clusters, name=cluster_name)

    task_collection = cluster.delete_ip_address(ip_address=ip_address)

    wait_for_task(task_collection_uuid=task_collection.uuid)
