import re


def check(pattern, string: str) -> bool:
    if string is None:
        return False

    return bool(re.match(pattern, str(string)))
