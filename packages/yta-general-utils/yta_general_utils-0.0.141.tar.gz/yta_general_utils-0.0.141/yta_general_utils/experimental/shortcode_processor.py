"""
    TODO:

    I have a problem here. If I use this as a library, I cannot 
    manually handle the different handlers I want to use nor 
    add them in the 'handle_shortcodes' method. I need to find
    a way in which I can use this in a better way.

    Maybe this is not suitable for the utils library and I have
    to use it manually in the project by coding itself inside 
    that project.
"""
from shortcodes import Parser
from enum import Enum


shortcodes_found = []
shortcode_previous_word_indexes = []

def specific_shortcode_handler(pargs, kwargs, context):
    """
    This is an specific shortcode handler that will specify the
    shortcode name in 'obj.shortcode' and what do we need to
    maintain in 'obj' variable to be able to work later.

    This method will be called everytime an ['specific_shortcode' ...]
    is found in the text in which we are parsing shortcodes, if this
    handler has been activated.
    """
    obj = {
        'shortcode': 'specific_shortcode',
        'previous_word_index': -1,
    }

    # TODO: This should be like this below and moved to specific folder
    class Example(Enum):
        KEYWORDS = 'keywords'
        DURATION = 'duration'
        ALL = [KEYWORDS, DURATION]

    for field in Example.ALL.value:
        if field in kwargs:
            obj[field] = kwargs[field]
    
    # TODO: Other fields later (why and which ones?)
    if 'audio' in kwargs:
        obj['audio'] = kwargs['audio']

    shortcodes_found.append(obj)
    
    return '[specific_shortcode]'

def handle_shortcodes(text):
    """
    This method processes the provided 'text' and finds the accepted shortcodes (see list below).
    It will return an object that contains 'shortcodes_found' and 'text_without_shortcodes'. At
    the same time, the 'shortcodes_found' is an array of objects that contains 'shortcode', 
    'keywords' and 'previous_word_index' indexes.

    'shortcodes' field includes the shortcode name. 'keywords' field includes the keywords to 
    look for the item we want, and 'previous_word_index' includes the index in which this word
    appears, to use it with the transcription to obtain the moment in which we should include 
    the result of this shortcode item.
    """
    # Found here:https://www.dmulholl.com/dev/shortcodes.html
    # We clean arrays to avoid strange behaviours
    global shortcodes_found
    global shortcode_previous_word_indexes

    # We register our shortcode parsers and ignore unsupported (unregistered)
    parser = Parser(start = '[', end = ']', ignore_unknown = True)
    parser.register(specific_shortcode_handler, 'specific_shortcode')

    shortcodes_found = []
    shortcode_previous_word_indexes = []

    # We parse all shortcodes
    output = parser.parse(text, context = None)
    words = output.split(' ')

    # Now I look for the previous word index for each shortcode
    index = 0
    while index < len(words):
        word = words[index]
        # TODO: Pay attention to shortcodes with characters next to ']' ('],', '].', etc.)
        # It doesn't get into this 'if' condition, so it fails later when accessing the 
        # previous word index
        if word.startswith('[') and word.endswith(']'):
            # Shortcode found, store previous word index
            if index == 0:
                # If shortcode is at the begining, treat it like if the previous word
                # was the first one, that would be exactly the same as if the shortcode
                # is just after the first word
                shortcode_previous_word_indexes.append(index)
            else:
                shortcode_previous_word_indexes.append(index - 1)
                print('Recognized "' + word + '" shortcode for the "' + words[index - 1] + '" word')
            # I remove the shortcode from the words array to safe next indexes
            del words[index]
            # I need to check again this position, the next word will be here
        else:
            index += 1

    # I save that index next to our shortcodes list object
    for index, shortcode in enumerate(shortcodes_found):
        shortcode['previous_word_index'] = shortcode_previous_word_indexes[index]

    # We clean the output (without shortcodes) to return it
    output = ' '.join(words)

    # TODO: What about shortcodes that have not been detected?
    return {
        'shortcodes_found': shortcodes_found.copy(),
        'text_without_shortcodes': output,
    }

        