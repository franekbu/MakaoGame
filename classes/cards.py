from classes import dictionaries as c_dict

class Card:
    def __init__(self, num:int, colour_series:int) -> None:
        """Creates a card object that represent a card from a deck in a game """
        self.__number:int = num
        self.name:str = self.__what_name()
        self.symbol:str = self.__what_colour(colour_series, 's')
        self.colour:str = self.__what_colour(colour_series, 'c')
        self.functional:bool = self.__is_functional()
        self.function:list|None = self.__what_function()

    def __str__(self):
        return f'{self.name}{self.symbol}'

    def __what_name(self) -> str:
        """Returns a card name """
        return c_dict.NAMES[self.__number]

    @staticmethod
    def __what_colour(colour_series:int, what:str) -> str | None:
        """If what = c returns cards colour, if what = s returns cards symbol """
        if what == 'c':
            return c_dict.COLOURS[colour_series]['name']
        elif what == 's':
            return c_dict.COLOURS[colour_series]['symbol']
        else:
            return None

    def __is_functional(self) -> bool:
        """Returns whether card has a function or not"""
        if self.__number == 13 and (self.colour == c_dict.COLOURS[3]['name'] or self.colour == c_dict.COLOURS[4]['name']):
            return True
        elif self.__number in [2, 3, 4, 11, 12, 14]:
            return True
        else:
            return False

    def __what_function(self) -> list:
        """Returns what function does a card have"""
        if self.functional:
            if self.__number == 13:
                return c_dict.FUNCTIONS[13][self.colour]
            else:
                return c_dict.FUNCTIONS[self.__number]
        else:
            return [None]
