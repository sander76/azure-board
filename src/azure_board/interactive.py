from __future__ import annotations

from typing import TYPE_CHECKING

from textual import on, work
from textual.app import App
from textual.widgets import Button, Label
from ticklist.annotation_iterators import ANNOTATION_ITERATORS
from ticklist.form import Form
from ticklist.types import NO_VALUE

if TYPE_CHECKING:
    from azure_board.cli import Add


class WorkItem(App):
    CSS_PATH = "interactive.tcss"

    def __init__(self, model: type[Add]):
        self._model = model
        self._last_model: Add | None = None

        super().__init__()

    def compose(self):
        yield Button("New", id="new")
        yield Button("Exit", id="exit")
        yield Button("New from last.", id="new_from_last")
        yield Label("", id="result")

    def on_mount(self) -> None:
        _form = Form(self._model, NO_VALUE, ANNOTATION_ITERATORS)

        self.push_screen(_form, self._check_result)

    def _check_result(self, result: Add | None):
        if result is None:
            self.exit()
        else:
            self._last_model = result
            try:
                item_result = self._last_model()
                self.query_one("#result", Label).update(f"Workitem created. id={item_result.id!r}")
            except Exception:
                self.query_one("#result", Label).update("something went wrong. Please check the logs.")

    @on(Button.Pressed, "#new")
    @work
    async def new_work_item(self) -> None:
        self.push_screen(Form(self._model, NO_VALUE, ANNOTATION_ITERATORS), self._check_result)

    @on(Button.Pressed, "#exit")
    @work
    async def exit_app(self):
        self.exit()

    @on(Button.Pressed, "#new_from_last")
    @work
    async def new_from_last(self) -> None:
        if self._last_model is None:
            return
        self.push_screen(Form(self._model, self._last_model, ANNOTATION_ITERATORS), self._check_result)
