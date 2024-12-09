import logging
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler

from azure_board.config import _SETTINGS_FOLDER

_FILE_FORMATTER = logging.Formatter("%(asctime)s - %(name)s %(levelname)s - %(message)s")


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # stream handler
    stream_handler = RichHandler(rich_tracebacks=False, tracebacks_show_locals=False, show_path=False)
    stream_handler.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)

    # file handler
    log_folder = _SETTINGS_FOLDER / "logs"
    log_folder.mkdir(exist_ok=True)
    file_handler = RotatingFileHandler(log_folder / "ab.log", maxBytes=300_000, backupCount=10)
    file_handler.setFormatter(_FILE_FORMATTER)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
