"""CMSes subcommands."""

import webbrowser
from enum import Enum
from typing import Optional, Union

import typer
from rich.panel import Panel
from rich.table import Table

from cyberfusion.ClusterSupport.cmses import (
    CMS,
    CMSOptionName,
    CMSSoftwareName,
)
from cyberfusion.ClusterSupport.virtual_hosts import (
    VirtualHostServerSoftwareName,
)
from cyberfusion.Common import generate_random_string
from cyberfusion.CoreCli._utilities import (
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    RANDOM_PASSWORD_MESSAGE,
    WordPressVersionStatus,
    catch_api_exception,
    check_wordpress_version,
    console,
    delete_api_object,
    get_cms_by_virtual_host_domain,
    get_latest_wordpress_version,
    get_object,
    get_support,
    handle_manual_error,
    print_warning,
    wait_for_task,
)

WORDPRESS_NGINX_CONFIG_COMMENT = "# WordPress Permalinks"
WORDPRESS_NGINX_CONFIG_LINE = "try_files $uri $uri/ /index.php?$args;"

app = typer.Typer()


@app.command("list")
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List CMSes."""
    console.print(get_support().get_table(objs=get_support().cmses, detailed=detailed))


@app.command()
@catch_api_exception
def get(
    virtual_host_domain: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show CMS."""
    console.print(
        get_support().get_table(
            objs=[
                get_cms_by_virtual_host_domain(
                    virtual_host_domain,
                )
            ],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create(
    virtual_host_domain: str,
    software_name: CMSSoftwareName = typer.Argument(default=..., case_sensitive=False),
    update_virtual_host_config: bool = typer.Option(
        True,
        "--update-virtual-host-config/--dont-update-virtual-host-config",
        help=f"Add `{WORDPRESS_NGINX_CONFIG_LINE}` to the virtual host custom config (when using nginx).",
    ),
) -> None:
    """Create CMS."""
    cms = CMS(get_support())
    virtual_host = get_object(get_support().virtual_hosts, domain=virtual_host_domain)

    cms.create(
        software_name=software_name,
        virtual_host_id=virtual_host.id,
        is_manually_created=True,
    )

    if not update_virtual_host_config:
        return

    if virtual_host.server_software_name != VirtualHostServerSoftwareName.NGINX:
        return

    if virtual_host.custom_config:
        # If config line is already present, no need to update

        for line in virtual_host.custom_config.splitlines():
            if line.lstrip() != WORDPRESS_NGINX_CONFIG_LINE:
                continue

            return
    else:
        # No custom config yet; set empty custom config so that we can use +=
        # below

        virtual_host.custom_config = ""

    virtual_host.custom_config += (
        f"\n{WORDPRESS_NGINX_CONFIG_COMMENT}\n{WORDPRESS_NGINX_CONFIG_LINE}"
    )
    virtual_host.update()

    console.print(
        get_support().get_table(
            objs=[cms],
            detailed=True,
        )
    )


class CMSLocaleEnum(str, Enum):
    """Enum for CMS locales."""

    EN_US = "en_US"
    NL_NL = "nl_NL"


@app.command()
@catch_api_exception
def install_wordpress(
    virtual_host_domain: str,
    database_name: str = typer.Option(default=..., prompt=True),
    database_user_name: str = typer.Option(default=..., prompt=True),
    database_user_password: str = typer.Option(
        default=...,
        prompt=True,
        hide_input=True,
    ),
    database_host: str = typer.Option(default="::1", prompt=True),
    site_title: str = typer.Option(default=..., prompt=True),
    site_url: str = typer.Option(default=..., prompt="Site URL"),
    locale: CMSLocaleEnum = typer.Option(
        default=CMSLocaleEnum.EN_US,
        prompt=True,
        show_default="en_US",
        show_choices=False,
    ),
    version: str = typer.Option(
        default="latest",
        prompt="Version (use `latest` for the latest version)",
        help="Specify version number or `latest` for the latest version of the CMS",
    ),
    admin_username: str = typer.Option(default="admin", prompt=True),
    admin_password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
    admin_email_address: str = typer.Option(
        default="admin@example.com",
        prompt=True,
    ),
    allow_insecure_version: bool = typer.Option(
        False,
        "--allow-insecure-version/--forbid-insecure-version",
        help="Allow insecure version to be installed",
    ),
) -> None:
    """Install WordPress.

    When not passing all the options, the command will work interactively.
    """

    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    # Check and/or fill version

    if version == "latest":
        if cms.software_name != CMSSoftwareName.WP:
            handle_manual_error("Latest version is only supported when using WordPress")

        version = get_latest_wordpress_version()

    version_status = check_wordpress_version(version)

    if version_status is None:
        print_warning(
            "Can't fetch WordPress versions. Version checking is disabled.",
        )
    elif version_status == WordPressVersionStatus.INSECURE:
        if not allow_insecure_version:
            handle_manual_error(
                "Insecure WordPress version selected. Select a newer version or use --allow-insecure-version"
            )

        print_warning("Insecure WordPress version selected.")
    elif version_status == WordPressVersionStatus.OUTDATED:
        print_warning("WordPress version outdated.")

    task_collection = cms.install_wordpress(
        database_name=database_name,
        database_user_name=database_user_name,
        database_user_password=database_user_password,
        database_host=database_host,
        site_title=site_title,
        site_url=site_url,
        locale=locale,
        version=version,
        admin_username=admin_username,
        admin_password=admin_password,
        admin_email_address=admin_email_address,
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command()
@catch_api_exception
def install_nextcloud(
    virtual_host_domain: str,
    database_name: str = typer.Option(default=..., prompt=True),
    database_user_name: str = typer.Option(default=..., prompt=True),
    database_user_password: str = typer.Option(
        default=...,
        prompt=True,
        hide_input=True,
    ),
    database_host: str = typer.Option(default="::1", prompt=True),
    admin_username: str = typer.Option(default="admin", prompt=True),
    admin_password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
) -> None:
    """Install NextCloud.

    When not passing all the options, the command will work interactively.
    """
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    task_collection = cms.install_nextcloud(
        database_name=database_name,
        database_user_name=database_user_name,
        database_user_password=database_user_password,
        database_host=database_host,
        admin_username=admin_username,
        admin_password=admin_password,
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command()
@catch_api_exception
def login(virtual_host_domain: str) -> None:
    """Get one time login URL."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    webbrowser.open(cms.get_one_time_login_url())


@app.command()
@catch_api_exception
def search_replace(
    virtual_host_domain: str, search_string: str, replace_string: str
) -> None:
    """Search & replace in CMS."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    task_collection = cms.search_replace(
        search_string=search_string, replace_string=replace_string
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command()
@catch_api_exception
def update_core(
    virtual_host_domain: str,
) -> None:
    """Update CMS core."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    task_collection = cms.update_core()

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command()
@catch_api_exception
def update_plugin(virtual_host_domain: str, plugin_name: str) -> None:
    """Update CMS plugin."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    task_collection = cms.update_plugin(
        name=plugin_name,
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command()
@catch_api_exception
def enable_plugin(virtual_host_domain: str, plugin_name: str) -> None:
    """Enable CMS plugin."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    cms.enable_plugin(name=plugin_name)


@app.command()
@catch_api_exception
def disable_plugin(virtual_host_domain: str, plugin_name: str) -> None:
    """Disable CMS plugin."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    cms.disable_plugin(name=plugin_name)


@app.command()
@catch_api_exception
def update_configuration_constant(
    virtual_host_domain: str,
    name: str,
    value: str,
    index: Optional[int] = None,
) -> None:
    """Update CMS configuration constant."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    _value: Union[int, bool, str, float] = value

    if value.isdigit():
        _value = int(value)
    elif value == "true":
        _value = True
    elif value == "false":
        _value = False

    if isinstance(_value, str):
        try:
            _value = float(value)
        except ValueError:
            pass

    cms.update_configuration_constant(name=name, value=_value, index=index)


@app.command()
@catch_api_exception
def update_option(virtual_host_domain: str, name: CMSOptionName, value: str) -> None:
    """Update CMS option."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    cms.update_option(name=name, value=value)


@app.command()
@catch_api_exception
def get_plugins(
    virtual_host_domain: str,
) -> None:
    """Get plugins."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    plugins = cms.get_plugins()

    table = Table(
        expand=True,
        show_lines=False,
        show_edge=False,
        box=None,
    )

    for column in [
        "Name",
        "Current Version",
        "Update Available",
        "Enabled",
    ]:
        table.add_column(column, overflow="fold")

    for plugin in plugins:
        table.add_row(
            plugin["name"],
            plugin["current_version"],
            (plugin["available_version"] if plugin["available_version"] else "No"),
            str(plugin["is_enabled"]),
        )

    console.print(Panel(table, title="Plugins", title_align="left"))


@app.command()
@catch_api_exception
def update_user_password(
    virtual_host_domain: str,
    user_id: int,
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
) -> None:
    """Update CMS user password."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    cms.update_user_credentials(user_id=user_id, password=password)


@app.command()
@catch_api_exception
def regenerate_salts(virtual_host_domain: str) -> None:
    """Regenerate CMS salts."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    cms.regenerate_salts()


@app.command()
@catch_api_exception
def install_theme_from_repository(
    virtual_host_domain: str, name: str, version: Optional[str] = None
) -> None:
    """Install CMS theme from repository."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    cms.install_theme_from_repository(name=name, version=version)


@app.command()
@catch_api_exception
def install_theme_from_url(virtual_host_domain: str, url: str) -> None:
    """Install CMS theme from URL."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    cms.install_theme_from_url(url=url)


@app.command()
@catch_api_exception
def delete(
    virtual_host_domain: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete CMS."""
    cms = get_cms_by_virtual_host_domain(virtual_host_domain)

    delete_api_object(obj=cms, confirm=confirm)
