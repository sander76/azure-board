from typing import Annotated, Literal, TypeVar

from clipstick import parse, short
from pydantic import BaseModel

from azure_board.client import BoardClient
from azure_board.config import (
    board_settings,
)
from azure_board.interactive import MyApp

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

    type: board_settings.item_types_annotation()  # type: ignore[valid-type]
    """Type of the work-item. (like 'Bug' or 'Task')"""

    area_path: Annotated[str, short("ap")] = board_settings.default_area_path

    assigned_to: Annotated[str | None, short("a")] = None
    """Full name of the person."""

    organization: Annotated[str, short("o")] = board_settings.default_organization
    """https://dev.azure.com/{your org}."""

    project: Annotated[str, short("p")] = board_settings.default_project
    """The project where your boards are in."""

    def __call__(
        self,
    ):
        client = BoardClient()
        client.create_item(self)


class In(BaseModel):
    """Go the interactive way."""

    action: Literal["create"]
    """Create a work item."""

    def __call__(self):
        match self.action:
            case "create":
                print("do stuff")
                app = MyApp(Add)
                app.run(inline=True)


class Main(BaseModel):
    """Azure board cli tooling."""

    sub_command: Add | In

    def __call__(self):
        self.sub_command()


def run():
    (parse(Main)())


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    print(parse(Main)())
