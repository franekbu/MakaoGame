from makao_game import dictionaries as c_dict
from makao_game.utils import colour_string

class Card:
    def __init__(self, num:int, colour_series:int) -> None:
        """Creates a card object that represent a card from a deck in a game """
        self._number:int = num
        self.name:str = self.__what_name()
        self.symbol:str = self.__what_colour(colour_series, 's')
        self.colour:str = self.__what_colour(colour_series, 'c')
        self.functional:bool = self.__is_functional()
        self.function: tuple[str, str | int] | None = self.__what_function()

    def __str__(self):
        if self.colour in ['Diamonds', 'Hearts']:
            symbol = colour_string(self.symbol, 'red')
        else:
            symbol = colour_string(self.symbol, 'black', 'bg')
        return f'{self.name}{symbol}'

    def __repr__(self):
        return f'{self.name}{self.symbol}'

    def __what_name(self) -> str:
        """Returns a card name """
        return c_dict.NAMES[self._number]

    @staticmethod
    def __what_colour(colour_series:int, what:str) -> str:
        """If what = c returns cards colour, if what = s returns cards symbol """
        if what == 'c':
            return c_dict.COLOURS[colour_series]['name']
        elif what == 's':
            return c_dict.COLOURS[colour_series]['symbol']
        else:
            raise ValueError

    def __is_functional(self) -> bool:
        """Returns whether card has a function or not"""
        if self._number == 13 and (self.colour == c_dict.COLOURS[3]['name'] or self.colour == c_dict.COLOURS[4]['name']):
            return True
        elif self._number in [2, 3, 4, 11, 12, 14]:
            return True
        else:
            return False

    def __what_function(self) -> tuple[str, str | int] | None:
        """Returns what function does a card have"""
        if self.functional:
            function: tuple[str, str | int] | dict[str, tuple[str, str | int]] = c_dict.FUNCTIONS[self._number]
            if isinstance(function, dict):
                return function[self.colour]
            elif isinstance(function, tuple):
                return function
            else:
                raise ValueError('Not supported type in FUNCTIONS dict')
        else:
            return None
