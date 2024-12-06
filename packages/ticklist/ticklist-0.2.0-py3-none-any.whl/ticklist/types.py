"""Tui-forms custom types."""

from enum import Enum
from typing import Any, Iterable, Protocol

from ticklist.tick_annotations import TickAnnotations


# For passing "undefined or none" values to and from widgets and forms, we
# will be using the NO_VALUE sentinel instead of `None`:
# In some cases `None` can be a valid value instead of a passing sentinel.
# For this reason and to avoid confusion NO_VALUE will be used everywhere.
class NOTHING(Enum):
    """A nothing enum.

    An implementation for a Sentinel value for NO_VALUE as suggested here:
    https://peps.python.org/pep-0484/#support-for-singleton-types-in-unions
    """

    token = 0


NO_VALUE: NOTHING = NOTHING.token


class AnnotationIterator(Protocol):
    """Annotation iterator protocol."""

    def __call__(
        self,
        annotation: Any,
        key: str,
        value: Any,
        default: Any,
        metadata: TickAnnotations,
    ) -> Iterable[tuple[Any, TickAnnotations]]:
        """Execute when called.

        Args:
            annotation: The annotation under evaluation.
            key: The key of the pydantic field.
            value: The optional value of the key.
            default: The optional default value of the key.
            metadata: Any information provided with the `Annotated` type annotation.

        Returns:
            Either a FieldData object, more annotations to be evaluated
                (when dealing with multiple possible field data objects,
                like in Unions/Enums etc.)
            or nothing (when the iterator does not match the annotation).
        """
