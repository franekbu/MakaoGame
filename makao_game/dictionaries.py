NUMERIC_CARDS: dict[int, str] = {num:f'{num}' for num in range(2,11)}
HIGH_CARDS: dict[int, str] = {
    11: 'Jack',
    12: 'Queen',
    13: 'King',
    14: 'Ace'}

NAMES: dict[int, str] = NUMERIC_CARDS | HIGH_CARDS
# | merges two dictionaries

COLOURS: dict[int, dict[str, str]] = {
    1: {'name': 'Clubs', 'symbol': '♣'},
    2: {'name': 'Diamonds', 'symbol': '♦'},
    3: {'name': 'Hearts', 'symbol': '♥'},
    4: {'name': 'Spades', 'symbol': '♠'}
}
# pik i kier muszą być 3 i 4, nieważna kolejność

FUNCTIONS_TYPES_NAMES: dict[str, str] = {
    'PULL': 'pull',
    'FREEZE': 'freeze',
    'DEMAND': 'demand',
    'ABOLISH': 'abolish',
    'REVERSE': 'reverse',
}

FUNCTIONS_DESCRIPTIONS: dict[str, str] = {
    'PULL': 'draw cards',
    'FREEZE': "can't play for a turn",
    'DEMAND': 'demand',
    'ABOLISH': 'abolish previous actions',
    'REVERSE': 'reverse order of turns and draw cards',
}

DEMAND_OPTIONS_NAMES: dict[str, str] = {
    'JACK': 'number',
    'ACE': 'colour'
}

FUNCTIONS: dict[int, tuple[str, str | int] | dict[str, tuple[str, str | int]]] = {
    2: (FUNCTIONS_TYPES_NAMES['PULL'], 2),
    3: (FUNCTIONS_TYPES_NAMES['PULL'], 3),
    4: (FUNCTIONS_TYPES_NAMES['FREEZE'], 1),
    11: (FUNCTIONS_TYPES_NAMES['DEMAND'], DEMAND_OPTIONS_NAMES['JACK']),
    12: (FUNCTIONS_TYPES_NAMES['ABOLISH'], 0),
    13: {
        'Hearts': (FUNCTIONS_TYPES_NAMES['PULL'], 5),
        'Spades': (FUNCTIONS_TYPES_NAMES['REVERSE'], 5),
    },
    14: (FUNCTIONS_TYPES_NAMES['DEMAND'], DEMAND_OPTIONS_NAMES['ACE']),
}

CSV_HEADERS: list[str] = ['Game_move','Player_name','Is_bot','Player_turn','Is_finished','Final_place','Is_frozen',
                         'Player_deck_size','Played_cards_count','Played_cards_names','Pulled_cards_count',
                         'Pulled_cards_names','Top_card_met','Is_card_functional','Card_function',
                         'Demanded_num','Demanded_col']

DATA_DIR_NAME: str = 'game_data'

MAX_NUM_OF_PLAYERS: int = 6

ASCII_START: str = '\033['
ASCII_END: str = '\033[0m'
ASCII_COLOURS: dict[str, str] = {
    'red': '31',
    'black': '30',
    'bg': '47',
    'yellow': '33'
}
