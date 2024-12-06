import unicodedata
import re


def remove_accents(text):
    """
    Removes the accents from the provided 'text'.
    """
    return ''.join(char for char in unicodedata.normalize('NFD', text) if unicodedata.category(char) != 'Mn')

def remove_marks(text):
    """
    Removes the existing quotation and exclamation marks and also commas and full stops.

    # This below could work eliminating no white spaces.
    pattern = re.compile('[\W_]+')
    return pattern.sub('', s)
    """
    # TODO: Try with a 're' implementation
    return text.replace('?', '').replace('¿', '').replace(',', '').replace('.', '').replace('¡', '').replace('!', '').replace('(', '').replace(')', '')

def remove_marks_and_accents(text):
    """
    Removes the existing accents and quotation and exclamation marks, and commas and full stops.
    """
    return remove_accents(remove_marks(text))

def remove_non_ascii_characters(text):
    """
    Removes any non-ascii character from the provided 'text' and returns it
    modified.
    """
    s = list(remove_accents(text))
    index = 0
    while index < len(s):
        char = s[index]
        if not char.isascii():
            del s[index]
        else:
            index += 1

    return ''.join(s)

def fix_ellipsis(text: str):
    """
    This method fixes the provided 'text' by removing the
    existing ellipsis (...).
    """
    text = re.sub(r'\.\.\.+', '', text)

    return text

def fix_unseparated_periods(text: str):
    """
    This method fixes the provided 'text' by applying a space
    after any period without it.
    """
    # Thank you: https://stackoverflow.com/a/70394076
    text = re.sub(r'\.(?!(?<=\d\.)\d) ?', '. ', text)
    
    return text

def fix_separated_parenthesis(text: str):
    """
    This method remove the spaces that are found before or/and
    after any parenthesis. For example, '( esto es de prueba )'
    will become '(esto es de prueba)'.
    """
    def fix_match(match):
        opening, content, closure = match.groups()
        if content:
            # Remove the whitespaces
            without_whitespaces = re.sub(r'\s+', ' ', content.strip())
            return f'{opening}{without_whitespaces}{closure}'
        
        return match.group(0)
    
    text = re.sub(r'(\()([^\(\)]+?)(\))', fix_match, text)
    
    return text

def fix_separated_square_brackets(text: str):
    """
    This method removes the spaces that are found before or/and
    after any square bracket. For example, '[  shortcode ]' will
    become '[shortcode]'
    """
    def fix_match(match):
        opening, content, closure = match.groups()
        if content:
            # Remove the whitespaces
            without_whitespaces = re.sub(r'\s+', ' ', content.strip())
            return f'{opening}{without_whitespaces}{closure}'
        
        return match.group(0)
    
    text = re.sub(r'(\[)([^\[\]]+?)(\])', fix_match, text)
    
    return text

def add_missing_spaces_before_and_after_parenthesis(text: str):
    """
    This method adds the missing spaces before and after any 
    parenthesis in the provided 'text'. For example, 'hola(nueve)siete'
    will become 'hola (nueve) siete'.
    """
    text = re.sub(r'(?<!\s)\((?!\s)', ' (', text)
    text = re.sub(r'\)(?!\s)', ') ', text)
    
    return text

def add_missing_spaces_before_and_after_square_brackets(text: str):
    """
    This method adds the missing spaces before and after any 
    square bracket in the provided 'text'. For example, 
    'hola[nueve]siete' will become 'hola [nueve] siete'.
    """
    text = re.sub(r'(?<!\s)\[(?!\s)', ' [', text)
    text = re.sub(r'\](?!\s)', '] ', text)
    
    return text

def fix_excesive_blank_spaces(text: str):
    """
    Checks the provided 'text' and removes the extra blank spaces.
    This means that any sentence with more than one blank space 
    will be replaced by only one blank space.
    """
    # TODO: Ok, why am I using not the 'repl' param in re.search?
    # I'm applying it in the new method below, please check if
    # valid to avoid the while, thank you
    filtered = re.search('[ ]{2,}', text)
    while filtered:
        index_to_replace = filtered.end() - 1
        s = list(text)
        s[index_to_replace] = ''
        text = ''.join(s)
        filtered = re.search('[ ]{2,}', text)

    return text

def numbers_to_text(text):
    """
    This method receives a text that could contain numbers and turns
    those numbers into text.

    This method is useful to let narration software work with just
    text and avoid numbers problems.
    """
    words = str(text).split(' ')

    SPECIAL_CHARS = ['¡', '!', ',', '.', '¿', '?', ':', '"', '\'', '#', '@']
    new_words = []
    # Iterate over each word to turn numbers into words
    for word in words:
        begining = ''
        ending = ''

        # We need to remove special chars at the begining or at the ending
        # to be able to work well with the important part of the word, but
        # we cannot simply delete ',' or '.' because could be in the middle
        # of a word
        if word[0] in SPECIAL_CHARS:
            begining = word[0]
            word = word[1:]
        if word[len(word) - 1] in SPECIAL_CHARS:
            ending = word[len(word) - 1]
            word = word[:1]

        try:
            word = float(word)
            # If here, it is a number, lets change its name
            # TODO: Implement logic here, so word will be the text, not the number
            print('Processing number: ' + str(word))
            accumulated_text = ''
            # We receive 123.456.789
            is_million = False
            is_one = False
            is_thousand = False
            is_ten = False
            divisor = 1000000000
            res = int(word / divisor)  # 1 . 000 . 000 . 000
            if res >= 1:
                is_million = True
                is_thousand = True
                accumulated_text += __process_unit(res)
                word -= divisor * res

            if is_thousand:
                accumulated_text += ' mil'
                is_thousand = False

            divisor = 100000000
            res = int(word / divisor)  # 100 . 000 . 000
            if res >= 1:
                is_million = True
                if res == 1:
                    is_one = True
                accumulated_text += __process_hundred(res)
                word -= divisor * res

            divisor = 10000000
            res = int(word / divisor) # 10 . 000 . 000
            if res >= 1:
                is_million = True
                is_ten = True
                if is_one:
                    accumulated_text += 'to'
                    is_one = False
                accumulated_text += __process_ten(res)
                word -= divisor * res

            divisor = 1000000
            res = int(word / divisor) # 1 . 000 . 000
            if res >= 1:
                is_million = True
                if is_one:
                    accumulated_text += 'to'
                    is_one: False
                if is_ten:
                    accumulated_text += ' y '
                    is_ten = False
                accumulated_text += __process_unit(res)
                word -= divisor * res

            if is_million:
                accumulated_text += ' millones'
                is_million = False

            divisor = 100000
            res = int(word / divisor) # 100 . 000
            if res >= 1:
                is_thousand = True
                if res == 1:
                    is_one = True
                accumulated_text += __process_hundred(res)
                word -= divisor * res

            divisor = 10000
            res = int(word / divisor) # 10 . 000
            if res >= 1:
                is_thousand = True
                is_ten = True
                if is_one:
                    accumulated_text += 'to'
                    is_one = False
                accumulated_text += __process_ten(res)
                word -= divisor * res

            divisor = 1000
            res = int(word / divisor) # 1 . 000
            if res >= 1:
                is_thousand = True
                if is_one:
                    accumulated_text += 'to'
                    is_one = False
                if is_ten:
                    accumulated_text += ' y '
                    is_ten = False
                accumulated_text += __process_unit(res)
                word -= divisor * res

            if is_thousand:
                accumulated_text += ' mil'
                is_thousand = False

            divisor = 100
            res = int(word / divisor) # 100
            if res >= 1:
                is_thousand = True
                if res == 1:
                    is_one = True
                accumulated_text += __process_hundred(res)
                word -= divisor * res

            divisor = 10
            res = int(word / divisor) # 10
            if res >= 1:
                is_thousand = True
                is_ten = True
                if is_one:
                    accumulated_text += 'to'
                    is_one = False
                accumulated_text += __process_ten(res)
                word -= divisor * res

            divisor = 1
            res = int(word / divisor) # 1
            if res >= 1:
                is_thousand = True
                if is_one:
                    accumulated_text += 'to'
                    is_one = False
                if is_ten:
                    accumulated_text += ' y '
                    is_ten = False
                accumulated_text += __process_unit(res)
                word -= divisor * res

            accumulated_text = accumulated_text.replace('  ', ' ').strip()
            # We need to replace in special cases
            accumulated_text = accumulated_text.replace('veinte y nueve', 'veintinueve')
            accumulated_text = accumulated_text.replace('veinte y ocho', 'veintiocho')
            accumulated_text = accumulated_text.replace('veinte y siete', 'veintisiete')
            accumulated_text = accumulated_text.replace('veinte y seis', 'veintiséis')
            accumulated_text = accumulated_text.replace('veinte y cinco', 'veinticinco')
            accumulated_text = accumulated_text.replace('veinte y cuatro', 'veinticuatro')
            accumulated_text = accumulated_text.replace('veinte y tres', 'veintitrés')
            accumulated_text = accumulated_text.replace('veinte y dos', 'veintidós')
            accumulated_text = accumulated_text.replace('veinte y uno', 'veintiuno')
            accumulated_text = accumulated_text.replace('diez y nueve', 'diecinueve')
            accumulated_text = accumulated_text.replace('diez y ocho', 'dieciocho')
            accumulated_text = accumulated_text.replace('diez y siete', 'diecisiete')
            accumulated_text = accumulated_text.replace('diez y seis', 'dieciséis')
            accumulated_text = accumulated_text.replace('diez y cinco', 'quince')
            accumulated_text = accumulated_text.replace('diez y cuatro', 'catorce')
            accumulated_text = accumulated_text.replace('diez y tres', 'trece')
            accumulated_text = accumulated_text.replace('diez y dos', 'doce')
            accumulated_text = accumulated_text.replace('diez y uno', 'once')

            word = accumulated_text
        except:
            pass

        new_words.append(begining + str(word) + ending)

    # We have the same size in 'words' and 'new_words', so lets build it
    final_text = " ".join(new_words)
    
    return final_text


def __process_hundred(number):
    """
    Receives a digit that represente the X00 part of a number and returns
    that number (according to its position) in words.

    This method returns ' novecientos' for 9 input and ' cien' for 1 input.
    """
    number_in_text = ''

    if number == 9:
        number_in_text = ' novecientos'
    elif number == 8:
        number_in_text = ' ochocientos'
    elif number == 7:
        number_in_text = ' setecientos'
    elif number == 6:
        number_in_text = ' seiscientos'
    elif number == 5:
        number_in_text = ' quinientos'
    elif number == 4:
        number_in_text = ' cuatrocientos'
    elif number == 3:
        number_in_text = ' trescientos'
    elif number == 2:
        number_in_text = ' doscientos'
    elif number == 1:
        number_in_text = ' cien'

    return number_in_text

def __process_ten(number):
    """
    Receives a digit that represente the X0 part of a number and returns
    that number (according to its position) in words.

    This method returns ' noventa' for 9 input and ' diez' for 1 input.
    """
    number_in_text = ''

    if number == 9:
        number_in_text = ' noventa'
    elif number == 8:
        number_in_text = ' ochenta'
    elif number == 7:
        number_in_text = ' setenta'
    elif number == 6:
        number_in_text = ' sesenta'
    elif number == 5:
        number_in_text = ' cincuenta'
    elif number == 4:
        number_in_text = ' cuarenta'
    elif number == 3:
        number_in_text = ' treinta'
    elif number == 2:
        number_in_text = ' veinte'
    elif number == 1:
        number_in_text = ' diez'

    return number_in_text

def __process_unit(number):
    """
    Receives a digit that represente the X part of a number and returns
    that number (according to its position) in words.

    This method returns ' nueve' for 9 input, and ' uno' for 1 input.
    """
    number_in_text = ''

    if number == 9:
        number_in_text = ' nueve'
    elif number == 8:
        number_in_text = ' ocho'
    elif number == 7:
        number_in_text = ' siete'
    elif number == 6:
        number_in_text = ' seis'
    elif number == 5:
        number_in_text = ' cinco'
    elif number == 4:
        number_in_text = ' cuatro'
    elif number == 3:
        number_in_text = ' tres'
    elif number == 2:
        number_in_text = ' dos'
    elif number == 1:
        number_in_text = ' uno'

    return number_in_text