import sys
import logging
import inspect
import pandas as pd


class IndentFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)
        self._indent_baseline = len(inspect.stack()) + 2

    def format(self, record):
        stack = inspect.stack()
        record.indent = '.' * (len(stack) - self._indent_baseline)
        out = logging.Formatter.format(self, record)
        del record.indent
        return out


custom_module_logger = logging.getLogger("CustomModule")
if not custom_module_logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(IndentFormatter(
        "%(asctime)s [%(module)20s] [%(levelname)8s] %(indent)s[%(funcName)s] %(message)s"))
    custom_module_logger.addHandler(handler)
    custom_module_logger.setLevel(logging.DEBUG)
    custom_module_logger.propagate = 0


def format_obj(name: str, value):
    if value is None:
        return f"[{name}]: None"
    if isinstance(value, dict):
        result = f"{name}:\n"
        for key, value in value.items():
            result = result + f"\t{key} = {value}\n"
        return result
    if isinstance(value, pd.DataFrame) or isinstance(value, pd.Series):
        return '\n' + '-' * 50 + \
            f"\n[{name}]:\n(value):\n{value}\n" + '-' * 20 + f"\n(dtypes):\n{value.dtypes}\n" + '-' * 20
    return f"\"{name}\": {value}"
