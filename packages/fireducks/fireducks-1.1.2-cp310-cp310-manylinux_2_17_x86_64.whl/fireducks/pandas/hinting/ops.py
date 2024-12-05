# Copyright (c) 2023 NEC Corporation. All Rights Reserved.

import logging

from typing import List, Optional

import numpy as np
import pandas
from fireducks.fireducks_ext import Metadata

from fireducks.pandas.hinting.hint import ColumnAxisHint, ColumnHint, TableHint

logger = logging.getLogger(__name__)


def _ensure_list(obj):
    return obj if isinstance(obj, list) else [obj]


def _is_supported_index(index):
    """
    This module does not support some index type.

    Ex:
        - `infer_project` dose not support:
            * `df["1/1/2000"]` on PeriodIndex.
            * `df[0.5] on IntervalIndex.from_breaks(np.arange(5))`
    """
    supported_dtypes = (
        np.bool_,
        np.int8,
        np.int16,
        np.int32,
        np.int64,
        np.uint8,
        np.uint16,
        np.uint32,
        np.uint64,
        np.float32,
        np.float64,
        np.object_,  # expect string, not python object
        # pandas.core.arrays.string_.StringDtype # Should we add this?
    )
    return index.dtype in supported_dtypes


def create_hint_from_pandas_frame(df: pandas.DataFrame) -> Optional[TableHint]:
    """Create a hint from pandas.DataFrame"""

    if not _is_supported_index(df.columns):
        return None

    isMultiLevel = isinstance(df.columns, pandas.MultiIndex)
    names = [list(name) if isMultiLevel else name for name in df.columns]
    columns = [ColumnHint(name) for name in names]
    return TableHint(columns=ColumnAxisHint(columns))


def create_hint_from_metadata(meta: Metadata) -> Optional[TableHint]:
    """Create a hint from fireducks.fireducks_ext.Metadata"""

    names = [name for name in meta.column_names]
    columns = [ColumnHint(name) for name in names]
    return TableHint(columns=ColumnAxisHint(columns))


def find_columns_by_name(
    columns: ColumnAxisHint, name, compare=None
) -> [ColumnHint]:
    def compare_exact(a, b):
        return a == b

    compare = compare or compare_exact
    return [col for col in columns if compare(col.name, name)]


def select_columns(hint: TableHint, keys) -> Optional[List[ColumnHint]]:
    """Select columns by keys as projection such as `df[["a", "b"]]`"""

    if hint.columns is None:
        return None

    # projection from multilevel is very complex. Not supported yet
    if hint.columns.is_multilevel:
        return None

    def check_name(name, key):
        name = name if isinstance(name, list) else [name]
        key = key if isinstance(key, list) else [key]
        if len(key) > len(name):
            return False
        return name[0 : len(key)] == key

    columns = []
    for key in keys:
        columns += find_columns_by_name(hint.columns, key, check_name)

    return columns


def infer_project(hint: TableHint, keys) -> Optional[TableHint]:
    """Infer TableHint for a project op.

    Args:
      keys (key-like): projection keys

    Returns:
      TableHint:
    """
    logger.debug("infer_project: hint=%s keys=%s", hint, keys)
    if hint is None:
        return None

    selected = select_columns(hint, _ensure_list(keys))
    if selected is None:
        return None

    return TableHint(columns=ColumnAxisHint(columns=selected))


def is_column_name(hint: TableHint, name) -> bool:
    """Return True if name is a column name, False if not or unknown.

    This method decides as project op.
    """
    if hint is None:
        return False

    selected = select_columns(hint, [name])
    return selected is not None and len(selected) > 0
