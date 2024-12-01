import logging
from typing import Annotated, Literal, TypeVar

from clipstick import parse, short
from pydantic import BaseModel

from azure_board.client import BoardClient
from azure_board.config import DEFAULT_AREA_PATH, DEFAULT_ORGANIZATION, DEFAULT_PROJECT, ITEM_TYPES

T = TypeVar("T", bound=BaseModel)


class Interactive(BaseModel):
    """Basemodel"""


class Add(Interactive):
    """Add a new work-item."""

    title: str
    """Title."""

    description: str
    """Description of the work item."""

    type: ITEM_TYPES
    """Type of the work-item. (like 'Bug' or 'Task')"""

    area_path: Annotated[str, short("ap")] = DEFAULT_AREA_PATH

    assigned_to: Annotated[str | None, short("a")] = None
    """Full name of the person."""

    """Description."""

    def __call__(self, parent):
        client = BoardClient()
        client.create_item(parent, self)


class Interactive(BaseModel):
    """Go the interactive way."""

    action: Literal["create"]

    def __call__(self, parent):
        match self.action:
            case "create":
                pass


class Main(BaseModel):
    organization: Annotated[str, short("o")] = DEFAULT_ORGANIZATION
    """https://dev.azure.com/{your org}."""

    project: Annotated[str, short("p")] = DEFAULT_PROJECT
    """The project where your boards are in."""

    sub_command: Add | Interactive

    def __call__(self):
        self.sub_command(self)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print(parse(Main)())
