from datetime import datetime


def get_rfc_datetime(year: int = 1900, month: int = 1, day: int = 1, hour: int = 0, minute: int = 0):
    """
    Receives a date based on provided parameters and turns it into
    a RFC datetime, returning it.

    TODO: Explain this better, please
    """
    dt = datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'

    return dt