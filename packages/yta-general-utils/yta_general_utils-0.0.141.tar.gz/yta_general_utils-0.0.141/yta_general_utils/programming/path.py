from yta_general_utils.file.filename import sanitize_filename, get_filename
from yta_general_utils.path import get_abspath_parent_folder

import inspect
import sys
import os


def get_code_abspath(code):
    """
    Returns the abspath of the file in which the code is written.
    The 'code' parameter must be a module, class, method, function,
    traceback, frame or code object to be correctly inspected.
    """
    return sanitize_filename(inspect.getfile(code))

def get_code_filename(code):
    """
    Returns the filename in which the code is written. The 'code' 
    parameter must be a module, class, method, function, traceback, 
    frame or code object to be correctly inspected.

    This method will include the filename with the extension.
    """
    return get_filename(inspect.getfile(code))

def get_project_abspath():
    """
    Returns the absolute path of the current project (the
    one that is being executed and using this library.

    The absolute path returned ends in '/' and has been
    sanitized.
    """
    return sanitize_filename(os.getcwd()) + '/'

def get_current_file_abspath(parent_levels: int = 0):
    """
    Returns the absolute path of the file that is currently
    being executed (in which the code is written). If 
    'parent_levels' provided, it will return the abspath
    to the parent folder that corresponds to the level
    requested.

    The absolute path is returned ending in '/' and has
    been sanitized.
    """
    abspath = sanitize_filename(os.path.dirname(os.path.abspath(sys.argv[0])))

    if parent_levels > 0:
        abspath = get_abspath_parent_folder(abspath, parent_levels)
    else:
        abspath += '/'

    return abspath