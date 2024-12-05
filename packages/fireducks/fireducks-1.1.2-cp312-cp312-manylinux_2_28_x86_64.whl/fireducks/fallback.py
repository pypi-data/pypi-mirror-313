# Copyright (c) 2023 NEC Corporation. All Rights Reserved.

from contextlib import contextmanager
import functools
import inspect
import logging
import time
import types
import warnings

from firefw import runtime, tracing

from fireducks.errors import FallbackWarning

logger = logging.getLogger(__name__)


class FallbackManager:
    _fallback_prohibited = False

    def __init__(self, flag):
        self.flag = flag

    def __enter__(self):
        FallbackManager._fallback_prohibited = self.flag

    def __exit__(self, exec_type, exec_value, traceback):
        FallbackManager._fallback_prohibited = False

    @classmethod
    def check(cls, msg):
        """Call this method just before falling back."""
        if cls._fallback_prohibited:
            raise RuntimeError(f"fallback prohibited: {msg}")


def prohibit_fallback(cond=True):
    """
    with prohibit_fallback():
        evaluate IR
    """
    return FallbackManager(cond)


def find_user_frame(package="fireducks"):
    for frame in runtime.get_frames(2):
        module = inspect.getmodule(frame)
        if module is None or not module.__name__.startswith(package):
            return frame
    return None


def get_attr_long_name(owner, name):
    if hasattr(owner, "__name__"):  # ex: pandas
        return f"{owner.__name__}.{name}"
    elif hasattr(owner, "__class__"):  # ex: DataFrame
        return f"{owner.__class__.__name__}.{name}"
    return name


class FallbackWarningBuilder:
    def __init__(self, name, reason, warn_fallback):
        self.reason = reason
        self.warn_fallback = warn_fallback
        if warn_fallback:
            self.start_time = time.time()
            self.name = name
            self.timings = {}

    @contextmanager
    def timing(self, key):
        if self.warn_fallback:
            t0 = time.time()
            yield
            self.timings[key] = time.time() - t0
        else:
            yield

    def warn(self, owner, stacklevel):
        if self.warn_fallback:
            tot = time.time() - self.start_time
            name = get_attr_long_name(owner, self.name)
            timings = " ".join(
                [f"{k} {v:.6f}" for k, v in self.timings.items()]
            )
            warnings.warn(
                f"{name} {tot:.6f} sec {timings} {self.reason}",
                FallbackWarning,
                stacklevel=stacklevel,
            )


def fallback_attr(
    fallbacker,
    name,
    reason=None,
    *,
    stacklevel=0,
    wrap_func=None,
    unwrap_func=None,
    log_lineno=False,
    warn_fallback=False,
):
    """
    Fallback attribute reference.

    Parameters
    ----------
    fallbacker: Callable which returns the object having the attribute.
    name:       Name of attribute
    reason:     Reason of fallback for logging
    stacklevel: Depth from user code for warning
    """
    warn_builder = FallbackWarningBuilder(name, reason, warn_fallback)

    at = ""
    if log_lineno:
        frame = find_user_frame()
        if frame is not None:
            at = f"at={inspect.getfile(frame)}:{frame.f_lineno}"
        else:
            at = "at=unknown"

    FallbackManager.check(f"fallback_attr: attr={name}: {reason}")

    with warn_builder.timing("getobj"):
        obj = fallbacker(reason=reason)

    logger.info(
        "fallback_attr: name=%s reason=%s %s",
        get_attr_long_name(obj, name),
        reason,
        at,
    )

    with warn_builder.timing("getattr"):
        with tracing.scope(tracing.Level.VERBOSE, f"fallback:getattr:{name}"):
            # to support attribute chain: e.g. getattr(df, "iloc.__setitem__")
            attr = obj
            for nm in name.split("."):
                attr = getattr(attr, nm)

    if isinstance(attr, (types.MethodType, types.FunctionType)):

        @functools.wraps(attr)
        def wrapper(*args, **kwargs):
            if isinstance(attr, types.MethodType):
                fullname = f"{type(attr.__self__).__name__}.{name}"
                logger.debug(
                    "fallback_attr.wrapper: call method `%s.%s` on %x",
                    type(attr.__self__).__name__,
                    name,
                    id(attr.__self__),
                )
            else:
                fullname = name
                logger.debug("fallback_attr.wrapper: call %s", name)
            reason = "argument for callback"

            with warn_builder.timing("args"):
                args = unwrap_func(args, reason=reason)
                kwargs = unwrap_func(kwargs, reason=reason)

            with warn_builder.timing("call"):
                with tracing.scope(
                    tracing.Level.VERBOSE, f"fallback:{fullname}"
                ):
                    ret = attr(*args, **kwargs)

            ret = wrap_func(ret)
            lv = stacklevel or 3
            warn_builder.warn(obj, stacklevel=lv)
            return ret

        return wrapper
    else:
        lv = stacklevel or 5
        warn_builder.warn(obj, stacklevel=lv)

    logger.debug("fallback_attr: return attr for %s: %s", name, type(attr))
    return wrap_func(attr)


def fallback_call(
    fallbacker,
    method,
    args=None,
    kwargs=None,
    *,
    reason=None,
    stacklevel=6,
    wrap_func=None,
    unwrap_func=None,
    log_lineno=False,
    warn_fallback=False,
):
    """
    Fallback a method call with packed arguments: args and kwargs.

    After resolving attribute, call it with arguments.

    Parameters
    ----------
    args, kwargs: Arguments passed to the method
    stacklevel:   Level from user code to warnings.warn
    """
    method = fallback_attr(
        fallbacker,
        method,
        reason,
        stacklevel=stacklevel,
        wrap_func=wrap_func,
        unwrap_func=unwrap_func,
        log_lineno=log_lineno,
        warn_fallback=warn_fallback,
    )
    assert callable(method)
    args = [] if args is None else args
    kwargs = {} if kwargs is None else kwargs
    # fallback_attr returns a wrapper for _wrap, _unwap. we can simply call a
    # method
    return method(*args, **kwargs)
