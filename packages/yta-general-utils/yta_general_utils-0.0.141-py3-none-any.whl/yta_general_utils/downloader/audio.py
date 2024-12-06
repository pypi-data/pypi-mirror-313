from yta_general_utils.downloader.utils import download_file
from yta_general_utils.file.filename import filename_is_type, replace_file_extension
from yta_general_utils.file.enums import FileType


def download_audio(url: str, output_filename: str):
    """
    Receives a downloadable url as 'url' and downloads that audio in
    our system as 'output_filename'. The 'output_filename' can be 
    changed to a valid audio filename if it is wrong.

    This method will return the final 'output_filename' in which the
    file has been downloaded if so.
    """
    # TODO: Check if url is a valid audio or not
    if not filename_is_type(output_filename, FileType.AUDIO):
        output_filename = replace_file_extension(output_filename, '.mp3')

    return download_file(url, output_filename)