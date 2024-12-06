from enum import Enum
from types import NoneType
from typing import Annotated, Literal

import pytest
from pydantic import BaseModel

from tests.conftest import compare_items
from ticklist import tick_annotations as ta
from ticklist.annotation_iterators import (
    ANNOTATION_ITERATORS,
    StringAndLiteralAnnotationNotAllowed,
    annotated_iterator,
    field_data_from_annotation,
)
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
from ticklist.types import NO_VALUE


def test_find_match_fail():
    with pytest.raises(ValueError):
        field_data_from_annotation(
            annotation=object(),
            key="my_key",
            value=NO_VALUE,
            default=NO_VALUE,
            annotation_iterators=[annotated_iterator],
            metadata={},
        )  # type: ignore


@pytest.mark.parametrize(
    "default,value,expected",
    [
        ("default_match", "value_match", ("value_match", True)),
        ("default_match", NO_VALUE, ("default_match", True)),
        # the matcher has a value of default,
        # but is not active as the current pydantic field
        # has a value which does not match this specific match object.
        ("default_match", 100, ("default_match", False)),
        (100, "value_match", ("value_match", True)),
        (100, NO_VALUE, (NO_VALUE, False)),
        (100, 100, (NO_VALUE, False)),
        (NO_VALUE, "value_match", ("value_match", True)),
        (NO_VALUE, NO_VALUE, (NO_VALUE, False)),
        (NO_VALUE, 100, (NO_VALUE, False)),
    ],
)
def test_evaluate_values(default, value, expected):
    """Checking output according to table as provided in the docstring."""

    def str_check(value, annotation) -> bool:
        return isinstance(value, annotation)

    result = FieldData._evaluate_values(
        annotation=str, default=default, value=value, check=str_check
    )

    assert result == expected


def test_field_data_for_string():
    class MyStringModel(BaseModel):
        my_string: str = "abc"

    key = "my_string"
    field_info = MyStringModel.model_fields[key]

    items = list(
        field_data_from_annotation(
            annotation=field_info.annotation,
            key=key,
            value=NO_VALUE,
            default=field_info.default,
            annotation_iterators=ANNOTATION_ITERATORS,
            metadata={},
        )
    )

    compare_items(
        items,
        FieldDataForString(
            annotation=field_info.annotation,
            key=key,
            value="abc",
            active=True,
            label="manual input",
        ),
    )


def test_field_data_for_optional_string():
    class MyOptionalString(BaseModel):
        optional_string: str | None = None

    key = "optional_string"
    field_info = MyOptionalString.model_fields[key]

    items = list(
        field_data_from_annotation(
            annotation=field_info.annotation,
            key=key,
            value=NO_VALUE,
            default=field_info.default,
            annotation_iterators=ANNOTATION_ITERATORS,
            metadata={},
        )
    )

    compare_items(
        items,
        FieldDataForString(
            annotation=str,
            key=key,
            value=NO_VALUE,
            active=False,
            label="manual input",
        ),
        FieldDataForNoneValue(
            annotation=NoneType(),
            key=key,
            active=True,
            value=None,
            label="None",
        ),
    )


def test_field_data_for_int():
    class MyModel(BaseModel):
        my_int: int = 10

    key = "my_int"
    field_info = MyModel.model_fields[key]

    items = list(
        field_data_from_annotation(
            annotation=field_info.annotation,
            key=key,
            value=NO_VALUE,
            default=field_info.default,
            annotation_iterators=ANNOTATION_ITERATORS,
            metadata={},
        )
    )

    compare_items(
        items,
        FieldDataForInt(
            annotation=field_info.annotation,
            key=key,
            value=10,
            active=True,
            label="manual input",
        ),
    )


def test_field_data_for_enum():
    class MyEnum(Enum):
        one = "one"
        two = "two"

    class EnumModel(BaseModel):
        choice: MyEnum = MyEnum.two

    field = "choice"
    field_info = EnumModel.model_fields[field]

    items = list(
        field_data_from_annotation(
            annotation=field_info.annotation,
            key=field,
            value=NO_VALUE,
            default=field_info.default,
            annotation_iterators=ANNOTATION_ITERATORS,
            metadata={},
        )
    )

    compare_items(
        items,
        FieldDataForEnumValue(
            MyEnum.one, "choice", MyEnum.one, active=False, label="one"
        ),
        FieldDataForEnumValue(
            MyEnum.two, "choice", MyEnum.two, active=True, label="two"
        ),
    )


def test_field_data_for_new_style_union():
    class MyEnum(Enum):
        one = "one"
        two = "two"

    class MyEnumOrString(BaseModel):
        my_value: MyEnum | str

    key = "my_value"
    field_info = MyEnumOrString.model_fields[key]

    items = field_data_from_annotation(
        annotation=field_info.annotation,
        key=key,
        value=NO_VALUE,
        default=field_info.default,
        annotation_iterators=ANNOTATION_ITERATORS,
        metadata={},
    )

    compare_items(
        items,
        FieldDataForEnumValue(
            MyEnum.one, key=key, value=MyEnum.one, active=False, label="one"
        ),
        FieldDataForEnumValue(
            MyEnum.two, key=key, value=MyEnum.two, active=False, label="two"
        ),
        FieldDataForString(
            annotation=str, key=key, value=NO_VALUE, active=False, label="manual input"
        ),
    )


def test_field_data_for_old_style_union():
    class MyEnum(Enum):
        A = "A"
        B = "B"

    class MyEnumOrString(BaseModel):
        my_value: MyEnum | str = MyEnum.B

    key = "my_value"
    field_info = MyEnumOrString.model_fields[key]

    items = field_data_from_annotation(
        annotation=field_info.annotation,
        key=key,
        value=NO_VALUE,
        default=field_info.default,
        annotation_iterators=ANNOTATION_ITERATORS,
        metadata={},
    )

    compare_items(
        items,
        FieldDataForEnumValue(
            MyEnum.A, key=key, value=MyEnum.A, active=False, label="A"
        ),
        FieldDataForEnumValue(
            MyEnum.B, key=key, value=MyEnum.B, active=True, label="B"
        ),
        FieldDataForString(
            str, key=key, value=NO_VALUE, active=False, label="manual input"
        ),
    )


def test_field_data_for_model():
    class SubModel(BaseModel):
        my_value: str

    class MyMainModel(BaseModel):
        my_sub_model: SubModel

    key = "my_sub_model"
    field_info = MyMainModel.model_fields[key]

    items = field_data_from_annotation(
        annotation=field_info.annotation,
        key=key,
        value=NO_VALUE,
        default=field_info.default,
        annotation_iterators=ANNOTATION_ITERATORS,
        metadata={},
    )

    compare_items(
        items,
        FieldDataForModel(
            SubModel, key=key, value=NO_VALUE, active=False, label="define"
        ),
    )


def test_field_data_union_with_models():
    class SubModel1(BaseModel):
        my_value: str

    class SubModel2(BaseModel):
        my_value: str

    class Model(BaseModel):
        model: (
            Annotated[SubModel1, ta.Label("submodel 1")]
            | Annotated[SubModel2, ta.Label("submodel 2")]
        )

    key = "model"
    field_info = Model.model_fields[key]

    items = field_data_from_annotation(
        annotation=field_info.annotation,
        key=key,
        value=NO_VALUE,
        default=field_info.default,
        annotation_iterators=ANNOTATION_ITERATORS,
        metadata=field_info.metadata,
    )

    compare_items(
        items,
        FieldDataForModel(
            SubModel1, key=key, value=NO_VALUE, active=False, label="submodel 1"
        ),
        FieldDataForModel(
            SubModel2, key=key, value=NO_VALUE, active=False, label="submodel 2"
        ),
    )


def test_field_data_for_literal():
    class Model(BaseModel):
        value: Literal["A", "B"] = "B"

    key = "value"
    field_info = Model.model_fields[key]
    items = field_data_from_annotation(
        annotation=field_info.annotation,
        key=key,
        value=NO_VALUE,
        default=field_info.default,
        annotation_iterators=ANNOTATION_ITERATORS,
        metadata=[],
    )

    compare_items(
        items,
        FieldDataForLiteralValue("A", key=key, value="A", active=False, label="A"),
        FieldDataForLiteralValue("B", key=key, value="B", active=True, label="B"),
    )


def test_field_data_for_boolean():
    class Model(BaseModel):
        value: bool

    key = "value"
    field_info = Model.model_fields[key]
    items = field_data_from_annotation(
        annotation=field_info.annotation,
        key=key,
        value=NO_VALUE,
        default=field_info.default,
        annotation_iterators=ANNOTATION_ITERATORS,
        metadata=field_info.metadata,
    )

    compare_items(
        items,
        FieldDataForBooleanValue(
            True,
            key=key,
            value=True,
            active=False,
            label="True",
        ),
        FieldDataForBooleanValue(
            False,
            key=key,
            value=False,
            active=False,
            label="False",
        ),
    )


def test_field_data_for_boolean_with_label():
    class Model(BaseModel):
        value: Annotated[bool, ta.BooleanLabels("YES", "NO")]

    key = "value"
    field_info = Model.model_fields[key]
    items = field_data_from_annotation(
        annotation=field_info.annotation,
        key=key,
        value=NO_VALUE,
        default=field_info.default,
        annotation_iterators=ANNOTATION_ITERATORS,
        metadata=field_info.metadata,
    )

    compare_items(
        items,
        FieldDataForBooleanValue(True, key=key, value=True, active=False, label="YES"),
        FieldDataForBooleanValue(False, key=key, value=False, active=False, label="NO"),
    )


def test_disallowed_string_and_literal():
    """Combination of String and Literal is not allowed.

    See exception docstring for more info.
    """

    class Model(BaseModel):
        value: Literal["B"] | str

    key = "value"
    field_info = Model.model_fields[key]

    with pytest.raises(StringAndLiteralAnnotationNotAllowed):
        field_data_from_annotation(
            annotation=field_info.annotation,
            key=key,
            value=NO_VALUE,
            default=field_info.default,
            annotation_iterators=ANNOTATION_ITERATORS,
            metadata=field_info.metadata,
        )
