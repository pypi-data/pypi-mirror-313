from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum

from .console import input_and_erase

__all__ = [
    'ENTER',
    'enter_to_continue',
    'format_shortcut',
    'Prompt',
    'PromptOption',
]

PROMPT_SEPARATOR = '-' * 3

ENTER = 'Enter'
ENTER_TO_CONTINUE = f'{ENTER} to continue'

TITLE_DELIMITER = ': '
MODIFIER_DELIMITER = ' + '
OPTION_DELIMITER = ' | '
PROMPT_SUFFIX = ': '

SHORTCUT_FORMAT = '[{shortcut}]'


def format_shortcut(shortcut: str) -> str:
    return SHORTCUT_FORMAT.format(shortcut=shortcut)


def highlight_initial(text: str) -> str:
    return format_shortcut(text[0]) + text[1:]


def normalize(text: str) -> str:
    return text.strip().lower()


@dataclass
class PromptOption[T]:
    """
    A prompt option with an action and optional modifiers.
    The first letters of the description and modifiers will be used as "shortcuts" for the action.
    """
    description: str
    action: T
    modifiers: dict[str, T] | None = None

    def format_description(self) -> str:
        """Format the description line for display (e.g., '[o]riginal + [s]lowly')."""
        return MODIFIER_DELIMITER.join(
            highlight_initial(option)
            for option in [self.description] + list((self.modifiers or {}).keys())
        )

    def get_shortcut_mapping(self) -> dict[str, T]:
        """Get a mapping of shortcuts to actions."""
        return {
            self.description[0]: self.action,
            **{
                self.description[0] + modifier[0]: modifier_action
                for modifier, modifier_action in (self.modifiers or {}).items()
            },
        }

    def format_shortcuts(self) -> str:
        """Format the shortcuts line for display (e.g., '[o] | [os]')."""
        return OPTION_DELIMITER.join(format_shortcut(shortcut) for shortcut in self.get_shortcut_mapping().keys())


class Prompt[T]:
    """A prompt that allows the user to choose from multiple options."""
    _title: str | None
    _options: list[PromptOption[T]]

    def __init__(self, title: str | None = None) -> None:
        self._title = title
        self._options = []

    @staticmethod
    def from_enum[T: StrEnum](enum: T, title: str | None = None) -> Prompt[T]:
        prompt = Prompt(title)
        for option in enum:
            prompt.add_option(PromptOption(
                description=option.value,
                action=option,
            ))
        return prompt

    def add_option(self, option: PromptOption) -> Prompt[T]:
        self._options.append(option)
        return self

    def _match(self, response: str) -> T | None:
        """
        Match the response to the corresponding action (None is returned if the response is empty).
        :raises ValueError: If the response is not one of the shortcuts or empty.
        """
        normalized_response = normalize(response)
        if normalized_response:
            for option in self._options:
                mapping = option.get_shortcut_mapping()
                if normalized_response in mapping:
                    return mapping[normalized_response]
            raise ValueError(f'Invalid response: {response}')
        else:
            return None

    def prompt(self) -> T | None:
        """
        Prompt the user for a choice and return the corresponding action (or None if the response is empty).
        If the response is invalid, the prompt is repeated until a valid response is given.
        """
        while True:
            response = input_and_erase(
                '\n'.join([
                    PROMPT_SEPARATOR,
                    (self._title + TITLE_DELIMITER if self._title else '') + OPTION_DELIMITER.join(
                        [option.format_description() for option in self._options] + [ENTER_TO_CONTINUE],
                    ),
                    OPTION_DELIMITER.join(
                        [option.format_shortcuts() for option in self._options] + [ENTER],
                    ) + PROMPT_SUFFIX,
                ]),
            )
            try:
                return self._match(response)
            except ValueError:
                pass


def enter_to_continue() -> None:
    """Prompt the user to press Enter to continue."""
    input_and_erase('\n'.join([
        PROMPT_SEPARATOR,
        ENTER_TO_CONTINUE + PROMPT_SUFFIX,
    ]))
