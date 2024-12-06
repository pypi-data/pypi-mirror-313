from yta_general_utils.file.filename import replace_file_extension, get_file_extension
from yta_general_utils.file.writer import FileWriter
from yta_general_utils.temp import create_temp_filename
from lxml.html import fromstring

import requests


# TODO: Move to a 'consts.py' (?)
DRIVE_RESOURCE_URL_START = 'https://drive.google.com/file/d/'
DOWNLOAD_URL = 'https://docs.google.com/uc?export=download&confirm=1'

class GoogleDriveResource:
    """
    Class to handle Google Drive Resources. Just instantiate it with its
    Google Drive url and it will be ready for download if the url is valid
    and available.

    A valid 'drive_url' must be like this:
    https://drive.google.com/file/d/1rcowE61X8c832ynh0xOt60TH1rJfcJ6z/view?usp=sharing&confirm=1
    """
    url: str = ''
    filename: str = ''
    id: str = ''

    def __init__(self, drive_url: str):
        """
        Initializes this instance and sets the 'url', the real 'filename'
        obtained from Google Drive and also the 'id' obtained from the url.
        """
        self.url = self.parse_url(drive_url)
        self.filename = self.get_filename(self.url)
        self.id = self.get_id(self.url)

    def download(self, output_filename: str = None):
        """
        Downloads the Google Drive Resource to the provided 'output_filename'.
        If not 'output_filename' parameter provided, the system will generate
        a temporary file. The downloaded file filename will be returned.
        """
        return self._download_resource(self.id, self.filename, output_filename)

    @classmethod
    def parse_url(cls, drive_url: str):
        """
        This method validates if the provided 'drive_url' is a valid
        Google Drive url and returns it if valid or raises an Exception
        if invalid.
        """
        drive_url = drive_url.replace('http://', 'https://')

        if not drive_url.startswith('https://'):
            drive_url = f'https://{drive_url}'

        if not drive_url.startswith(DRIVE_RESOURCE_URL_START):
            raise Exception(f'Provided "google_drive_url" parameter {drive_url} is not valid. It must be like "{DRIVE_RESOURCE_URL_START}..."')
    
        if not 'confirm=t' in drive_url:
            # previously was '&confirm=1' to avoid virus scan as they say:
            # https://github.com/tensorflow/datasets/issues/3935#issuecomment-2067094366
            drive_url += '&confirm=t'

        return drive_url

    @classmethod
    def is_url_available(cls, drive_url: str):
        """
        This method validates if the provided 'drive_url' is available
        for access and download.
        """
        # TODO: Check somehow that url is available or raise Exception if not
        return True
        drive_file_name = fromstring(requests.get(drive_url).content).findtext('.//title').split('-')[0].strip()

    @classmethod
    def get_id(cls, drive_url: str):
        """
        Parses the 'drive_url' and returns the Google Drive Resource id
        if url is valid.
        """
        drive_url = cls.parse_url(drive_url)

        return drive_url.replace(DRIVE_RESOURCE_URL_START, '').split('/')[0]

    @classmethod
    def get_filename(cls, drive_url: str):
        """
        Parses the 'drive_url' and returns the Google Drive Resource 
        filename if url is valid. This is the real filename in Google
        Drive.
        """
        drive_url = cls.parse_url(drive_url)

        return fromstring(requests.get(drive_url).content).findtext('.//title').split('-')[0].strip()

    @classmethod
    def download_from_url(cls, drive_url: str, output_filename: str = None):
        drive_url = cls.parse_url(drive_url)
        id = cls.get_id(drive_url)
        filename = cls.get_filename(drive_url)

        return cls._download_resource(id, filename, output_filename)
    
    @classmethod
    def _download_resource(cls, id: str, filename: str, output_filename: str = None):
        session = requests.Session()
        # Trying to obtain the web title to get the file name
        response = session.get(DOWNLOAD_URL, params = {'id': id}, stream = True)

        # Look for a token to be able to download
        token = None
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                token = value
                break

        if token:
            params = {'id': id, 'confirm': token}
            response = session.get(DOWNLOAD_URL, params = params, stream = True)
            # TODO: Handle virus unchecked Google warning that contains this below:
            # <title>Google Drive - Virus scan warning</title>
            # check Notion for the entire error message

        if not output_filename:
            # This extension will be replaced instantly after this line
            output_filename = create_temp_filename('tmp_googledrive.mp4')

        # We make sure the output extension fits the real one
        output_filename = replace_file_extension(output_filename, get_file_extension(filename))

        # Save response
        FileWriter.write_file_by_chunks_from_response(response, output_filename)

        return output_filename

    
    
    
        
# TODO: Remove these methods below when GoogleDriveResource working
def download_file_from_google_drive(drive_url: str, output_filename: str = None):
    """
    @deprecated 
    Downloads a file from a given Google Drive url that must be
    generated by sharing the file and making it public (this
    means anyone can view and download it).

    The file will be stored locally as 'output_filename', but 
    the extension could be changed if the provided one is
    different than the one that the Google Drive file has.
    This final created file name will be returned.

    A valid 'drive_url' must be like this:
    https://drive.google.com/file/d/1rcowE61X8c832ynh0xOt60TH1rJfcJ6z/view?usp=sharing&confirm=1
    """
    # TODO: Check if drive_url is valid and downloadable (regex?)

    # This is to avoid virus scan
    if not 'confirm=t' in drive_url:
        # previously was '&confirm=1' to avoid virus scan as they say:
        # https://github.com/tensorflow/datasets/issues/3935#issuecomment-2067094366
        drive_url += '&confirm=t'

    # Lets get file id and file name
    drive_file_id = drive_url.replace('https://drive.google.com/file/d/', '').split('/')[0]
    # We fire a simple get request to obtain file name from url title
    drive_file_name = fromstring(requests.get(drive_url).content).findtext('.//title').split('-')[0].strip()

    DOWNLOAD_URL = "https://docs.google.com/uc?export=download&confirm=1"

     # Lets download the file
    session = requests.Session()
    
    # Trying to obtain the web title to get the file name
    response = session.get(DOWNLOAD_URL, params = {'id': drive_file_id}, stream = True)

    # Look for a token to be able to download
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break

    if token:
        params = {'id': drive_file_id, 'confirm': token}
        response = session.get(DOWNLOAD_URL, params = params, stream = True)
        # TODO: Handle virus unchecked Google warning that contains this below:
        # <title>Google Drive - Virus scan warning</title>
        # check Notion for the entire error message

    if not output_filename:
        # This extension will be replaced instantly after this line
        output_filename = create_temp_filename('tmp_googledrive.mp4')

    # We make sure the output extension fits the real one
    output_filename = replace_file_extension(output_filename, get_file_extension(drive_file_name))

    # Save response
    FileWriter.write_file_by_chunks_from_response(response, output_filename)

    return output_filename

# TODO: Move this to another file
def get_id_from_google_drive_url(google_drive_url: str):
    """
    @deprecated
    This method obtains the Google Drive element id and returns it if
    the provided 'google_drive_url' is valid.
    """
    if not google_drive_url:
        return None
    
    # url should be like: https://drive.google.com/file/d/1My5V8gKcXDQGGKB9ARAsuP9MIJm0DQOK/view?usp=sharing&confirm=1
    if not google_drive_url.startswith('https://drive.google.com/file/d/'):
        raise Exception(f'Provided "google_drive_url" parameter {google_drive_url} is not valid. It must be like "https://drive.google.com/file/d/..."')

    google_drive_url = google_drive_url.replace('https://drive.google.com/file/d/', '')

    if '/' in google_drive_url:
        google_drive_url = google_drive_url.split('/')[0]

    return google_drive_url
