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
        frm = form.form_factory(MyModel, NO_VALUE, ANNOTATION_ITERATORS)
        self.push_screen(frm)


if __name__ == "__main__":
    app = MyApp()
    app.run()
