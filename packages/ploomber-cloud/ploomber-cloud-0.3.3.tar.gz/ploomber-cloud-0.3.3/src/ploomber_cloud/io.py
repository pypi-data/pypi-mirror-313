import click
from typing import Callable, Any
from dataclasses import dataclass


@dataclass
class ValidationResult:
    is_valid: bool
    error_message: str
    value_validated: Any


def prompt(
    validator: Callable[[Any], ValidationResult], exit_if_invalid=False, **kwargs
):
    """
    A click.prompt wrapper that keeps prompting the user until they submit a valid
    value. See test_io.py for example use.
    """
    is_valid = False
    value_validated = None

    while not is_valid:
        value = click.prompt(**kwargs)

        # if no validator is provided, return the value as is
        if validator is None:
            return value

        result = validator(value)
        is_valid = result.is_valid

        if not is_valid:
            click.secho(f"Invalid value: {value} ({result.error_message})", fg="red")
            if exit_if_invalid:
                raise ValueError(result.error)
        else:
            value_validated = result.value_validated

    return value_validated
