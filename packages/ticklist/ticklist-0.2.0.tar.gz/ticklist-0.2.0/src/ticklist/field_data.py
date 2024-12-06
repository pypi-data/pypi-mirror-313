"""Field data module.

Objects representing individual field annotations.
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from enum import Enum
from typing import Any, Self

from pydantic import BaseModel
from typing_extensions import override

from ticklist import tick_annotations as ta
from ticklist.field_widgets import (
    FieldWidget,
    FieldWidgetForFixedValue,
    FieldWidgetForInt,
    FieldWidgetForModel,
    FieldWidgetForString,
)
from ticklist.types import NO_VALUE


class FieldData(metaclass=ABCMeta):
    """A base field data object."""

    @property
    @abstractmethod
    def field_widget(self) -> type[FieldWidget]:
        """Associated FieldWidget."""

    def __init__(
        self,
        annotation: Any,
        key: str,
        value: Any,
        active: bool,
        label: str,
    ) -> None:
        """Init.

        Args:
            annotation: The (partial) annotation data
            key: The pydantic key/field.
            value: The value of this pydantic field.
            active: Active state.
            label: The label for this widget.
        """
        self.model = annotation
        self.key = key
        self.value = value
        self.active = active
        self.label = label

    @classmethod
    @abstractmethod
    def parse(
        cls,
        annotation: Any,
        key: str,
        value: Any,
        default: Any,
        metadata: ta.TickAnnotations,
    ) -> Self:
        """Return FieldData object(s) based on provided data.

        Args:
            annotation: An annotation (or partial).
            key: the field (key) for this annotation.
            value: An optional value.
            default: An optional default.
            metadata: Any information provided with the `Annotated` type annotation.
        """

    @staticmethod
    def _evaluate_values(
        annotation: Any,
        default: Any,
        value: Any,
        check: Callable[[Any, Any], bool],
    ) -> tuple[Any, bool]:
        """Return the value and active property of this match object.

        Args:
            annotation: field annotation info
            default: A default value
            value: A previously defined value
            check: the check to perform whether default or value match the annotation.
                This is a callable that excepts both default and value as arg 1 and the
                field info as arg 2.

        Returns:
            A value and an active boolean.

        A pydantic field can be represented by multiple field-widgets.
        For example the following model:

        ```python
        class MyModel(BaseModel):
            my_choice: int | str = 'abc'
        ```

        This results in two field widgets. An int and string widget (observe
        the checkbox at the start and the 'abc' value.):

        ```
        my_choice
            [x] manual entry (str)  [abc____]  # <-- string widget.
            [ ] manual entry (int)  [_______]  # <-- int widget.
        ```

        The default value of the pydantic field is 'abc' which
        makes the string widget "active" and have the value of "abc".

        But when the model is defined *without* default value none of the widgets
        would be "active" and have no value.

        Another scenario would be the above model with default of 'abc' but with an
        extra value provided (When you're editing an earlier object for example).

        ```python
        # the added value for MyModel (which matches the int annotation):

        model = MyModel(my_choice=22)
        ```

        This would result in the following widget:

        ```
        my_choice
            [ ] manual entry (str)  [abc____]  # <-- string widget.
            [x] manual entry (int)  [22_____]  # <-- int widget.
        ```

        - The string widget has the default value but is *not* active.
        - The int widget has the provided value *and* is active.


        The above scenarios are evaluated based on the provided annotation,
        the defined default and an optional value. The following scenarios can occur:

        incoming           |  result
                           |
        default   value    |   value     active
        ---------------------------------------
        match     match    |   =value    true
        match     NO_VALUE |   =default  true
        match     no-match |   =default  false

        no-match  match    |   =value    true
        no-match  NO_VALUE |   NO_VALUE  false
        no-match  no-match |   NO_VALUE  false
                           |
        NO_VALUE  match    |   =value    true
        NO_VALUE  NO_VALUE |   NO_VALUE  false
        NO_VALUE  no-match |   NO_VALUE  false

        """
        _value = NO_VALUE
        _active = False
        if check(default, annotation):
            _value = default
            if value is NO_VALUE:
                _active = True
        if check(value, annotation):
            _value = value
            _active = True

        return _value, _active


class FieldDataForString(FieldData):
    """Field data for a string type."""

    @property
    def field_widget(self) -> type[FieldWidget]:
        """Associated FieldWidget."""
        return FieldWidgetForString

    @override
    @classmethod
    def parse(
        cls,
        annotation: Any,
        key: str,
        value: Any,
        default: Any,
        metadata: ta.TickAnnotations,
    ) -> Self:
        def _check(value: Any, annotation: Any) -> bool:
            return isinstance(value, annotation)

        _value, _active = cls._evaluate_values(annotation, default, value, _check)

        return cls(
            annotation=annotation,
            key=key,
            value=_value,
            active=_active,
            label="manual input",
        )


class FieldDataForInt(FieldData):
    """Field data for an int type."""

    @property
    def field_widget(self) -> type[FieldWidget]:
        """Associated FieldWidget."""
        return FieldWidgetForInt

    @override
    @classmethod
    def parse(
        cls,
        annotation: Any,
        key: str,
        value: Any,
        default: Any,
        metadata: ta.TickAnnotations,
    ) -> Self:
        def _check(value: Any, annotation: Any) -> bool:
            return isinstance(value, annotation)

        _value, _active = cls._evaluate_values(annotation, default, value, _check)

        return cls(
            annotation=annotation,
            key=key,
            value=_value,
            active=_active,
            label="manual input",
        )


class FieldDataForEnumValue(FieldData):
    """Field data for an Enum value.

    Not to be mistaken for an enum type.
    This is one item from a defined enum.
    """

    @property
    def field_widget(self) -> type[FieldWidget]:
        """Associated FieldWidget."""
        return FieldWidgetForFixedValue

    @override
    @classmethod
    def parse(
        cls,
        annotation: Enum,
        key: str,
        value: Any,
        default: Any,
        metadata: ta.TickAnnotations,
    ) -> Self:
        def check(value: Any, annotation: Any) -> bool:
            if value == annotation:
                return True
            return False

        _, _active = cls._evaluate_values(annotation, default, value, check)
        return cls(
            annotation=annotation,
            key=key,
            value=annotation,
            active=_active,
            label=str(annotation.value),
        )


class FieldDataForLiteralValue(FieldData):
    """Field data for a Literal value.

    Not to be mistaken for a Literal type.
    This is one item from a defined Literal type.
    """

    @property
    def field_widget(self) -> type[FieldWidget]:
        """Associated FieldWidget."""
        return FieldWidgetForFixedValue

    @override
    @classmethod
    def parse(
        cls,
        annotation: str,
        key: str,
        value: Any,
        default: Any,
        metadata: ta.TickAnnotations,
    ) -> Self:
        def check(value: Any, annotation: Any) -> bool:
            if value == annotation:
                return True
            return False

        _, _active = cls._evaluate_values(annotation, default, value, check)
        return cls(
            annotation=annotation,
            key=key,
            value=annotation,
            active=_active,
            label=annotation,
        )


class FieldDataForNoneValue(FieldData):
    """Field data for none value."""

    @property
    def field_widget(self) -> type[FieldWidget]:
        """Associated FieldWidget."""
        return FieldWidgetForFixedValue

    @override
    @classmethod
    def parse(
        cls,
        annotation: None,
        key: str,
        value: Any,
        default: Any,
        metadata: ta.TickAnnotations,
    ) -> Self:
        def check(value: Any, annotation: Any) -> bool:
            if value is annotation:
                return True
            return False

        _, _active = cls._evaluate_values(annotation, default, value, check)
        return cls(
            annotation=annotation,
            key=key,
            value=annotation,
            active=_active,
            label="None",
        )


class FieldDataForBooleanValue(FieldData):
    """Field data for a boolean value."""

    @property
    def field_widget(self) -> type[FieldWidget]:
        """Associated FieldWidget."""
        return FieldWidgetForFixedValue

    @override
    @classmethod
    def parse(
        cls,
        annotation: bool,
        key: str,
        value: Any,
        default: Any,
        metadata: ta.TickAnnotations,
    ) -> Self:
        def check(value: Any, annotation: Any) -> bool:
            if value is annotation:
                return True
            return False

        _, _active = cls._evaluate_values(annotation, default, value, check)

        if boolean_label := metadata.get("boolean_labels", None):
            if annotation:
                label = boolean_label.label_for_true
            else:
                label = boolean_label.label_for_false
        else:
            label = str(annotation)

        return cls(
            annotation=annotation,
            key=key,
            value=annotation,
            active=_active,
            label=label,
        )


class FieldDataForModel(FieldData):
    """Field data for a pydantic model."""

    @property
    def field_widget(self) -> type[FieldWidget]:
        """Associated FieldWidget."""
        return FieldWidgetForModel

    @override
    @classmethod
    def parse(
        cls,
        annotation: type[BaseModel],
        key: str,
        value: Any,
        default: Any,
        metadata: ta.TickAnnotations,
    ) -> Self:
        def _check(value: Any, annotation: type[BaseModel]) -> bool:
            return isinstance(value, annotation)

        if label_data := metadata.get("label"):
            label = label_data.value
        else:
            label = "define"

        _value, _active = cls._evaluate_values(annotation, default, value, check=_check)
        return cls(annotation, key=key, value=_value, active=_active, label=label)
