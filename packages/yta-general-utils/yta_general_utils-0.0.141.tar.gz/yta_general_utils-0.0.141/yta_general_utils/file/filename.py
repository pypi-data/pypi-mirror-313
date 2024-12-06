from yta_general_utils.file.enums import FileType
from moviepy import VideoFileClip, AudioFileClip

import os


def sanitize_filename(filename: str):
    """
    This method checks the provided 'filename' and turns any 
    backslash character into a '/' (slash) one, returning the
    new string.
    """
    if '\\' in filename:
        filename = filename.replace('\\', '/')

    return filename

def get_filename(filename):
    """
    This method returns the filename, avoiding the path, of
    the provided 'filename'. This method includes the extension
    if existing.
    """
    aux = sanitize_filename(filename).split('/')

    return aux[len(aux) - 1]

def filename_is_type(filename: str, type: FileType):
    """
    Checks if the provided 'filename' is a valid filename and if 
    its type is the given 'type' or not (based on the extension).
    This method will return True if the 'filename' is valid and
    belongs to the provided 'type', or False if not. It wil raise
    a Exception if something is bad formatted or missing.
    """
    if not filename:
        raise Exception('No "filename" provided.')
    
    if not isinstance(filename, str):
        raise Exception('The "filename" provided is not a str.')

    type = FileType.to_enum(type)
    
    extension = get_file_extension(filename)
    if not extension:
        raise Exception('Provided "filename" has no valid extension to be checked.')
    
    return type.is_accepted_value(extension)

# TODO: Rename these methods below to 'filename' instead of 'file'
# TODO: Implement the use of our RegularExpression enums
def file_is_type(filename: str, type: FileType):
    """
    Checks if the provided 'filename' is a valid filename and if 
    its type is the given 'type' or not (based on the extension).
    This method will return True if the 'filename' is valid, 
    belongs to the provided 'type' and is a valid file (it will
    be checked by trying to instantiate the file as real), or 
    False if not. It wil raise an Exception if something is bad 
    formatted or missing.
    """
    if not filename:
        raise Exception('No "filename" provided.')
    
    if not isinstance(filename, str):
        raise Exception('The "filename" provided is not a str.')

    type = FileType.to_enum(type)
    
    extension = get_file_extension(filename)
    if not extension:
        raise Exception('Provided "filename" has no valid extension to be checked.')
    
    if not filename_is_type(filename, type):
        return False
    
    # TODO: I should do this with another library to
    # avoid 'moviepy' dependency
    if type == FileType.VIDEO:
        try: 
            VideoFileClip(filename)
        except:
            return False
    elif type == FileType.AUDIO:
        try:
            AudioFileClip(filename)
        except:
            return False
        
# TODO: Maybe move this below to a 'file_checker.py'?
def file_has_extension(filename):
    if get_file_extension(filename):
        return True
    
    return False

def ensure_file_extension(filename: str, extension: str):
    """
    This method returns the provided 'filename' with the
    also provided 'extension', making sure that this
    extension is used in the filename.

    This method is useful when you need a file to have an
    specific extension.
    """
    # TODO: Please, improve this method...
    if extension is None or not isinstance(extension, str) or not extension:
        raise Exception('No valid "extension" provided.')
    
    if '.' in extension:
        extension = extension.replace('.', '')

    # TODO: Ensure extension is a valid file extension
    filename_extension = get_file_extension(filename)
    if not filename_extension:
        filename += f'.{extension}'
    elif filename_extension != extension:
        filename = replace_file_extension(filename, extension)

    return filename

def get_file_extension(filename: str):
    """
    Returns the extension of the provided 'filename' that
    doesn't include the '.'.

    If you provide '.png' as 'filename' it will return
    a False. If the filename has no extension, it will 
    return None.
    """
    # TODO: Is this (https://stackoverflow.com/a/49689414) better (?)
    filename, ext = os.path.splitext(filename)

    if '.' in ext:
        ext = ext.replace('.', '')

    return ext

def replace_file_extension(filename: str, extension: str):
    """
    Replaces the original 'filename' extension with the provided
    'extension'.
    """
    # TODO: Improve this code below by raising exceptions
    if not filename:
        return None
    
    if not extension:
        return None
    
    if not '.' in extension:
        extension = '.' + extension

    root, ext = os.path.splitext(extension)
    
    if root and ext:
        # Provided 'extension' is not valid
        return None

    root, ext = os.path.splitext(filename)
    
    return root + extension

def get_file_filename_without_extension(filename: str):
    """
    This method receives a full 'filename' that could be
    an absolute or relative path (including slashes) and
    returns only the filename part (excluding the
    extension and path).

    (!) Passing '.png' or similar as 'filename' parameter
    will fail.

    TODO: Maybe check this condition above (?) but what
    about '.gitignore' file?
    """
    if not filename:
        return None
    
    filename = get_filename(filename)
    filename, ext = os.path.splitext(filename)

    return filename