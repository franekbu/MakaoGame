# __init__.py simplifies the imports of the package
# thanks to this you don't have to code 'from classes.game import Game' and just can 'from classes import Game'

# importing classes
from .game import Game
from .player import Player, BotPlayer
from .cards import Card
from .utils import get_data_path, colour_string

# importing variables (consts)
from .dictionaries import (NAMES, FUNCTIONS, COLOURS, CSV_HEADERS, DATA_DIR_NAME, MAX_NUM_OF_PLAYERS,
                           ASCII_COLOURS, ASCII_END, ASCII_START)

# tells what will ve imported if * used
__all__ = ['Card', 'Player', 'BotPlayer', 'Game', 'get_data_path', 'colour_string', 'NAMES', 'FUNCTIONS', 'COLOURS',
           'CSV_HEADERS', 'DATA_DIR_NAME', 'MAX_NUM_OF_PLAYERS', 'ASCII_START', 'ASCII_END', 'ASCII_COLOURS']

print("Module 'makao_game' was imported!") # telling if import was successful