# Copyright (c) 2023 NEC Corporation. All Rights Reserved.

from collections import abc
import os
import glob
import pathlib
import logging

import numpy as np
from pandas.io.common import is_url, is_fsspec_url
from pandas.core.dtypes.common import is_scalar
import pandas._libs.missing as libmissing

from firefw import tracing

with tracing.scope(tracing.Level.DEFAULT, "import pandas"):
    import pandas
    from pandas.util._decorators import deprecate_nonkeyword_arguments
    import pandas.api.extensions as pandas_extensions
    from pandas.core.dtypes.common import (
        is_list_like,
        is_object_dtype,
    )

from fireducks import ir, irutils
import fireducks.core
from fireducks.pandas.frame import DataFrame
from fireducks.pandas.series import Series
import fireducks.pandas.utils as utils

import fireducks.pandas.hinting.ops as hinting

logger = logging.getLogger(__name__)

#
# FireDucks API
#


def from_pandas(obj):
    logger.debug("from_pandas: %s", type(obj))

    if isinstance(obj, pandas.DataFrame):
        return DataFrame.from_pandas(obj)
    elif isinstance(obj, pandas.Series):
        return Series.from_pandas(obj)
    raise RuntimeError(
        "fireducks.from_pandas: unknown object is given: " f"{type(obj)}"
    )


#
# Pandas copmat API
#


@deprecate_nonkeyword_arguments(version=None, allowed_args=["objs"])
def concat(*args, **kwargs):
    arg = utils.decode_args(args, kwargs, pandas.concat)
    if isinstance(arg.objs, abc.Mapping):
        if arg.keys is None:
            arg.keys = list(arg.objs.keys())
        arg.objs = [arg.objs[k] for k in arg.keys]
    else:
        # If `objs` is a generator expression, we can get the values from
        # `objs` just once, so overwrite it with the expanded list.
        arg.objs = list(arg.objs)
        args = (arg.objs,) + args[1:]

    if not arg.objs:
        raise ValueError("No objects to concatenate")

    class Concat:
        def __init__(self, objs):
            self.objs = objs

    op = Concat(arg.objs)
    cls = None
    if all([isinstance(obj, DataFrame) for obj in arg.objs]):
        cls = DataFrame
    if all([isinstance(obj, Series) for obj in arg.objs]):
        cls = Series

    if cls is None:
        reason = "objs are not DataFrame or Series"
    else:
        reason = arg.is_not_default(
            [
                "axis",
                "join",
                "keys",
                "levels",
                "names",
                "verify_integrity",
                "sort",
                "copy",
            ]
        )

    if reason:
        return utils.fallback_call_packed(
            utils._get_pandas_module,
            "concat",
            args,
            kwargs,
            reason=reason,
        ).__finalize__(op, method="concat")

    objs = irutils.make_tuple_of_tables(arg.objs)
    return cls._create(
        ir.concat(
            objs, ignore_index=arg.ignore_index, no_align=(cls == Series)
        )
    ).__finalize__(op, method="concat")


def get_dummies(*args, **kwargs):
    decoded = utils.decode_args(args, kwargs, pandas.get_dummies)

    reason = None
    if not isinstance(decoded.data, DataFrame):
        reason = "input is not a DataFrame"

    if is_object_dtype(np.dtype(decoded.dtype)):
        raise ValueError("dtype=object is not a valid dtype for get_dummies")

    if reason is None:
        reason = decoded.is_not_default(
            exclude=[
                "data",
                "columns",
                "prefix",
                "prefix_sep",
                "drop_first",
                "dtype",
            ]
        )

    if reason is None:
        if decoded.columns is not None and not isinstance(
            decoded.columns, list
        ):
            reason = (
                "Unsupported columns of type "
                f"'{type(decoded.columns).__name__}'"
            )
        if decoded.prefix is not None and not isinstance(
            decoded.prefix, (str, list)
        ):
            reason = (
                "Unsupported prefix of type "
                f"'{type(decoded.prefix).__name__}'"
            )
        if not isinstance(decoded.prefix_sep, str):
            reason = (
                "Unsupported prefix_sep of "
                f"type '{type(decoded.prefix_sep).__name__}'"
            )

        default_dtype = np.uint8 if utils._pd_version_under2 else np.bool_
        dtype = default_dtype if decoded.dtype is None else decoded.dtype
        if not utils.is_supported_dtype(dtype):
            reason = f"Unsupported dtype '{decoded.dtype}'"

    if reason is not None:
        return utils.fallback_call_packed(
            utils._get_pandas_module,
            "get_dummies",
            args,
            kwargs,
            reason=reason,
        )

    data = decoded.data
    dtype = utils.to_supported_dtype(dtype)
    columns = irutils.make_vector_or_scalar_of_column_name(decoded.columns)
    prefix = irutils.make_vector_or_scalar_of_column_name(decoded.prefix)
    prefix_sep = decoded.prefix_sep
    drop_first = bool(decoded.drop_first)
    value = ir.get_dummies(
        data._value, columns, prefix, prefix_sep, dtype, drop_first
    )
    return DataFrame._create(value)


def isnull(obj):
    if is_scalar(obj):
        return libmissing.checknull(obj)
    elif isinstance(obj, type):
        return False
    elif isinstance(obj, (DataFrame, Series)):
        return obj.isnull()

    return utils.fallback_call(
        utils._get_pandas_module,
        "isnull",
        obj,
        __fireducks_reason="obj is not DataFrame or Series",
    )


isna = isnull


def melt(frame, *args, **kwargs):
    if isinstance(frame, DataFrame):
        return frame.melt(*args, **kwargs)

    return utils.fallback_call(
        utils._get_pandas_module,
        "melt",
        frame,
        *args,
        __fireducks_reason="obj is not DataFrame",
        **kwargs,
    )


def merge(left, right, *args, **kwargs):
    return left.merge(right, *args, **kwargs)


def notna(obj):
    if isinstance(obj, (DataFrame, Series)):
        return ~(obj.isnull())

    return utils.fallback_call(
        utils._get_pandas_module,
        "notna",
        obj,
        __fireducks_reason="obj is not DataFrame or Series",
    )


notnull = notna


def read_csv(*args, **kwargs):
    decoded = utils.decode_args(args, kwargs, pandas.read_csv)
    names = decoded.names
    filepath_or_buffer = decoded.filepath_or_buffer
    index_col = decoded.index_col
    usecols = decoded.usecols
    dtype = decoded.dtype
    sep = decoded.sep
    delimiter = decoded.delimiter
    header = decoded.header

    if isinstance(header, bool):
        raise TypeError(
            "Passing a bool to header is invalid. Use header=None for no "
            "header or header=int or list-like of ints to specify the "
            "row(s) making up the column names"
        )

    reason = None
    if not utils._pd_version_under2:
        dtype_backend = decoded.dtype_backend
        if (
            dtype_backend is not pandas_extensions.no_default
            and dtype_backend not in {"pyarrow"}
        ):
            reason = f"unsupported dtype_backend: '{dtype_backend}'"

    if names is not pandas_extensions.no_default and not irutils._is_str_list(
        names
    ):
        reason = "names is not a list of string"
    elif not isinstance(
        filepath_or_buffer, (str, pathlib.PosixPath, pathlib.WindowsPath)
    ):
        reason = "filepath_or_buffer is not filepath"
    elif usecols is not None and not irutils._is_str_list(usecols):
        reason = "usecols is not a list of string"
    elif (
        header is not None
        and header != "infer"
        and not isinstance(header, int)
    ):
        reason = "unsupported header of type: '{type(header)}'"
    elif (
        dtype is not None
        and not isinstance(dtype, dict)
        and not utils.is_supported_dtype(dtype)
    ):
        reason = f"dtype is not supported: {dtype}"
    elif decoded.encoding not in (None, "utf-8", "utf8", "UTF-8", "UTF8"):
        reason = f"unsupported encoding: {decoded.encoding}"
    elif isinstance(dtype, dict):
        for key, typ in dtype.items():
            if not isinstance(key, str):
                reason = f"column name of dtype is not string: {key}"
            elif not utils.is_supported_dtype(typ):
                reason = f"dtype is not supported: {typ}"
        if hasattr(dtype, "default_factory"):  # defaultdict
            default_dtype = dtype.default_factory()
            if not utils.is_supported_dtype(default_dtype):
                reason = f"default dtype is not supported: {default_dtype}"

    if reason is None and index_col is not None:
        if isinstance(index_col, bool):
            reason = "index_col is of boolean-type"
        else:  # bool is instance of int
            index_col = (
                [index_col] if isinstance(index_col, int) else index_col
            )
            if not irutils._is_list_of(index_col, int):
                reason = "index_col is not None, integer or list-of-integers"

    if reason is None:
        exclude_args = [
            "names",
            "filepath_or_buffer",
            "index_col",
            "usecols",
            "dtype",
            "sep",
            "delimiter",
            "header",
            "encoding",
        ]
        if not utils._pd_version_under2:
            exclude_args.append("dtype_backend")
        reason = decoded.is_not_default(exclude=exclude_args)

    if reason is None:
        path = os.path.expanduser(filepath_or_buffer)
        if is_url(path):
            reason = "path is url"
        if is_fsspec_url(path):
            reason = "seems like fsspec path"

    if reason is None:
        if header != "infer" and usecols is not None:
            reason = "usecols with header is provided"

    if reason is not None:
        return utils.fallback_call_packed(
            utils._get_pandas_module,
            "read_csv",
            args,
            kwargs,
            reason=reason,
        )

    # when include_columns is empty, all columns are returned
    include_columns = [] if usecols is None else usecols

    from fireducks.fireducks_ext import ReadCSVOptions

    if isinstance(header, int) and header < 0:
        raise ValueError(
            "Passing negative integer to header is invalid. For no header, use header=None instead"
        )

    options = ReadCSVOptions()
    # based on understanding of relationship between header and skiprows: #3385
    if names is not pandas_extensions.no_default:  # with names
        if len(names) != len(set(names)):
            raise ValueError("Duplicate names are not allowed.")
        options.names = names
        options.skiprows = (
            0 if header is None or header == "infer" else header + 1
        )
    else:  # without names
        if header is None:
            options.skiprows = 0
            options.autogenerate_column_names = True
        else:
            options.skiprows = 0 if header == "infer" else header

    if index_col is not None:
        options.index_col = index_col
    if include_columns:
        options.include_columns = include_columns
    if delimiter is None:
        delimiter = sep
    if delimiter is pandas_extensions.no_default:
        delimiter = ","
    options.delimiter = delimiter

    if isinstance(dtype, dict):
        for k, v in dtype.items():
            options.set_column_type(k, utils.to_supported_dtype(v))
        if hasattr(dtype, "default_factory"):  # defaultdict
            options.default_dtype = utils.to_supported_dtype(
                dtype.default_factory()
            )
    elif dtype is not None:
        options.default_dtype = utils.to_supported_dtype(dtype)

    options = fireducks.core.make_available_value(
        options, ir.ReadCSVOptionsType
    )

    if fireducks.core.get_ir_prop().has_metadata:
        value_meta = ir.read_csv_metadata(path, options)
        meta = fireducks.core.evaluate([value_meta])[0]
        _hint = hinting.create_hint_from_metadata(meta)
        value = ir.read_csv_with_metadata(path, options, value_meta)
        return DataFrame._create(value, hint=_hint)
    else:
        value = ir.read_csv(path, options)
        return DataFrame._create(value)


def read_json(*args, **kwargs):
    decoded = utils.decode_args(args, kwargs, pandas.read_json)
    reason = None

    path_or_buf = decoded.path_or_buf
    lines = decoded.lines
    if not isinstance(
        path_or_buf, (str, pathlib.PosixPath, pathlib.WindowsPath)
    ):
        reason = "path_or_buf is not a filepath"

    if not lines:
        reason = "target is not a new-line terminated json file"

    if reason is None:
        exclude = ["path_or_buf", "lines"]
        if not utils._pd_version_under2:
            exclude.append("engine")
        reason = decoded.is_not_default(exclude=exclude)

    if reason is None:
        path = os.path.expanduser(path_or_buf)
        if is_url(path):
            reason = "path is url"
        if is_fsspec_url(path):
            reason = "seems like fsspec path"

    if reason is not None:
        return utils.fallback_call_packed(
            utils._get_pandas_module,
            "read_json",
            args,
            kwargs,
            reason=reason,
        )

    value = ir.read_json(path)
    return DataFrame._create(value)


def read_parquet(*args, **kwargs):
    decoded = utils.decode_args(args, kwargs, pandas.read_parquet)
    path = decoded.path
    engine = decoded.engine
    columns = decoded.columns

    reason = []
    # engine=pyarrow should be supported?
    if engine not in {"auto", "pyarrow"}:
        reason += [f"unsupported engine: '{engine}'"]

    if not utils._pd_version_under2:
        dtype_backend = decoded.dtype_backend
        if (
            dtype_backend is not pandas_extensions.no_default
            and dtype_backend not in {"pyarrow"}
        ):
            reason += [f"unsupported dtype_backend: '{dtype_backend}'"]

    if columns is None:
        columns_ = []
    elif isinstance(columns, str):
        columns_ = [columns]
    elif isinstance(columns, list):
        if not irutils._is_str_list(columns):
            reason += ["'columns' is not a list-of-strings"]
        columns_ = columns
    else:
        reason += ["unsupported 'columns' of type: {type(columns).__name__}"]

    if isinstance(path, (str, pathlib.PosixPath, pathlib.WindowsPath)):
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            dir_contents = glob.glob(os.path.join(path, "*"))
            if any([os.path.isdir(e) for e in dir_contents]):
                reason += ["path is a directory containing other directories"]
        elif is_url(path):
            reason += ["path is url"]
        elif is_fsspec_url(path):
            reason += ["seems like fsspec path"]
    else:
        reason += ["path is not string"]

    exclude_args = ["path", "engine", "columns"]
    if not utils._pd_version_under2:
        exclude_args.append("dtype_backend")
    no_default = decoded.is_not_default(exclude=exclude_args)
    if no_default:
        reason += [no_default]

    if len(reason) > 0:
        return utils.fallback_call_packed(
            utils._get_pandas_module,
            "read_parquet",
            args,
            kwargs,
            reason="; ".join(reason),
        )

    columns = irutils.make_tuple_of_column_names(columns_)
    if os.path.isdir(path):
        loaded_data = []
        for file in sorted(dir_contents):
            loaded_data.append(
                DataFrame._create(ir.read_parquet(file, columns))
            )
        return concat(loaded_data)
    return DataFrame._create(ir.read_parquet(path, columns))


def to_datetime(*args, **kwargs):
    arg = utils.decode_args(args, kwargs, pandas.to_datetime)
    reason = arg.is_not_default(exclude=["arg", "format"])

    data = arg.arg
    if not isinstance(data, Series):
        reason = f"to_datetime on non-Series input of type: '{type(data)}'"

    if arg.format is not None:
        if isinstance(arg.format, str):
            if arg.format.startswith("ISO") or arg.format == "mixed":
                reason = f"unsupported format: '{arg.format}'"
        else:
            reason = f"non-string format: '{arg.format}'"

    if reason is not None:
        return utils.fallback_call(
            utils._get_pandas_module,
            "to_datetime",
            *args,
            **kwargs,
            __fireducks_reason=reason,
        )
    fmt = irutils.make_scalar(arg.format)
    return Series._create(ir.to_datetime(data._value, fmt))


# pandas.io.to_parquet is not found in the API document as far as we know. But
# pandas_tests uses it. We provide it as fireducks.pandas.to_parquet because
# fireducks does not provide fireducks.pandas.io package at the moment.
def to_parquet(*args, **kwargs):
    def get_module(reason=None):
        from pandas.io import parquet

        return parquet

    return utils.fallback_call(
        get_module,
        "to_parquet",
        *args,
        **kwargs,
        __fireducks_reason="to_parquet is fallback",
    )


def to_pickle(obj, *args, **kwargs):
    logger.debug("to_pickle")
    pandas.to_pickle(utils._unwrap(obj), *args, **kwargs)


import sys
import pandas


def _get_pandas_api_module(reason=None):
    return pandas.api


# Borrow unknown module attributes from pandas
def __getattr__(name):
    logger.debug("Borrow %s from pandas.api", name)
    if name in ["__path__", "__spec__"]:
        return object.getattr(sys.modules[__name__], name)
    reason = f"borrow {name} from pandas.api"
    return utils.fallback_attr(_get_pandas_api_module, name, reason=reason)
