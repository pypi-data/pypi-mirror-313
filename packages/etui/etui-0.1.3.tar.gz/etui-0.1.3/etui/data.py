import json


def is_json(s: str) -> bool:
    """Validate if input is a valid JSON-string

    Args:
        s (str): Input string

    Returns:
        bool: Is valid
    """
    try:
        _ = json.loads(s)
        return True
    except (ValueError, TypeError):
        return False


def inspect(obj: object) -> None:
    """Inspect object and print to Console

    Args:
        obj (object): Object to inspect
    """
    from pprint import pprint

    pprint(vars(obj))
