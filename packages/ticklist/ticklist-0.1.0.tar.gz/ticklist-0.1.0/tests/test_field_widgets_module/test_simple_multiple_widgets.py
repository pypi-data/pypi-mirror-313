"""Multiple widgets representing a single pydantic field.

Using the textual test frame work we create an app with a form
containing multiple widgets representing a single pydantic field.

    ____________________________________________________
    |                                                    |
    |  my_value:                                         |
    |      [ ] A                                         |
    |      [ ] B                                         |
    |                                                    |
    |                         [ OK ][ CANCEL ]           |
    |____________________________________________________|
"""

from enum import Enum
from typing import Literal

import pytest
from pydantic import BaseModel

from tests.app_with_form import MyApp
from tests.test_field_widgets_module import check_state, click_option_container
from ticklist.form import _Form


class LiteralModel(BaseModel):
    """The model which creates multiple field widgets."""

    my_value: Literal["A", "B"]


class EnumModelWithDefault(BaseModel):
    """Same as above, but with a default value and using enums."""

    class MyEnum(Enum):
        A = "A"
        B = "B"

    my_value: MyEnum = MyEnum.B


class BooleanModel(BaseModel):
    my_value: bool


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "app,result,enabled",
    [
        (MyApp(LiteralModel), {}, (False, False)),
        (
            MyApp(LiteralModel, LiteralModel(my_value="B")),
            {"my_value": "B"},
            (False, True),
        ),
        (
            MyApp(EnumModelWithDefault),
            {"my_value": EnumModelWithDefault.MyEnum.B},
            (False, True),
        ),
        (
            MyApp(
                EnumModelWithDefault,
                EnumModelWithDefault(my_value=EnumModelWithDefault.MyEnum.A),
            ),
            {"my_value": EnumModelWithDefault.MyEnum.A},
            (True, False),
        ),
        (MyApp(BooleanModel), {}, (False, False)),
        (
            MyApp(BooleanModel, BooleanModel(my_value=True)),
            {"my_value": True},
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
@pytest.mark.parametrize(
    "app,value",
    [
        (MyApp(LiteralModel), "A"),
        (MyApp(EnumModelWithDefault), EnumModelWithDefault.MyEnum.A),
    ],
)
async def test_manual_input(app, value):
    async with app.run_test() as pilot:
        my_form = app.query_one(_Form)
        option_1, option_2 = app.query(".option_container").nodes

        await click_option_container(option_1, pilot)
        check_state(option_1, True)
        check_state(option_2, False)
        assert my_form.obj == {"my_value": value}
