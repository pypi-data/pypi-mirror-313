from typing import Any


def check(name: str, value: Any, type_: type, required_: bool):
    if required_:
        assert value is not None, f"{name} is required"

        if isinstance(value, str):
            assert value != "", f"{name} is empty"
    elif value is None:
        return

    assert isinstance(value, type_), f"{name} must be a {type_.__name__} and not {type(value).__name__}"


def required(name: str, value: Any, type_: type):
    check(name, value, type_, required_=True)


def optional(name: str, value: Any, type_: type):
    check(name, value, type_, required_=False)
