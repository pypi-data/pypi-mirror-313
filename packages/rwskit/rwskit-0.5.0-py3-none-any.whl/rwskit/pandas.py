"""Utilities for working with pandas."""

# Python Modules
import logging

# 3rd Party Modules
import numpy as np
import pandas as pd
from icontract import require

# Project Modules
from rwskit.collections_ import get_first_non_null_value
from rwskit.numpy import get_dtype


log = logging.getLogger(__name__)


def _expand_list(df: pd.DataFrame, column_name: str, string_fill: str) -> pd.DataFrame:
    column = df.pop(column_name)
    min_length = column.map(len).min()
    max_length = column.map(len).max()
    new_names = [f"{column_name}__{i}" for i in range(max_length)]
    new_shape = (len(df.index), max_length)
    dtype = get_dtype(get_first_non_null_value(column))
    is_str = np.issubdtype(dtype, np.str_)
    fill_value = string_fill if is_str else np.nan

    if is_str:
        # max_length is the length of the list, not the max length string
        # in the list.
        max_string_length = max((len(s) if s else 0 for sublist in column for s in sublist))
        dtype = f"U{max(max_string_length, len(string_fill))}"

    if min_length == max_length:
        # We just need to replace 'None`, with the string fill value.
        values = [
            [string_fill if v is None and is_str else v for v in inner_list]
            for inner_list in column.to_list()
        ]
        new_data = np.array(values, dtype=dtype)
    else:
        # Otherwise we need to pad and fill an empty array of the correct
        # dtype.
        # Convert to float so we can fill all missing values with NaN
        if np.issubdtype(dtype, np.number) or dtype == np.bool_:
            dtype = np.float64

        new_data = np.full(new_shape, fill_value=fill_value, dtype=dtype)

        for i, values in enumerate(column):
            # If `None` appears inside a string list, replace it with the
            # fill value. Note, if we don't replace it here, then it
            # will be inserted into the array as the string 'None'.
            values = [fill_value if v is None and is_str else v for v in values]
            new_data[i, :len(values)] = values

    df[new_names] = pd.DataFrame(new_data, index=column.index, columns=new_names)

    return df


@require(
    lambda string_fill: string_fill is not None,
    "The 'string_fill' value cannot be None."
)
def flatten_data_frame(
        df: pd.DataFrame,
        string_fill: str = "[UNK]",
        in_place: bool = False
) -> pd.DataFrame:
    """Converts columns containing lists into (new) individual columns in the ``DataFrame``.

    If one or more columns in a DataFrame consist of lists, this method will
    remove the original column and replace it with ``N`` columns, where
    ``N`` is the maximum length of the lists in the original column.

    If the lists are of unequal length, the additional columns will be appended
    to the right. Lists of strings will be padded using the given
    ``string_fill`` value. All others will be padded with ``np.nan``. Note,
    most numpy types will convert ``np.nan`` into an appropriate missing
    value for that type. For example, when used to fill ``np.datetime64``
    objects, the resulting object will be ``np.datetime64('NaT')``.

    If the lists are numeric (including boolean) and they do not have equal
    lengths, the new columns will have ``dtype=np.float64`` regardless of
    the original dtype.

    .. note::
        Nested lists within a column are not supported and will not be
        flattened.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame to flatten.
    string_fill : any, defualt = '[UNK]'
        Use this value to pad string lists. All other data types will use
        ``np.nan``
    in_place : bool, default = False
        Whether to modify the DataFrame in place or return a copy.

    Returns
    -------
    df : pandas.DataFrame
        The modified DataFrame

    Examples
    --------

    .. code-block:: python

        >>>input_df = pd.DataFrame({
            "A": [["1"], ["2", "3"]],
            "B": [["4", "5"], ["6", "7", "8"]],
            "C": [[1], [2, 3]],
            "D": [True, False]
        })
        >>>print(input_df)
                A          B       C      D
        0     [1]     [4, 5]     [1]   True
        1  [2, 3]  [6, 7, 8]  [2, 3]  False

        >>>flatten_data_frame(input_df)
          A__0   A__1 B__0 B__1   B__2  C__0  C__1      D
        0    1  [UNK]    4    5  [UNK]   1.0   NaN   True
        1    2      3    6    7      8   2.0   3.0  False

    """

    if not in_place:
        df = df.copy()

    for c in df.columns:
        if isinstance(df[c].iat[0], list):
            df = _expand_list(df, c, string_fill)

    return df
