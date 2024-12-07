"""Certificate managers subcommands."""

from typing import List, Optional

import typer

from cyberfusion.ClusterSupport.certificate_managers import (
    CertificateManager,
    ProviderName,
)
from cyberfusion.CoreCli._utilities import (
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    EMPTY_TO_CLEAR_MESSAGE,
    catch_api_exception,
    confirm_clear,
    console,
    delete_api_object,
    get_object,
    get_support,
    wait_for_task,
)

app = typer.Typer()


@app.command("list")
@catch_api_exception
def list_(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """List certificate managers."""
    console.print(
        get_support().get_table(
            objs=get_support().certificate_managers,
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def get(
    common_name: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Get certificate manager."""
    console.print(
        get_support().get_table(
            objs=[
                get_object(
                    get_support().certificate_managers,
                    common_names=common_name,
                )
            ],
            detailed=detailed,
        )
    )


@app.command()
@catch_api_exception
def create(common_names: List[str], cluster_name: str) -> None:
    """Create certificate manager."""
    certificate_manager = CertificateManager(get_support())

    cluster = get_object(get_support().clusters, name=cluster_name)

    certificate_manager.create(
        common_names=common_names,
        provider_name=ProviderName.LETS_ENCRYPT,
        request_callback_url=None,
        cluster_id=cluster.id,
    )

    console.print(
        get_support().get_table(
            objs=[certificate_manager],
            detailed=True,
        )
    )


@app.command()
@catch_api_exception
def request(common_name: str) -> None:
    """Request certificate."""
    certificate_manager = get_object(
        get_support().certificate_managers, common_names=common_name
    )

    task_collection = certificate_manager.request()

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command()
@confirm_clear
@catch_api_exception
def update_request_callback_url(
    common_name: str,
    request_callback_url: Optional[str] = typer.Argument(
        default=None, help=EMPTY_TO_CLEAR_MESSAGE
    ),
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Update request callback URL."""
    certificate_manager = get_object(
        get_support().certificate_managers, common_names=common_name
    )

    certificate_manager.request_callback_url = request_callback_url
    certificate_manager.update()


@app.command()
@catch_api_exception
def delete(
    common_name: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete certificate manager."""
    certificate_manager = get_object(
        get_support().certificate_managers, common_names=common_name
    )

    delete_api_object(obj=certificate_manager, confirm=confirm)
