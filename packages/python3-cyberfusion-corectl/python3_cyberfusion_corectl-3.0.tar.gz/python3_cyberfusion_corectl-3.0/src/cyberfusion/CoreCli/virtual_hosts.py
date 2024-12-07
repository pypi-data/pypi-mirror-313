"""Virtual hosts subcommands."""

import os
from pathlib import Path
from typing import List, Optional

import typer

from cyberfusion.ClusterSupport.unix_users import UNIXUser
from cyberfusion.ClusterSupport.virtual_hosts import (
    AllowOverrideDirective,
    AllowOverrideOptionDirective,
    VirtualHost,
    VirtualHostServerSoftwareName,
)
from cyberfusion.CoreCli._utilities import (
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    EMPTY_TO_CLEAR_MESSAGE,
    catch_api_exception,
    confirm_clear,
    console,
    delete_api_object,
    get_first_found_virtual_host_server_software,
    get_object,
    get_support,
    handle_manual_error,
    print_warning,
    wait_for_task,
)

app = typer.Typer()


def get_virtual_hosts_by_domain_or_server_alias(
    domain_or_server_alias: str,
) -> Optional[VirtualHost]:
    """Get virtual hosts by domain or server alias."""
    by_domain = get_support()._filter_objects(
        get_support().virtual_hosts, domain=domain_or_server_alias
    )
    by_server_alias = get_support()._filter_objects(
        get_support().virtual_hosts, server_aliases=domain_or_server_alias
    )

    return by_domain or by_server_alias or None


def get_virtual_host(domain_or_server_alias: str) -> VirtualHost:
    """Get virtual host by domain or server alias."""
    virtual_hosts = get_virtual_hosts_by_domain_or_server_alias(domain_or_server_alias)

    if virtual_hosts:
        return virtual_hosts[0]

    handle_manual_error(f"Object '{domain_or_server_alias}' not found")


@app.command("list")
@catch_api_exception
def list_(detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)) -> None:
    """List virtual hosts."""
    console.print(
        get_support().get_table(
            objs=get_support().virtual_hosts,
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get(
    domain: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show virtual host."""
    console.print(
        get_support().get_table(
            objs=[get_virtual_host(domain)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get_document_root(domain: str) -> None:
    """Show document root of virtual host."""
    document_root = get_virtual_host(domain).get_document_root_contains_files()

    for property_ in document_root:
        console.print(f"{property_}: {document_root[property_]}")


@app.command()
@catch_api_exception
def get_custom_config(domain: str) -> None:
    """Show custom config."""
    virtual_host = get_virtual_host(domain)

    console.print(virtual_host.custom_config)


@app.command()
@catch_api_exception
def create(
    domain: str,
    server_software_name: Optional[VirtualHostServerSoftwareName] = typer.Option(
        default=None, help="Default is first found server software"
    ),
    add_www: bool = typer.Option(True, "--add-www/--dont-add-www"),
    document_root_relative: str = typer.Option(
        "htdocs",
        "--document-root",
        help="Relative to UNIX user virtual hosts directory + domain",
    ),
    custom_config_file: Optional[Path] = typer.Option(
        None, exists=True, dir_okay=False
    ),
    unix_user_username: str = typer.Argument(default=...),
) -> None:
    """Create virtual host."""
    unix_user = get_object(get_support().unix_users, username=unix_user_username)

    document_root = _get_document_root(
        base_root=_get_base_root(unix_user=unix_user, domain=domain),
        document_root=document_root_relative,
    )

    create_virtual_host(
        domain=domain,
        unix_user=unix_user,
        server_software_name=(
            server_software_name.value if server_software_name is not None else None
        ),
        add_www=add_www,
        document_root=document_root,
        fpm_pool_id=None,
        passenger_app_id=None,
        custom_config_file=custom_config_file,
    )


@app.command()
@catch_api_exception
def create_fpm_pool(
    domain: str,
    server_software_name: Optional[VirtualHostServerSoftwareName] = typer.Option(
        default=None, help="Default is first found server software"
    ),
    add_www: bool = typer.Option(True, "--add-www/--dont-add-www"),
    document_root_relative: str = typer.Option(
        "htdocs",
        "--document-root",
        help="Relative to UNIX user virtual hosts directory + domain",
    ),
    custom_config_file: Optional[Path] = typer.Option(
        None, exists=True, dir_okay=False
    ),
    unix_user_username: str = typer.Argument(default=...),
    fpm_pool_name: str = typer.Argument(default=...),
) -> None:
    """Create virtual host with FPM pool."""
    fpm_pool = get_object(get_support().fpm_pools, name=fpm_pool_name)
    unix_user = get_object(get_support().unix_users, username=unix_user_username)

    document_root = _get_document_root(
        base_root=_get_base_root(unix_user=unix_user, domain=domain),
        document_root=document_root_relative,
    )

    create_virtual_host(
        domain=domain,
        unix_user=unix_user,
        server_software_name=(
            server_software_name.value if server_software_name is not None else None
        ),
        add_www=add_www,
        document_root=document_root,
        fpm_pool_id=fpm_pool.id,
        passenger_app_id=None,
        custom_config_file=custom_config_file,
    )


@app.command()
@catch_api_exception
def create_passenger_app(
    domain: str,
    server_software_name: Optional[VirtualHostServerSoftwareName] = typer.Option(
        default=None, help="Default is first found server software"
    ),
    add_www: bool = typer.Option(True, "--add-www/--dont-add-www"),
    document_root_relative: str = typer.Option(
        "public",
        "--document-root",
        help="Relative to Passenger app root",
    ),
    custom_config_file: Optional[Path] = typer.Option(
        None, exists=True, dir_okay=False
    ),
    unix_user_username: str = typer.Argument(default=...),
    passenger_app_name: str = typer.Argument(default=...),
) -> None:
    """Create virtual host with Passenger app."""
    passenger_app = get_object(get_support().passenger_apps, name=passenger_app_name)
    unix_user = get_object(get_support().unix_users, username=unix_user_username)

    document_root = _get_document_root(
        base_root=passenger_app.app_root,
        document_root=document_root_relative,
    )

    create_virtual_host(
        domain=domain,
        unix_user=unix_user,
        server_software_name=(
            server_software_name.value if server_software_name is not None else None
        ),
        add_www=add_www,
        document_root=document_root,
        fpm_pool_id=None,
        passenger_app_id=passenger_app.id,
        custom_config_file=custom_config_file,
    )


def create_virtual_host(
    domain: str,
    unix_user: UNIXUser,
    server_software_name: Optional[VirtualHostServerSoftwareName],
    add_www: bool,
    document_root: str,
    fpm_pool_id: Optional[int],
    passenger_app_id: Optional[int],
    custom_config_file: Optional[Path],
) -> None:
    """Create virtual host."""
    virtual_host = VirtualHost(get_support())

    # Set server aliases

    server_aliases = []

    if add_www:
        server_aliases.append(f"www.{domain}")

    # Set custom config

    custom_config = None

    if custom_config_file:
        custom_config = custom_config_file.read_text()

    # Set server software name

    if server_software_name is None:
        server_software_name = get_first_found_virtual_host_server_software(
            cluster_id=unix_user.cluster_id
        )

    # Set allow_override_directives + allow_override_option_directives

    allow_override_directives: Optional[List[AllowOverrideDirective]]
    allow_override_option_directives: Optional[List[AllowOverrideOptionDirective]]

    if server_software_name == VirtualHostServerSoftwareName.NGINX:
        allow_override_directives = None
        allow_override_option_directives = None
    else:
        allow_override_directives = [
            AllowOverrideDirective.AUTHCONFIG,
            AllowOverrideDirective.FILEINFO,
            AllowOverrideDirective.INDEXES,
            AllowOverrideDirective.LIMIT,
        ]
        allow_override_option_directives = [
            AllowOverrideOptionDirective.INDEXES,
            AllowOverrideOptionDirective.MULTIVIEWS,
            AllowOverrideOptionDirective.NONE,
            AllowOverrideOptionDirective.SYMLINKSIFOWNERMATCH,
        ]

    virtual_host.create(
        domain=domain,
        server_aliases=server_aliases,
        unix_user_id=unix_user.id,
        document_root=document_root,
        public_root=_get_public_root(
            base_root=_get_base_root(unix_user=unix_user, domain=domain)
        ),
        fpm_pool_id=fpm_pool_id,
        passenger_app_id=passenger_app_id,
        server_software_name=server_software_name,
        custom_config=custom_config,
        allow_override_directives=allow_override_directives,
        allow_override_option_directives=allow_override_option_directives,
    )

    console.print(
        get_support().get_table(
            objs=[virtual_host],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def add_server_alias(domain: str, server_alias: str) -> None:
    """Add server alias."""
    virtual_host = get_virtual_host(domain)

    virtual_host.server_aliases.append(server_alias)
    virtual_host.update()


@app.command()
@catch_api_exception
def remove_server_alias(domain: str, server_alias: str) -> None:
    """Remove server alias."""
    virtual_host = get_virtual_host(domain)

    try:
        virtual_host.server_aliases.remove(server_alias)
    except ValueError:
        handle_manual_error(f"Server alias '{server_alias}' not found")

    virtual_host.update()


@app.command()
@catch_api_exception
def add_allow_override_directive(
    domain: str, allow_override_directive: AllowOverrideDirective
) -> None:
    """Add allow override directive."""
    virtual_host = get_virtual_host(domain)

    virtual_host.allow_override_directives.append(allow_override_directive)
    virtual_host.update()


@app.command()
@catch_api_exception
def remove_allow_override_directive(
    domain: str, allow_override_directive: AllowOverrideDirective
) -> None:
    """Remove allow override directive."""
    virtual_host = get_virtual_host(domain)

    try:
        virtual_host.allow_override_directives.remove(allow_override_directive)
    except ValueError:
        handle_manual_error("Allow override directive not found")

    virtual_host.update()


@app.command()
@catch_api_exception
def add_allow_override_option_directive(
    domain: str, allow_override_option_directive: AllowOverrideOptionDirective
) -> None:
    """Add allow override option directive."""
    virtual_host = get_virtual_host(domain)

    virtual_host.allow_override_option_directives.append(
        allow_override_option_directive
    )
    virtual_host.update()


@app.command()
@catch_api_exception
def remove_allow_override_option_directive(
    domain: str, allow_override_option_directive: AllowOverrideOptionDirective
) -> None:
    """Remove allow override option directive."""
    virtual_host = get_virtual_host(domain)

    try:
        virtual_host.allow_override_option_directives.remove(
            allow_override_option_directive
        )
    except ValueError:
        handle_manual_error("Allow override option directive not found")

    virtual_host.update()


@app.command()
@catch_api_exception
def update_document_root(
    domain: str,
    document_root: str = typer.Argument(
        default=..., help="Path relative to UNIX user home directory"
    ),
) -> None:
    """Update document root."""
    virtual_host = get_virtual_host(domain)
    unix_user = get_object(get_support().unix_users, id_=virtual_host.unix_user_id)

    virtual_host.document_root = _get_document_root(
        base_root=unix_user.home_directory, document_root=document_root
    )

    virtual_host.update()


@app.command()
@catch_api_exception
def update_server_software_name(
    domain: str, server_software_name: VirtualHostServerSoftwareName
) -> None:
    """Update server software name."""
    virtual_host = get_virtual_host(domain)

    if server_software_name == VirtualHostServerSoftwareName.NGINX:
        virtual_host.allow_override_directives = None
        virtual_host.allow_override_option_directives = None
    else:
        virtual_host.allow_override_directives = []
        virtual_host.allow_override_option_directives = []

    virtual_host.server_software_name = server_software_name
    virtual_host.update()


@app.command()
@confirm_clear
@catch_api_exception
def update_fpm_pool(
    domain: str,
    fpm_pool_name: Optional[str] = typer.Argument(
        default=None, help=EMPTY_TO_CLEAR_MESSAGE
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update FPM pool."""
    virtual_host = get_virtual_host(domain)

    fpm_pool_id = None

    if fpm_pool_name:
        fpm_pool_id = get_object(get_support().fpm_pools, name=fpm_pool_name).id

    virtual_host.fpm_pool_id = fpm_pool_id
    virtual_host.update()


@app.command()
@confirm_clear
@catch_api_exception
def update_passenger_app(
    domain: str,
    passenger_app_name: Optional[str] = typer.Argument(
        default=None, help=EMPTY_TO_CLEAR_MESSAGE
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update Passenger app."""
    virtual_host = get_virtual_host(domain)

    passenger_app_id = None

    if passenger_app_name:
        passenger_app_id = get_object(
            get_support().passenger_apps, name=passenger_app_name
        ).id

    virtual_host.passenger_app_id = passenger_app_id
    virtual_host.update()


@app.command()
@confirm_clear
@catch_api_exception
def update_custom_config(
    domain: str,
    custom_config_file: Path = typer.Argument(
        default=None,
        help=EMPTY_TO_CLEAR_MESSAGE,
        exists=True,
        dir_okay=False,
        resolve_path=True,
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Overwrite custom config using a file."""
    virtual_host = get_virtual_host(domain)

    custom_config = None

    if custom_config_file:
        custom_config = custom_config_file.read_text()

    virtual_host.custom_config = custom_config
    virtual_host.update()


@app.command()
@catch_api_exception
def edit_custom_config(domain: str) -> None:
    """Edit custom config using $EDITOR."""
    virtual_host = get_virtual_host(domain)

    virtual_host.custom_config = typer.edit(virtual_host.custom_config)

    if virtual_host.custom_config is None:
        print_warning("No changes have been made")

        return

    virtual_host.update()


@app.command()
@catch_api_exception
def delete(
    domain: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete virtual host."""
    virtual_host = get_virtual_host(domain)

    delete_api_object(obj=virtual_host, confirm=confirm)


def _get_base_root(*, unix_user: UNIXUser, domain: str) -> str:
    """Get base root."""
    return os.path.join(unix_user.virtual_hosts_directory, domain)


def _get_public_root(*, base_root: str) -> str:
    """Get default public root."""
    return os.path.join(base_root, "htdocs")


def _get_document_root(*, base_root: str, document_root: str) -> str:
    """Get default document root."""
    return os.path.join(base_root, document_root)


@app.command()
@catch_api_exception
def sync_domain_root(
    left_virtual_host_domain: str,
    right_virtual_host_domain: str,
) -> None:
    """Sync virtual host domain root."""
    left_virtual_host = get_virtual_host(left_virtual_host_domain)
    right_virtual_host = get_virtual_host(right_virtual_host_domain)

    task_collection = left_virtual_host.sync_domain_root(
        right_virtual_host_id=right_virtual_host.id
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)
