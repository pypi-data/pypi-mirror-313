# Python Modules
import importlib
from types import UnionType

from typing import Any, Type, Union, get_args, get_origin

# 3rd Party Modules
from icontract import require

# Project Modules


def is_union(type_: Any) -> bool:
    """Check if the given ``type_`` is a union of types.

    A type can be a union if it uses the :class:`~typing.Union` type hint or
    the ``|`` operator.

    Parameters
    ----------
    type_ : Any
        The type to check.

    Returns
    -------
    bool
        ``True`` if the given type is a union, otherwise ``False``.

    """
    return get_origin(type_) is Union or isinstance(type_, UnionType)


def is_optional(type_: Any) -> bool:
    """Check if a type is optional.

    An optional type is either defined by class:`typing.Optional` or by
    a :class:`~typing.Union` containing ``None``.

    Parameters
    ----------
    type_ : Any
        The type to check.

    Returns
    -------
    bool
        ``True`` if ``type_`` is optional.

    """
    return is_union(type_) and type(None) in get_args(type_)


@require(
    lambda cls: isinstance(cls, type),
    "The input must be a class type."
)
def get_qualified_name(cls: type) -> str:
    """Get the fully qualified name of this class.

    The fully qualified name is the full path of package names, the module
    name, and class name.

    Parameters
    ----------
    cls : Type[Any]

    Returns
    -------
    str
        The fully qualified name of this class.

    Raises
    ------
    icontract.ViolationError
        If the input ``cls`` is not a type.
    """
    module, name = cls.__module__, cls.__qualname__

    if module is not None and module != "__builtin__":
        name = module + "." + name

    return name


@require(
    lambda qualified_class_name: "." in qualified_class_name,
    "The 'qualified_class_name' must at least refer to a module (the "
    "provided name does not contain a '.')."
)
@require(
    lambda qualified_class_name: bool(qualified_class_name),
    "The 'qualified_class_name' cannot be empty."
)
def type_from_string(qualified_class_name: str) -> type:
    """Import and return the type object from a fully qualified class name.

    Parameters
    ----------
    qualified_class_name : str
        The fully qualified class name.

    Returns
    -------
    type
        The type object corresponding to the fully qualified class name.

    Raises
    ------
    icontract.ViolationError
        If the input ``qualified_class_name`` is ``None`` or empty.
    ModuleNotFoundError
        If the input ``qualified_class_name`` cannot be loaded.
    """
    tokens = qualified_class_name.split('.')
    module_name, class_name = '.'.join(tokens[:-1]), tokens[-1]

    module = importlib.import_module(module_name)

    return getattr(module, class_name)
