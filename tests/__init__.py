import os
from pathlib import Path

os.environ["AZURE_BOARD_FOLDER"] = str(Path(__file__).parent / "test_board_settings")
