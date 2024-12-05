# Copyright (c) 2023 NEC Corporation. All Rights Reserved.

import logging
import warnings

import numpy as np
import pandas

from pandas.core.common import get_cython_func
from pandas.core.groupby.base import (
    # groupby_other_methods,
    # dataframe_apply_allowlist,
    reduction_kernels,
    transform_kernel_allowlist,
)
from pandas.core.util.numba_ import maybe_use_numba
from pandas.util._validators import validate_bool_kwarg

from fireducks import ir, irutils
from fireducks.irutils import (
    _is_str_list,
    irable_scalar,
    is_column_name,
    make_column_name,
    make_vector_or_scalar_of_str,
    make_tuple_of_column_names,
)
import fireducks.pandas.utils as utils

from fireducks.pandas import (
    DataFrame,
    Series,
)

logger = logging.getLogger(__name__)

if utils._pd_version_under2:
    from pandas.core.groupby.base import series_apply_allowlist
else:
    # pandas doesn't have series_apply_allowlist since v2.2.0.
    series_apply_allowlist = frozenset(
        {
            "is_monotonic_decreasing",
            "diff",
            "is_monotonic_increasing",
            "nsmallest",
            "fillna",
            # "mad", # not in v2.2.0
            "hist",
            "cov",
            "plot",
            "skew",
            "nlargest",
            "quantile",
            # "tshift", # not in v2.2.0
            "idxmax",
            "dtype",
            "corr",
            "take",
            "unique",
            "idxmin",
        }
    )


def _install_agg(cls, method, parent=None):
    """Define a method as a wrapper to call agg."""

    # do not override
    if hasattr(cls, method):
        return

    def wrapper(self, *args, **kwargs):
        # TODO: Why not fallback in agg?
        if args or kwargs:
            return self._fallback_call(
                method,
                *utils._unwrap(args),
                **kwargs,
                __fireducks_reason="args and kwargs are not supported",
            )
        return self.agg(method)

    utils.install_wrapper(cls, method, wrapper, parent)


def validate_groupby_target(target, by):
    ser_as_key = False

    if isinstance(by, Series):
        # will get evaluated, optimization might not work
        new_col = utils.get_unique_column_name(target.columns)
        target = target.copy()
        target[new_col] = by
        # print(target)
        ser_as_key = True
        by = new_col

    return target, by, ser_as_key


def process_agg_output(out, ser_as_key, as_index, by, new_col):
    if ser_as_key:
        if as_index:
            # "by" must be a series
            # out.index.name = by.name
            by_cols = irutils.make_tuple_of_scalars([by.name])
            out._rebind(
                ir.rename_index(out._value, by_cols), invalidate_cache=True
            )
        else:
            warnings.warn(
                "A grouping was used that is not in the columns of the"
                " DataFrame and so was excluded from the result. This"
                " grouping will be included in a future version of pandas."
                " Add the grouping as a column of the DataFrame to"
                " silence this warning.",
                FutureWarning,
            )
            out = out.drop(columns=new_col)
    return out


def is_supported_group_keys(keys):
    if isinstance(keys, Series):
        return True

    if isinstance(keys, list):
        return all([is_column_name(x) for x in keys])

    return is_column_name(keys)


def is_supported_selection(selection):
    def is_selection_supported_type(obj):
        return isinstance(obj, (int, float, str))

    if selection is None:
        return True
    if isinstance(selection, (list, tuple)) and all(
        [is_selection_supported_type(x) for x in selection]
    ):
        return True
    if is_selection_supported_type(selection):
        return True

    return False


def make_groupkey_ops(by):
    if not isinstance(by, list):
        by = [by]
    return make_tuple_of_column_names(by)


def make_selection_ops(selection):
    if isinstance(selection, list):
        cols = [make_column_name(col) for col in selection]
        selection = ir.make_vector_or_scalar_of_column_name_from_vector(cols)
    else:
        selection = make_column_name(selection)
        selection = ir.make_vector_or_scalar_of_column_name_from_scalar(
            selection
        )
    return selection


def find_unsupported_agg_funcs(funcs):
    # arrow does not support these functions.
    funcs_backends_not_supported = {
        "backfill",
        "bfill",
        "corr",
        "cumcount",
        "cummax",
        "cummin",
        "cumprod",
        "cumsum",
        "diff",
        "describe",
        "ffill",
        "fillna",
        "head",
        "idxmax",
        "idxmin",
        "mad",
        "ngroup",
        "nlargest",
        "nsmallest",
        "nth",
        "pad",
        "pct_change",
        "rank",
        "sem",
        "shift",
        "skew",
        "tail",
        "tshift",
    }  # yapf: disable

    def is_unsupported(f):
        return not isinstance(f, str) or f in funcs_backends_not_supported

    flat = np.asarray(
        sum([f if isinstance(f, list) else [f] for f in funcs], [])
    )
    return flat[[is_unsupported(f) for f in flat]]


def _setup_FireDucksGroupBy(cls):
    utils.install_fallbacks(cls, ["__len__"])
    utils.install_fallbacks(cls, ["__dir__"], override=True)
    return cls


@_setup_FireDucksGroupBy
class FireDucksGroupBy:
    def __init__(
        self,
        obj,
        by=None,
        axis=0,
        level=None,
        as_index=True,
        sort=True,
        dropna=True,
        *groupby_args,
        selection=None,
        observed=True,
        **groupby_kwargs,
    ):
        self._obj = obj
        self._by = by
        self._as_index = as_index
        self._sort = sort
        self._dropna = dropna
        self._selection = selection

        # `observed` argument is always used as True, but is checked to return a ValueError.
        validate_bool_kwarg(observed, "observed")

        # Fallback if args has unsupported arguments.
        self._groupby_args = groupby_args
        self._groupby_kwargs = groupby_kwargs
        if axis != 0:
            self._groupby_kwargs["axis"] = axis
        if level is not None:
            self._groupby_kwargs["level"] = level

        self._unwrap_cache = None

    def _has_unsupported_groupby_args(self):
        if not is_supported_group_keys(self._by):
            return "unsupported group key"

        if not is_supported_selection(self._selection):
            return "unsupported selection"

        if self._groupby_args or self._groupby_kwargs:
            return "unsupported args or kwargs is used"

        return None

    def _unwrap(self, reason=None):
        if self._unwrap_cache is not None:
            return self._unwrap_cache

        logger.debug("%s._unwrap", type(self).__name__)
        grpby = self._obj._fallback_call(
            "groupby",
            *self._groupby_args,
            by=utils._unwrap(self._by),
            as_index=self._as_index,
            sort=self._sort,
            dropna=self._dropna,
            observed=True,
            __fireducks_reason=reason,
            **self._groupby_kwargs,
        )
        if isinstance(grpby, utils.PandasWrapper):
            grpby = grpby._pandas_obj
        if self._selection is not None:
            return grpby[self._selection]
        self._unwrap_cache = grpby
        return grpby

    def _fallback_call(self, __fireducks_method, *args, **kwargs):
        return utils.fallback_call(
            self._unwrap, __fireducks_method, *args, **kwargs
        )

    def __getattr__(self, name):
        logger.debug("SeriesGroupBy.__getattr__: name=%s", name)
        reason = f"{type(self).__name__}.__getattr__ for {name} is called"
        return utils.fallback_attr(self._unwrap, name, reason)

    def __iter__(self):
        return self._fallback_call(
            "__iter__",
            __fireducks_reason="DataFrameGroupby.__iter__ is not supported",
        )

    def aggregate(self, func=None, *args, **kwargs):
        """fireducks is implemented assuming numeric_only argument is
        'True'."""

        logger.debug("GroupBy.aggregate: %s", type(self))

        reason = self._has_unsupported_groupby_args()

        if not reason:
            aggArgs = utils.make_agg_args(func, *args, **kwargs)
            if aggArgs is None:
                reason = "unsupported aggregated args"

        if not reason:
            fn = func[0] if _is_str_list(func) and len(func) == 1 else func

            if isinstance(fn, str):
                # these methods returns more than 1 rows per group.
                # hence when any of them is specified as scalar value
                # to aggregate(), calling the respective member method.
                # Otherwise, when specified with any other aggregator
                # it will fallback to pandas.
                if fn in ("shift", "head", "tail"):
                    return getattr(self, fn)()

        if not reason:
            unsup_agg = find_unsupported_agg_funcs(aggArgs.funcs)
            if len(unsup_agg) > 0:
                reason = f"agg function is not supported {unsup_agg}"

            # To raise the same error as pandas, fallback is used when column
            # is not selected
            def is_selected(selection, col):
                if not isinstance(selection, list):
                    return selection == col
                return col in selection

            if self._selection is not None:
                for col in aggArgs.columns:
                    if not is_selected(self._selection, col):
                        reason = "column for aggregation is not selected"

        if reason:
            # fireducks: GT #807
            if func is DataFrame.sum:
                func = pandas.DataFrame.sum
            return self._fallback_call(
                "agg",
                func,
                *utils._unwrap(args),
                __fireducks_reason=reason,
                **kwargs,
            )

        return self._aggregate(func, aggArgs)

    agg = aggregate

    def apply(self, func, *args, **kwargs):
        if callable(func):
            # Creat a wrapper of func to pass pandas's apply when fallback.
            #
            # If func accepts pandas, we can simply pass first argument, i.e.
            # pandas.DataFrame, to func and return result of func.
            #
            # If func accepts fireducks, we have to do _wrap and _unwrap.
            #
            # Here we assume that if func is from numpy it accepts pandas,
            # otherwise it accepts fireducks.

            # pandas.GroupBy.apply() replaces built-in max/min/sum with
            # numpy max/min/sum. Since this wrapper hides builtin funcs
            # from pandas, we replace those here.
            # See GT #675
            _builtin_table = {sum: np.sum, max: np.max, min: np.min}
            func = _builtin_table.get(func, func)

            if getattr(func, "__module__", None) == "numpy":

                def wrapper(df, *args_, **kwargs_):
                    # ignore numpy error as panadas.
                    with np.errstate(all="ignore"):
                        return func(df, *args_, **kwargs_)

            else:

                def wrapper(df, *args_, **kwargs_):
                    return utils._unwrap(
                        func(utils._wrap(df), *args_, **kwargs_),
                        reason="return value of user function passed to apply",
                    )

            return self._fallback_call(
                "apply",
                wrapper,
                *args,
                **kwargs,
                __fireducks_reason="DataFrameGroupby.apply is not supported",
            )
        return self._fallback_call(
            "apply",
            func,
            *args,
            **kwargs,
            __fireducks_reason="func is not callable",
        )

    def _evaluate(self):
        return self._unwrap()

    def transform(self, func, *args, engine=None, **kwargs):
        use_numba = maybe_use_numba(engine)
        if use_numba:
            # Incompatibility: 013
            warnings.warn("numba is not supported", UserWarning)

        # - Wrapper function cannot use numba.
        # - String function catnot wrap.
        # - If func is in the list of get_cython_func(),
        #   pandas.Groupby._transform() will call the internal function.
        if use_numba or not callable(func) or get_cython_func(func):
            wrapper = func
        else:

            def wrapper(df, *args_, **kwargs_):
                return utils._unwrap(
                    func(utils._wrap(df), *args_, **kwargs_),
                    reason="return value of user function passed to apply",
                )

        reason = "transform function is not supported"
        return self._fallback_call(
            "transform",
            wrapper,
            *utils._unwrap(args),
            __fireducks_reason=reason,
            engine=engine,
            **kwargs,
        )


def _setup_SeriesGroupBy(cls):
    pandas_class = pandas.core.groupby.generic.SeriesGroupBy

    # pandas.DataFrame has corrwith function, but pandas.Series doesn't have
    # corrwith function
    for m in reduction_kernels - set(["corrwith"]):
        _install_agg(cls, m, pandas_class)

    for m in series_apply_allowlist:
        _install_agg(cls, m, pandas_class)

    return cls


@_setup_SeriesGroupBy
class SeriesGroupBy(FireDucksGroupBy):
    """SeriesGroupBy is groupby which returns Series.

    There are two cases where SeriesGroupBy is created:
        1. groupby on Series: series.groupby()
        2. groupby and selection on DataFrame: df.groupby(key)[col]
    """

    def _aggregate(self, func, aggArgs):
        target, by_cols, ser_as_key = validate_groupby_target(
            self._obj, self._by
        )
        selection = make_selection_ops(self._selection)
        funcs, columns, relabels = aggArgs.to_ir()
        value = ir.groupby_select_agg(
            target._value,
            make_groupkey_ops(by_cols),
            funcs,
            columns,
            relabels,
            selection,
            self._as_index,
            self._dropna,
            self._sort,
        )

        cls = DataFrame
        if isinstance(func, str):
            cls = Series
        ret = cls._create(value)
        return process_agg_output(
            ret, ser_as_key, self._as_index, self._by, by_cols
        )

    def aggregate(self, func=None, *args, **kwargs):
        logger.debug("SeriesGroupBy.aggregate: %s", type(self))

        reason = None
        if (
            self._selection is None
            or isinstance(self._selection, (tuple, list))
            or not is_supported_selection(self._selection)
        ):
            reason = "Series.groupby is not supported"

        if not reason:
            if isinstance(self._selection, str) and func is None and not args:
                # For SeriesGroupBy with kwargs case:
                # df.groupby("a")["b"].agg(Sum="sum", Max="max")
                # is to be converted as:
                # df.groupby("a").agg(Sum=("b", "sum"), Max=("b", "max"))
                new_kwargs = {}
                for k, v in kwargs.items():
                    if isinstance(v, str):
                        new_kwargs[k] = (self._selection, v)
                    else:
                        reason = "unsupported aggregated args"
                        break

                if not reason:
                    return DataFrameGroupBy(
                        self._obj,
                        *self._groupby_args,
                        by=self._by,
                        as_index=self._as_index,
                        sort=self._sort,
                        dropna=self._dropna,
                        **self._groupby_kwargs,
                    ).aggregate(func, *args, **new_kwargs)

        if reason:
            return self._fallback_call(
                "agg",
                func,
                *utils._unwrap(args),
                __fireducks_reason=reason,
                **kwargs,
            )

        return super().aggregate(func, *args, **kwargs)

    agg = aggregate

    @property
    def dtype(self):
        return self.__getattr__("dtype")

    @property
    def is_monotonic_decreasing(self):
        return self.__getattr__("is_monotonic_decreasing")

    @property
    def is_monotonic_increasing(self):
        return self.__getattr__("is_monotonic_increasing")

    def transform(self, func, *args, **kwargs):
        # Temporarily fallback until supported by dfkl
        if False:
            if (
                self._has_unsupported_groupby_args() is not None
                or isinstance(self._by, Series)
                or not self._as_index
                or args
                or kwargs
                or (not isinstance(func, str) and not _is_str_list(func))
            ):
                return super().transform(func, *args, **kwargs)

            if self._selection is None:
                by = make_vector_or_scalar_of_str(self._by)
                value = ir.groupby_transform(self._obj._value, by, func)
            elif isinstance(self._selection, str):
                assert isinstance(self._obj, DataFrame)
                by = make_vector_or_scalar_of_str(self._by)
                selection = make_vector_or_scalar_of_str(self._selection)
                value = ir.groupby_select_transform(
                    self._obj._value, by, selection, func
                )

            return Series._create(value)

        return super().transform(func, *args, **kwargs)

    def _head_or_tail(self, is_head, n=5):
        reason = []
        if (
            self._selection is None
            or isinstance(self._selection, (tuple, list))
            or not is_supported_selection(self._selection)
        ):
            reason.append("Series.groupby is not supported")

        reason_args = self._has_unsupported_groupby_args()
        if reason_args is not None:
            reason.append(reason_args)

        if not isinstance(n, int):
            reason.append(f"unsupported 'n' = {n} of type: {type(n).__name__}")

        if len(reason) > 0:
            func = "head" if is_head else "tail"
            return self._fallback_call(
                func, n, __fireducks_reason="; ".join(reason)
            )

        with_selector = True
        selection = make_selection_ops(self._selection)
        target, by_cols, ser_as_key = validate_groupby_target(
            self._obj, self._by
        )
        value = ir.groupby_head_or_tail(
            target._value,
            make_groupkey_ops(by_cols),
            selection,
            with_selector,
            n,
            self._dropna,
            is_head,
        )
        return Series._create(value)

    def head(self, n=5):
        logger.debug("SeriesGroupBy.head: %s", type(self))
        return self._head_or_tail(True, n=n)

    def tail(self, n=5):
        logger.debug("SeriesGroupBy.tail: %s", type(self))
        return self._head_or_tail(False, n=n)

    def shift(self, *args, **kwargs):
        arg = utils.decode_args(
            args, kwargs, pandas.core.groupby.SeriesGroupBy.shift
        )
        reason = []

        reason_no_default = arg.is_not_default(["freq", "axis", "fill_value"])
        if reason_no_default is not None:
            reason.append(reason_no_default)

        if (
            self._selection is None
            or isinstance(self._selection, (tuple, list))
            or not is_supported_selection(self._selection)
        ):
            reason.append("Series.groupby is not supported")

        reason_args = self._has_unsupported_groupby_args()
        if reason_args is not None:
            reason.append(reason_args)

        if not isinstance(arg.periods, int):
            reason.append(
                f"unsupported 'periods' = {arg.periods} "
                f"of type: {type(arg.periods).__name__}"
            )

        if len(reason) > 0:
            return self._fallback_call(
                "shift", *args, **kwargs, __fireducks_reason="; ".join(reason)
            )

        with_selector = True
        selection = make_selection_ops(self._selection)
        target, by_cols, ser_as_key = validate_groupby_target(
            self._obj, self._by
        )
        value = ir.groupby_shift(
            target._value,
            make_groupkey_ops(by_cols),
            selection,
            with_selector,
            arg.periods,
            self._dropna,
        )
        return Series._create(value)


def _setup_DataFrameGroupBy(cls):
    pandas_cls = pandas.core.groupby.generic.DataFrameGroupBy

    # FIXME: use groupby_other_methods
    other_methods = [
        # non-aggregation methods
        "corr",
        "cov",
        "hist",
        "plot",
        "take",
    ]
    utils.install_fallbacks(cls, other_methods, pandas_cls)

    # Exclude 'nth' because it is a callable property, not a method.
    for m in transform_kernel_allowlist - {"nth"}:
        _install_agg(cls, m, pandas_cls)
    return cls


@_setup_DataFrameGroupBy
class DataFrameGroupBy(FireDucksGroupBy):
    def __getattr__(self, name):
        logger.debug("DataFrameGroupBy.__getattr__: name=%s", name)

        # Check if `name` should be a column name. See DataFrame.__getattr__
        # for details.
        from pandas.core.groupby.generic import (
            DataFrameGroupBy as PandasDataFrameGroupBy,
        )

        if name not in PandasDataFrameGroupBy.__dict__:
            if self._obj._is_column_name(name):
                return self[name]

        reason = f"{type(self).__name__}.__getattr__ for {name} is called"
        return utils.fallback_attr(self._unwrap, name, reason)

    def __getitem__(self, key):
        if self._selection:
            raise IndexError(f"Column(s) {self._selection} already selected")
        if not isinstance(key, list) and self._as_index:
            return SeriesGroupBy(
                self._obj,
                *self._groupby_args,
                by=self._by,
                as_index=self._as_index,
                sort=self._sort,
                dropna=self._dropna,
                selection=key,
                **self._groupby_kwargs,
            )
        else:
            return DataFrameGroupBy(
                self._obj,
                *self._groupby_args,
                by=self._by,
                as_index=self._as_index,
                sort=self._sort,
                dropna=self._dropna,
                selection=key,
                **self._groupby_kwargs,
            )

    def _aggregate(self, func, aggArgs):
        target, by_cols, ser_as_key = validate_groupby_target(
            self._obj, self._by
        )
        if self._selection is None:
            funcs, columns, relabels = aggArgs.to_ir()
            value = ir.groupby_agg(
                target._value,
                make_groupkey_ops(by_cols),
                funcs,
                columns,
                relabels,
                self._as_index,
                self._dropna,
                self._sort,
            )
        else:
            funcs, columns, relabels = aggArgs.to_ir()
            selection = make_selection_ops(self._selection)
            value = ir.groupby_select_agg(
                target._value,
                make_groupkey_ops(by_cols),
                funcs,
                columns,
                relabels,
                selection,
                self._as_index,
                self._dropna,
                self._sort,
            )

        funcs = ["cumcount", "ngroup", "size"]
        cls = DataFrame
        logger.debug(f"check class: {func}")
        if isinstance(func, str) and self._as_index and func in funcs:
            logger.debug("check class: Series")
            cls = Series
        ret = cls._create(value)
        return process_agg_output(
            ret, ser_as_key, self._as_index, self._by, by_cols
        )

    @property
    def dtypes(self):
        return self.__getattr__("dtypes")

    def transform(self, func, *args, **kwargs):
        # Temporarily fallback until supported by dfkl
        if False:
            if (
                isinstance(func, str)
                and func not in transform_kernel_allowlist
            ):
                msg = f"'{func}' is not a valid function name for transform"
                raise ValueError(msg)

            if (
                self._has_unsupported_groupby_args() is not None
                or isinstance(self._by, Series)
                or args
                or kwargs
                or not isinstance(func, str)
            ):
                return super().transform(func, *args, **kwargs)

            if self._selection is None:
                by = make_vector_or_scalar_of_str(self._by)
                value = ir.groupby_transform(self._obj._value, by, func)
            else:
                by = make_vector_or_scalar_of_str(self._by)
                selection = make_vector_or_scalar_of_str(self._selection)
                value = ir.groupby_select_transform(
                    self._obj._value, by, selection, func
                )

            funcs = ["cumcount", "ngroup"]
            cls = DataFrame
            if isinstance(func, str) and self._as_index and func in funcs:
                cls = Series
            return cls._create(value)

        return super().transform(func, *args, **kwargs)

    def _head_or_tail(self, is_head, n=5):
        reason = []

        reason_args = self._has_unsupported_groupby_args()
        if reason_args is not None:
            reason.append(reason_args)

        if not isinstance(n, int):
            reason.append(f"unsupported 'n' = {n} of type: {type(n).__name__}")

        if len(reason) > 0:
            func = "head" if is_head else "tail"
            return self._fallback_call(
                func, n, __fireducks_reason="; ".join(reason)
            )

        if self._selection is None:
            with_selector = False
            selection = make_selection_ops([])
        else:
            with_selector = True
            selection = make_selection_ops(self._selection)

        target, by_cols, ser_as_key = validate_groupby_target(
            self._obj, self._by
        )
        value = ir.groupby_head_or_tail(
            target._value,
            make_groupkey_ops(by_cols),
            selection,
            with_selector,
            n,
            self._dropna,
            is_head,
        )
        ret = DataFrame._create(value)
        if ser_as_key and not with_selector:
            # head/tail includes key-column in result as well,
            # hence the appended column needs to be dropped from result
            ret = ret.drop(columns=by_cols)
        return ret

    def head(self, n=5):
        logger.debug("DataFrameGroupBy.head: %s", type(self))
        return self._head_or_tail(True, n=n)

    def tail(self, n=5):
        logger.debug("DataFrameGroupBy.tail: %s", type(self))
        return self._head_or_tail(False, n=n)

    def _corrwith(self, *args, **kwargs):
        # arg = utils.decode_args(
        #    args, kwargs, pandas.core.groupby.DataFrameGroupBy.corrwith
        # )
        arg = utils.decode_args(args, kwargs, self.corrwith)
        reason = []

        reason_no_default = arg.is_not_default(
            ["drop", "axis", "method", "numeric_only"]
        )
        if reason_no_default is not None:
            reason.append(reason_no_default)

        reason_args = self._has_unsupported_groupby_args()
        if reason_args is not None:
            reason.append(reason_args)

        if reason_args is not None:
            if isinstance(self._by, Series):
                reason.append("corrwith: series as key is not supported")

        if not isinstance(arg.other, Series):
            reason.append(
                f"unsupported 'other' of type: {type(arg.other).__name__}"
            )

        if self._selection is None:
            nkeys = 1 if irable_scalar(self._by) else len(self._by)
            # shape check might cause evaluation, but better than fallback
            if (self._obj.shape[1] - nkeys) != 1:
                reason.append(
                    "Unsupported corrwith with multiple non-key-columns"
                )
            else:
                with_selector = False
                selection = make_selection_ops([])
        else:
            if (
                isinstance(self._selection, (tuple, list))
                and len(self._selection) != 1
            ):
                reason.append("Unsupported selection with multiple columns")
            else:
                with_selector = True
                selection = make_selection_ops(self._selection)

        if len(reason) > 0:
            return self._fallback_call(
                "corrwith",
                *args,
                **kwargs,
                __fireducks_reason="; ".join(reason),
            )

        by = make_groupkey_ops(self._by)
        value = ir.groupby_corrwith(
            self._obj._value,
            by,
            selection,
            arg.other._value,
            self._as_index,
            self._dropna,
            self._sort,
            with_selector,
        )
        return DataFrame._create(value)

    # pandas.core.groupby.DataFrameGroupBy.corrwith is a property
    # hence difficult to inspect signature
    def corrwith(
        self, other, axis=0, drop=False, method="pearson", numeric_only=False
    ):
        return self._corrwith(
            other,
            axis=axis,
            drop=drop,
            method=method,
            numeric_only=numeric_only,
        )

    def shift(self, *args, **kwargs):
        arg = utils.decode_args(
            args, kwargs, pandas.core.groupby.DataFrameGroupBy.shift
        )
        reason = []

        reason_no_default = arg.is_not_default(["freq", "axis", "fill_value"])
        if reason_no_default is not None:
            reason.append(reason_no_default)

        reason_args = self._has_unsupported_groupby_args()
        if reason_args is not None:
            reason.append(reason_args)

        if not isinstance(arg.periods, int):
            reason.append(
                f"unsupported 'periods' = {arg.periods} "
                f"of type: {type(arg.periods).__name__}"
            )

        if len(reason) > 0:
            return self._fallback_call(
                "shift", *args, **kwargs, __fireducks_reason="; ".join(reason)
            )

        if self._selection is None:
            with_selector = False
            selection = make_selection_ops([])
        else:
            with_selector = True
            selection = make_selection_ops(self._selection)

        target, by_cols, ser_as_key = validate_groupby_target(
            self._obj, self._by
        )
        value = ir.groupby_shift(
            target._value,
            make_groupkey_ops(by_cols),
            selection,
            with_selector,
            arg.periods,
            self._dropna,
        )
        return DataFrame._create(value)
