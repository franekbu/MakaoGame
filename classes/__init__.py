# __init__.py simplifies the imports of the package
# thanks to this you don't have to code 'from classes.game import Game' and just can 'from classes import Game'

# importing classes
from .game import Game
from .player import Player, BotPlayer
from .cards import Card

# importing variables (consts)
from .dictionaries import NAMES, FUNCTIONS, COLOURS, CSV_HEADERS, DATA_DIR_PATH

# tells what will ve imported if * used
__all__ = ['Card', 'Player', 'BotPlayer', 'Game', 'NAMES', 'FUNCTIONS', 'COLOURS', 'CSV_HEADERS', 'DATA_DIR_PATH']

print("Module 'classes' was imported!") # telling if import was successful