"""
    TODO: This could be mixed with the 'filename' functionality
    as it is similar but we treat it as paths and filenames while
    they are the same (a filename is a relative path)
"""
from yta_general_utils.file.filename import sanitize_filename
from pathlib import Path


def get_abspath_parent_folder(abspath, levels = 1):
    """
    Iterates over the provided 'abspath' and goes to the parent
    folder that is 'levels' levels above. This method will
    return the new abspath sanitized and ended in '/'.
    """
    # TODO: Handle when 'levels' is greater than possible
    import os.path

    if levels <= 0:
        return abspath

    for i in range(levels):
        abspath = os.path.dirname(abspath)

    return sanitize_filename(abspath) + '/'

def create_file_abspath(file_abspath: str):
    """
    This method will create the folders needed to be able to
    create the provided 'file_abspath'. This will create
    all the folders until reaching the file level.

    @param
        **file_abspath**
        File absolute path that we need to be able to work with
        that file. This must include filename and extension.
    """
    if not file_abspath or not ':/' in file_abspath or file_abspath.endswith('/'):
        raise Exception('No valid absolute path provided.')

    Path(get_abspath_parent_folder(file_abspath)).mkdir(parents = True, exist_ok = True)

    return file_abspath

def is_abspath(filename: str):
    """
    Checks if the provided 'filename' is an absolute path or not,
    returning True if yes or False if not.
    """
    # TODO: Please, improve this with a library or something
    # Check this: https://stackoverflow.com/questions/3320406/how-to-check-if-a-path-is-absolute-path-or-relative-path-in-a-cross-platform-way
    return ':\\' in filename or ':/' in filename
