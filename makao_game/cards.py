from __future__ import annotations

from makao_game import dictionaries as c_dict
from makao_game.utils import colour_string
from makao_game.cards_actions import CardsActions

PULL: str = c_dict.FUNCTIONS_TYPES_NAMES['PULL']
FREEZE: str = c_dict.FUNCTIONS_TYPES_NAMES['FREEZE']
DEMAND: str = c_dict.FUNCTIONS_TYPES_NAMES['DEMAND']
ABOLISH: str = c_dict.FUNCTIONS_TYPES_NAMES['ABOLISH']
REVERSE: str = c_dict.FUNCTIONS_TYPES_NAMES['REVERSE']

class Card:
    def __init__(self, num: int, colour_series: int) -> None:
        """Creates a card object that represent a card from a deck in a game """
        self._number: int = num
        self.name: str = self._what_name()
        self.symbol: str = self._what_colour(colour_series, 's')
        self.colour: str = self._what_colour(colour_series, 'c')
        self.function: tuple[str, str | int] | None = self._what_function()

    def __str__(self) -> str:
        symbol: str
        if self.colour in ['Diamonds', 'Hearts']:
            symbol = colour_string(self.symbol, 'red')
        else:
            symbol = colour_string(self.symbol, 'black', 'bg')
        return f'{self.name}{symbol}'

    def __repr__(self) -> str:
        return f'{self.name}{self.symbol}'

    def _what_name(self) -> str:
        """Returns a card name """
        return c_dict.NAMES[self._number]

    @staticmethod
    def _what_colour(colour_series: int, what: str) -> str:
        """If what = c returns cards colour, if what = s returns cards symbol """
        if what == 'c':
            return c_dict.COLOURS[colour_series]['name'].capitalize()
        elif what == 's':
            return c_dict.COLOURS[colour_series]['symbol']
        else:
            raise ValueError

    def _is_functional(self) -> bool:
        """Returns whether card has a function or not"""
        if self._number == 13 and (self.colour == c_dict.COLOURS[3]['name'] or self.colour == c_dict.COLOURS[4]['name']):
            return True
        elif self._number in [2, 3, 4, 11, 12, 14]:
            return True
        else:
            return False

    def _what_function(self) -> tuple[str, str | int] | None:
        """Returns what function does a card have"""
        if self._is_functional():
            function: tuple[str, str | int] | dict[str, tuple[str, str | int]] = c_dict.FUNCTIONS[self._number]
            if isinstance(function, dict):
                return function[self.colour]
            elif isinstance(function, tuple):
                return function
        else:
            return None

    def can_be_played(self, old_card: Card, game_actions: CardsActions) -> bool:
        """Returns True if card can be played on old card, with current game actions"""

        if isinstance(self.function, tuple) and isinstance(old_card.function, tuple):
            if self.function[0] == ABOLISH or old_card.function[0] == ABOLISH:
                return True

        action_type: str | None = game_actions.action_type
        if action_type is None:
            return self.colour == old_card.colour or self.name == old_card.name
        elif action_type == PULL:
            if isinstance(self.function, tuple):
                return (self.function[0] == PULL or self.function[0] == REVERSE) and \
                (self.colour == old_card.colour or self.name == old_card.name)
            return False
        elif action_type == FREEZE:
            if isinstance(self.function, tuple):
               return self.function[0] == FREEZE
            return False
        elif action_type == DEMAND:
            if isinstance(self.function, tuple):
                return self.name == old_card.name
            elif game_actions.demanded_type == c_dict.DEMAND_OPTIONS_NAMES['JACK']:
                return self.name == game_actions.demanded_value
            elif game_actions.demanded_type == c_dict.DEMAND_OPTIONS_NAMES['ACE']:
                return self.colour == game_actions.demanded_value
            else:
                raise ValueError('Action type set to Demand but nor demand type set correctly')
        else:
            raise ValueError('Action type is neither None or any other FUNCTIONS_TYPES_NAMES')
