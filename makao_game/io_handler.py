from abc import ABC, abstractmethod
import asyncio
from enum import Enum

from makao_game.utils import colour_string
from makao_game.dictionaries import COLOURS

class IODataType(Enum):
    MAKAO = 'makao'
    DEMAND = 'demand'
    CARD = 'card'
    GAME = 'game'
    PLAY_PASS = 'play'
    YES_NO = 'yes'

class IOHandler(ABC):
    @abstractmethod
    async def get_user_input(self, data_type: IODataType, username: str | None, message: str = '') -> str:
        """Takes user's input and returns it"""
        pass

    @abstractmethod
    async def display_message(self, message: str, warning: bool = False) -> None:
        """Displays message to user
        If warning set to True, makes message distinguish
        """
        pass

    @abstractmethod
    def supported_symbols(self) -> dict[str, str]:
        """Returns dict with key of colour card and value of what to display to user instead of raw symbols"""
        pass

class ConsoleIOHandler(IOHandler):
    async def get_user_input(self, data_type: IODataType, username: str | None, message: str = '') -> str:
        user_input: str = await asyncio.to_thread(input, message)
        return user_input

    async def display_message(self, message: str, warning: bool = False) -> None:
        if warning:
            message = colour_string(message, 'red')
        await asyncio.to_thread(print, message)

    def supported_symbols(self) -> dict[str, str]:
        symbols: dict[str, str] = {COLOURS[num]['name']: COLOURS[num]['symbol'] for num in COLOURS}
        for colour in symbols:
            if colour in ['Hearts', 'Diamonds']:
                symbols[colour] = colour_string(symbols[colour], 'red')
            else:
                symbols[colour] = colour_string(symbols[colour], colour='black', bg_colour='bg')

        return symbols
