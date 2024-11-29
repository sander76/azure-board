from typing import Annotated, Self, Type, TypeVar

from clipstick import parse, short
from pydantic import BaseModel, create_model
from pydantic_core import PydanticUndefined
from rich import print

from baringa_board.client import BoardClient
from baringa_board.config import load_board_settings
from baringa_board.fillers import Filler, StringEntryFiller

T = TypeVar("T", bound=BaseModel)


def _interactive_fill(model: T) -> T:
    """Interactive fill of pydantic fields.

    Walk over all fields, check for none and if none, get the interactive fill operation from the `Annotated` tag.
    """

    interactive_data = {}
    for field, field_info in model.model_fields.items():
        if getattr(model, field) is not None:
            continue

        filler = field_info.metadata
        for anno in filler:
            if isinstance(anno, Filler):
                result = anno.ask()
                interactive_data[field] = result

    if interactive_data:
        new_data = model.model_dump() | interactive_data

        return model.model_validate(new_data)
    return model


class Interactive(BaseModel):
    """Basemodel"""

    def __call__(self: Self) -> Self:
        filled = _interactive_fill(self)
        return filled


class Add(Interactive):
    """Add a new work-item."""

    title: Annotated[str | None, short("t"), StringEntryFiller("title")] = None
    """Title of the work-item."""

    type: Annotated[str | None, short("y"), StringEntryFiller("type")] = None
    """Type of the work-item."""

    description: Annotated[str | None, short("d"), StringEntryFiller("description")] = None
    """Type of the work-item."""

    def __call__(self):
        filled = super().__call__()
        client = BoardClient()
        client.create_item(**filled.model_dump())


class Remove(BaseModel):
    """remove a work item."""


class Main(BaseModel):
    organization: Annotated[str, short("o"), StringEntryFiller("organization")] = load_board_settings().get(
        "organization", PydanticUndefined
    )
    """https://dev.azure.com/{your org}."""

    project: Annotated[str, short("p"), StringEntryFiller("project")] = load_board_settings().get(
        "project", PydanticUndefined
    )
    """The project where your boards are in."""

    sub_command: Add | Remove


if __name__ == "__main__":
    print(parse(Main)())
