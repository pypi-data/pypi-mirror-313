from yta_general_utils.programming.enum import YTAEnum as Enum

import re


class RegularExpression(Enum):
    """
    Custom YTAEnum class to hold regular expressions and to
    be able to use them directly within this class. You
    inherit this class, set your regular expressions as enum
    items and automatically they will have the 'parse' method
    to validate any string.
    """
    @staticmethod
    def is_regex(string: str):
        """
        Check if the provided 'string' is a valid regular expression
        or not, returning True or False.
        """
        try:
            re.compile(string)
            return True
        except re.error:
            return False
        
    def parse(self, string: str):
        """
        Check this Regular Expression with the provided 'string'. It returns
        True if valid or False if not.
        """
        if not isinstance(string, str):
            raise Exception(f'The provided "string" parameter "{string}" is not a string.')
        
        return bool(re.match(self.value, string))
    
# TODO: Move this to more specific regular expressions and
# maybe hold them in the library you are using them
class GeneralRegularExpression(RegularExpression):
    """
    Enum class to encapsulate useful regular expressions for our system
    and to simplify the way we check those regular expressions with some
    provided parameters.
    """
    FILENAME_WITH_EXTENSION = r'^[\w,\s-]+\.[a-zA-Z0-9]{2,}$'
    """
    Check if the string is a filename with a valid extension (which must
    be a common filename with a dot '.' and at least two
    alphanumeric characters).
    
    Example of a valid input: 'filename.mp3'.
    """
    YOUTUBE_VIDEO_URL = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)'
    """
    Check if the string contains a valid Youtube video url.

    Example of a valid input: 'https://www.youtube.com/watch?v=OpA2ZxnRs6'
    """
    TIKTOK_SHORT_VIDEO_URL = r'^https://vm\.tiktok\.com/[a-zA-Z0-9]+$'
    """
    Check if the string contains a valid Tiktok short video url.
    This url is generated when you share a Tiktok. (?)

    Example of a valid input: 'https://vm.tiktok.com/ZGeSJ6YRA'
    """
    TIKTOK_LONG_VIDEO_URL = r'^https://www\.tiktok\.com/@[a-zA-Z0-9]+/video/\d+.*$'
    """
    Check if the string contains a valid Tiktok long video url.
    This url is the main url of a Tiktok video. (?)

    Example of a valid input: 'https://www.tiktok.com/@ahorayasabesque/video/7327001175616703777?_t=8jqq93LWqsC&_r=1'
    """