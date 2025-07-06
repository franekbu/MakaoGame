NUMERIC_CARDS:dict = {num:f'{num}' for num in range(2,11)}
HIGH_CARDS:dict = {
    11: 'Jack',
    12: 'Queen',
    13: 'King',
    14: 'Ace'}

NAMES:dict = NUMERIC_CARDS | HIGH_CARDS
# | merges two dictionaries

COLOURS:dict = {
    1: {'name': 'Clubs', 'symbol': '♣'},
    2: {'name': 'Diamonds', 'symbol': '♦'},
    3: {'name': 'Hearts', 'symbol': '♥'},
    4: {'name': 'Spades', 'symbol': '♠'}
}
# pik i kier musza byc 3 i 4, niewazna kolejnosc

FUNCTIONS:dict = {
    2: ['add', 2],
    3: ['add', 3],
    4: ['pause', 1],
    11: ['demand', 'number'],
    12: ['shield', 0],
    13: {
        'Hearts': ['add', 5],
        'Spades': ['subtract', 5]
    },
    14: ['demand', 'colour']
}

CSV_HEADERS:list[str] = ['Game_move','Player_name','Is_bot','Player_turn','Is_finished','Final_place','Is_frozen',
                         'Player_deck_size','Played_cards_count','Played_cards_names','Pulled_cards_count',
                         'Pulled_cards_names','Top_card_met','Is_card_functional','Card_function',
                         'Demanded_num','Demanded_colour']

DATA_DIR_NAME:str = 'game_data'

MAX_NUM_OF_PLAYERS:int = 5
