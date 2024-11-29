from functools import cache
from pathlib import Path

from pydantic_settings import BaseSettings

_SETTINGS_FOLDER = Path.home() / ".settings" / "azure_board"


class BoardSettings(BaseSettings):
    organization: str
    """most of times: https://dev.azure.com/{your org}"""

    project: str
    """The project where your boards are in."""

    states: list[str]
    """Possible states of a work item. (like 'completed', 'triaged')"""

    item_type: list[str]
    """Possible types of a work item. (like 'bug' or 'task')"""


@cache
def load_board_settings() -> dict:
    try:
        return BoardSettings.model_validate_json((_SETTINGS_FOLDER / "boards.json").read_bytes()).model_dump()
    except FileNotFoundError:
        return {}
