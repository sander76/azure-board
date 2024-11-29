from collections.abc import Sequence
from dataclasses import dataclass

import questionary


class Filler:
    """Base filler."""

    def __init__(self, message: str, allow_none: bool = False):
        self._message = message
        self._allow_none = allow_none

    def ask(self) -> str:
        raise NotImplementedError


class StringEntryFiller(Filler):
    """Fill with a simple user prompt."""

    def ask(self) -> str:
        message = self._message + " [return for none]" if self._allow_none else self._message

        result = questionary.text(message).ask()

        return result


class OptionFiller(Filler):
    """Use a list of options to make a single choice."""

    def __init__(self, message: str, choices: Sequence[str], allow_none: bool = False):
        super().__init__(message, allow_none)
        self._choices = list(choices)

    def ask(self) -> str:
        if self._allow_none:
            self._choices.append("Select nothing")
        result = questionary.select(self._message, choices=self._choices)

        return result
