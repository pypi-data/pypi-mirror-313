"""Mail subcommands."""

from typing import List, Optional

import typer

from cyberfusion.ClusterSupport.mail_accounts import MailAccount
from cyberfusion.ClusterSupport.mail_aliases import MailAlias
from cyberfusion.ClusterSupport.mail_domains import MailDomain
from cyberfusion.ClusterSupport.mail_hostnames import MailHostname
from cyberfusion.Common import generate_random_string
from cyberfusion.CoreCli._utilities import (
    BOOL_MESSAGE,
    CONFIRM_MESSAGE,
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
)

app = typer.Typer()


CHARACTER_AT = "@"

HELP_PANEL_MAIL_HOSTNAMES = "Mail Hostnames"
HELP_PANEL_MAIL_DOMAINS = "Mail Domains"
HELP_PANEL_MAIL_ACCOUNTS = "Mail Accounts"
HELP_PANEL_MAIL_ALIASES = "Mail Aliases"


@app.command(rich_help_panel=HELP_PANEL_MAIL_DOMAINS)
@catch_api_exception
def list_domains() -> None:
    """List mail domains."""
    console.print(get_support().get_table(objs=get_support().mail_domains))


@app.command(rich_help_panel=HELP_PANEL_MAIL_DOMAINS)
@catch_api_exception
def get_domain(domain: str) -> None:
    """Show mail domain."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().mail_domains, domain=domain)]
        )
    )


@app.command(rich_help_panel=HELP_PANEL_MAIL_ACCOUNTS)
@catch_api_exception
def list_accounts() -> None:
    """List mail accounts."""
    console.print(get_support().get_table(objs=get_support().mail_accounts))


@app.command(rich_help_panel=HELP_PANEL_MAIL_ACCOUNTS)
@catch_api_exception
def get_account(email_address: str) -> None:
    """Show mail account."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().mail_accounts, email_address=email_address)]
        )
    )


@app.command(rich_help_panel=HELP_PANEL_MAIL_ALIASES)
@catch_api_exception
def list_aliases() -> None:
    """List mail aliases."""
    console.print(get_support().get_table(objs=get_support().mail_aliases))


@app.command(rich_help_panel=HELP_PANEL_MAIL_ALIASES)
@catch_api_exception
def get_alias(email_address: str) -> None:
    """Show mail alias."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().mail_aliases, email_address=email_address)]
        )
    )


@app.command(rich_help_panel=HELP_PANEL_MAIL_HOSTNAMES)
@catch_api_exception
def list_hostnames() -> None:
    """List mail hostnames."""
    console.print(
        get_support().get_table(
            objs=get_support().mail_hostnames,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_MAIL_HOSTNAMES)
@catch_api_exception
def get_hostname(domain: str) -> None:
    """Show mail hostname."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().mail_hostnames, domain=domain)]
        )
    )


@app.command(rich_help_panel=HELP_PANEL_MAIL_ACCOUNTS)
@catch_api_exception
def account_usage(
    email_address: str,
    hours_before: Optional[int] = None,
    days_before: Optional[int] = None,
    amount: Optional[int] = typer.Option(default=None, show_default="All"),
) -> None:
    """Show disk usage graph.

    Using --hours-before OR --days-before is required.
    """
    mail_account = get_object(get_support().mail_accounts, email_address=email_address)

    timestamp, time_unit = get_usages_timestamp(
        days_before=days_before, hours_before=hours_before
    )

    usages = get_support().mail_account_usages(
        mail_account_id=mail_account.id,
        timestamp=timestamp,
        time_unit=time_unit,
    )[:amount]

    typer.echo(get_usages_plot(usages=usages))


@app.command(rich_help_panel=HELP_PANEL_MAIL_DOMAINS)
@catch_api_exception
def create_domain(
    domain: str,
    catch_all_forward_email_addresses: Optional[List[str]] = None,
    local: bool = True,
    unix_user_username: str = typer.Argument(default=...),
) -> None:
    """Create mail domain."""
    mail_domain = MailDomain(get_support())

    if not catch_all_forward_email_addresses:
        catch_all_forward_email_addresses = []

    mail_domain.create(
        domain=domain,
        catch_all_forward_email_addresses=catch_all_forward_email_addresses,
        is_local=local,
        unix_user_id=get_object(
            get_support().unix_users, username=unix_user_username
        ).id,
    )

    console.print(
        get_support().get_table(
            objs=[mail_domain],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_MAIL_ACCOUNTS)
@catch_api_exception
def create_account(
    email_address: str,
    quota: Optional[int] = None,
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
) -> None:
    """Create mail account."""
    mail_account = MailAccount(get_support())

    local_part, domain = email_address.rsplit(CHARACTER_AT, 1)

    mail_account.create(
        local_part=local_part,
        password=password,
        quota=quota,
        mail_domain_id=get_object(get_support().mail_domains, domain=domain).id,
    )

    console.print(
        get_support().get_table(
            objs=[mail_account],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_MAIL_ALIASES)
@catch_api_exception
def create_alias(
    alias_address: str,
    forward_email_addresses: List[str],
) -> None:
    """Create mail alias."""
    mail_alias = MailAlias(get_support())

    local_part, domain = alias_address.rsplit(CHARACTER_AT, 1)

    mail_alias.create(
        local_part=local_part,
        forward_email_addresses=forward_email_addresses,
        mail_domain_id=get_object(get_support().mail_domains, domain=domain).id,
    )

    console.print(
        get_support().get_table(
            objs=[mail_alias],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_MAIL_HOSTNAMES)
@catch_api_exception
def create_hostname(
    domain: str,
    cluster_name: str,
    certificate_id: Optional[int] = None,
) -> None:
    """Create mail hostname."""
    mail_hostname = MailHostname(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    mail_hostname.create(
        domain=domain, certificate_id=certificate_id, cluster_id=cluster.id
    )

    console.print(
        get_support().get_table(
            objs=[mail_hostname],
            detailed=True,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_MAIL_DOMAINS)
@catch_api_exception
def update_local(
    domain: str, state: bool = typer.Argument(default=..., help=BOOL_MESSAGE)
) -> None:
    """Update is local."""
    mail_domain = get_object(get_support().mail_domains, domain=domain)

    mail_domain.is_local = state
    mail_domain.update()


@app.command(rich_help_panel=HELP_PANEL_MAIL_DOMAINS)
@catch_api_exception
def add_catch_all_forward_addresses(
    domain: str, catch_all_forward_email_addresses: List[str]
) -> None:
    """Add catch all forward email addresses."""
    mail_domain = get_object(get_support().mail_domains, domain=domain)

    mail_domain.catch_all_forward_email_addresses.extend(
        catch_all_forward_email_addresses
    )
    mail_domain.update()


@app.command(rich_help_panel=HELP_PANEL_MAIL_DOMAINS)
@catch_api_exception
@exit_with_status
def remove_catch_all_forward_addresses(
    domain: str, catch_all_forward_email_addresses: List[str]
) -> int:
    """Remove catch all forward email addresses."""
    mail_domain = get_object(get_support().mail_domains, domain=domain)

    exit_code = 0
    success = False

    for address in catch_all_forward_email_addresses:
        try:
            mail_domain.catch_all_forward_email_addresses.remove(address)
            success = True
        except ValueError:
            print_warning(f"Address '{address}' not found, skipping.")
            exit_code = 64

    if not success:
        handle_manual_error("No addresses have been removed")

    mail_domain.update()

    return exit_code


@app.command(rich_help_panel=HELP_PANEL_MAIL_ACCOUNTS)
@catch_api_exception
def update_account_password(
    email_address: str,
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
) -> None:
    """Update mail account password."""
    mail_account = get_object(get_support().mail_accounts, email_address=email_address)

    mail_account.password = password
    mail_account.update()


@app.command(rich_help_panel=HELP_PANEL_MAIL_ACCOUNTS)
@catch_api_exception
def update_account_quota(email_address: str, quota: Optional[int]) -> None:
    """Update mail account quota.

    Use 0 for no quota.
    """
    mail_account = get_object(get_support().mail_accounts, email_address=email_address)

    if quota == 0:
        quota = None

    mail_account.quota = quota
    mail_account.update()


@app.command(rich_help_panel=HELP_PANEL_MAIL_ALIASES)
@catch_api_exception
def add_alias_forward_addresses(
    email_address: str, forward_email_addresses: List[str]
) -> None:
    """Add alias forward addresses."""
    mail_alias = get_object(get_support().mail_aliases, email_address=email_address)

    mail_alias.forward_email_addresses.extend(forward_email_addresses)
    mail_alias.update()


@app.command(rich_help_panel=HELP_PANEL_MAIL_ALIASES)
@catch_api_exception
@exit_with_status
def remove_alias_forward_addresses(
    email_address: str, forward_email_addresses: List[str]
) -> int:
    """Remove alias forward address."""
    mail_alias = get_object(get_support().mail_aliases, email_address=email_address)

    exit_code = 0
    success = False

    for address in forward_email_addresses:
        try:
            mail_alias.forward_email_addresses.remove(address)
            success = True
        except ValueError:
            print_warning(f"Address '{address}' not found, skipping.")
            exit_code = 64

    if not success:
        handle_manual_error("No addresses have been removed")

    mail_alias.update()

    return exit_code


@app.command(rich_help_panel=HELP_PANEL_MAIL_HOSTNAMES)
@confirm_clear
@catch_api_exception
def update_hostname_certificate(
    domain: str,
    certificate_id: Optional[int] = typer.Argument(
        default=None, help=EMPTY_TO_CLEAR_MESSAGE
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update certificate for mail hostname."""
    mail_hostname = get_object(get_support().mail_hostnames, domain=domain)

    mail_hostname.certificate_id = certificate_id
    mail_hostname.update()


@app.command(rich_help_panel=HELP_PANEL_MAIL_DOMAINS)
@catch_api_exception
def delete_domain(
    domain: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete mail domain."""
    mail_domain = get_object(get_support().mail_domains, domain=domain)

    delete_api_object(obj=mail_domain, confirm=confirm)


@app.command(rich_help_panel=HELP_PANEL_MAIL_ACCOUNTS)
@catch_api_exception
def delete_account(
    email_address: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete mail account."""
    mail_account = get_object(get_support().mail_accounts, email_address=email_address)

    delete_api_object(obj=mail_account, confirm=confirm)


@app.command(rich_help_panel=HELP_PANEL_MAIL_ALIASES)
@catch_api_exception
def delete_alias(
    email_address: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete mail alias."""
    mail_alias = get_object(get_support().mail_aliases, email_address=email_address)

    delete_api_object(obj=mail_alias, confirm=confirm)


@app.command(rich_help_panel=HELP_PANEL_MAIL_HOSTNAMES)
@catch_api_exception
def delete_hostname(
    domain: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete mail hostname."""
    mail_hostname = get_object(get_support().mail_hostnames, domain=domain)

    delete_api_object(obj=mail_hostname, confirm=confirm)
