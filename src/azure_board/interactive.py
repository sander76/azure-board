from pydantic import BaseModel
from textual.app import App
from textual.widgets import Button
from ticklist.annotation_iterators import ANNOTATION_ITERATORS
from ticklist.form import ScreenResult, form_factory
from ticklist.types import NO_VALUE


class MyApp(App):
    CSS_PATH = "interactive.tcss"

    def __init__(self, model: type[BaseModel]):
        self._model = model
        self._last_model: BaseModel | None = None
        super().__init__()

    def compose(self):
        yield Button("New")
        yield Button("Exit")
        yield Button("New from last.")

    def on_mount(self) -> None:
        _form = form_factory(self._model, NO_VALUE, ANNOTATION_ITERATORS)

        self.push_screen(_form, self._check_result)

    def _check_result(self, result: ScreenResult | None):
        if result is None:
            self.exit()
        elif result.action == "ok":
            result.model()
        elif result.action == "cancel":
            self.exit()
