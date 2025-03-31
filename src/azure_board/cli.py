from typing import Annotated, Literal, TypeVar

from networkx import bellman_ford_predecessor_and_distance
from pydantic import BaseModel, create_model

from azure_board.client import ItemResult, board_client
from azure_board.config import (
    BoardSettings,
    board_settings,
    load_board_settings,
)
from azure_board.interactive import WorkItem
from azure_board.setup_logging import setup_logging

T = TypeVar("T", bound=BaseModel)


class AzureBoard(BaseModel):
    """Basemodel"""

    def __call__(self):
        raise NotImplementedError


class Add(AzureBoard):
    """Add a new work-item."""

    title: str
    """Title."""

    description: str
    """Description of the work item."""

    type: Literal["Bug", "Task"]
    """Type of the work-item. (like 'Bug' or 'Task')"""

    area_path: str

    assigned_to: str | None
    """Full name of the person."""

    organization: str
    """https://dev.azure.com/{your org}."""

    project: str
    """The project where your boards are in."""

    def __call__(
        self,
    ) -> ItemResult:
        client = board_client()
        return client.create_item(self)


def with_config(settings: BoardSettings):
    board_settings = load_board_settings()
    Add.model_fields["organization"].default = board_settings.organization
    Add.model_fields["project"].default = board_settings.project
    Add.model_fields["type"].annotation = board_settings.item_types

    return Add


def run():
    setup_logging()
    app = WorkItem(with_config(Add))
    app.run()


if __name__ == "__main__":
    setup_logging()
    run()
