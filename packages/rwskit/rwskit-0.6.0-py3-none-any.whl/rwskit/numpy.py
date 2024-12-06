"""
Numpy utilities.
"""
from __future__ import annotations

# Python Modules
import datetime
import logging

from typing import Any, Callable, Literal, Optional

# 3rd Party Modules
import numpy as np
import pandas as pd

# Project Modules
from rwskit.collections_ import get_first_non_null_value, is_iterable

log = logging.getLogger(__name__)


CompleteCheckType = Literal["finite", "nan"]
"""
The valid values for the ``check_type`` parameter of :meth:`is_complete`.
"""

_python_to_dtype_map = {
    int: np.int_,
    bool: np.bool_,
    float: np.float64,
    complex: np.complex128,
    bytes: np.bytes_,
    str: np.str_,
    datetime.datetime: np.datetime64,
    datetime.date: np.datetime64,
    pd.Timestamp: np.datetime64,
}


def get_dtype(obj: Optional[Any]) -> Optional[np.dtype]:
    """
    Return a dtype that can be used to represent an arbitrary object.

    For objects that are already numpy arrays or scalars, the dtype from that
    object is returned. For other python objects, a set of heuristics are used.
    If the object is iterable, the method will try to determine the type of
    object

    If the dtype can't be determined, either because the input object was
    ``None``, or it is a collection that does not contain any non-null
    values, then the method will return ``None``.

    Parameters
    ----------
    obj : Any
        An object.

    Returns
    -------
    numpy.dtype, optional
        A dtype that can be used to represent an arbitrary object, or ``None``
        if the input object is ``None``.

    """
    if obj is None:
        return None

    if isinstance(obj, str) or not is_iterable(obj):
        # Try to use numpy to automatically detect the dtype
        dtype = np.array(obj).dtype

        # We've found a specific dtype so return it.
        if dtype != np.object_:
            return dtype

        return _python_to_dtype_map.get(type(obj), np.object_)
    else:
        # Get the first non-null value in the iterable
        a_value = get_first_non_null_value(obj)

        # Recurse on the fetched object.
        return get_dtype(a_value)


def is_structured(array: np.ndarray) -> bool:
    """
    Checks if a numpy array is a structured array or not.

    Parameters
    ----------
    array : np.ndarray
        The array to check.

    Returns
    -------
    bool
        ``True`` if the array is a structured array, ``False`` otherwise.
    """
    return array.dtype.names is not None


# region is_complete
def is_complete(array: np.ndarray, check_type: CompleteCheckType = "finite") -> bool:
    """
    An array is complete if all its numeric values are finite and all other
    values are not ``None``.

    .. note::
        For arrays with ``dtype=np.object_``, the method only checks to make sure
        no value in the array is ``None``.

    Parameters
    ----------
    check_type : {"finite", "nan"}
        Determines how completeness is defined.

        nan
            Requires that no values are ``np.NaN`` or ``None``.
        finite
            In addition to the criteria for ``nan`` all values must also be
            finite (i.e., not ``np.inf`` or ``-np.inf``).

    array : np.ndarray
        The array to check.

    Returns
    -------
    bool
        ``True`` if the array is complete, ``False`` otherwise.
    """
    complete_fn = _get_complete_function(check_type, array)

    if is_structured(array):
        return _is_structured_complete(array, complete_fn)

    return _is_unstructured_complete(array, complete_fn)


def _get_complete_function(
        check_type: CompleteCheckType,
        array: np.ndarray
) -> Callable[[np.ndarray], bool]:
    # np.dot is always fastest for 1D arrays.
    if check_type == "finite" and array.ndim <= 1:
        return lambda a: np.isfinite(np.dot(a, a))

    # When checking for finite values, we have to use an accumulating
    # function, otherwise the possibly infinite values don't propagate.
    if check_type == "finite":
        return lambda a: np.isfinite(np.sum(a))

    if array.ndim <= 1:
        return lambda a: not np.isnan(np.dot(a, a))

    # When checking for NaNs in greater than 1D creating a boolean
    # mask is fastest for small N, but eventually np.sum is faster.
    if array.size < 1500000:
        return lambda a: not np.any(np.isnan(a))

    return lambda a: np.isnan(np.sum(a))


def _is_unstructured_complete(
        array: np.ndarray,
        complete_fn: Callable[[np.ndarray], bool],
) -> bool:
    # Check if floating point values are finite.
    if np.issubdtype(array.dtype, np.floating):
        return complete_fn(array)

    # Check if object types are non-null
    if np.issubdtype(array.dtype, np.object_):
        return None not in array

    # All other values must have a value
    return True


def _is_structured_complete(
        array: np.ndarray,
        complete_fn: Callable[[np.ndarray], bool],
) -> bool:
    return all(
        _is_unstructured_complete(array[c], complete_fn)
        for c in array.dtype.names
    )
# endregion is_complete


# region finite_cases
def finite_cases(array: np.ndarray) -> np.ndarray:
    """
    Return only the rows whose values are finite and not ``None``.

    Parameters
    ----------
    array : np.ndarray
        The input array with possibly invalid values.

    Returns
    -------
    np.ndarray
        An array with only non-null finite values.
    """
    if is_structured(array):
        return _structured_finite_cases(array)

    return _unstructured_finite_cases(array)


def _unstructured_finite_cases(array: np.ndarray) -> np.ndarray:
    return array[np.isfinite(array).all(axis=1)]


def _structured_finite_cases(array: np.ndarray) -> np.ndarray:
    masks = []

    for field in array.dtype.names:
        column = array[field]

        if np.issubdtype(column.dtype, np.floating):
            masks.append(np.isfinite(column))
        elif np.issubdtype(column.dtype, np.object_):
            try:
                masks.append(np.isfinite(column.astype(float)))
            except ValueError:
                masks.append(column != None)

    mask = np.logical_and(*masks)

    return array[mask]
# endregion finite_cases


# region group_by
def group_by(array: np.ndarray, column: str | int) -> list[np.ndarray]:
    """
    Group an ``array`` by the values in the given ``column``. If ``array`` is
    as structured array, then ``column`` should be the name of one of the
    fields, otherwise it should be the index of the column you want to use.

    Parameters
    ----------
    array : np.ndarray
        The array to group.
    column : str | int
        If ``array`` is structured then ``column`` should be the name of the
        column to group by. Otherwise, it should be the index of the column.

    Returns
    -------
    list
        Returns the group as a list of arrays.
    """
    # Based on vincent's method: https://stackoverflow.com/a/43094244
    if is_structured(array):
        # The indices such that the rows would be sorted by the values in
        # the given `column`.
        indices = array[column].argsort()

        # The input array sorted by those indices.
        sorted_array = array[indices]

        # When `return_index=True` np.unique will return two arrays. The
        # first will be the actual unique values. The second will be
        # the indices in the original array that point to the first instance
        # of each unique value. To split the array into groups we want all
        # but the first value of the second array.
        group_indices = np.unique(sorted_array[column], return_index=True)[1][1:]
    else:
        # The indices such that the rows would be sorted by the values in
        # the given `column`.
        indices = array[:, column].argsort()

        # The input array sorted by those indices.
        sorted_array = array[indices]

        # When `return_index=True` np.unique will return two arrays. The
        # first will be the actual unique values. The second will be
        # the indices in the original array that point to the first instance
        # of each unique value. To split the array into groups we want all
        # but the first value of the second array.
        group_indices = np.unique(sorted_array[:, column], return_index=True)[1][1:]

    # Get the groups
    return np.split(sorted_array, group_indices)
# endregion group_by
