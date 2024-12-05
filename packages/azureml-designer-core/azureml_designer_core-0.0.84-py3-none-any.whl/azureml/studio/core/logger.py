import ast
import logging
import re
import sys
import time
from contextlib import contextmanager
from traceback import StackSummary, walk_tb
from functools import wraps
from typing import Union

from azureml.studio.core.utils.strutils import truncate_lines

"""
General logging interface for AML Studio.

Usage:

from azureml.studio.core.logger import logger

logger.debug("debug log")
logger.info("info log")
logger.warning("warn log")
"""
ROOT_TAG = 'studio'
LOGGER_TAG = 'studio.core'


class _LoggerContext:
    INDENT_SIZE = 4

    def __init__(self):
        self._indent_level = 0

    def increase_indent(self):
        self._indent_level += 1

    def decrease_indent(self):
        if self._indent_level <= 0:
            raise ValueError(f"Log indent level is currently {self._indent_level}, cannot be decreased.")
        self._indent_level -= 1

    @property
    def prefix_indent_str(self):
        return ('|' + ' ' * (self.INDENT_SIZE-1)) * self._indent_level


class ExceptionFormatter:
    def format(self, exc_info):
        return '\n'.join(self._formatted_chain_lines(exc_info))

    def _exceptions(self, exc_info):
        exc, value, trace_back = exc_info
        cause = value.__cause__
        if cause is not None:
            cause_exc_info = type(cause), cause, cause.__traceback__
            yield from self._exceptions(cause_exc_info)
        yield exc_info

    def _frames(self, trace_back):
        return StackSummary.extract(walk_tb(trace_back), capture_locals=True)

    def _formatted_chain_lines(self, exc_info):
        for index, exc in enumerate(self._exceptions(exc_info)):
            if index > 0:
                yield '\nThe above exception was the direct cause of the following exception:\n'
            yield from self._formatted_exception_lines(exc)

    def _formatted_exception_lines(self, exc_info):
        exc_type, exc_value, trace_back = exc_info
        yield 'Traceback (most recent call last):'
        for frame in self._frames(trace_back):
            yield from self._formatted_frame_lines(frame)
            yield ''
        yield f'  {exc_type.__name__}: {exc_value}'

    def _formatted_frame_lines(self, frame):
        from azureml.studio.core.utils.strutils import truncate_lines, indent_block
        yield f'  File "{frame.filename}", line {frame.lineno}, in {frame.name}'
        code = frame.line
        if code:
            yield f'    {code}'
            for var_name in self._get_var_names(code):
                if frame.locals is not None and var_name in frame.locals:
                    # `frame.locals`'s values comes from each local variable's `__repr__` method,
                    # which sometimes get too long (say, `DataFrame` will print the contents),
                    # so we truncate them to limited lines if needed.
                    #
                    # Also, generally `__repr__` will escape '\n' as '\\n' by default.
                    # so we must do the un-escape first to perform correct truncation.
                    #
                    # >>> a = """first
                    # ... second"""
                    # >>> a
                    # 'first\nsecond'
                    # >>> str(a)
                    # 'first\nsecond'
                    # >>> repr(a)
                    # "'first\\nsecond'"
                    # >>> repr(a).encode()
                    # b"'first\\nsecond'"
                    # >>> repr(a).encode('utf8')
                    # b"'first\\nsecond'"
                    # >>> repr(a).encode('utf8').decode('utf8')
                    # "'first\\nsecond'"
                    # >>> repr(a).encode('utf8').decode('unicode-escape')
                    # "'first\nsecond'"
                    raw_var_value = frame.locals.get(var_name)
                    unescaped = raw_var_value.encode('utf8').decode('unicode_escape')
                    var_value = truncate_lines(unescaped, max_line_count=5, max_line_length=500)

                    # format the lines to be easy to read
                    value_block = f'{var_name} = {var_value}'
                    first_prefix = f'      > '
                    subsequent_prefix = f'      | ' + (' ' * (len(var_name) + 4))
                    formatted = indent_block(value_block, prefix=first_prefix, subsequent_prefix=subsequent_prefix)
                    yield formatted

    @staticmethod
    def _get_var_names(code):
        try:
            tree = ast.parse(code, mode='exec')
            for node in ast.walk(tree):
                if getattr(node, 'id', None):
                    yield node.id
        except SyntaxError:
            pass


logger_context = _LoggerContext()


class LogFormatter(logging.Formatter):
    def __init__(self):
        super().__init__('%(asctime)s %(name)-20s %(levelname)-10s %(message)s')

    def formatException(self, exc_info):
        try:
            return ExceptionFormatter().format(exc_info)
        except Exception:
            # Add exception try-except due to bug 1152696. The case is ExceptionFormatter can fail in some corner
            # cases, so falls back to logging.Formatter.formatException.
            return super().formatException(exc_info)

    def format(self, record):
        original = record.msg
        record.msg = f"{logger_context.prefix_indent_str}{record.msg}"
        result = super().format(record)
        # Make sure the msg is recovered, otherwise the parent loggers give wrong indents.
        record.msg = original
        return result


class LogHandler(logging.StreamHandler):
    def __init__(self, stream=sys.stdout):
        super().__init__(stream)
        self.setFormatter(LogFormatter())


# Use basicConfig instead of logger.addHandler to avoid the influence of the basicConfig called in other packages.
logging.basicConfig(handlers=[LogHandler()])
root_logger = logging.getLogger(ROOT_TAG)
logger = logging.getLogger(LOGGER_TAG)


def get_logger(name=None):
    """Gets an instance of logger with namespace 'studio.'.

    e.g. get_logger('module') will return a logger with tag 'studio.module'.
    """
    if not name:
        return root_logger

    if not re.match(pattern=r'[a-z]+', string=name):
        raise ValueError(f"Invalid log name '{name}'. Should only contains lowercase letters.")

    return logging.getLogger(f"{ROOT_TAG}.{name}")


# TODO: for backward compatibility, to be removed
module_host_logger = get_logger('modulehost')
module_logger = get_logger('module')
common_logger = get_logger('common')


def set_root_logger_level(level):
    root_logger.setLevel(level)


# Set default logger level to DEBUG
set_root_logger_level(logging.DEBUG)


class TimeProfile:
    def __init__(self, tag, logger=logger):
        self.tag = tag
        self.logger = logger

    def __enter__(self):
        self.logger.info(f"{self.tag} - Start:")
        self.start_time = time.perf_counter()
        logger_context.increase_indent()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.perf_counter()
        elapsed_time = end_time - self.start_time
        logger_context.decrease_indent()
        self.logger.info(f"{self.tag} - End with {elapsed_time:.4f}s elapsed.")


def time_profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with TimeProfile(f"{func.__qualname__}", logger):
            ret = func(*args, **kwargs)
        return ret
    return wrapper


@contextmanager
def indented_logging_block():
    logger_context.increase_indent()
    yield
    logger_context.decrease_indent()


class _TruncatedLogValue:
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        # Pass obj directly if it is str to avoid introducing extra symbols
        obj_repr = self.obj if isinstance(self.obj, str) else self.obj.__repr__()
        return truncate_lines(obj_repr, max_line_count=5, max_line_length=500)


def log_dict_values(name, obj: dict, key_filter=None, truncate_long_item_text=False):
    if key_filter is not None:
        obj = {k: v for k, v in obj.items() if key_filter(k)}

    logger.debug(f"{name}:")
    with indented_logging_block():
        if not obj:
            logger.debug(f"(empty)")
            return
        for name, value in obj.items():
            if truncate_long_item_text:
                value = _TruncatedLogValue(value)
            logger.debug(f"{name} = {value}")


def log_list_values(name, obj: Union[list, tuple], truncate_long_item_text=False):
    logger.debug(f"{name}:")
    with indented_logging_block():
        if not obj:
            logger.debug(f"(empty)")
            return
        for index, value in enumerate(obj):
            if truncate_long_item_text:
                value = _TruncatedLogValue(value)
            logger.debug(f"[{index}] = {value}")
