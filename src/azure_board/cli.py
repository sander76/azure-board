from typing import Annotated, Literal, TypeVar

from clipstick import parse, short
from pydantic import BaseModel

from azure_board.client import ItemResult, board_client
from azure_board.config import (
    board_settings,
)
from azure_board.interactive import WorkItem
from azure_board.setup_logging import setup_logging

T = TypeVar("T", bound=BaseModel)


class AzureBoard(BaseModel):
    """Basemodel"""

    def __call__(self):
        raise NotImplementedError


annotated_area_path = Annotated[board_settings.available_area_paths_annotation, short("ap")]  # type: ignore[name-defined]


class Add(AzureBoard):
    """Add a new work-item."""

    title: str
    """Title."""

    description: str
    """Description of the work item."""

    type: board_settings.item_types_annotation()  # type: ignore[valid-type]
    """Type of the work-item. (like 'Bug' or 'Task')"""

    area_path: annotated_area_path = board_settings.default_area_path

    assigned_to: str | None = board_settings.assigned_to
    """Full name of the person."""

    organization: Annotated[str, short("o")] = board_settings.default_organization
    """https://dev.azure.com/{your org}."""

    project: Annotated[str, short("p")] = board_settings.default_project
    """The project where your boards are in."""

    def __call__(
        self,
    ) -> ItemResult:
        client = board_client()
        return client.create_item(self)


class In(BaseModel):
    """Go the interactive way."""

    action: Literal["create"]
    """Create a work item."""

    def __call__(self):
        match self.action:
            case "create":
                print("do stuff")
                app = WorkItem(Add)
                app.run(inline=True)


class Main(BaseModel):
    """Azure board cli tooling."""

    sub_command: Add | In

    def __call__(self):
        self.sub_command()


def run():
    setup_logging()
    (parse(Main)())


if __name__ == "__main__":
    setup_logging()
    print(parse(Main)())
