"""Pydantic field widgets."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel
from textual.app import ComposeResult
from textual.geometry import Size
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Button, Input, Static
from typing_extensions import override

from ticklist.types import NO_VALUE

if TYPE_CHECKING:
    from ticklist.field_data import FieldData  # pragma: no cover


class FieldWidget(Static, can_focus=False):
    """A base widget displaying a (or part of a) pydantic field.

    Depending on annotation a pydantic field representation can consist
    of one or more widgets. If -for example- a `str` annotation is used,
    the field will get a string input widget. If an annotation representing
    multiple options (like a Union, Enum, Literal) multiple widgets will
    be displayed for that pydantic field.
    """

    DEFAULT_CSS = """
    FieldWidget {
        layout: horizontal;
        margin-left: 5;
    }
    Input {
        min-width: 40;
        width: auto;
    }

    """

    class ValueChanged(Message):
        """A value has changed."""

        def __init__(self, key: str, value: Any) -> None:
            """Init.

            Args:
                key: the key/field of the pydantic field.
                value: the value of the widget.
            """
            self.key = key
            self.value = value
            super().__init__()

    value: Any = reactive(NO_VALUE, init=False, always_update=True)
    """The pydantic value associated with the widget."""

    def __init__(self, field_data: FieldData) -> None:
        """Init.

        Args:
            field_data: Field data for this widget.
        """
        self._key = field_data.key
        # super needs to become before the setting of a reactive value.
        super().__init__(classes="field_widget")
        self.value = field_data.value

    def watch_value(self) -> None:
        """Watch the value property."""
        self.post_message(FieldWidget.ValueChanged(self._key, self.value))


class FieldWidgetForString(FieldWidget):
    """Input widget for strings."""

    @override
    def compose(self) -> ComposeResult:
        yield Input(
            value="" if self.value is NO_VALUE else str(self.value), classes="input"
        )

    def on_input_changed(self, event: Input.Changed) -> None:
        """Execute on input change."""
        event.stop()

        self.value = event.value


class FieldWidgetForInt(FieldWidget):
    """Input widget for ints."""

    @override
    def compose(self) -> ComposeResult:
        yield Input(
            value="" if self.value is NO_VALUE else str(self.value),
            classes="input",
            type="integer",
        )

    def on_input_changed(self, event: Input.Changed) -> None:
        """Execute on input change."""
        event.stop()

        self.value = event.value


class FieldWidgetForFixedValue(FieldWidget):
    """A fixed value item.

    A fixed value represents a choice from a range of values
    originating from a collection-like object (ie. a Union or Enum).
    This value will never be alone and always be displayed in a group
    of OptionContainers.
    """

    @override
    def __init__(self, field_data: FieldData) -> None:
        with self.prevent(FieldWidget.ValueChanged):
            super().__init__(field_data)

    @override
    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        return 1


class FieldWidgetForModel(FieldWidget):
    """A Field widget for a pydantic model."""

    class EditModel(Message):
        """Model encountered message."""

        def __init__(
            self, model: type[BaseModel], value: BaseModel, widget: FieldWidget
        ) -> None:
            """Init.

            Args:
                model: The encountered model.
                value: The instantiated model or Nothing.
                widget: This widget.
            """
            self.model = model
            self.value = value
            self.widget = widget
            super().__init__()

    @override
    def __init__(self, field_data: FieldData) -> None:
        self._label = field_data.label
        self._model = field_data.model
        super().__init__(field_data)

    @override
    def compose(self) -> ComposeResult:
        yield Button("edit", id="edit_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Run on button press."""
        event.stop()

        self.post_message(FieldWidgetForModel.EditModel(self._model, self.value, self))
