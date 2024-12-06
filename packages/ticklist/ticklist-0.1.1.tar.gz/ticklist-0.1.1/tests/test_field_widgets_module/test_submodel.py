import pytest
from pydantic import BaseModel
from textual.widgets import Input

from tests.app_with_form import MyApp
from ticklist.form import _Form


class MyModel(BaseModel):
    class SubModel(BaseModel):
        my_value: str = "some_default"

    my_sub_model: SubModel


class MyModelWithDefault(BaseModel):
    class SubModel(BaseModel):
        my_value: str = "some_default"

    my_sub_model: SubModel = SubModel()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "app,result",
    [
        (MyApp(MyModel), {}),
        (
            MyApp(MyModelWithDefault),
            {"my_sub_model": MyModelWithDefault.SubModel()},
        ),
        (
            MyApp(
                MyModelWithDefault,
                MyModelWithDefault(**{"my_sub_model": {"my_value": "A"}}),
            ),
            {"my_sub_model": MyModelWithDefault.SubModel(**{"my_value": "A"})},
        ),
    ],
)
async def test_initial_values(app, result):
    """Form object has default model value at startup."""
    async with app.run_test():
        my_form = app.query_one(_Form)

        assert my_form.obj == result


@pytest.mark.asyncio
async def test_manual_input():
    app = MyApp(MyModel)

    async with app.run_test() as pilot:
        my_main_model_form = app.query_one(_Form)
        assert my_main_model_form.obj == {}
        # this will push a new form with SubModel as form data.
        await pilot.click("#edit_button")

        # Return to the previous screen (with model MyMainModel) by cancelling.
        await pilot.click("#cancel")
        assert my_main_model_form.obj == {}

        # Open the submodel form again.
        await pilot.click("#edit_button")
        # Return to the previous screen (with model MyMainModel) but now by "OK".
        await pilot.click("#ok")
        assert my_main_model_form.obj == {
            "my_sub_model": MyModel.SubModel(**{"my_value": "some_default"})
        }

        # open the form again to edit the SubModel
        await pilot.click("#edit_button")

        # cancel again
        await pilot.click("#cancel")
        assert my_main_model_form.obj == {
            "my_sub_model": MyModel.SubModel(**{"my_value": "some_default"})
        }

        # open the form again to edit the SubModel
        await pilot.click("#edit_button")

        # get the input field for the "my_value" property of the SubModel
        sub_model_form = app.query(_Form).last()
        inp = sub_model_form.query_one(Input)
        inp.clear()
        inp.focus()

        await pilot.press(*list("Another value"))
        # we make sure the object is updated.
        assert sub_model_form.obj == {"my_value": "Another value"}

        # but we cancel and check whether we have still the previous value.
        await pilot.click("#cancel")
        assert my_main_model_form.obj == {
            "my_sub_model": MyModel.SubModel(**{"my_value": "some_default"})
        }
