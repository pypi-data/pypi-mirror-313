"""Security TXT policies subcommands."""

from datetime import datetime
from typing import Annotated, List, Optional

import typer

from cyberfusion.ClusterSupport.security_txt_policies import (
    PreferredLanguage,
    SecurityTXTPolicy,
)
from cyberfusion.CoreCli._utilities import (
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    catch_api_exception,
    console,
    delete_api_object,
    exit_with_status,
    get_object,
    get_support,
    handle_manual_error,
    print_warning,
)

app = typer.Typer()


@app.command("list")
@catch_api_exception
def list_(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """List security.txt policies."""
    console.print(
        get_support().get_table(
            objs=get_support().security_txt_policies, detailed=detailed
        )
    )


@app.command()
@catch_api_exception
def get(
    id_: int = typer.Argument(metavar="id", default=...),
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show security.txt policy."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().security_txt_policies, id_=id_)],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create(
    expires: Annotated[
        datetime,
        typer.Argument(formats=["%Y-%m-%d %H:%M:%S"]),  # noqa: F722
    ],
    email_contacts: Optional[List[str]] = None,
    url_contacts: Optional[List[str]] = None,
    encryption_key_urls: Optional[List[str]] = None,
    acknowledgment_urls: Optional[List[str]] = None,
    policy_urls: Optional[List[str]] = None,
    opening_urls: Optional[List[str]] = None,
    preferred_languages: Optional[List[PreferredLanguage]] = None,
    cluster_name: str = typer.Argument(default=...),
) -> None:
    """Create security.txt policy."""
    security_txt_policy = SecurityTXTPolicy(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    security_txt_policy.create(
        expires_timestamp=datetime.strftime(expires, "%Y-%m-%d %H:%M:%S"),
        email_contacts=email_contacts,
        url_contacts=url_contacts,
        encryption_key_urls=encryption_key_urls,
        acknowledgment_urls=acknowledgment_urls,
        policy_urls=policy_urls,
        opening_urls=opening_urls,
        preferred_languages=preferred_languages,
        cluster_id=cluster.id,
    )

    console.print(
        get_support().get_table(
            objs=[security_txt_policy],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def add_email_contacts(
    id_: int = typer.Argument(metavar="id", default=...),
    email_contacts: List[str] = typer.Argument(default=...),
) -> None:
    """Add email contacts."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    security_txt_policy.email_contacts.extend(email_contacts)
    security_txt_policy.update()


@app.command()
@catch_api_exception
@exit_with_status
def remove_email_contacts(
    id_: int = typer.Argument(metavar="id", default=...),
    email_contacts: List[str] = typer.Argument(default=...),
) -> int:
    """Remove email contacts."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    exit_code = 0
    success = False

    for email_contact in email_contacts:
        try:
            security_txt_policy.email_contacts.remove(email_contact)
            success = True
        except ValueError:
            print_warning(f"Email contact '{email_contact}' not found, skipping.")
            exit_code = 64

    if not success:
        handle_manual_error("No email contacts have been removed")

    security_txt_policy.update()

    return exit_code


@app.command()
@catch_api_exception
def add_url_contacts(
    id_: int = typer.Argument(metavar="id", default=...),
    url_contacts: List[str] = typer.Argument(default=...),
) -> None:
    """Add URL contacts."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    security_txt_policy.url_contacts.extend(url_contacts)
    security_txt_policy.update()


@app.command()
@catch_api_exception
@exit_with_status
def remove_url_contacts(
    id_: int = typer.Argument(metavar="id", default=...),
    url_contacts: List[str] = typer.Argument(default=...),
) -> int:
    """Remove URL contacts."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    exit_code = 0
    success = False

    for url_contact in url_contacts:
        try:
            security_txt_policy.url_contacts.remove(url_contact)
            success = True
        except ValueError:
            print_warning(f"URL contact '{url_contact}' not found, skipping.")
            exit_code = 64

    if not success:
        handle_manual_error("No URL contacts have been removed")

    security_txt_policy.update()

    return exit_code


@app.command()
@catch_api_exception
def add_encryption_key_urls(
    id_: int = typer.Argument(metavar="id", default=...),
    encryption_key_urls: List[str] = typer.Argument(default=...),
) -> None:
    """Add encryption key URLs."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    security_txt_policy.encryption_key_urls.extend(encryption_key_urls)
    security_txt_policy.update()


@app.command()
@catch_api_exception
@exit_with_status
def remove_encryption_key_urls(
    id_: int = typer.Argument(metavar="id", default=...),
    encryption_key_urls: List[str] = typer.Argument(default=...),
) -> int:
    """Remove encryption key URLs."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    exit_code = 0
    success = False

    for encryption_key_url in encryption_key_urls:
        try:
            security_txt_policy.encryption_key_urls.remove(encryption_key_url)
            success = True
        except ValueError:
            print_warning(
                f"Encryption key URL '{encryption_key_url}' not found, skipping."
            )
            exit_code = 64

    if not success:
        handle_manual_error("No encryption key URLs have been removed")

    security_txt_policy.update()

    return exit_code


@app.command()
@catch_api_exception
def add_acknowledgment_urls(
    id_: int = typer.Argument(metavar="id", default=...),
    acknowledgment_urls: List[str] = typer.Argument(default=...),
) -> None:
    """Add acknowledgment URLs."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    security_txt_policy.acknowledgment_urls.extend(acknowledgment_urls)
    security_txt_policy.update()


@app.command()
@catch_api_exception
@exit_with_status
def remove_acknowledgment_urls(
    id_: int = typer.Argument(metavar="id", default=...),
    acknowledgment_urls: List[str] = typer.Argument(default=...),
) -> int:
    """Remove acknowledgment URLs."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    exit_code = 0
    success = False

    for acknowledgment_url in acknowledgment_urls:
        try:
            security_txt_policy.acknowledgment_urls.remove(acknowledgment_url)
            success = True
        except ValueError:
            print_warning(
                f"Acknowledgment URL '{acknowledgment_url}' not found, skipping."
            )
            exit_code = 64

    if not success:
        handle_manual_error("No acknowledgment URLs have been removed")

    security_txt_policy.update()

    return exit_code


@app.command()
@catch_api_exception
def add_policy_urls(
    id_: int = typer.Argument(metavar="id", default=...),
    policy_urls: List[str] = typer.Argument(default=...),
) -> None:
    """Add policy URLs."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    security_txt_policy.policy_urls.extend(policy_urls)
    security_txt_policy.update()


@app.command()
@catch_api_exception
@exit_with_status
def remove_policy_urls(
    id_: int = typer.Argument(metavar="id", default=...),
    policy_urls: List[str] = typer.Argument(default=...),
) -> int:
    """Remove policy URLs."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    exit_code = 0
    success = False

    for policy_url in policy_urls:
        try:
            security_txt_policy.policy_urls.remove(policy_url)
            success = True
        except ValueError:
            print_warning(f"Policy URL '{policy_url}' not found, skipping.")
            exit_code = 64

    if not success:
        handle_manual_error("No policy URLs have been removed")

    security_txt_policy.update()

    return exit_code


@app.command()
@catch_api_exception
def add_opening_urls(
    id_: int = typer.Argument(metavar="id", default=...),
    opening_urls: List[str] = typer.Argument(default=...),
) -> None:
    """Add opening URLs."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    security_txt_policy.opening_urls.extend(opening_urls)
    security_txt_policy.update()


@app.command()
@catch_api_exception
@exit_with_status
def remove_opening_urls(
    id_: int = typer.Argument(metavar="id", default=...),
    opening_urls: List[str] = typer.Argument(default=...),
) -> int:
    """Remove opening URLs."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    exit_code = 0
    success = False

    for opening_url in opening_urls:
        try:
            security_txt_policy.opening_urls.remove(opening_url)
            success = True
        except ValueError:
            print_warning(f"Opening URL '{opening_url}' not found, skipping.")
            exit_code = 64

    if not success:
        handle_manual_error("No opening URLs have been removed")

    security_txt_policy.update()

    return exit_code


@app.command()
@catch_api_exception
def add_preferred_languages(
    id_: int = typer.Argument(metavar="id", default=...),
    preferred_languages: List[str] = typer.Argument(default=...),
) -> None:
    """Add preferred languages."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    security_txt_policy.preferred_languages.extend(preferred_languages)
    security_txt_policy.update()


@app.command()
@catch_api_exception
@exit_with_status
def remove_preferred_languages(
    id_: int = typer.Argument(metavar="id", default=...),
    preferred_languages: List[str] = typer.Argument(default=...),
) -> int:
    """Remove preferred languages."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    exit_code = 0
    success = False

    for preferred_language in preferred_languages:
        try:
            security_txt_policy.preferred_languages.remove(preferred_language)
            success = True
        except ValueError:
            print_warning(
                f"Preferred language '{preferred_language}' not found, skipping."
            )
            exit_code = 64

    if not success:
        handle_manual_error("No preferred languages have been removed")

    security_txt_policy.update()

    return exit_code


@app.command()
@catch_api_exception
def update_expires(
    id_: int = typer.Argument(metavar="id", default=...),
    # Comes after , so must have default value, but using typer.Argument again
    # causes:
    #
    # > typer.utils.MixedAnnotatedAndDefaultStyleError: Cannot specify `Argument`
    # in `Annotated` and default value together for 'expires'
    expires: Annotated[
        Optional[datetime],
        typer.Argument(formats=["%Y-%m-%d %H:%M:%S"]),  # noqa: F722
    ] = None,
) -> None:
    """Update expires."""
    if not expires:
        return

    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    security_txt_policy.expires_timestamp = datetime.strftime(
        expires, "%Y-%m-%d %H:%M:%S"
    )
    security_txt_policy.update()


@app.command()
@catch_api_exception
def delete(
    id_: int = typer.Argument(metavar="id", default=...),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete security.txt policy."""
    security_txt_policy = get_object(get_support().security_txt_policies, id_=id_)

    delete_api_object(obj=security_txt_policy, confirm=confirm)
