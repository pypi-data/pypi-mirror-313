from __future__ import annotations

# Python Modules
import datetime
import importlib
import logging

from dataclasses import Field, MISSING, fields, is_dataclass
from types import NoneType
from typing import Any, Iterable, Iterator, Mapping, Optional, Type, TypeVar, get_args, \
    get_origin, get_type_hints


# 3rd Party Modules
from dateutil.parser import parse as parse_date
from icontract import ViolationError, require
from pydantic.dataclasses import dataclass

# Project Modules
from rwskit import types_ as types_
from rwskit.types_ import type_from_string


log = logging.getLogger(__name__)

D = TypeVar("D")
"""A type intended to represent a dataclass."""


def is_frozen(cls: Type) -> bool:
    """Checks if a class is a frozen dataclass.

    This will return ``True`` if the input ``cls`` is both a dataclass (either
    ``dataclasses.dataclass`` or ``pydantic.dataclasses.dataclass``) and
    it is frozen.
    """
    if not is_dataclass(cls):
        return False

    return getattr(cls, "__dataclass_params__").frozen


def has_default_value(field: Field) -> bool:
    """
    Checks if a ``field`` has a default value.

    Parameters
    ----------
    field : Field
        The field to check.

    Returns
    -------
    bool
        ``True`` if the field has a default value either directly or via
        a default factory.
    """
    return field.default is not MISSING or field.default_factory is not MISSING


def is_optional(field: Field) -> bool:
    """Checks if a ``field`` is optional.

    Parameters
    ----------
    field : Field
        The field to check.

    Returns
    -------
    bool
        ``True`` if the field is optional.
    """
    return types_.is_optional(field.type)


def is_required(field: Field) -> bool:
    """Checks if a ``field`` is required.

    A field is required if it is not optional and does not have a default value.

    Parameters
    ----------
    field : Field
        The field to check,

    Returns
    -------
    bool
        ``True`` if the field is required.
    """
    return not (is_optional(field) or has_default_value(field))


@require(
    lambda cls: is_dataclass(cls),
    "The class 'cls' must be a dataclass."
)
def resolve_type_hints(
        cls: Type[Any],
        type_map: Optional[dict[str, Type[Any]]] = None,
        max_tries: int = 50
) -> dict[str, Any]:
    """Try to resolve the type hints for a dataclass.

    Sometimes func:`typing.get_type_hints` fails with a ``NameError`` when
    the type hint has not already been imported. This method will try to
    catch those errors and dynamically import the unresolved class.

    Parameters
    ----------
    cls : Type[Any]
        The dataclass to resolve the type hints for.
    type_map : dict[str, Type[Any]], optional
        Additional mappings from string names to type classes, which can be
        used in addition to ``globals()`` for resolving type hint classes.
    max_tries : int
        The maximum number of times the method will try to resolve missing
        type hints.

    Returns
    -------
    dict[str, Any]
        The dictionary containing the resolved type hints.

    Raises
    ------
    icontract.ViolationError
        If the input ``cls`` is not a dataclass.
    """
    # We need to ensure that any type hint used in the dataclass (including
    # ones defined in its parents) are imported and available when
    # 'get_type_hints' is called. To do that we'll get the list of classes
    # in the current classes type hierarchy and dynamically import all the
    # objects in its module. This is a very heavy-handed way to ensure the
    # necessary objects are available, but it's not obvious there is a
    # more fine-grained way to guarantee the necessary objects are available.
    class_hierarchy = cls.mro()
    dynamic_vars = [vars(importlib.import_module(c.__module__)) for c in class_hierarchy]
    dynamic_vars = {k: v for d in dynamic_vars for k, v in d.items()}
    globalns = globals() | (type_map or {}) | dynamic_vars

    for _ in range(max_tries):
        try:
            hints = get_type_hints(cls, globalns=globalns, localns=locals())
        except NameError as e:
            # Try to resolve (and import) unknown classes.
            # The error message will look something like:
            # NameError: name 'ClassName' is not defined.
            # Splitting on `'` should give us 3 tokens with the class name in
            # the middle (with index 1).
            missing_class_name = str(e).split("'")[1]
            try:
                globalns[missing_class_name] = type_from_string(missing_class_name)
            except (ViolationError, ModuleNotFoundError):
                pass  # Not all type hints are classes.
        else:
            return hints

    raise NameError(f"Could not resolve all type hints for {cls}.")


# region Construct Dataclass
@require(
    lambda data, dataclass_type:
        set(data.keys()).issubset({f.name for f in fields(dataclass_type)}),
    "The 'data' keys must be a subset of the dataclass fields."
)
@require(
    lambda data, dataclass_type:
        all(not is_required(f) or data.get(f.name) is not None for f in fields(dataclass_type)),
    "The 'data' must contain non-null entries for all required fields."
)
@require(
    lambda dataclass_type: is_dataclass(dataclass_type),
    "'dataclass_type' must be a dataclass."
)
@require(
    lambda data: isinstance(data, Mapping),
    "'data' must be a mapping (e.g., dict)."
)
def construct_dataclass(
        data: Mapping[str, Any],
        dataclass_type: Type[D],
        type_map: Optional[dict[str, Any]] = None
) -> D:
    """Construct a dataclass from a mapping.

    Try to construct a possibly nested dataclass of ``dataclass_type``
    from a mapping provided by ``data``. If the dataclass cannot be
    constructed from the data a ``TypeError`` will be raised.

    Parameters
    ----------
    data : Mapping[str, Any]
        The dictionary (or other mapping) to try to convert.
    dataclass_type : Type[D]
        The dataclass type we will try to construct.
    type_map : dict[str, Any], optional
        By default this method will use ``globals()`` to try to resolve the
        type hints for the dataclass fields. You can specify any additional
        mappings with ``type_map`` which will be appended to the default.

    Returns
    -------
    D
        The dataclass object we have constructed.

    Raises
    ------
    icontract.ViolationError
        If the ``dataclass_type`` is not a dataclass.
    TypeError
        If the dictionary cannot be converted to the dataclass type.

    """
    type_hints = resolve_type_hints(dataclass_type, type_map)

    # Create the keyword arguments we'll use to construct the dataclass.
    # We will only create arguments that have an entry in the mapping
    # and let the dataclass try to create defaults where necessary
    # when entries are missing in the mapping. Note, this might fail,
    # but that just means the data is not compatible with this dataclass.
    kwargs = {
        f.name: _handle_field(f, type_hints[f.name], data[f.name], type_map)
        for f in fields(dataclass_type)
        if f.name in data
    }

    try:
        return dataclass_type(**kwargs)
    except TypeError as e:
        raise ValueError(f"Error creating an instance of {dataclass_type.__name__}: {e}")


def _handle_field(field, field_type: Any, value: Any, type_map: dict[str, Any]) -> Any:
    """Try to construct a dataclass field from a given value.

    Parameters
    ----------
    field : dataclasses.Field
        The dataclass field we are trying to construct.
    field_type : Any
        The type of the field. We use this value instead of ``Field.type``
        because any forward references should have already been resolved.
    value : Any
        The value to construct the field from.

    Returns
    -------
    Any
        The appropriate value for the field.

    Raises
    ------
    ValueError
        If we can't construct the field from the given value.

    """
    # Handle Union types
    if types_.is_union(field_type):
        return _handle_union_type(field, field_type, value, type_map)

    # Anything below here should be either a raw type, generic, or nested
    # dataclass.
    field_origin = get_origin(field_type)

    # Handle basic types or dataclasses.
    # This needs to be first because 'field_origin' can't be None
    # when using 'issubclass'.
    if field_origin is None:
        return _handle_basic_types(field, field_type, value, type_map)

    # Handle mappings (e.g., dicts)
    if issubclass(field_origin, Mapping):
        return _handle_mapping_types(field, field_type, field_origin, value, type_map)

    # Handle tuples separately because the typing is idiosyncratic.
    if issubclass(field_origin, tuple):
        return _handle_tuple_types(field, field_type, value, type_map)

    # Handle other iterables
    if issubclass(field_origin, Iterable) and not isinstance(value, str):
        return _handle_iterable_types(field, field_type, field_origin, value, type_map)

    raise ValueError(f"Field '{field}' has an unsupported container type: {field_origin}")


def _handle_union_type(field: Field, field_type: Any, value: Any, type_map: dict[str, Any]) -> Any:
    field_args = get_args(field_type)

    if NoneType in field_args and value is None:
        return None

    for arg in field_args:
        try:
            return _handle_field(field, arg, value, type_map)
        except (ValueError, TypeError):
            continue

    raise ValueError(
        f"Field '{field.name}' with value '{value}' cannot be converted to any type in "
        f"{field_args}."
    )


def _handle_basic_types(field: Field, field_type: Any, value: Any, type_map: dict[str, Any]) -> Any:
    # If the value is already an instance of the field type, we can just
    # return it.
    if isinstance(value, field_type):
        return value

    if isinstance(value, str) and issubclass(field_type, (datetime.date, datetime.datetime)):
        return parse_date(value)  # noqa

    if is_dataclass(field_type):
        return construct_dataclass(value, field_type, type_map)

    raise TypeError(
        f"Field '{field.name}' expected type '{field_type}', but got '{type(value)}"
    )


def _handle_mapping_types(
        field: Field,
        field_type: Any,
        field_origin,
        value: Any,
        type_map: dict[str, Any]
) -> Any:
    if not isinstance(value, Mapping):
        raise TypeError(
            f"Field '{field.name}' expected type '{field_type}', but got '{type(value)}"
        )

    field_args = get_args(field_type)
    key_type = field_args[0] if field_args else Any
    value_type = field_args[1] if field_args and len(field_args) > 1 else Any

    return field_origin(
        (_handle_field(field, key_type, k, type_map), _handle_field(field, value_type, v, type_map))
        for k, v in value.items()
    )


def _handle_tuple_types(
        field: Field,
        field_type: Any,
        value: Any,
        type_map: dict[str, Any]
) -> tuple:
    if not isinstance(value, Iterable):
        raise TypeError(
            f"Field '{field.name}' expected type '{field_type}', but got {type(value)}"
        )

    values = list(value)
    n_values = len(values)
    field_args = get_args(field_type)

    ellipsis_index = field_args.index(Ellipsis) if Ellipsis in field_args else -1
    if not field_args or ellipsis_index == 0:
        # Note tuple[...] does not seem to be valid (pydantic will complain)
        # Can be any length and type
        inner_types = [Any for _ in range(n_values)]
    elif ellipsis_index > 0:
        # Can be any length
        inner_types = [
            field_args[i] if i < ellipsis_index else field_args[ellipsis_index - 1]
            for i in range(n_values)
        ]
    else:
        # Must be a specific length and specific types
        if n_values != len(field_args):
            raise ValueError(
                f"Field '{field.name}' expected length {n_values} but got {len(field_args)}"
            )
        inner_types = field_args

    return tuple(_handle_field(field, t, e, type_map) for t, e in zip(inner_types, values))


def _handle_iterable_types(
        field: Field,
        field_type: Any,
        field_origin: Any,
        value: Any,
        type_map: dict[str, Any]
) -> Iterable:
    if not isinstance(value, Iterable):
        raise TypeError(
            f"Field '{field.name}' expected type '{field_type}', but got {type(value)}"
        )

    field_args = get_args(field_type)
    inner_type = field_args[0] if field_args else Any

    return field_origin(_handle_field(field, inner_type, item, type_map) for item in value)
# endregion Construct Dataclass


class DataclassRegistry:
    """A class for registering and managing a collection of dataclasses."""

    def __init__(self):
        """Initialize the registry."""
        self.registered_classes: set[Type[D]] = set()

    def __iter__(self) -> Iterator[Type[D]]:
        return iter(self.registered_classes)

    def __len__(self) -> int:
        return len(self.registered_classes)

    def register(self, *classes: Type[D]):
        """
        Add a class to the registry.

        Parameters
        ----------
        classes : Type[D]
            The class or classes to add.
        """
        for cls in classes:
            self.registered_classes.add(cls)

    def construct_registered_dataclass(
            self,
            data: Mapping[str, Any],
            type_map: Optional[dict[str, Any]] = None
    ) -> D:
        """Try to construct one of the registered dataclasses from the given data.

        Parameters
        ----------
        data : Mapping[str, Any]
            The data to use for constructing a dataclass.
        type_map : dict[str, Any], optional
            Additional types that should be made available (imported) when
            resolving type hints for the registered dataclasses.

        Returns
        -------
        D
            An instance of a registered dataclass that is compatible with the
            given data.

        Raises
        ------
        icontract.ViolationError
            If ``data`` does not contain values for all required attributes
            of the dataclass (or any nested dataclass).
        icontract.ViolationError
            If ``data`` is not a :class:`~typing.Mapping`.
        ValueError
            If a registered dataclass cannot be constructed from the data.

        """
        successful_constructions = []

        for dataclass_type in self.registered_classes:
            try:
                instance = construct_dataclass(data, dataclass_type, type_map)
            except (ValueError, TypeError, ViolationError):
                continue
            else:
                successful_constructions.append(instance)

        if len(successful_constructions) == 0:
            raise ValueError(f"The 'data' cannot be used to construct any registered dataclasses.")

        if len(successful_constructions) > 1:
            dataclass_names = [type(instance).__name__ for instance in successful_constructions]

            raise ValueError(
                f"The 'data' is ambiguous and can be used to construct multiple dataclasses: "
                f"{dataclass_names}."
            )

        return successful_constructions[0]


class FrozenDataclassMeta(type):
    """Turn the class into a ``pydantic`` dataclass if it is not one already.

    .. note::
        Although this will turn any class that uses it into a ``pydantic``
        dataclass, it will cause most linters (including PyCharm)
        to issue unresolved attribute warnings for all attributes.
    """

    def __new__(
            cls: Type[FrozenDataclassMeta],
            name: str,
            bases: tuple[Type, ...],
            namespace: dict[str, Any],
            **kwargs: Any
    ) -> Type[dataclass]:
        new_cls = super().__new__(cls, name, bases, namespace, **kwargs)
        new_cls = dataclass(new_cls, frozen=True)  # noqa

        return new_cls


class EnforceFrozenDataclassMeta(type):
    """Requires that the class must be a standard or pydantic dataclass.

    Any class using this metaclass is not a frozen dataclass will raise a
    ``TypeError`` exception.

    .. note::
        This is not particularly useful because the metaclass will be
        applied before any decorators, so even if a class is decorated
        with @dataclass it will still raise a TypeError here, because
        it has not been applied yet.
    """

    def __new__(
            cls: Type[EnforceFrozenDataclassMeta],
            name: str,
            bases: tuple[Type, ...],
            namespace: dict[str, Any],
            **kwargs: Any
    ) -> EnforceFrozenDataclassMeta:
        new_cls = super().__new__(cls, name, bases, namespace, **kwargs)

        if not is_frozen(new_cls):
            raise TypeError(
                f"{name} must be decorated with '@dataclasses.dataclass(frozen=True)' or "
                f"'@pydantic.dataclasses.dataclass(frozen=True)'"
            )

        return new_cls
