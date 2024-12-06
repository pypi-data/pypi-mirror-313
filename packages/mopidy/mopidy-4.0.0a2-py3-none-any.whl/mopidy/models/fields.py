from __future__ import annotations

import sys
from collections.abc import Callable
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    TypeVar,
    cast,
    overload,
)

from mopidy.types import Uri

if TYPE_CHECKING:
    from collections.abc import Iterable

T = TypeVar("T")
V = TypeVar("V")
TField = TypeVar("TField", bound="Field")


class Field(Generic[T]):
    """Base field for use in
    :class:`~mopidy.models.immutable.ValidatedImmutableObject`. These fields
    are responsible for type checking and other data sanitation in our models.

    For simplicity fields use the Python descriptor protocol to store the
    values in the instance dictionary. Also note that fields are mutable if
    the object they are attached to allow it.

    Default values will be validated with the exception of :class:`None`.

    :param default: default value for field
    :param type: if set the field value must be of this type
    :param choices: if set the field value must be one of these
    """

    def __init__(
        self,
        default: T | None = None,
        type: type[T] | None = None,
        choices: Iterable[T] | None = None,
    ) -> None:
        self._name: str | None = None  # Set by ValidatedImmutableObjectMeta
        self._choices = choices
        self._default = default
        self._type = type

        if self._default is not None:
            self.validate(self._default)

    def validate(self, value: T) -> T:
        """Validate and possibly modify the field value before assignment."""
        if self._type and not isinstance(value, self._type):
            msg = f"Expected {self._name} to be a {self._type}, not {value!r}"
            raise TypeError(msg)
        if self._choices and value not in self._choices:
            msg = f"Expected {self._name} to be a one of {self._choices}, not {value!r}"
            raise TypeError(msg)
        return value

    @overload
    def __get__(self: TField, obj: None, objtype: None) -> TField: ...

    @overload
    def __get__(self, obj: object, objtype: type[object]) -> T: ...

    def __get__(
        self: TField,
        obj: object | None,
        objtype: type[object] | None,
    ) -> T | TField:
        if not obj:
            return self
        return cast(T, getattr(obj, f"_{self._name}", self._default))

    def __set__(self, obj: object, value: T) -> None:
        if value is not None:
            value = self.validate(value)

        if value is None or value == self._default:
            self.__delete__(obj)
        else:
            setattr(obj, f"_{self._name}", value)

    def __delete__(self, obj: object) -> None:
        if hasattr(obj, f"_{self._name}"):
            delattr(obj, f"_{self._name}")


class String(Field[str]):
    """Specialized :class:`Field` which is wired up for bytes and unicode.

    :param default: default value for field
    """

    def __init__(self, default: str | None = None) -> None:
        # TODO: normalize to unicode?
        # TODO: only allow unicode?
        # TODO: disallow empty strings?
        super().__init__(type=str, default=default)


class Date(String):
    """:class:`Field` for storing ISO 8601 dates as a string.

    Supported formats are ``YYYY-MM-DD``, ``YYYY-MM`` and ``YYYY``, currently
    not validated.

    :param default: default value for field
    """

    # TODO: make this check for YYYY-MM-DD, YYYY-MM, YYYY using strptime.


class Identifier(String):
    """:class:`Field` for storing values such as GUIDs or other identifiers.

    Values will be interned.

    :param default: default value for field
    """

    def validate(self, value: str) -> str:
        value = super().validate(value)
        if isinstance(value, bytes):
            value = value.decode()
        return sys.intern(value)


class URI(Field[Uri]):
    """:class:`Field` for storing URIs.

    Values will be interned, currently not validated.

    :param default: default value for field
    """

    def validate(self, value: Uri) -> Uri:
        value = super().validate(value)
        if isinstance(value, bytes):
            value = value.decode()
        # TODO: validate URIs?
        return Uri(sys.intern(value))


class Integer(Field[int]):
    """:class:`Field` for storing integer numbers.

    :param default: default value for field
    :param min: field value must be larger or equal to this value when set
    :param max: field value must be smaller or equal to this value when set
    """

    def __init__(self, default=None, min=None, max=None) -> None:
        self._min = min
        self._max = max
        super().__init__(type=int, default=default)

    def validate(self, value: int) -> int:
        value = super().validate(value)
        if self._min is not None and value < self._min:
            msg = f"Expected {self._name} to be at least {self._min}, not {value:d}"
            raise ValueError(msg)
        if self._max is not None and value > self._max:
            msg = f"Expected {self._name} to be at most {self._max}, not {value:d}"
            raise ValueError(msg)
        return value


class Boolean(Field[bool]):
    """:class:`Field` for storing boolean values.

    :param default: default value for field
    """

    def __init__(self, default=None) -> None:
        super().__init__(type=bool, default=default)


class Collection(Field[tuple[V, ...] | frozenset[V]]):
    """:class:`Field` for storing collections of a given type.

    :param type: all items stored in the collection must be of this type
    :param container: the type to store the items in
    """

    def __init__(
        self,
        type: type,
        container: Callable[[], tuple | frozenset] = tuple,
    ) -> None:
        super().__init__(type=type, default=container())

    def validate(self, value: Iterable[Any]) -> tuple[V, ...] | frozenset[V]:
        assert self._default is not None
        assert self._type is not None
        if isinstance(value, str):
            msg = (
                f"Expected {self._name} to be a collection of "
                f"{self._type.__name__}, not {value!r}"
            )
            raise TypeError(msg)
        for v in value:
            if not isinstance(v, self._type):
                msg = (
                    f"Expected {self._name} to be a collection of "
                    f"{self._type.__name__}, not {value!r}"
                )
                raise TypeError(msg)
        return self._default.__class__(value)
