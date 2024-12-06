import json
from pathlib import Path

from pydantic import TypeAdapter
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.driver import Driver
from textual.widget import Widget
from textual.widgets import Button, Label, ListItem, ListView, Pretty

from demo.models import MyCar
from ticklist import annotation_iterators, form
from ticklist.annotation_iterators import ANNOTATION_ITERATORS
from ticklist.types import NO_VALUE


def _list_item_for_car(car: MyCar) -> ListItem:
    return ListItem(Label(car.customer_name))


cars_adapter = TypeAdapter(list[MyCar])


def _save_cars(cars: list[MyCar]) -> None:
    cars_file = Path(__file__).parent / "cars.json"
    cars_file.write_bytes(cars_adapter.dump_json(cars))


def _load_cars() -> list[MyCar]:
    cars_file = Path(__file__).parent / "cars.json"
    if not cars_file.exists():
        return []
    return cars_adapter.validate_json(cars_file.read_bytes())


class MyApp(App):
    """An app for testing purposes."""

    CSS_PATH = "main.tcss"

    cars: list[MyCar]

    def compose(self) -> ComposeResult:
        self.cars = _load_cars()
        with Horizontal(id="buttons"):
            yield Button("new car", id="new_car")
            yield Button("save cars", id="save_cars")
            yield Button("edit car", id="edit_car")

        with Horizontal():
            yield ListView(*(_list_item_for_car(car) for car in self.cars), id="cars")
            yield Pretty({})

    @on(Button.Pressed, "#save_cars")
    def _save(self) -> None:
        _save_cars(self.cars)

    @on(Button.Pressed, "#new_car")
    @work
    async def _order_car(self) -> None:
        car = await self._manage_car()
        if car is None:
            return
        self.cars.append(car)
        self._update_cars_view()

    @on(Button.Pressed, "#edit_car")
    @work
    async def _edit_car(self) -> None:
        idx = self.query_one(ListView).index
        if idx is None:
            return

        selected_car = self.cars[idx]
        updated_car = await self._manage_car(instance=selected_car)
        if updated_car is None:
            return
        self.cars[idx] = updated_car
        self._update_cars_view()

    async def _manage_car(self, instance: MyCar | None = None) -> MyCar | None:
        if instance is None:
            instance = NO_VALUE
        frm = form.form_factory(MyCar, instance, ANNOTATION_ITERATORS)
        car = await self.app.push_screen_wait(frm)

        print("this is my cars.")
        return car

    def _update_cars_view(self) -> None:
        cars_view = self.query_one(ListView)
        cars_view.clear()

        cars_view.extend((_list_item_for_car(car) for car in self.cars))

    @on(ListView.Highlighted)
    def _on_car_selected(self, event: ListView.Highlighted) -> None:
        idx = event.list_view.index
        if idx is None:
            return
        car: MyCar = self.cars[idx]

        jsonned_dict = json.loads(car.model_dump_json())

        self.query_one(Pretty).update(jsonned_dict)


if __name__ == "__main__":
    app = MyApp()
    app.run()
