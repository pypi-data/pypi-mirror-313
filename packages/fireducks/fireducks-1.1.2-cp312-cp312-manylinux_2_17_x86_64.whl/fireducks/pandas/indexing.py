# Copyright (c) 2023 NEC Corporation. All Rights Reserved.

import logging
import numpy as np

import fireducks.core
import fireducks.pandas.utils as utils
from fireducks import ir, irutils

logger = logging.getLogger(__name__)


def getitem_fallbacker(target, key, reason):
    return utils.fallback_call(
        target._unwrap, "__getitem__", key, __fireducks_reason=reason
    )


class _Indexer:
    def __init__(self, obj, name):
        self.obj = obj
        self.name = name

    def _unwrap(self, reason=None):
        return getattr(self.obj._unwrap(reason=reason), self.name)

    def __getitem__(self, key):
        reason = "fallback _Indexer(" + self.name + ").__getitem__"
        return getitem_fallbacker(self, key, reason)

    def __setitem__(self, key, value):
        reason = "fallback _Indexer(" + self.name + ").__setitem__"
        self.obj._fallback_mutating_method(
            self.name + ".__setitem__",
            args=[key, value],
            reason=reason,
        )


def is_column_locator(obj):
    if isinstance(obj, str):
        return True
    if irutils._is_str_list(obj):
        return True
    return False


def is_full_slice(slobj):
    return (
        isinstance(slobj, slice)
        and slobj.start is None
        and slobj.stop is None
        and slobj.step is None
    )


class _LocIndexer(_Indexer):
    def __init__(self, obj):
        super().__init__(obj, "loc")

    def __getitem__(self, key):
        from fireducks.pandas.series import Series

        t_cls = self.obj.__class__

        if isinstance(key, Series):
            dtype = utils._deduce_dtype(key)
            if dtype is not None and dtype == bool:
                return t_cls._create(ir.filter(self.obj._value, key._value))

        if isinstance(key, tuple) and len(key) == 2:
            r, c = key
            if is_full_slice(r):
                if is_full_slice(c):  # e.g., loc[:, :]
                    return self.obj
                elif is_column_locator(c):  # e.g., loc[:, ['a', 'b']]
                    return self.obj[c]
                elif isinstance(c, slice):  # e.g., loc[:, ['a':'b']]
                    st_loc = self.obj.columns.get_loc(c.start)
                    end_loc = self.obj.columns.get_loc(c.stop)
                    if isinstance(st_loc, int) and isinstance(end_loc, int):
                        return self.obj._take(
                            slice(st_loc, end_loc + 1, c.step), axis=1
                        )

            if isinstance(r, Series):
                projected = None
                if is_full_slice(c):
                    # TODO: support column slicing
                    projected = self.obj
                elif is_column_locator(c):
                    projected = self.obj[c]
                elif isinstance(c, slice):
                    st_loc = self.obj.columns.get_loc(c.start)
                    end_loc = self.obj.columns.get_loc(c.stop)
                    if isinstance(st_loc, int) and isinstance(end_loc, int):
                        projected = self.obj._take(
                            slice(st_loc, end_loc + 1, c.step), axis=1
                        )

                if projected is not None:
                    dtype = utils._deduce_dtype(r)
                    if dtype is not None and dtype == bool:
                        return projected.__class__._create(
                            ir.filter(projected._value, r._value)
                        )
                    else:  # TODO: support index selection
                        return _LocIndexer(projected)[r]

            # get single element
            if isinstance(r, int) and isinstance(c, str):
                if (
                    fireducks.core.get_fireducks_options().fast_fallback
                    and self.obj._fireducks_meta.is_cached()
                ):
                    cache = self.obj._fireducks_meta.get_cache()
                    return cache.loc[key]

        reason = "fallback _LocIndexer(" + self.name + ").__getitem__"
        return getitem_fallbacker(self, key, reason)

    def __setitem__(self, key, val):
        from fireducks.pandas import Series

        checked = False
        if isinstance(self.obj, Series):
            if (
                isinstance(key, Series) or utils._is_index_like(key)
            ) and irutils.irable_scalar(val):
                checked = True
                from_non_indexed_arraylike = not isinstance(key, Series)
                index_or_mask = (
                    Series(key) if from_non_indexed_arraylike else key
                )
                value = irutils.make_scalar(val)
                cname = irutils.make_column_name(None)
                is_series = True
        else:  # DataFrame
            if isinstance(key, tuple) and len(key) == 2:
                r, c = key
                if (
                    (isinstance(r, Series) or utils._is_index_like(r))
                    and isinstance(c, str)
                    and irutils.irable_scalar(val)  # TODO: support other cases
                ):
                    checked = True
                    from_non_indexed_arraylike = not isinstance(r, Series)
                    index_or_mask = (
                        Series(r) if from_non_indexed_arraylike else r
                    )
                    value = irutils.make_scalar(val)
                    cname = irutils.make_column_name(c)
                    is_series = False

        if checked:
            res_value = ir.loc_setter_with_scalar(
                self.obj._value,
                index_or_mask._value,
                value,
                cname,
                from_non_indexed_arraylike,
                is_series,
            )
            return self.obj._rebind(res_value, invalidate_cache=True)

        reason = "fallback _LocIndexer(" + self.name + ").__setitem__"
        self.obj._fallback_mutating_method(
            self.name + ".__setitem__",
            args=[key, val],
            reason=reason,
        )


class _IlocIndexer(_Indexer):
    def __init__(self, obj):
        super().__init__(obj, "iloc")

    def __getitem__(self, key):
        from fireducks.pandas import Series, Index
        from fireducks.pandas.generic import _Scalar

        reason = "fallback _ILocIndexer(" + self.name + ").__getitem__"

        # slice rows of input frame/series: iloc[range(2)]
        if isinstance(key, range):
            key = slice(key.start, key.stop, key.step)

        # slice rows of input frame/series: iloc[:2]
        if isinstance(key, slice):
            return self.obj._slice(key)

        # filter rows of input frame/series based on given indices...
        if isinstance(key, (list, Series, Index, np.ndarray)):  # iloc[[0,3]]
            return self.obj._take(key, axis=0)

        def _take_col(col_idx):
            # take doesn't support int
            idx = irutils.make_vector_or_scalar_of_scalar(col_idx)
            return Series._create(
                ir.take(
                    self.obj._value,
                    idx,
                    axis=1,
                    check_boundary=True,
                    check_negative=True,
                    ignore_index=False,
                )
            )

        if isinstance(self.obj, Series):
            if isinstance(key, int):
                # get single element
                if (
                    fireducks.core.get_fireducks_options().fast_fallback
                    and self.obj._fireducks_meta.is_cached()
                ):  # read from cache
                    cache = self.obj._fireducks_meta.get_cache()
                    return cache.iloc[key]
                else:
                    value = ir.iloc_scalar(self.obj._value, key)
                    return _Scalar(value)._unwrap()

            return getitem_fallbacker(self, key, reason)

        # if not Series, self.obj must be a DataFrame
        if isinstance(key, int):  # e.g., df.iloc[0]
            # slice specified row of the dataframe, and fallback
            start = key if key >= 0 else key + len(self.obj)
            if start < 0:
                raise IndexError("single positional indexer is out-of-bounds")
            target = self.obj._slice(slice(start, start + 1))
            reason += f" on {key}th row-slice"
            return getitem_fallbacker(_IlocIndexer(target), 0, reason)

        if isinstance(key, tuple) and len(key) == 2:
            r, c = key
            # get single element
            if isinstance(r, int) and isinstance(c, int):
                if (
                    fireducks.core.get_fireducks_options().fast_fallback
                    and self.obj._fireducks_meta.is_cached()
                ):  # read from cache
                    cache = self.obj._fireducks_meta.get_cache()
                    return cache.iloc[key]
                else:
                    projected = _take_col(c)
                    value = ir.iloc_scalar(projected._value, r)
                    return _Scalar(value)._unwrap()

            is_supported_colp = isinstance(
                c, (int, range, slice, list, tuple, Series, Index, np.ndarray)
            )

            if is_supported_colp:
                # let's project target columns first
                if is_full_slice(c):  # e.g, iloc[:, :]
                    projected = self.obj
                elif isinstance(c, int):  # e.g, iloc[:, 0]
                    projected = _take_col(c)
                else:  # e.g., iloc[:, :2], iloc[:, [0,3]]
                    projected = self.obj._take(c, axis=1)

                # let's perform slice/filter rows on projected columns
                if is_full_slice(r):
                    # projected-columns, all-rows
                    return projected
                elif isinstance(r, range):
                    # projected-columns, sliced-rows
                    r = slice(r.start, r.stop, r.step)
                    return projected._slice(r)
                elif isinstance(r, slice):
                    # projected-columns, sliced-rows
                    return projected._slice(r)
                elif isinstance(r, (list, Series, Index, np.ndarray)):
                    # projected-columns, filter-rows as per given row-indices
                    return projected._take(r, axis=0)
                elif isinstance(r, int):  # e.g., df.iloc[0, :]
                    # slice specified row from projected-columns, and fallback
                    start = r if r >= 0 else r + len(self.obj)
                    if start < 0:
                        raise IndexError(
                            "single positional indexer is out-of-bounds"
                        )
                    target = projected._slice(slice(start, start + 1))
                    reason += f" on {r}th row-slice of projected columns"
                    return getitem_fallbacker(_IlocIndexer(target), 0, reason)
                else:
                    reason += " on projected columns"
                    return getitem_fallbacker(
                        _IlocIndexer(projected), r, reason
                    )

        return getitem_fallbacker(self, key, reason)
