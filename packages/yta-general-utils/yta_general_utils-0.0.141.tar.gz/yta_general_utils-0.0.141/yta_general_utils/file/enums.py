from yta_general_utils.programming.enum import YTAEnum as Enum


class ImageFileExtension(Enum):
    """
    Enum class to encapsulate all existing image file extensions.
    """
    PNG = 'png'
    """
    Portable Network Graphics
    """
    JPEG = 'jpeg'
    """
    Joint Photographic Experts Group
    """
    JPG = 'jpg'
    """
    Joint Photographic Experts Group
    """
    WEBP = 'webp'
    """
    Web Picture
    """
    BMP = 'bmp'
    """
    Bitmap Image File
    """
    GIF = 'gif'
    """
    Graphics Interchange Format
    """
    TIFF = 'tiff'
    """
    Tagged Image File
    """
    PSD = 'psd'
    """
    Photoshop Document
    """
    PDF = 'pdf'
    """
    Portable Document Format
    """
    EPS = 'eps'
    """
    Encapsulated Postcript
    """
    AI = 'ai'
    """
    Adobe ILlustrator Document
    """
    INDD = 'indd'
    """
    Adobe Indesign Document
    """
    RAW = 'raw'
    """
    Raw Image Formats
    """
    CDR = 'cdr'
    """
    Corel Draw
    """
    # TODO: Add more

    @classmethod
    def default(cls):
        return cls.PNG

class AudioFileExtension(Enum):
    """
    Enum class to encapsulate all existing audio file extensions.
    """
    WAV = 'wav'
    """
    Waveform Audio
    """
    MP3 = 'mp3'
    """
    MPEG Audio Layer 3.
    """
    M4A = 'm4a'
    """
    MPEG-4 Audio
    """
    FLAC = 'flac'
    """
    Free Lossless Audio Codec.
    """
    WMA = 'wma'
    """
    Windows Media Audio
    """
    AAC = 'aac'
    """
    Advanced Audio Coding
    """
    # TODO: Add more

    @classmethod
    def default(cls):
        return cls.WAV

class VideoFileExtension(Enum):
    """
    Enum class to encapsulate all existing video file extensions.
    """
    MOV = 'mov'
    """
    Apple video
    """
    MP4 = 'mp4'
    """
    MPEG-4
    """
    WEBM = 'webm'
    """
    Developed by Google, subgroup of the open and standard Matroska Video Container (MKV)
    """
    AVI = 'avi'
    """
    Audio Video Interleave
    """
    WMV = 'wmv'
    """
    Windows Media Video
    """
    AVCHD = 'avchd'
    """
    Advanced Video Coding High Definition
    """
    FVL = '.flv'
    """
    Flash Video
    """
    # TODO: Add more

    @classmethod
    def default(cls):
        return cls.MP4

# These classes above should be used by the ffmpeg_handler and other
# declarations I make in our app to be consistent and reuse the code

class FileType(Enum):
    """
    Enum that represents the different file types and the valid
    extensions we accept for those file types. This Enum is to
    be used when checking filenames parameter.

    For example, we will use this to make sure the filename they
    gave to us is a video file type if we are storing a video 
    file.
    """
    IMAGE = ImageFileExtension.get_all()
    AUDIO = AudioFileExtension.get_all()
    VIDEO = VideoFileExtension.get_all()