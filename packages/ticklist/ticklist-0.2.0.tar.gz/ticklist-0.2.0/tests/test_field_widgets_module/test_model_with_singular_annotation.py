"""Test class for testing annotations which result in a single input field.

Examples: int, str.
"""

import pytest
from pydantic import BaseModel
from textual.widgets import Input

from tests.app_with_form import MyApp
from ticklist.form import _Form


class MyStringModel(BaseModel):
    my_value: str


class MyStringModelWithDefault(BaseModel):
    my_value: str = "my_default"


class MyIntModel(BaseModel):
    my_value: int


class MyIntModelWithDefault(BaseModel):
    my_value: int = 999


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "app,result",
    [
        (MyApp(MyStringModel), {}),
        (MyApp(MyStringModelWithDefault), {"my_value": "my_default"}),
        (MyApp(MyIntModel), {}),
        (MyApp(MyIntModelWithDefault), {"my_value": "999"}),
    ],
)
async def test_initial_values(app, result):
    """Form object has default model value at startup."""

    async with app.run_test():
        my_form = app.query_one(_Form)

        assert my_form.obj == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "app,manual_input",
    [
        (MyApp(MyStringModel), "custom_string"),
        (MyApp(MyStringModelWithDefault), "custom_string"),
        (MyApp(MyIntModel), "12"),
        (MyApp(MyIntModelWithDefault), "12"),
    ],
)
async def test_manual_input(app, manual_input):
    """User entry in input ends up in form object."""

    async with app.run_test() as pilot:
        my_form = app.query_one(_Form)
        my_inp = app.query_one(Input)

        my_inp.clear()
        my_inp.focus()
        # simulate manual key presses.
        await pilot.press(*list(manual_input))

        assert my_form.obj == {"my_value": manual_input}
