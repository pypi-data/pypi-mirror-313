from yta_general_utils.programming.parameter_validator import NumberValidator

import random


def randrangefloat(start: float, end: float, step: float):
    """
    Calculate and return a random float number between the provided
    'start' and 'end' limits using the also provided float 'step'.

    TODO: Is limit included (?) Please, review and, if necessary,
    include it as a parameter.
    """
    # TODO: What about strings that are actually parseable
    # as those numbers (?)
    if not NumberValidator.is_number(start):
        raise Exception('The provided "start" parameter is not a number.')
    
    if not NumberValidator.is_number(end):
        raise Exception('The provided "end" parameter is not a number.')
    
    start = float(start)
    end = float(end)

    # Swap limits if needed
    if end < start:
        start, end = end, start

    # TODO: What if 'start' and 'end' are the same (?)
    return random.choice([round(start + i * step, 4) for i in range(int((end - start) / step) + 1) if start + i * step <= end])

def random_int_between(start: int, end: int, step: int = 1):
    # TODO: What about strings that are actually parseable
    # as those numbers (?)
    if not NumberValidator.is_number(start):
        raise Exception('The provided "start" parameter is not a number.')
    
    if not NumberValidator.is_number(end):
        raise Exception('The provided "end" parameter is not a number.')
    
    start = int(start)
    end = int(end)
    
    # Swap limits if needed
    if end < start:
        start, end = end, start

    # TODO: What if 'start' and 'end' are the same (?)
    return random.randrange(start, end + 1, step)

def random_bool():
    """
    Return a boolean value chosen randomly.
    """
    return bool(random.getrandbits(1))