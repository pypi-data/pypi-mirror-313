"""Pydantic data form.

Create or edit pydantic objects by filling out a form.

Based on pydantic field data the form is
auto populated with the correct widgets to create/edit the pydantic model.

Example:
```python

class MyModel(BaseModel):
    name:str

    ports: int | Literal['ANY','OPAQUE'] = 10
```

This model results in the following form:

```
 ____________________________________________________
|                                                    |
|  name:                                             |
|      [_______________]                             |
|                                                    |
|  ports:                                            |
|      [x] manual input  [10___]                     |
|      [ ] ANY                                       |
|      [ ] OPAQUE                                    |
|                                                    |
|                                                    |
|                         [ OK ][ CANCEL ]           |
|                                                    |
|____________________________________________________|
```
"""

from typing import Any, Collection, Type, TypeVar

from pydantic import BaseModel, ValidationError
from pydantic_core import ErrorDetails
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Click, Key, Show
from textual.geometry import Size
from textual.message import Message
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Label, Pretty, Static
from typing_extensions import override

from ticklist.annotation_iterators import field_data_from_annotation
from ticklist.field_data import (
    FieldData,
)
from ticklist.field_widgets import (
    FieldWidget,
    FieldWidgetForModel,
)
from ticklist.types import NO_VALUE, NOTHING, AnnotationIterator


class _Option(Static, can_focus=True):
    """A checkbox belonging to a group.

    Only one item in a group can be checked.
    """

    DEFAULT_CLASSES = "field_option"

    DEFAULT_CSS = """
    _Option {
        width: auto;
        height: auto;
        align: left top;
        margin-right: 4;
    }
    _Option.checked {
        text-style: bold;
        color: $secondary
    }
    _Option:focus {
        color: $secondary-lighten-2;
    }
    """

    class Changed(Message):
        """Checked Message.

        Emitted when this option has changed.
        """

        def __init__(self, idx: int) -> None:
            """Init.

            Args:
                idx: The index of this option inside the option group.
            """
            self.idx = idx
            super().__init__()

    checked: reactive[bool] = reactive(False, init=False)
    """The value of the button. `True` for on, `False` for off."""

    def __init__(self, idx: int, checked: bool) -> None:
        """Init.

        Args:
            idx: Collection index of this Option inside the OptionGroup.
            checked: Whether this Option should be checked in compose.
        """
        super().__init__(classes="option")
        self.idx = idx
        self.checked = checked

    async def _on_click(self, event: Click) -> None:
        event.stop()
        if self.checked:
            # Cannot uncheck an option.
            return
        else:
            self.checked = True

    @on(Key)
    def key_pressed(self, key: Key) -> None:
        if key.key in ["space", "enter"]:
            self.checked = True

    def watch_checked(self) -> None:
        """React to the value being changed."""
        self.set_class(self.checked, "checked")

        if self.checked:
            self.post_message(self.Changed(self.idx))

    def render(self) -> str:
        """Render the checkbox."""
        if self.checked:
            return "[X]"
        else:
            return "[ ]"

    @override
    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        return 1

    @override
    def get_content_width(self, container: Size, viewport: Size) -> int:
        return 3


class _OptionGroup(Static, can_focus=False):
    """A group of FieldWidgets selectable by an option button."""

    DEFAULT_CSS = """
    .option_container {
        height:auto;
        layout: horizontal;
        # border: solid grey;
        margin-left: 3;
        margin-bottom: 0;  # Vertical space between individual options.
    }
    .field_label {
        # content-align: left middle;
        height: 100%;
    }
    """

    def __init__(
        self,
        field_data: Collection[FieldData],
    ) -> None:
        """Init.

        Args:
            field_data: Collection of FieldData objects.
                Used for composing the widgets.
        """
        self._field_data = field_data
        super().__init__(classes="option_group")

    @override
    def compose(self) -> ComposeResult:
        for idx, data in enumerate(self._field_data):
            with Horizontal(classes="option_container"):
                yield _Option(idx, data.active)
                yield Label(data.label, classes="field_widget_label")
                _field_widget = data.field_widget(data)
                _field_widget.disabled = not data.active
                yield _field_widget

    @on(_Option.Changed)
    def _option_checked(self, event: _Option.Changed) -> None:
        for container in self.query(Horizontal):
            _option = container.query_one(_Option)
            _field_widget = container.query_one(FieldWidget)

            if _option.idx == event.idx:
                # this field widget must be enabled.
                _field_widget.disabled = False
                self.post_message(
                    FieldWidget.ValueChanged(
                        _field_widget._key, value=_field_widget.value
                    )
                )
            else:
                _option.checked = False
                _field_widget.disabled = True


ModelType = TypeVar("ModelType", bound=BaseModel)


def form_factory(
    model_type: type[ModelType],
    instance: ModelType | NOTHING,
    annotation_iterators: Collection[AnnotationIterator],
) -> Screen[ModelType]:
    """Return a form with correct typing."""
    return _Form(model_type, instance, annotation_iterators)


class _Form(Screen):  # type: ignore
    """Pydantic form.

    Contains widgets for creating and editing pydantic objects.
    """

    DEFAULT_CSS = """
    .field_label {
        text-style: bold;
        margin-top:1;
    }
    .button_container {
        layout: horizontal;
        height: auto;
        margin-top:3;
    }
    .title {
        background: $secondary;
        text-style: bold;
        width: 100%;
        padding:1;
    }
    .field_error {
        color: $error;
    }
    """

    def __init__(
        self,
        model: Type[ModelType],
        instance: ModelType | NOTHING,
        annotation_iterators: Collection[AnnotationIterator],
        model_info: bool = False,
    ) -> None:
        """Init.

        Args:
            model: the Pydantic model.
                The annotation data in this model is used for populating
                this form.
            instance: An optional instance of this model containing
                (default) values to be used. Defaults to None.
            annotation_iterators: An annotation iterator evaluates an annotation and
                either results in a field data object or allows to continue iteration.
        """
        self._model = model
        self.obj: dict[str, Any] = {}
        self._instance = instance

        # copy of the instance in case this form
        # is cancelled and you need to return the old values.
        self._old_instance = instance

        self._annotation_iterators = annotation_iterators
        self._model_info = model_info
        super().__init__()

    def _instantiate(self) -> bool:
        errors: list[ErrorDetails] = []
        try:
            self._instance = self._model(**self.obj)

        except ValidationError as err:
            errors = err.errors(
                include_context=False, include_url=False, include_input=False
            )

            return False
        finally:
            self._display_issues(errors)
        return True

    def _display_issues(self, errors: list[ErrorDetails]) -> None:
        if self._model_info:
            error_output = self.query_one(Pretty)
            error_output.update(errors)

        print("display issues")
        labels = self.query(".field_label")
        for label in labels:
            _key = label.id.split("_", maxsplit=1)[-1]  # type: ignore
            for error in errors:
                if _key in error["loc"]:
                    label.add_class("field_error")
                    break
            else:
                label.remove_class("field_error")

    @override
    def compose(self) -> ComposeResult:
        yield Label(self._model.__name__, classes="title")
        for field, field_info in self._model.model_fields.items():
            if self._instance is NO_VALUE:
                value = NO_VALUE
            else:
                value = getattr(self._instance, field)

            # label showing the pydantic field/key.
            yield Label(field, classes="field_label", id=f"label_{field}")

            items = field_data_from_annotation(
                annotation=field_info.annotation,
                key=field,
                value=value,
                default=field_info.default,
                annotation_iterators=self._annotation_iterators,
                metadata=field_info.metadata,
            )

            if len(items) == 1:
                yield items[0].field_widget(items[0])
            else:
                yield _OptionGroup(items)

        if self._model_info:
            # the current value of the object from which we are going to instantiate
            # the model.
            yield Label(str(self.obj), id="obj")

        if self._model_info:
            # used for pydantic validation error output.

            yield Pretty("")

        with Container(classes="button_container"):
            yield Button("OK", variant="primary", id="ok")
            yield Button("CANCEL", variant="error", id="cancel")

    def _on_show(self, event: Show) -> None:
        self._instantiate()

    @on(FieldWidget.ValueChanged)
    def _field_widget_value_changed(self, event: FieldWidget.ValueChanged) -> None:
        """Run when a field-widget has changed its value."""
        event.stop()

        if event.value is NO_VALUE:
            # a field widget has been selected which has no value yet.
            # Further action from the user is required.
            # To prevent and old values to stick around we will
            # delete the key of this value.
            self.obj.pop(event.key, None)
        else:
            self.obj[event.key] = event.value
        if self._model_info:
            # this is here for debugging purposes and shows the dict with the latest values.
            lbl = self.query_one("#obj", expect_type=Label)
            lbl.update(str(self.obj))
        self._instantiate()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Run when button is pressed.

        This screen is popped from the view stack.
        When ok is pressed the resulting object is returned to the parent
        of this screen.
        On cancel, either the old instance is returned or None.
        """
        event.stop()

        match (event.button.id, self._instantiate(), self._old_instance):
            case "ok", True, _:
                self.dismiss(self._instance)
            case "cancel", _, NOTHING.token:
                self.dismiss(None)
            case "cancel", _, _:
                self.dismiss(self._old_instance)

    @on(FieldWidgetForModel.EditModel)
    def _on_edit_model(self, event: FieldWidgetForModel.EditModel) -> None:
        def form_close_callback(result: BaseModel | None) -> None:
            if result:
                event.widget.value = result

        self.app.push_screen(
            _Form(event.model, event.value, self._annotation_iterators),
            form_close_callback,
        )
