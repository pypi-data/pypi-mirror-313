"""Crons subcommands."""

import typer

from cyberfusion.ClusterSupport.task_collections import TaskCollection
from cyberfusion.CoreCli._utilities import (
    catch_api_exception,
    get_support,
    wait_for_task,
)

app = typer.Typer()


@app.command()
@catch_api_exception
def results(
    uuid: str,
) -> None:
    """Get task collection results."""
    wait_for_task(
        task_collection_uuid=uuid,
    )


@app.command()
@catch_api_exception
def retry(uuid: str) -> None:
    """Retry task collection."""
    TaskCollection.retry(get_support(), uuid)

    wait_for_task(task_collection_uuid=uuid)
