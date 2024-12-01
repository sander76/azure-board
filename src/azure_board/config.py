import os
from functools import cache
from pathlib import Path
from typing import Literal

from pydantic_core import PydanticUndefined
from pydantic_settings import BaseSettings

_SETTINGS_FOLDER = Path(os.environ.get("AZURE_BOARD_FOLDER", Path.home() / ".config" / "azure_board"))


def to_snake(val: str) -> str:
    """Convert a string to snake case.

    >>> to_snake("a Word")
    'a_word'

    >>> to_snake("a word")
    'a_word'

    >>> to_snake("aWord")
    'a_word'

    >>> to_snake("A Word")
    'a_word'

    >>> to_snake("AWord")
    'a_word'

    >>> to_snake("a worD")
    'a_wor_d'

    >>> to_snake("a word ")
    'a_word'

    >>> to_snake("a wor D")
    'a_wor_d'

    >>> to_snake("a 1")
    'a_1'
    """

    def walk():
        str_iter = iter(val)
        try:
            while True:
                char = next(str_iter)
                if char == " ":
                    next_char = next(str_iter)
                    if next_char.isupper():
                        # concat a combination of two characters consisting of a space and an upper case char
                        # to a single underscore.
                        yield from ("_", next_char.lower())
                    else:
                        yield from ("_", next_char)
                elif char.isupper():
                    yield from ("_", char.lower())
                else:
                    yield char
        except StopIteration:
            return

    return "".join(walk()).lstrip("_")


class BoardSettings(BaseSettings):
    organization: str
    """most of times: https://dev.azure.com/{your org}"""

    project: str
    """The project where your boards are in."""

    states: list[str]
    """Possible states of a work item. (like 'completed', 'triaged')"""

    item_types: list[str]
    """Possible types of a work item. (like 'bug' or 'task')"""

    area_path: str
    """Default area path"""


@cache
def load_board_settings() -> BoardSettings | None:
    try:
        return BoardSettings.model_validate_json((_SETTINGS_FOLDER / "boards.json").read_bytes())
    except FileNotFoundError:
        return None


ITEM_TYPES = Literal[*load_board_settings().item_types] if load_board_settings() else str  # type: ignore[union-attr]
DEFAULT_ORGANIZATION = load_board_settings().organization if load_board_settings() else PydanticUndefined  # type: ignore[union-attr]
DEFAULT_PROJECT = load_board_settings().project if load_board_settings() else PydanticUndefined  # type: ignore[union-attr]
DEFAULT_AREA_PATH = load_board_settings().area_path if load_board_settings() else PydanticUndefined  # type: ignore[union-attr]
