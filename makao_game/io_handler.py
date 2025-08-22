from abc import ABC, abstractmethod

class IOHandler(ABC):
    @abstractmethod
    def get_user_input(self, message: str) -> str:
        """Takes user's input and returns it"""
        pass

    @abstractmethod
    def display_message(self, message: str) -> None:
        """Displays message to user"""
        pass


class ConsoleIOHandler(IOHandler):
    def get_user_input(self, message: str) -> str:
        user_input: str = input(message)
        return user_input

    def display_message(self, message: str) -> None:
        print(message)