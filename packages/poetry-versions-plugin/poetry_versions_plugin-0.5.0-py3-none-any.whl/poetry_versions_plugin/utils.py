import inspect
import re
from functools import wraps

from cleo.io.outputs.output import Verbosity
from poetry_versions_plugin import PLUGIN_NAME


def pyproject_get(pyproject, path, default=None):
    """
    Retrieve a value from a nested dictionary using a dot-separated key path.

    :param pyproject: The pyproject dictionary to search.
    :param path: The dot-separated key path, e.g., 'tool.versions.settings.allow_dirty'.
    :param default: The default value to return if the path is not found.
    :return: The value found at the path, or the default value.
    """

    # Regular expression to split on dots, but ignore dots within quotes
    pattern = r'\.(?=(?:[^"]*"[^"]*")*[^"]*$)'
    keys = re.split(pattern, path)

    current = pyproject.data

    try:
        for key in keys:
            # Strip quotes from the key if they exist
            if key.startswith('"') and key.endswith('"'):
                key = key[1:-1]

            current = current[key]

        return current
    except (KeyError, TypeError):
        return default


def wrap_write_line(func):
    @wraps(func)
    def wrapper(self, event, event_name, dispatcher):
        # Define a helper function to simplify the write_line operation
        def write_line(message, verbosity: Verbosity = Verbosity.VERBOSE):
            io = event.io

            if verbosity == Verbosity.VERBOSE:
                # Dynamically get the caller function's name
                caller_function_name = inspect.stack()[1].function
                full_message = f'<b>{PLUGIN_NAME}</b>: {caller_function_name} {event_name} {message}'
                io.write_line(full_message, verbosity)
            else:
                full_message = f'<b>{PLUGIN_NAME}</b>: {message}'
                io.write_line(full_message, verbosity)

        # Inject the simplified write_line into the function's local scope
        func_globals = func.__globals__
        original_write_line = func_globals.get('write_line')
        func_globals['write_line'] = write_line

        try:
            return func(self, event, event_name, dispatcher)
        finally:
            # Restore the original write_line function, if any
            if original_write_line is not None:
                func_globals['write_line'] = original_write_line
            else:
                del func_globals['write_line']

    return wrapper
