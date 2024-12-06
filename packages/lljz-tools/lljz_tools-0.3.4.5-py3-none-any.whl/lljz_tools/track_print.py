# coding=utf-8
import logging
import sys
import traceback

from .log_manager import LogManager

print_raw = print

__print = LogManager(
    'print', console_level='INFO', file_path="/python_print",
    fmt='{asctime} | {name} | {module}:{funcName}:{lineno} - {message}'
).get_logger()


def track_print(*args, sep=' ', end='\n', file=None, flush=False):  # noqa
    __print.info(sep.join(map(str, args)), stacklevel=2)


def patch_print():
    try:
        __builtins__.print = track_print
    except AttributeError:
        __builtins__['print'] = track_print


def restore_print():
    try:
        __builtins__.print = print_raw
    except AttributeError:
        __builtins__['print'] = print_raw


patch_print()


def __traceback_exception_print(self, *, file=None, chain=True):
    """Print the result of self.format(chain=chain) to 'file'."""

    if file is None:
        file = sys.stderr
    for line in self.format(chain=chain):
        print_raw(line, file=file, end="")


def __print_list(extracted_list, file=None):
    """Print the list of tuples as returned by extract_tb() or
    extract_stack() as a formatted stack trace to the given file."""
    if file is None:
        file = sys.stderr
    for item in traceback.StackSummary.from_list(extracted_list).format():
        print_raw(item, file=file, end="")


traceback.TracebackException.print = __traceback_exception_print
traceback.print_list = __print_list


def disable_print():
    __logger = LogManager('print').get_logger()
    __logger.setLevel(logging.ERROR)


if __name__ == '__main__':
    def add():
        print('Hello World!')


    # disable_print()
    add()
