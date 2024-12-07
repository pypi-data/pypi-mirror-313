"""Command line interface for the Cyberfusion Core API."""

import configparser
import json
import os
import shutil
import subprocess
from typing import List, Optional

import typer

from cyberfusion.ClusterApiCli import METHOD_DELETE, ClusterApiCallException
from cyberfusion.Common import get_tmp_file
from cyberfusion.CoreCli import (
    api_users,
    basic_authentication_realms,
    borg,
    certificate_managers,
    certificates,
    clusters,
    cmses,
    crons,
    custom_config_snippets,
    custom_configs,
    customers,
    daemons,
    databases,
    domain_routers,
    firewall_groups,
    firewall_rules,
    fpm_pools,
    ftp_users,
    haproxy_listens,
    hosts_entries,
    htpasswd,
    logs,
    mail,
    malwares,
    mariadb_encryption_keys,
    nodes,
    passenger_apps,
    redis_instances,
    security_txt_policies,
    sites,
    ssh_keys,
    task_collections,
    unix_users,
    url_redirects,
    virtual_hosts,
)
from cyberfusion.CoreCli._utilities import (
    DETAILED_MESSAGE,
    PATH_CONFIG_LOCAL,
    PATH_DIRECTORY_CONFIG_CLI,
    PATH_DIRECTORY_CONFIG_GENERIC,
    HttpMethod,
    catch_api_exception,
    console,
    get_package_version,
    get_support,
    handle_manual_error,
    state,
)

HELP_PANEL_CLI_MANAGEMENT = "CLI Management"

NAME_COMMAND_API_USERS = "api-users"
NAME_COMMAND_BASIC_AUTHENTICATION_REALMS = "basic-authentication-realms"
NAME_COMMAND_BORG = "borg"
NAME_COMMAND_CERTIFICATES = "certificates"
NAME_COMMAND_CERTIFICATE_MANAGERS = "certificate-managers"
NAME_COMMAND_CLUSTERS = "clusters"
NAME_COMMAND_CMSES = "cmses"
NAME_COMMAND_CRONS = "crons"
NAME_COMMAND_TASK_COLLECTIONS = "task-collections"
NAME_COMMAND_HOSTS_ENTRIES = "hosts-entries"
NAME_COMMAND_MARIADB_ENCRYPTION_KEYS = "mariadb-encryption-keys"
NAME_COMMAND_SECURITY_TXT_POLICIES = "security-txt-policies"
NAME_COMMAND_CUSTOM_CONFIG_SNIPPETS = "custom-config-snippets"
NAME_COMMAND_CUSTOM_CONFIGS = "custom-configs"
NAME_COMMAND_CUSTOMERS = "customers"
NAME_COMMAND_DATABASES = "databases"
NAME_COMMAND_DOMAIN_ROUTERS = "domain-routers"
NAME_COMMAND_FIREWALL_GROUPS = "firewall-groups"
NAME_COMMAND_FPM_POOLS = "fpm-pools"
NAME_COMMAND_FTP_USERS = "ftp-users"
NAME_COMMAND_HAPROXY_LISTENS = "haproxy-listens"
NAME_COMMAND_HTPASSWD = "htpasswd"
NAME_COMMAND_LOGS = "logs"
NAME_COMMAND_MAIL = "mail"
NAME_COMMAND_MALWARES = "malwares"
NAME_COMMAND_SITES = "sites"
NAME_COMMAND_NODES = "nodes"
NAME_COMMAND_PASSENGER_APPS = "passenger-apps"
NAME_COMMAND_REDIS_INSTANCES = "redis-instances"
NAME_COMMAND_FIREWALL_RULES = "firewall-rules"
NAME_COMMAND_SSH_KEYS = "ssh-keys"
NAME_COMMAND_UNIX_USERS = "unix-users"
NAME_COMMAND_URL_REDIRECTS = "url-redirects"
NAME_COMMAND_VIRTUAL_HOSTS = "virtual-hosts"
NAME_COMMAND_DAEMONS = "daemons"

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.callback()
def callback(
    clusters_names: List[str] = typer.Option(
        [],
        "--cluster-name",
        "-c",
        help="Cluster name to operate on. To operate on all clusters, do not set.",
    ),
) -> None:
    """Cyberfusion Core API CLI."""
    state["clusters_names"] = clusters_names


app.add_typer(clusters.app, name=NAME_COMMAND_CLUSTERS, help="Clusters")
app.add_typer(
    virtual_hosts.app,
    name=NAME_COMMAND_VIRTUAL_HOSTS,
    help="Virtual Hosts",
)
app.add_typer(fpm_pools.app, name=NAME_COMMAND_FPM_POOLS, help="FPM Pools")
app.add_typer(unix_users.app, name=NAME_COMMAND_UNIX_USERS, help="UNIX Users")
app.add_typer(logs.app, name=NAME_COMMAND_LOGS, help="Logs")
app.add_typer(
    certificates.app,
    name=NAME_COMMAND_CERTIFICATES,
    help="Certificates",
)
app.add_typer(
    certificate_managers.app,
    name=NAME_COMMAND_CERTIFICATE_MANAGERS,
    help="Certificate Managers",
)
app.add_typer(
    url_redirects.app,
    name=NAME_COMMAND_URL_REDIRECTS,
    help="URL Redirects",
)
app.add_typer(
    crons.app,
    name=NAME_COMMAND_CRONS,
    help="Crons",
)
app.add_typer(
    task_collections.app,
    name=NAME_COMMAND_TASK_COLLECTIONS,
    help="Task Collections",
)
app.add_typer(
    hosts_entries.app,
    name=NAME_COMMAND_HOSTS_ENTRIES,
    help="Hosts Entries",
)
app.add_typer(
    mariadb_encryption_keys.app,
    name=NAME_COMMAND_MARIADB_ENCRYPTION_KEYS,
    help="MariaDB Encryption Keys",
)
app.add_typer(
    security_txt_policies.app,
    name=NAME_COMMAND_SECURITY_TXT_POLICIES,
    help="Security TXT Policies",
)
app.add_typer(databases.app, name=NAME_COMMAND_DATABASES, help="Databases")
app.add_typer(cmses.app, name=NAME_COMMAND_CMSES, help="CMSes")
app.add_typer(
    passenger_apps.app,
    name=NAME_COMMAND_PASSENGER_APPS,
    help="Passenger Apps",
)
app.add_typer(nodes.app, name=NAME_COMMAND_NODES, help="Nodes")
app.add_typer(malwares.app, name=NAME_COMMAND_MALWARES, help="Malwares")
app.add_typer(sites.app, name=NAME_COMMAND_SITES, help="Sites")
app.add_typer(ssh_keys.app, name=NAME_COMMAND_SSH_KEYS, help="SSH Keys")
app.add_typer(mail.app, name=NAME_COMMAND_MAIL, help="Mail")
app.add_typer(borg.app, name=NAME_COMMAND_BORG, help="Borg")
app.add_typer(
    redis_instances.app,
    name=NAME_COMMAND_REDIS_INSTANCES,
    help="Redis Instances",
)
app.add_typer(
    firewall_rules.app,
    name=NAME_COMMAND_FIREWALL_RULES,
    help="Firewall Rules",
)
app.add_typer(htpasswd.app, name=NAME_COMMAND_HTPASSWD, help="Htpasswd")
app.add_typer(
    basic_authentication_realms.app,
    name=NAME_COMMAND_BASIC_AUTHENTICATION_REALMS,
    help="Basic Authentication Realms",
)
app.add_typer(
    firewall_groups.app,
    name=NAME_COMMAND_FIREWALL_GROUPS,
    help="Firewall Groups",
)
app.add_typer(ftp_users.app, name=NAME_COMMAND_FTP_USERS, help="FTP Users")
app.add_typer(
    domain_routers.app,
    name=NAME_COMMAND_DOMAIN_ROUTERS,
    help="Domain Routers",
)
app.add_typer(
    custom_config_snippets.app,
    name=NAME_COMMAND_CUSTOM_CONFIG_SNIPPETS,
    help="Custom Config Snippets",
)
app.add_typer(
    custom_configs.app,
    name=NAME_COMMAND_CUSTOM_CONFIGS,
    help="Custom Configs",
)
app.add_typer(
    customers.app,
    name=NAME_COMMAND_CUSTOMERS,
    help="Customers",
)
app.add_typer(
    haproxy_listens.app,
    name=NAME_COMMAND_HAPROXY_LISTENS,
    help="HAProxy Listens",
)
app.add_typer(
    api_users.app,
    name=NAME_COMMAND_API_USERS,
    help="API Users",
    hidden=True,
)

app.add_typer(daemons.app, name=NAME_COMMAND_DAEMONS, help="Daemons")


@app.command()
@catch_api_exception
def tombstones(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show Tombstones"""
    console.print(
        get_support().get_table(
            objs=get_support().tombstones,
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_CLI_MANAGEMENT)
@catch_api_exception
def update() -> None:
    """Update CLI to Latest Version"""
    original_version = get_package_version()

    output = subprocess.run(
        ["pipx", "upgrade", "python3-cyberfusion-corectl"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )

    new_version = get_package_version()

    if output.stdout.startswith("upgraded package"):
        console.print(f"CLI updated from version {original_version} to {new_version}.")
    elif "is already at latest version" in output.stdout:
        console.print(f"CLI already up to date (version {original_version}).")


@app.command(rich_help_panel=HELP_PANEL_CLI_MANAGEMENT)
def setup(
    api_user_username: str = typer.Option(
        ...,
        "--username",
        "-u",
        prompt="API username",
    ),
    api_user_password: str = typer.Option(
        ...,
        "--password",
        "-p",
        prompt="API password",
        hide_input=True,
    ),
) -> None:
    """Set Up CLI with Core API Credentials"""
    exists = os.path.exists(PATH_CONFIG_LOCAL)

    # Create directories which contain config file

    if not exists:
        for directory in [
            PATH_DIRECTORY_CONFIG_GENERIC,
            PATH_DIRECTORY_CONFIG_CLI,
        ]:
            if os.path.exists(directory):
                continue

            os.mkdir(directory)
            os.chmod(directory, 0o700)

    # Write credentials to config file

    config = configparser.ConfigParser()

    config["clusterapi"] = {}
    config["clusterapi"]["serverurl"] = "https://core-api.cyberfusion.io"
    config["clusterapi"]["username"] = api_user_username
    config["clusterapi"]["password"] = api_user_password

    tmp_file_path = get_tmp_file()

    with open(tmp_file_path, "w") as file:
        config.write(file)

    # Test API credentials

    try:
        get_support(tmp_file_path).request.api_user_info  # Do any request
    except ClusterApiCallException as e:
        handle_manual_error(e.body["detail"] + " The config file was not written.")

    # Create and set permissions on config file before writing to it

    with open(PATH_CONFIG_LOCAL, "w"):
        pass

    os.chmod(PATH_CONFIG_LOCAL, 0o600)

    # Copy config

    shutil.copyfile(tmp_file_path, PATH_CONFIG_LOCAL)

    # Show message

    message = "Config file created. You can now use the CLI."

    if exists:
        message += " (Overwrote existing config file)"

    console.print(message)


@app.command()
@catch_api_exception
def request(
    method: HttpMethod,
    path: str,
    data: Optional[str] = typer.Option(default=None),
) -> None:
    """Manually Call API Endpoint"""
    parsed_data = {}

    if data:
        parsed_data = json.loads(data)

    if not path.startswith("/"):
        path = "/" + path

    func = getattr(get_support().request, method)

    if method == METHOD_DELETE:
        func(path)
    else:
        func(path, parsed_data)

    response = get_support().request.execute()

    console.print(response)


# Run when running this outside of setup.py console_scripts

if __name__ == "__main__":
    app()
