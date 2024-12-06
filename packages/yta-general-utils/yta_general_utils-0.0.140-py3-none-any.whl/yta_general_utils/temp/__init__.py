from yta_general_utils.file.remover import FileRemover
from yta_general_utils.programming.path import get_project_abspath
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.programming.env import get_current_project_env
from random import randint
from datetime import datetime

import os


def initialize():
    """
    This method loads the current project dotenv ('.env' file in
    root folder), looks for a 'WIP_FOLDER' variable definition 
    in that file and, if not defined, sets it as the default
    'yta_wip' value and creatis the folder if it doesn't exist.

    This method is to ensure that there is a temporary folder to
    work with and available since the begining.
    """
    WIP_FOLDER = get_current_project_env('WIP_FOLDER')
    if not WIP_FOLDER:
        # We force creating the dir
        WIP_FOLDER = get_project_abspath() + 'yta_wip/'
        if not FileValidator.is_folder(WIP_FOLDER):
            os.mkdir(WIP_FOLDER)

    return WIP_FOLDER

WIP_FOLDER = initialize()

def get_temp_filename(filename):
    """
    Receives a 'filename' and turns it into a temporary filename that is
    returned including a random suffix datetime related.

    This method uses the current datetime and a random integer number to
    be unique.

    If you provide 'file.wav' it will return something like 
    'file_202406212425.wav'.
    """
    delta = (datetime.now() - datetime(1970, 1, 1))
    aux = filename.split('.')

    return aux[0] + '_' + str(int(delta.total_seconds())) + str(randint(0, 10000)) + '.' + aux[1]

def create_temp_filename(filename):
    """
    Returns a temporary file name that includes the 'WIP_FOLDER'
    set in environment variable and also a random and datetime
    related suffix.

    The WIP (Work In Progress) folder will be set to 'yta_wip'
    if not found in .env.

    If you provide 'file.wav' it will return something like 
    '$WIP/file_202406212425.wav'.
    """
    # TODO: Rename this as it uses wip and we do not mention it
    # TODO: Issue if no extension provided
    return create_custom_temp_filename(get_temp_filename(filename))

# TODO: Maybe rename this methods...
def create_custom_temp_filename(filename):
    """
    Returns a new 'filename' that includes the 'WIP_FOLDER' but
    preserves the original name. This is for using the temporary
    folder but without any internal logic.

    The WIP (Work In Progress) folder will be set to 'yta_wip'
    if not found in .env.
    """
    return WIP_FOLDER + filename

def clean_temp_folder():
    """
    Removes all the existing files in the temporary folder. This folder is
    the one set in the environment 'WIP_FOLDER' variable.

    The WIP (Work In Progress) folder will be set to 'yta_wip'
    if not found in .env.
    """
    FileRemover.delete_files(WIP_FOLDER)