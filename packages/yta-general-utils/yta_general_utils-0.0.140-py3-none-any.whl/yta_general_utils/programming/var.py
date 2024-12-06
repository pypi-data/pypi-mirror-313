def snake_to_camel(snake_str: str):
    """
    Turns the provided 'snake_str' variable name (that is like 
    this_is_the_variable_name) into a upper camel case variable
    name (for the previous it would be ThisIsTheVariableName).
    """
    if not snake_str:
        raise Exception('No "snake_str" provided.')
    
    if not isinstance(snake_str, str):
        raise Exception('The "snake_str" parameter provided is not a string.')
    
    return ''.join(word.title() for word in snake_str.split('_'))
    