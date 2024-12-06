from typing import Literal
from uuid import uuid4

import pytest
from pydantic import BaseModel

from tests.app_with_form import MyApp
from tests.test_field_widgets_module import check_state, click_option_container
from ticklist.form import _Form, _Option


@pytest.mark.asyncio
async def test_option_container_double_click():
    """Multiple clicks on option group does not change state.

    An option container is always part of a group. Inside this group
    only one option can be active and you can not "unselect" an option
    by clicking it a second time.
    """

    class MyModel(BaseModel):
        my_value: Literal["A", "B"]

    app = MyApp(MyModel)

    async with app.run_test() as pilot:
        form = app.query_one(_Form)
        option_1, option_2 = app.query(".option_container").nodes

        await click_option_container(option_1, pilot)
        check_state(option_1, True)
        check_state(option_2, False)
        assert form.obj == {"my_value": "A"}

        # doing an identical click. check whether nothing has changed.
        await click_option_container(option_1, pilot)
        check_state(option_1, True)
        check_state(option_2, False)
        assert form.obj == {"my_value": "A"}


@pytest.mark.asyncio
@pytest.mark.parametrize("keys", ["space", "enter"])
async def test_checkbox_by_key(keys):
    class MyModel(BaseModel):
        my_value: Literal["A", "B"]

    app = MyApp(MyModel)

    async with app.run_test() as pilot:
        form = app.query_one(_Form)
        option_1, option_2 = app.query(".option_container").nodes

        check_state(option_1, False)
        check_state(option_2, False)

        option = option_1.query_one(_Option)
        option.focus()

        await pilot.press(keys)

        check_state(option_1, True)
        assert form.obj == {"my_value": "A"}
