import logging
import os
from enum import Enum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic_core import PydanticUndefined
from pydantic_settings import BaseSettings

_logger = logging.getLogger(__name__)
_logger.debug(f"azure board folder{os.environ.get('AZURE_BOARD_FOLDER')}")
_SETTINGS_FOLDER = Path(os.environ.get("AZURE_BOARD_FOLDER", Path.home() / ".config" / "azure_board"))

AZURE_BOARD_DRYRUN = "AZURE_BOARD_DRYRUN"


class AzureBoard(BaseModel):
    """Basemodel"""

    model_config = ConfigDict(use_attribute_docstrings=True)

    def __call__(self):
        raise NotImplementedError


class BoardSettings(BaseSettings):
    organization: str | None = None
    """most of times: https://dev.azure.com/{your org}"""

    project: str = "unknown"
    """The project where your boards are in."""

    states: list[str] = []
    """Possible states of a work item. (like 'completed', 'triaged')"""

    item_types: list[str] | None = None
    """Possible types of a work item. (like 'bug' or 'task')"""

    area_path: str | None = None
    """Default area path"""

    available_area_paths: list[str] | None = None
    """Available area paths."""

    assigned_to: str
    """default person to assign the task to."""

    @property
    def default_area_path(self):
        return self.area_path or PydanticUndefined  # type: ignore[union-attr]

    @property
    def available_area_paths_annotation(self):
        return Literal[*self.available_area_paths] if self.available_area_paths else str

    @property
    def default_organization(self):
        return self.organization or PydanticUndefined  # type: ignore[union-attr]

    @property
    def default_project(self):
        return self.project or PydanticUndefined


def load_board_settings() -> BoardSettings:
    _logger.info(f"loading config from {_SETTINGS_FOLDER}")
    try:
        return BoardSettings.model_validate_json((_SETTINGS_FOLDER / "boards.json").read_bytes())
    except FileNotFoundError:
        _logger.warning("File not found")
        return BoardSettings()


board_settings: BoardSettings = load_board_settings()
_logger.info(board_settings)
