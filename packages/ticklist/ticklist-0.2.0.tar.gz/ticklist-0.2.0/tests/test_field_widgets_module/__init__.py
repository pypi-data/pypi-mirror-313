from uuid import uuid4

from textual.containers import Container

from ticklist.form import _Option


def check_state(option_container: Container, enabled: bool):
    """Check the state of the checkbox and field widget inside the option_container

    helper function.
    """
    field_widget = option_container.query_one("FieldWidget")
    option = option_container.query_one(_Option)

    assert field_widget.disabled is not enabled
    assert option.checked is enabled


async def click_option_container(option_container: Container, pilot):
    """Make this option container active by clicking the option checkbox.

    helper function.
    """
    option = option_container.query_one(_Option)
    if not option.id:
        option.id = f"custom_id{uuid4()!s}"

    await pilot.click(f"#{option.id}")
