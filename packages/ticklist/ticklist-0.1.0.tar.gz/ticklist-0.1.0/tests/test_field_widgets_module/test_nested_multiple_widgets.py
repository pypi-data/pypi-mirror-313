"""Multiple widgets representing a single pydantic field.

Using the textual test frame work we create an app with a form
containing multiple widgets representing a single pydantic field.
"""

from typing import Literal

import pytest
from pydantic import BaseModel
from textual.widgets import Input

from tests.app_with_form import MyApp
from tests.test_field_widgets_module import check_state, click_option_container
from ticklist.form import _Form


class MyModel(BaseModel):
    """The model which creates multiple field widgets.
    It will create the following form:
    ____________________________________________________
    |                                                    |
    |  my_value:                                         |
    |      [ ] A                                         |
    |      [ ] manual input _______________              |
    |                                                    |
    |                         [ OK ][ CANCEL ]           |
    |____________________________________________________|

    """

    my_value: Literal["A"] | int


class MyModelWithDefault(BaseModel):
    """Same as above, but with a default value."""

    my_value: Literal["A"] | int = 5


class MyModelWithOptional(BaseModel):
    my_value: int | None = None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "app,result,enabled",
    [
        (MyApp(MyModel), {}, (False, False)),
        (MyApp(MyModelWithDefault), {"my_value": "5"}, (False, True)),
        (
            MyApp(MyModelWithDefault, MyModelWithDefault(my_value="A")),
            {"my_value": "A"},
            (True, False),
        ),
        (MyApp(MyModelWithOptional), {"my_value": None}, (False, True)),
        (
            MyApp(MyModelWithOptional, MyModelWithOptional(my_value=1)),
            {"my_value": "1"},
            (True, False),
        ),
    ],
)
async def test_initial_values(app, result, enabled):
    """Form object has default model value at startup."""
    async with app.run_test():
        my_form = app.query_one(_Form)
        option_1, option_2 = app.query(".option_container").nodes

        check_state(option_1, enabled[0])
        check_state(option_2, enabled[1])
        assert my_form.obj == result


@pytest.mark.asyncio
async def test_manual_input():
    app = MyApp(MyModel)
    async with app.run_test() as pilot:
        my_form = app.query_one(_Form)
        option_1, int_input = app.query(".option_container").nodes

        # select the first option
        await click_option_container(option_1, pilot)
        check_state(option_1, True)
        check_state(int_input, False)
        assert my_form.obj == {"my_value": "A"}

        # select the second option
        await click_option_container(int_input, pilot)
        inp = int_input.query_one(Input)
        inp.focus()
        await pilot.press(*list("123"))
        check_state(option_1, False)
        check_state(int_input, True)
        assert my_form.obj == {"my_value": "123"}
