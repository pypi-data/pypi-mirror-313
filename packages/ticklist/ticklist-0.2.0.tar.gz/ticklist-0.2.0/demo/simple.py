from typing import Literal

from pydantic import BaseModel
from textual.app import App

from ticklist import form
from ticklist.annotation_iterators import ANNOTATION_ITERATORS
from ticklist.types import NO_VALUE


class MyModel(BaseModel):
    name: str
    types: Literal["abc", "def"]


class MyApp(App):
    def on_mount(self) -> None:
        frm = form._Form(MyModel, NO_VALUE, ANNOTATION_ITERATORS)
        self.push_screen(frm, self._check_result)

    def _check_result(self, result: form.ScreenResult | None) -> None:
        pass


if __name__ == "__main__":
    app = MyApp()
    app.run()
