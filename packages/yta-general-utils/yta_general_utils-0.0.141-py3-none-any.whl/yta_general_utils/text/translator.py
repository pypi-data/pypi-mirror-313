from yta_general_utils.web.scrapper.chrome_scrapper import google_translate
from enum import Enum
from typing import Union


# TODO: Implement YTAEnum instead of Enum
class GoogleLanguage(Enum):
    # TODO: Implement more languages
    ENGLISH = 'en'
    SPANISH = 'es'

# TODO: Create class GoogleTranslator to wrap this
def translate_text(text: str, input_language: Union[GoogleLanguage, str] = GoogleLanguage.ENGLISH, output_language: Union[GoogleLanguage, str] = GoogleLanguage.SPANISH):
    """
    Returns the provided 'text' translated into the 'output_language' 
    using Google Traductor by chromedriver navigation.

    TODO: Make this have Enums with the different available Google
    Translate languages.
    """
    if not text:
        raise Exception('No "text" provided.')
    
    if not isinstance(text, str) and not isinstance(text, GoogleLanguage):
        raise Exception('The "text" provided is not a GoogleLanguage or a str.')
    
    if not input_language:
        raise Exception('No "input_language" provided.')
    
    if not output_language:
        raise Exception('No "output_language" provided.')

    return google_translate(text, input_language, output_language)
