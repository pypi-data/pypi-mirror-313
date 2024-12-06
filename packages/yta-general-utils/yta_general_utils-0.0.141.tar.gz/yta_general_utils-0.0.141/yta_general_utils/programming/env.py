from yta_general_utils.programming.path import get_project_abspath
from dotenv import load_dotenv

import os


# TODO: Create a Environment class to wrap maybe (?)
def load_current_project_dotenv():
    """
    This methods looks for the '.env' file in the project that is
    currently being executed (the code, not the library) and loads
    it.

    This means that any project in which you are importing this 
    library, the '.env' file in its main folder will be loaded.
    """
    dotenv_path = os.path.join(get_project_abspath(), '.env')
    load_dotenv(dotenv_path)

def get_current_project_env(variable: str):
    """
    Loads the current project environment '.env' configuration file
    and returns, if available, the 'variable' variable value.

    This method does a 'load_dotenv' method call within the current
    project absolute path any time you call it, so it ensures 
    loading the values correctly if available.
    
    You can use directly this method instead of 'os.getenv()'
    without using any 'load_dotenv()' method before because it is 
    implicitely called within the current project.
    """
    load_current_project_dotenv()

    return os.getenv(variable)
