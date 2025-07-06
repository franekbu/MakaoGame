# __init__.py simplifies the imports of the package
# thanks to this you don't have to code 'from classes.game import Game' and just can 'from classes import Game'

# importing classes
from .game import Game
from .player import Player, BotPlayer
from .cards import Card
from .utils import get_data_path

# importing variables (consts)
from .dictionaries import NAMES, FUNCTIONS, COLOURS, CSV_HEADERS, DATA_DIR_NAME

# tells what will ve imported if * used
__all__ = ['Card', 'Player', 'BotPlayer', 'Game', 'get_data_path', 'NAMES', 'FUNCTIONS', 'COLOURS', 'CSV_HEADERS', 'DATA_DIR_NAME']

print("Module 'classes' was imported!") # telling if import was successful