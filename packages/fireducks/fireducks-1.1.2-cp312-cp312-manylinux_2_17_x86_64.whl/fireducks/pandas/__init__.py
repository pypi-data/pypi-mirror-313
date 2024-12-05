# Copyright (c) 2023 NEC Corporation. All Rights Reserved.
"""
fireducks.pandas provides pandas-like API on top of fireducks.
"""

import os
import sys

env = os.environ.get("FIREDUCKS_DISABLE")
if env is not None:
    from pandas import *  # noqa
else:
    import logging

    from fireducks import __dfkl_version__

    from fireducks.core import get_fireducks_options
    from fireducks.pandas.api import (
        concat,
        from_pandas,
        get_dummies,
        isna,
        isnull,
        melt,
        merge,
        notna,
        notnull,
        read_csv,
        read_json,
        read_parquet,
        to_parquet,
        to_pickle,
        to_datetime,
    )
    from fireducks.pandas.config import (
        option_context,
        options,
        set_option,
    )
    from fireducks.pandas.frame import DataFrame
    from fireducks.pandas.series import Series

    # FireDucks original API
    from fireducks.pandas.feat import (  # noqa
        aggregation,
        merge_with_mask,
        multi_target_encoding,
    )

    import fireducks.pandas.utils as _utils
    from fireducks.pandas.utils import (  # noqa
        prohibit_fallback,
        _get_pandas_module,
    )

    from fireducks.pandas.wrappers import (
        Categorical,
        CategoricalIndex,
        DatetimeIndex,
        Index,
        IntervalIndex,
        MultiIndex,
        PeriodIndex,
        RangeIndex,
        TimedeltaIndex,
    )

    if _utils._pd_version_under2:
        # pandas does not have NumericIndex class since v2.0.
        from fireducks.pandas.wrappers import (
            Float64Index,
            Int64Index,
            UInt64Index,
            NumericIndex,
        )

    logger = logging.getLogger(__name__)

    def set_version(is_fireducks):
        global __version__, __git_version__

        if is_fireducks:
            from fireducks import __version__, __git_version__
        else:
            from pandas import __version__, __git_version__

    # 3.7 or later supports module's __getattr__
    if sys.version_info.major > 3 or (
        sys.version_info.major == 3 and sys.version_info.minor >= 7
    ):
        # Borrow unknown attribute from pandas
        def __getattr__(name):
            logger.debug("Borrow %s from pandas", name)
            reason = f"borrow {name} from pandas"
            return _utils.fallback_attr(
                _get_pandas_module, name, reason=reason
            )

    else:
        m = sys.modules[__name__]

        class Wrapper:
            def __getattr__(self, name):
                logger.debug("Borrow %s from pandas", name)
                reason = f"borrow {name} from pandas"
                return _utils.fallback_attr(
                    _get_pandas_module, name, reason=reason
                )

        w = Wrapper()
        names = [
            "from_pandas",
            "read_csv",
            "to_pickle",
            "DataFrame",
            "Series",
            "prohibit_fallback",
            "__path__",
            "__spec__",
        ]
        for name in names:
            setattr(w, name, getattr(m, name))
        w.__name__ = "fireducks.pandas"
        sys.modules[__name__] = w

    set_version(is_fireducks=get_fireducks_options().fireducks_version)

    __all__ = (
        "__dfkl_version__",
        "from_pandas",
        # pandas api
        "__version__",
        "__git_version__",
        "DataFrame",
        "Series",
        "Categorical",
        "CategoricalIndex",
        "DatetimeIndex",
        "Index",
        "IntervalIndex",
        "MultiIndex",
        "PeriodIndex",
        "RangeIndex",
        "TimedeltaIndex",
        "concat",
        "get_dummies",
        "isna",
        "isnull",
        "melt",
        "merge",
        "notna",
        "notnull",
        "read_csv",
        "read_parquet",
        "to_parquet",
        "to_pickle",
    )

    # pandas does not have NumericIndex class since v2.0.
    if _utils._pd_version_under2:
        __all__ += (
            "Float64Index" "Int64Index",
            "NumericIndex",
            "UInt64Index",
        )

    def load_ipython_extension(ipython):
        # cf. https://ipython.readthedocs.io/en/stable/config/extensions/
        from fireducks import importhook
        from fireducks import ipyext

        hook = importhook._get_current_hook()
        if hook is not None:
            raise RuntimeError(
                f"another import-hook is already active: {hook!r}"
            )
        importhook.activate_hook(__name__)

        ipyext.load_ipython_extension(ipython)

    def unload_ipython_extension(ipython):
        # cf. https://ipython.readthedocs.io/en/stable/config/extensions/
        from fireducks import importhook

        importhook.deactivate_hook()
