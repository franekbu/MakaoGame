from __future__ import annotations
from typing import Type, Any
from enum import Enum

MAIN_COMMAND: str = 'makao'

EXAMPLE: str = 'makao play --cards "1,2,3" -d "diamonds" --makao'

class FLAGS(Enum):
    MAKAO = ('makao', None, False, "use to declare makao,")
    AFTER_MAKAO = ('after-makao', None, False, "use to declare after makao,")
    DEMAND = ('demand', 'd', True, "use to set what you demand,")
    CARDS = ('cards', 'c', True, "use to say which cards you play,")
    PLAYERS = ('players', None, True, "use to say who's gonna play,")
    BOTS = ('bots', None, True, "use to say how many bots of which names're gonna play,")
    END = ('kill', 'k', False, "same as sub_command,")

    def __init__(self, long_flag: str, short_flag: str | None, takes_args: bool, description: str) -> None:
        self._long_flag: str = long_flag
        self._short_flag: str | None = short_flag
        self._takes_args: bool = takes_args
        self._description: str = description

    @classmethod
    def _missing_(cls: Type[FLAGS], value: Any) -> FLAGS | None:
        if isinstance(value, str):
            for member in cls:
                if value == member._long_flag or value == member._short_flag:
                    return member
        return None

    @property
    def long_flag(self) -> str:
        return self._long_flag

    @property
    def short_flag(self) -> str | None:
        return self._short_flag
    
    @property
    def takes_args(self) -> bool:
        return self._takes_args
    
    @property
    def description(self) -> str:
        return self._description + f'-{self._short_flag,}'


class SUB_COMMANDS(Enum):
    START = ('start', [FLAGS.PLAYERS, FLAGS.BOTS], "starts a game with provided players' mentions and bots names")
    SAVE = ('save', [FLAGS.END], "save game progress, so it can be continued from that moment in the future")
    END = ('kill', None, "ends game without saving progress")
    PLAY = ('play', [FLAGS.CARDS, FLAGS.DEMAND, FLAGS.MAKAO, FLAGS.AFTER_MAKAO], "play your turn")
    PASS = ('pass', None, "pass your turn")
    UPDATE = ('update', [FLAGS.DEMAND, FLAGS.MAKAO, FLAGS.AFTER_MAKAO], "if any needed data wasn't provided by flags earlier, use this to update it when asked")
    INFO = ('info', None, "display info about game")
    HELP = ('help', None, "display sub_commands and flags instructions")

    def __init__(self, name_: str, sup_flags: list[FLAGS] | None, description: str) -> None:
        self._name_str: str = name_
        self._sup_flags: list[FLAGS] | None = sup_flags
        self._description: str = description

    @classmethod
    def _missing_(cls: Type[SUB_COMMANDS], value: Any) -> SUB_COMMANDS | None:
        if isinstance(value, str):
            for member in cls:
                if value == member._name_str:
                    return member
        return None

    @property
    def name_str(self) -> str:
        return self._name_str
  
    @property
    def sup_flags(self) -> list[FLAGS] | None:
        return self._sup_flags
    
    @property
    def description(self) -> str:
        return self._description
