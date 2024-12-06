from yta_general_utils.programming.regular_expressions import RegularExpression


class ColorRegularExpression(RegularExpression):
    HEX = r'^(#|0x|0X)[0-9a-fA-F]{6,8}$'
    """
    Accepts colors with or without alpha, that include the
    '#', '0x' or '0X' begining.
    """