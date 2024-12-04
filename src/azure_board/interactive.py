from pydantic import BaseModel
from textual.app import App
from textual.widgets import Input, Label
from ticklist.annotation_iterators import ANNOTATION_ITERATORS
from ticklist.form import form_factory
from ticklist.types import NO_VALUE


class MyApp(App):
    CSS_PATH = "interactive.tcss"

    def __init__(self, model: type[BaseModel]):
        self._model = model
        self._form = None
        self._last_model: BaseModel | None = None
        super().__init__()

    def compose(self):
        yield Label("some label")

    def on_mount(self) -> None:
        self._form = form_factory(self._model, NO_VALUE, ANNOTATION_ITERATORS)
        self.push_screen(self._form, self._check_result)

    def _check_result(self, result: BaseModel | None):
        if result is None:
            # exit somehow.
            pass
        elif self._last_model == result:
            # exit somehow.
            pass
        else:
            result()
