from yta_general_utils.downloader.utils import download_file
from yta_general_utils.file.filename import filename_is_type, replace_file_extension
from yta_general_utils.file.enums import FileType


def download_video(url, output_filename: str):
    """
    Receives a downloadable url as 'url' and downloads that video in
    our system as 'output_filename'.
    """
    # TODO: Check if url is a valid audio or not
    if not filename_is_type(output_filename, FileType.VIDEO):
        output_filename = replace_file_extension(output_filename, '.mp4')

    return download_file(url, output_filename)