"""Utilities for working with collections."""

# Python Modules
from types import GeneratorType
from typing import Any, Iterable, Optional


# 3rd Party Modules

# Project Modules


def is_iterable(obj: Any, consider_string_iterable: bool = False) -> bool:
    """
    Tests if the object is iterable.

    Parameters
    ----------
    obj : any
        An object.
    consider_string_iterable : bool, default = False
        Whether to consider strings iterable or not.

    Returns
    -------
    bool
        ``True`` if ``obj`` is iterable.
    """
    if isinstance(obj, str):
        return consider_string_iterable

    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def is_generator(obj: Any) -> bool:
    """
    Checks if the object is a generator.

    Parameters
    ----------
    obj : any
        An object.

    Returns
    -------
    bool
        ``True`` if the object is a generator.

    """
    return isinstance(obj, GeneratorType)


def get_first_non_null_value(collection: Iterable) -> Optional[Any]:
    """Recursively try to get the first non-null value in a collection.

    This method will recursively traverse the collection until it finds
    a non-iterable value that is not ``None``.

    Parameters
    ----------
    collection : Iterable
        The collection to retrieve the value from.

    Returns
    -------
    Any, optional
        The first non-null value in the series, if one exists, otherwise return
        ``None``.

    """
    for value in collection:
        if is_iterable(value) and not isinstance(value, str):
            value = get_first_non_null_value(value)

        if value is not None:
            return value

    return None


