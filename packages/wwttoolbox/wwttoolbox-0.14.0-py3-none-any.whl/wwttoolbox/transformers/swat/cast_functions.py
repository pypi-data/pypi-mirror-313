def str_to_int(s: str) -> int:
    """Convert a string to an integer.

    If unable to convert, None is returned.
    """
    try:
        return int(s)
    except Exception:
        return None


def str_to_float(s: str) -> float:
    """Convert a string to a float.

    If unable to convert, None is returned.
    """
    try:
        return float(s)
    except Exception:
        return None
