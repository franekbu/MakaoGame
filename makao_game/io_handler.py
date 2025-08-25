from abc import ABC, abstractmethod

from makao_game.utils import colour_string

class IOHandler(ABC):
    @abstractmethod
    def get_user_input(self, message: str = '') -> str:
        """Takes user's input and returns it"""
        pass

    @abstractmethod
    def display_message(self, message: str, warning: bool = False) -> None:
        """Displays message to user
        If warning set to True, makes message distinguish
        """
        pass

    @abstractmethod
    def allow_ascii(self) -> bool:
        """Returns True if IOHandler allows ascii to be passed"""
        pass

class ConsoleIOHandler(IOHandler):
    def get_user_input(self, message: str = '') -> str:
        user_input: str = input(message)
        return user_input

    def display_message(self, message: str, warning: bool = False) -> None:
        if warning:
            message = colour_string(message, 'red')
        print(message)

    def allow_ascii(self) -> bool:
        return True