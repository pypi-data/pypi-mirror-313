import inspect


# TODO: This whole file has to be reviewed and refactored
# or maybe removed due to new PythonValidator, NumberValidator
# etc.
def code_file_is(parameter, filename):
    """
    Checks if the provided 'parameter' code is contained in the also
    provided 'filename'. This method is useful to check Enum objects
    or classes as we know the name we use for the files.

    This method was created to be able to check if a function that
    was passed as parameter was part of a custom Enum we created
    and so we could validate the was actually that custom Enum.
    Working with classes was not returning the custom Enum class
    created, so we needed this.
    """
    # TODO: Is this useful or needed (?)
    if inspect.getfile(parameter).endswith(filename):
        return True
    
    return False