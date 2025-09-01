from abc import ABC, abstractmethod
import asyncio

from makao_game.utils import colour_string

class IOHandler(ABC):
    @abstractmethod
    async def get_user_input(self, message: str = '') -> str:
        """Takes user's input and returns it"""
        pass

    @abstractmethod
    async def display_message(self, message: str, warning: bool = False) -> None:
        """Displays message to user
        If warning set to True, makes message distinguish
        """
        pass

    @abstractmethod
    def allow_ascii(self) -> bool:
        """Returns True if IOHandler allows ascii to be passed"""
        pass

class ConsoleIOHandler(IOHandler):
    async def get_user_input(self, message: str = '') -> str:
        user_input: str = await asyncio.to_thread(input, message)
        return user_input

    async def display_message(self, message: str, warning: bool = False) -> None:
        if warning:
            message = colour_string(message, 'red')
        await asyncio.to_thread(print, message)

    def allow_ascii(self) -> bool:
        return True
