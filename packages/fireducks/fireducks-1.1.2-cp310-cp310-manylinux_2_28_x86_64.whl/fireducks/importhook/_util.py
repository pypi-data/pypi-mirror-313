# Copyright (c) 2023 NEC Corporation. All Rights Reserved.

import logging


# NOTE: str.removeprefix is available from Python 3.9
def removeprefix(s, prefix):
    if s.startswith(prefix):
        return s[len(prefix):]  # fmt: skip
    else:
        return s[:]


# NOTE: str.removesuffix is available from Python 3.9
def removesuffix(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]  # fmt: skip
    else:
        return s[:]


class LoggingHandlerWrapper:
    _handler = logging.StreamHandler()

    @classmethod
    def _set(cls, handler):
        cls._handler = handler

    @classmethod
    def get(cls):
        return cls._handler


def get_logger():
    return logging.getLogger(__package__)


def get_logging_handler():
    return LoggingHandlerWrapper.get()


_logger = get_logger()
_logger.addHandler(logging.NullHandler())
_logger.propagate = False
