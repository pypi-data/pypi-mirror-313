from yta_general_utils.image.checker import is_valid_image
from yta_general_utils.file.filename import sanitize_filename
from moviepy import AudioFileClip, VideoFileClip
from pathlib import Path


class FileValidator:
    """
    Class to simplify and encapsulate the functionality related
    to file and folders validation.
    """
    @staticmethod
    def is_file(filename):
        """
        Checks if the provided 'filename' is an existing and
        valid file. It returns True if yes or False if not.
        """
        filename = sanitize_filename(filename)
        filename = Path(filename)

        try:
            return filename.exists() and filename.is_file()
        except:
            # TODO: Maybe print stack (?)
            return False

    @staticmethod
    def is_folder(filename):
        """
        Checks if the provided 'filename' is an existing and
        valid folder. It returns True if yes or False if not.
        """
        filename = sanitize_filename(filename)
        filename = Path(filename)

        try:
            return filename.exists() and filename.is_dir()
        except:
            # TODO: Maybe print stack (?)
            return False

    @staticmethod
    def file_exists(filename):
        """
        Checks if the provided 'filename' file or folder exist. It
        returns True if existing or False if not. This method
        sanitizes the provided 'filename' before checking it.
        """
        filename = sanitize_filename(filename)

        try:
            return Path(filename).exists()
        except:
            # TODO: Maybe print stack (?)
            return False

    # TODO: I should do this with another library to
    # avoid 'moviepy' dependency
    @staticmethod
    def file_is_audio_file(filename):
        """
        Checks if the provided 'filename' is an audio file by
        trying to instantiate it as a moviepy AudioFileClip.
        This method sanitizes the provided 'filename' before 
        checking it.
        """
        filename = sanitize_filename(filename)

        try:
            AudioFileClip(filename)
        except:
            return False
        
        return True

    # TODO: I should do this with another library to
    # avoid 'moviepy' dependency
    @staticmethod
    def file_is_video_file(filename):
        """
        Checks if the provided 'filename' is a video file by
        trying to instantiate it as a moviepy VideoFileClip.
        This method sanitizes the provided 'filename' before
        checking it.
        """
        filename = sanitize_filename(filename)

        try:
            VideoFileClip(filename)
        except:
            return False
        
        return True

    @staticmethod
    def file_is_image_file(filename: str):
        """
        Checks if the provided 'filename' is a valid image
        file by opening and verifying it with the Pillow
        library.
        """
        filename = sanitize_filename(filename)

        return is_valid_image(filename)