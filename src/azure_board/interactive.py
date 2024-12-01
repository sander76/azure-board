from pydantic import BaseModel
from ticklist.annotation_iterators import ANNOTATION_ITERATORS
from ticklist.form import form_factory
from ticklist.types import NO_VALUE


class MyApp(App):
    def __init__(self, model: BaseModel):
        self._model = model
        super().__init__()

    def on_mount(self) -> None:
        frm = form_factory(self._model, NO_VALUE, ANNOTATION_ITERATORS)
        self.push_screen(frm)
