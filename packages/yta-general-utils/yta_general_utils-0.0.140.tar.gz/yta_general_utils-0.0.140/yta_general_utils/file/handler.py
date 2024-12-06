# TODO: Find a more specific and better way of classifying these
# files and methods. I moved here to avoid using __init__.py

from yta_general_utils.file.filename import sanitize_filename
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.programming.enum import YTAEnum as Enum
from shutil import move as shutil_move, copyfile as shutil_copyfile

import glob


class FileSearchOption(Enum):
    """
    Enum that allows us setting the strategy dynamically when 
    searching for files.
    """
    FILES_AND_FOLDERS = 'fifo'
    """
    This option, when set, will return files and folders.
    """
    FILES_ONLY = 'fi'
    """
    This option, when set, will return files only.
    """
    FOLDERS_ONLY = 'fo'
    """
    This option, when set, will return folders only.
    """

class FileHandler:
    @staticmethod
    def get_list(abspath, option: FileSearchOption = FileSearchOption.FILES_AND_FOLDERS, pattern: str = '*', recursive: bool = False):
        """
        List what is inside the provided 'abspath'. This method will list files and
        folders, files or only folders attending to the provided 'option'. It will
        also filter the files/folders that fit the provided 'pattern' (you can use
        '*' as wildcard, so for example '*.jpg' will list all images). This method
        can also be used in a recursive way if 'recursive' parameter is True, but
        take care of memory consumption and it would take its time to perform.

        This method returns a list with all existing elements absolute paths 
        sanitized.
        """
        if not abspath:
            return None
        
        abspath = sanitize_filename(abspath)
        list = []

        # This below get files and folders
        files_and_folders = [sanitize_filename(f) for f in glob.glob(pathname = abspath + pattern, recursive = recursive)]

        if option == FileSearchOption.FILES_ONLY:
            for f in files_and_folders:
                if FileValidator.is_file(f):
                    list.append(f)
        elif option == FileSearchOption.FOLDERS_ONLY:
            for f in files_and_folders:
                if FileValidator.is_folder(f):
                    list.append(f)
        elif option == FileSearchOption.FILES_AND_FOLDERS:
            list = files_and_folders
        
        return list

    @staticmethod
    def rename_file(origin_filename: str, destination_filename: str, replace_if_existing: bool = False):
        """
        Renames the 'origin_filename' to the 'destination_filename'.
        If 'replace_if_existing' is True, it will replace the destination
        file if possible and allowed. If it is False, it will fail.

        TODO: Remove 'replace_if_existing' if not used.
        """
        if not origin_filename:
            return None
        
        if not destination_filename:
            return None
        
        shutil_move(origin_filename, destination_filename)

    @staticmethod
    def copy_file(origin_filename: str, destination_filename: str):
        """
        Makes a copy of the provided 'origin_filename' and 
        stores it as 'destination_filename'.

        The destination folder must exist.
        """
        if not origin_filename:
            return None

        if not destination_filename:
            return None

        shutil_copyfile(origin_filename, destination_filename)