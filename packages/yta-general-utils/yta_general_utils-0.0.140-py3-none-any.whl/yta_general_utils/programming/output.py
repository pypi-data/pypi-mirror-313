from yta_general_utils.file.filename import ensure_file_extension, file_has_extension, get_file_extension
from yta_general_utils.file.enums import FileType, AudioFileExtension, VideoFileExtension, ImageFileExtension
from yta_general_utils.temp import create_temp_filename
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.programming.enum import YTAEnum as Enum
from typing import Union


def handle_output_filename(output_filename: Union[None, str], expected_extension: Union[None, AudioFileExtension, VideoFileExtension, ImageFileExtension, FileType] = None):
    """
    Handle the provided 'output_filename' to ensure that it is the
    expected for our system. We could want to write a file or to not
    write it, and we need to make sure the extension is the expected
    one.

    This method should be called within any method that is capable
    to write (mandatory or optional) a filename locally.

    This method will return None when no file writting expected or
    the expected filename when you do want to write.
    """
    if not expected_extension and not output_filename:
        return None
    
    if expected_extension:
        # TODO: Remove this explanation below in a near future
        # When validating types based on Enum items, we can receive
        # the Enum class or an Enum instance. If we receive the Enum class
        # we will be able to choose any of the existing Enum items. If we
        # receive the instance, we will only be able to accept the value
        # of that Enum. If we receive a string and we accept it, we will
        # try to convert it to our accepted Enum classes and, if found,
        # convert to the corresponding instance to work as if the instance
        # was the passed parameter
        if not PythonValidator.is_string(expected_extension) and not PythonValidator.is_class(expected_extension, AudioFileExtension) and not PythonValidator.is_instance(expected_extension, AudioFileExtension) and not PythonValidator.is_class(expected_extension, ImageFileExtension) and not PythonValidator.is_instance(expected_extension, ImageFileExtension) and not PythonValidator.is_class(expected_extension, VideoFileExtension) and not PythonValidator.is_instance(expected_extension, VideoFileExtension):
            raise Exception(f'The provided parameter "expected_extension" is not valid.')
        
        if PythonValidator.is_string(expected_extension):
            expected_extension = Enum.parse_as_enum(expected_extension, [AudioFileExtension, ImageFileExtension, VideoFileExtension])

        # Here 'expected_extension' is a YTAEnum class or instance

    if output_filename is not None and not PythonValidator.is_string(output_filename):
        raise Exception(f'The provided "output_filename" parameter "{str(output_filename)}" is not a string.')
   
    # We don't accept 'output_filename' without extension
    if not expected_extension and not file_has_extension(output_filename):
        raise Exception(f'The provided "output_filename" parameter "{str(output_filename)}" has no valid extension and there is no "expected_extension" parameter provided.')
    
    if expected_extension:
        if PythonValidator.is_a_class(expected_extension):
            # A class, I can accept any of the Enum item values
            default_exception = expected_extension.default().value
            accepted_extensions = expected_extension.get_all_values()
        elif PythonValidator.is_an_instance(expected_extension):
            # An instance, I can only accept that Enum instance value
            default_exception = expected_extension.value
            accepted_extensions = [expected_extension.value]

        if output_filename:
            extension = get_file_extension(output_filename)
            if extension not in accepted_extensions:
                output_filename = ensure_file_extension(output_filename, default_exception)
        else:
            output_filename = create_temp_filename(f'tmp_filename.{default_exception}')

    # TODO: Maybe check if output_filename has no extension to
    # raise Exception if that happens (?)
    return output_filename