"""Annotation iterators."""

from __future__ import annotations

import logging
from enum import Enum
from inspect import isclass
from types import NoneType, UnionType
from typing import Any, Collection, Iterable, Literal, get_args

from pydantic import BaseModel

from ticklist import tick_annotations as ta
from ticklist.field_data import (
    FieldData,
    FieldDataForBooleanValue,
    FieldDataForEnumValue,
    FieldDataForInt,
    FieldDataForLiteralValue,
    FieldDataForModel,
    FieldDataForNoneValue,
    FieldDataForString,
)
from ticklist.types import AnnotationIterator

_logger = logging.getLogger(__name__)


class StringAndLiteralAnnotationNotAllowed(Exception):
    """A combination of `Literal` and `str` is not allowed.

    It can produce unwanted results.
    Consider this example:

    ```python
    class MyModel(BaseModel):
        my_value: Literal['B','A'] | str = 'A'
    ```

    All annotations are traversed (Literal['A'], Literal['B'] and str) and
    evaluated with the default value of 'A'. This will match on both the
    Literal['A'] and the str, activating both, which is an error.

    An alternative to the Literal would be the use of an Enum.
    """

    def __init__(self, annotation: Any) -> None:
        """Init.

        Args:
            annotation: The failing annotation.
        """
        self.annotation = annotation
        super().__init__(
            f"Annotation with `Literal` AND `str` is not allowed. {self.annotation=}"
        )


def field_data_from_annotation(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    annotation_iterators: Collection[AnnotationIterator],
    metadata: list[Any],
) -> tuple[FieldData, ...]:
    """Extract FieldData objects from annotation information.

    Args:
        annotation: The type annotation.
        key: The key of the (pydantic) field.
        value: An optional value of the key.
        default: An optional default value of the key.
        annotation_iterators: A collection of annotation iterators.
        metadata: metadata provided by the pydantic model.

    Raises:
        StringAndLiteralAnnotationNotAllowed: _description_

    Returns:
        _description_
    """
    _tick_annotations = ta.to_tick_annotations(metadata)

    field_data = tuple(
        _iter_over_annotation(
            annotation, key, value, default, annotation_iterators, _tick_annotations
        )
    )

    _field_data_types = set((fd.__class__ for fd in field_data))

    if ({FieldDataForString, FieldDataForLiteralValue}).issubset(_field_data_types):
        raise StringAndLiteralAnnotationNotAllowed(annotation)

    return field_data


def bool_type_iterator(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    metadata: ta.TickAnnotations,
) -> Iterable[tuple[Any, ta.TickAnnotations]]:
    """Yield values for a boolean annotation."""
    if annotation is bool:
        _logger.debug("annotation: Bool %s", annotation)
        yield (
            FieldDataForBooleanValue.parse(True, key, value, default, metadata),
            metadata,
        )
        yield (
            FieldDataForBooleanValue.parse(False, key, value, default, metadata),
            metadata,
        )


def none_type_iterator(
    annotation: Any, key: str, value: Any, default: Any, metadata: ta.TickAnnotations
) -> Iterable[tuple[Any, ta.TickAnnotations]]:
    """Yield a value for a none type."""
    if annotation is NoneType:
        yield (
            FieldDataForNoneValue.parse(None, key, value, default, metadata),
            metadata,
        )


def enum_type_iterator(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    metadata: ta.TickAnnotations,
) -> Iterable[tuple[Any, ta.TickAnnotations]]:
    """Yield values for an enum annotation."""
    if isclass(annotation) and issubclass(annotation, Enum):
        _logger.debug("annotation: Enum class %s", annotation)
        for anno in annotation:
            yield anno, metadata


def enum_item_type_iterator(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    metadata: ta.TickAnnotations,
) -> Iterable[tuple[FieldDataForEnumValue, ta.TickAnnotations]]:
    """Yield value for an individual enum item."""
    if isinstance(annotation, Enum):
        _logger.debug("annotation: Enum value %s", annotation)
        yield (
            FieldDataForEnumValue.parse(annotation, key, value, default, metadata),
            metadata,
        )


def str_type_iterator(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    metadata: ta.TickAnnotations,
) -> Iterable[tuple[FieldDataForString, ta.TickAnnotations]]:
    """Yield value for a string annotation."""
    if isclass(annotation) and issubclass(annotation, str):
        _logger.debug("annotation: str %s", annotation)
        yield (
            FieldDataForString.parse(annotation, key, value, default, metadata),
            metadata,
        )


def int_type_iterator(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    metadata: ta.TickAnnotations,
) -> Iterable[tuple[FieldDataForInt, ta.TickAnnotations]]:
    """Yield value of an int annotation."""
    if isclass(annotation) and issubclass(annotation, int):
        _logger.debug("annotation: Int %s", annotation)
        yield FieldDataForInt.parse(annotation, key, value, default, metadata), metadata


def union_type_iterator(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    metadata: ta.TickAnnotations,
) -> Iterable[Any]:
    """Yield values for a union annotation."""
    # Nowadays Unions are created using the pipe | character, where earlier
    # a typing.Union was used. Both are also stored differently
    # (Inside the __annotation__ property
    # or the FieldInfo.annotation of a pydantic field).
    #
    # A bit more strange is that in some situations even when using the pipe | character
    # the annotation is still stored in the old style.
    # This at least appears when a Literal type is involved. This might change
    # in future python version, but for now, this union check looks for both
    # union styles.
    if isinstance(annotation, UnionType) or getattr(annotation, "__name__", None) in (
        "Optional",
        "Union",
    ):
        _logger.debug("annotation: Union %s", annotation)
        for arg in get_args(annotation):
            yield arg, metadata


def model_type_iterator(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    metadata: ta.TickAnnotations,
) -> Iterable[Any]:
    """Yield value for a pydantic BaseModel annotation."""
    if isclass(annotation) and issubclass(annotation, BaseModel):
        _logger.debug("annotation: Basemodel %s", annotation)
        yield FieldDataForModel.parse(annotation, key, value, default, metadata), None


def literal_type_iterator(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    metadata: ta.TickAnnotations,
) -> Iterable[Any]:
    """Yield values for a Literal annotation."""
    origin = getattr(annotation, "__origin__", None)
    if origin is Literal:
        _logger.debug("annotation: Literal definition %s", annotation)
        for arg in get_args(annotation):
            yield arg, metadata


def literal_value_iterator(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    metadata: ta.TickAnnotations,
) -> Iterable[tuple[FieldDataForLiteralValue, ta.TickAnnotations]]:
    """Yield values for a Literal Value annotation."""
    if isinstance(annotation, str):
        _logger.debug("annotation: Literal value %s", annotation)
        yield (
            FieldDataForLiteralValue.parse(annotation, key, value, default, metadata),
            metadata,
        )


def annotated_iterator(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    metadata: ta.TickAnnotations,
) -> Iterable[tuple[Any, ta.TickAnnotations]]:
    """Yield values defined inside an annotation."""
    nm = getattr(annotation, "__name__", None)
    if nm == "Annotated":
        _anno = annotation.__origin__

        _meta = metadata | ta.to_tick_annotations(annotation.__metadata__)

        yield _anno, _meta


ANNOTATION_ITERATORS: tuple[AnnotationIterator, ...] = (
    bool_type_iterator,
    none_type_iterator,
    enum_type_iterator,
    enum_item_type_iterator,
    str_type_iterator,
    int_type_iterator,
    union_type_iterator,
    model_type_iterator,
    literal_type_iterator,
    literal_value_iterator,
    annotated_iterator,
)


def _iter_over_annotation(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    annotation_iterators: Collection[AnnotationIterator],
    metadata: ta.TickAnnotations,
) -> Iterable[FieldData]:
    if isinstance(annotation, FieldData):
        yield annotation

    else:
        found = False
        for annotation_iterator in annotation_iterators:
            for _annotation, meta in annotation_iterator(
                annotation, key, value, default, metadata=metadata
            ):
                found = True
                yield from _iter_over_annotation(
                    _annotation, key, value, default, annotation_iterators, meta
                )
            if found:
                break
        else:
            raise ValueError(f"No FieldDataType found for {annotation}")
