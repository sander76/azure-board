import logging
from typing import Annotated, Literal, TypeVar

from clipstick import parse, short
from pydantic import BaseModel

from azure_board.client import BoardClient
from azure_board.config import DEFAULT_AREA_PATH, DEFAULT_ORGANIZATION, DEFAULT_PROJECT, ITEM_TYPES
from azure_board.interactive import MyApp

T = TypeVar("T", bound=BaseModel)


class AzureBoard(BaseModel):
    """Basemodel"""


class Add(AzureBoard):
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

    organization: Annotated[str, short("o")] = DEFAULT_ORGANIZATION
    """https://dev.azure.com/{your org}."""

    project: Annotated[str, short("p")] = DEFAULT_PROJECT
    """The project where your boards are in."""

    def __call__(
        self,
    ):
        client = BoardClient()
        client.create_item(self)


class AzureBoard(BaseModel):
    """Go the interactive way."""

    action: Literal["create"]

    def __call__(self):
        match self.action:
            case "create":
                print("do stuff")
                app = MyApp(Add)
                app.run(inline=True)


class Main(BaseModel):
    sub_command: Add | AzureBoard

    def __call__(self):
        self.sub_command()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print(parse(Main)())
