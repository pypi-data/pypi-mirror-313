#from yta_general_utils.programming.parameter_validator import ParameterValidator
from yta_general_utils.programming.output import handle_output_filename
from yta_general_utils.downloader.audio import download_audio
from yta_general_utils.downloader.gif import download_gif
from yta_general_utils.downloader.google_drive import GoogleDriveResource
from yta_general_utils.downloader.image import download_image
from yta_general_utils.downloader.video import download_video


# TODO: Make all submethods return the element read (image as Pillow,
# video as VideoFileClip or numpy, etc. and also the filename
class Downloader:
    """
    Class to encapsulate the functionality related to download resources
    from the Internet.
    """
    # TODO: Maybe move the checkings to the specific 'download_x' method
    # and not here that is more a encapsulation class
    @staticmethod
    def download_audio(url: str, output_filename: str):
        """
        Download the audio file from the provided 'url' and stores
        it locally as 'output_filename'.
        """
        # TODO: Refactor the parameter validation to avoid cyclic imports
        #ParameterValidator.validate_string_mandatory_parameter(url)

        # TODO: Add more checkings here (?)
        output_filename = handle_output_filename(output_filename)

        return download_audio(url, output_filename)
    
    @staticmethod
    def download_gif(query: str, output_filename: str):
        """
        Search for a gif with the provided 'query' and download it,
        if existing, to a local file called 'output_filename'.
        """
        #ParameterValidator.validate_string_mandatory_parameter(query)
        output_filename = handle_output_filename(output_filename, '.gif')

        return download_gif(query, output_filename)
    
    @staticmethod
    def download_google_drive_resource(google_drive_url: str, output_filename: str):
        """
        Download the Google Drive resource from the given 'google_drive_url',
        if existing and available, to a local file called 'output_filename'.
        """
        #ParameterValidator.validate_string_mandatory_parameter(google_drive_url)
        output_filename = handle_output_filename(output_filename)
        
        return GoogleDriveResource.download_from_url(google_drive_url, output_filename)
    
    @staticmethod
    def download_image(url: str, output_filename: str):
        """
        Download the image from the provided 'url' and stores it, if
        existing and available, as a local file called 'output_filename'.
        """
        #ParameterValidator.validate_string_mandatory_parameter(url)
        output_filename = handle_output_filename(output_filename)
        
        return download_image(url, output_filename)

    @staticmethod
    def download_video(url: str, output_filename: str):
        """
        Download the video from the provided 'url' and stores it, if
        existing and available, as a local file called 'output_filename'.
        """
        #ParameterValidator.validate_string_mandatory_parameter(url)
        output_filename = handle_output_filename(output_filename)
        
        return download_video(url, output_filename)


