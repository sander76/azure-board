from typing import TypeVar

from pydantic import BaseModel

from azure_board.client import ItemResult, board_client
from azure_board.config import (
    BoardSettings,
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

    type: str
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


def with_config(defaults: BoardSettings):
    Add.model_fields["organization"].default = defaults.organization
    Add.model_fields["project"].default = defaults.project
    Add.model_fields["type"].annotation = defaults.item_types_annotation()
    Add.model_fields["area_path"].default = defaults.area_path
    Add.model_fields["area_path"].annotation = defaults.available_area_paths_annotation
    Add.model_fields["assigned_to"].default = defaults.assigned_to

    return Add


def run():
    setup_logging()
    app = WorkItem(with_config(load_board_settings()))
    app.run()


if __name__ == "__main__":
    run()
