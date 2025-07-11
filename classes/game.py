from classes.player import Player, BotPlayer
from classes import dictionaries as c_dict
from classes.utils import get_data_path
from classes.cards import Card
from datetime import datetime
import pandas as pd
import random
import os


class Game:
    def __init__(self, **names:list[str]):
        """available kwargs: players, bots\n
        Creates class that handles all logic in a game
        """
        self.players:list[Player|BotPlayer] = self._create_players(**names)
        self.finishers:list[Player|BotPlayer] = []
        self.main_deck:list[Card] = self._create_deck()
        self._dealing_cards()
        self.play_deck:list[Card] = [self._start_card()] # deck where you put cards you play
        self.colours = self._ingame_colours()
        self.demands:list[str|int|None] = [None]
        self.stack_pull:int = 0
        self.stack_frozen:int = 0
        self.stack_demands:int = 0 # how long demanding number or colour stands
        self.reverse_order:bool = False
        self.current_player:Player|BotPlayer = self.players[0]
        self.turn:int = 0
        self.game_data:list[dict[str,str|int|bool]] = []
        self.data_dir_path:str = get_data_path()

    # maybe upgrade it a little
    def __str__(self):
        return f'Game players: {[player.name for player in self.players]}'

    @staticmethod
    def _ingame_colours() -> list[str]:
        """Returns list of names of colours that are used in a game"""
        colours:list[str] = []
        for col in c_dict.COLOURS:
            colours.append(c_dict.COLOURS[col]['name'].lower())
            colours.append(c_dict.COLOURS[col]['symbol'])
        return colours

    @staticmethod
    def _create_deck() -> list[Card]:
        """Returns list of card, representing whole standard cards deck"""
        deck: list = []
        for num in range(2, 15):
            for colour in range(1, 5):
                deck.append(Card(num=num, colour_series=colour))
        return deck

    @staticmethod
    def _deck_to_print(deck_to_show:list[Card]) -> str:
        """Returns string of cards in chosen deck that is ready to be printed"""
        return ', '.join([f'{i + 1}:{card}' for i, card in enumerate(deck_to_show)])

    @staticmethod
    def _create_players(**pre_names:list[str]) -> list[Player | BotPlayer]:
        """available kwargs: players, bots\n
        If no kwargs used ask user what names and how may human or bot players he wants\n
        returns list of objects of players from class Player and BotPlayer
        """
        players_names:list[str] = []
        bots_names:list[str] = []
        if len(pre_names) > 0:
            try:
                if len(pre_names['players']) > 0:
                    for name in pre_names['players']:
                        while name in players_names:
                            print('You have present repetitive names')
                            print('Names cannot repeat!')
                            name = input(f'What is new {name} name?')
                        players_names.append(name)
            except KeyError:
                print('No humans players.')
            try:
                if len(pre_names['bots']) > 0:
                    for name in pre_names['bots']:
                        while name in players_names or name in bots_names:
                            print('You have present repetitive names')
                            print('Names cannot repeat!')
                            name = input(f'What is new {name} name?')
                        bots_names.append(name)
            except KeyError:
                print('No bots players.')
        else:
            num_players:int
            num_bots:int = 0
            play_with_bots:str = input('Do you want to play with bots?')
            if play_with_bots.lower() in ['yes', 'y']:
                try:
                    num_players = int(input('How many human players do you want to play?'))
                    num_bots = int(input('How many bots players do you want to play?'))
                    while num_players + num_bots < 2 or num_players + num_bots > 5:
                        print('Number of all players combined (humans and bots) must be within 2 and 5!')
                        num_players = int(input('How many human players do you want to play?'))
                        num_bots = int(input('How many bots players do you want to play?'))
                except ValueError:
                    print('You gave a letter not a number!')
                    print('There will be 1 human player and 1 bot.')
                    num_players = 1
                    num_bots = 1
            else:
                try:
                    num_players = int(input('How many players do you want to play?: '))
                    while num_players < 2 or num_players > 5:
                        print('Number of players must be within 2 and 5')
                        num_players = int(input('How many players do you want to play?: '))
                except ValueError:
                    print('You gave a letter not a number!')
                    print('There will be 2 players')
                    num_players = 2

            for num in range(num_players):
                name = input(f'What is {num + 1}. players name?')
                while name in players_names:
                    print('Names cannot repeat!')
                    name = input(f'What is new {num + 1}. players name?')
                players_names.append(name)

            for num in range(num_bots):
                name = input(f'What is {num + 1}. bot name?')
                while name in bots_names:
                    print('Names cannot repeat!')
                    name = input(f'What is new {num + 1}. bot name?')
                bots_names.append(name)

        players:list[Player] = [Player(player_name=name) for name in players_names]
        bots:list[BotPlayer] = [BotPlayer(bot_name=name) for name in bots_names]
        all_players:list[Player|BotPlayer] = players + bots

        if input('Do you want to shuffle the order of players?').lower() in ['yes', 'y']:
            random.shuffle(all_players)
        return all_players

    @staticmethod
    def _shuffle_deck(deck:list[Card]) -> None:
        """Just shuffle the deck"""
        random.shuffle(deck)

    def _dealing_cards(self):
        """Deals cards among players\n
        if number of players is grater than 3 deals each 5 cards, else 7
        """
        self._shuffle_deck(self.main_deck)
        if len(self.players) < 4:
            num_of_cards = 7
        else:
            num_of_cards = 5
        for num in range(0, num_of_cards):
            for player in self.players:
                card = self.main_deck.pop(0)
                player.deck.append(card)

    def _start_card(self) -> Card:
        """Chose from deck one card that is put at the start of play_deck\n
        card is non-functional and is not a King
        """
        card = random.choice(self.main_deck)
        while card.functional or card.name == 'King':
            card = random.choice(self.main_deck)
        self.main_deck.remove(card)
        return card

    def _pulled_cards(self, num_of_cards) -> list[Card]:
        """Returns list of cards for player to pull"""
        new_cards:list[Card] = []
        for num in range(0, num_of_cards):
            if len(self.main_deck) == 0:
                self._update_main_deck()
            try:
                new_cards.append(self.main_deck[0])
                self.main_deck.pop(0)
            except IndexError:
                print('You ran out of cards to pull\nPlay your damn cards!')
                return []
        return new_cards

    def _update_demands(self, num_cards_played:int) -> None:
        """Checks what demands new card has set and changes games demands according to them\n
            2/3/kings = ['add'] stack_pull+=,\n
            4 = ['pause'] stack_frozen +=,\n
            queen = [None] stacks = 0,\n
            jack/ace = ['number/colour', str(demanded_thing), str(rows demands stand)]
        """
        if self.play_deck[0].functional:
            # '2' or '3' or king♥ card played
            if self.play_deck[0].function[0] == 'add':
                self.demands = self.play_deck[0].function
                self.stack_pull += self.demands[1]
            # king♠ card played
            elif self.play_deck[0].function[0] == 'subtract':
                self.reverse_order = not self.reverse_order
                self.demands = ['add']
                self.stack_pull += 5
            # queen card played
            elif self.play_deck[0].function[0] == 'shield':
                self.stack_frozen = 0
                self.stack_pull = 0
                self.demands = [None]
            # '4' card played
            elif self.play_deck[0].function[0] == 'pause':
                self.demands = self.play_deck[0].function
                self.stack_frozen += 1
                print('demands == pause')
            elif self.play_deck[0].function[0] == 'demand':
                # jack card played
                if self.play_deck[0].function[1] == 'number':
                    if type(self.current_player) == BotPlayer:
                        self.demands = ['number', self.current_player.choosing_demands('number')]
                    else:
                        demanded_number:str = input('What number do you demand?: ')
                        while 4 > int(demanded_number) or int(demanded_number) > 10:
                            print(f'Wrong number!\nNumbers you can use demand are between 5 and 10')
                            demanded_number:str = input('So what number do you demand?: ')
                        self.demands = ['number', demanded_number]
                    self.stack_demands = len(self.players)
                # ace card played
                elif self.play_deck[0].function[1] == 'colour':
                    print(f'Available colours names: {self.colours}')
                    if type(self.current_player) == BotPlayer:
                        self.demands = ['colour', self.current_player.choosing_demands('colour')]
                    else:
                        demanded_color:str = input('What colour do you demand?: ').lower()
                        while demanded_color not in self.colours:
                            print(f'Wrong colour!\nColours you can use are: {self.colours}')
                            print('Do not use symbols!')
                            demanded_color:str = input('So what colour do you demand?: ').lower()
                        self.demands = ['colour', demanded_color.capitalize()]
                    self.stack_demands = len(self.players)
                else:
                    print('you fucked sth up on demand demands ')
                    raise ValueError
            else:
                print('you fucked up updating functional demands')
                raise ValueError

            if num_cards_played > 1:
                if self.demands[0] == 'pause':
                    self.stack_frozen += num_cards_played - 1
                elif self.demands[0] == 'add':
                    self.stack_pull += self.demands[1]*(num_cards_played - 1)

        elif self.demands[0] in ['colour', 'number']:
            if self.stack_demands > 1:
                self.stack_demands -= 1
            else:
                self.stack_demands = 0
                self.demands = [None]
        else:
            self.demands = [None]

    def _handle_player_move(self, player: Player | BotPlayer) -> None:
        """PLayer chooses and plays the cards and then if needed says makao"""
        # maybe call it playing card
        cards_to_play:list[Card] = player.choosing_card(self.play_deck[0], self.demands)
        for card in cards_to_play:
            self.play_deck.insert(0, card)
            player.deck.remove(card)

        self._update_demands(len(cards_to_play))

        if not player.say_makao():
            player.deck.extend(self._pulled_cards(5))

    def _update_main_deck(self) -> None:
        """Takes cards from overstacking play_deck and returns them to main_deck so players can pull them from it"""
        if len(self.main_deck) < 21:
            while len(self.play_deck) > 1:
                self.main_deck.append(self.play_deck[-1])
                self.play_deck.pop(-1)
        self._shuffle_deck(self.main_deck)

    def _next_player(self) -> None:
        """Sets new current player for a next round"""
        c_player =  self.players.index(self.current_player)
        if not self.reverse_order:
            try:
                self.current_player = self.players[c_player + 1]
            except IndexError:
                self.current_player = self.players[0]
        else:
            try:
                self.current_player = self.players[c_player - 1]
            except IndexError:
                self.current_player = self.players[-1]

    def _handle_finisher(self, player: Player | BotPlayer):
        """Removes player from active players list adds him to finishers and checks if demands len should be shortened"""
        # checking if he just played demands card
        if self.demands[0] in ['number', 'colour']:
            if self.stack_demands == len(self.players):
                self.stack_demands -= 1

        print('Congrats!!! You finished the game!')
        self.finishers.append(player)
        self.players.remove(player)

    def _handle_no_play_action(self, passed:bool) -> None:
        """Handles logic when player didnt have valid cards or passed his turn
        accordingly changes demands, stacks and decide how much player has to pull
        """
        player:Player|BotPlayer = self.current_player
        # TODO 2. Make available to play first pulled card if it can be played
        if self.demands[0] == 'pause':
            print('sleep begins')
            player.frozen_rows = self.stack_frozen - 1  # - 1 because already he is frozen in this round
            self.stack_frozen = 0
            self.demands = [None]

        elif self.demands[0] in ['number', 'colour']:
            player.deck.extend(self._pulled_cards(1))
            print(f'{player.name} did not have valid cards, he pulled new card')
            if self.stack_demands > 1:
                self.stack_demands -= 1
            else:
                self.stack_demands = 0
                self.demands = [None]

        elif self.stack_pull > 0:
            player.deck.extend(self._pulled_cards(self.stack_pull))
            print(f'{player.name} did not have valid cards, he pulled {self.stack_pull} new cards')
            self.stack_pull = 0
            self.demands = [None]

        else:
            player.deck.extend(self._pulled_cards(1))
            self.stack_pull = 0
            self.demands = [None]
            if passed:
                print(f'{player.name} did not want to play his cards, he pulled new one')
            else:
                print(f'{player.name} did not have valid cards, he pulled new card')

    def _display_turn_start_info(self) -> None:
        """Display info at the beginning of player's turn such as:\n
        - what card is on the table\n
        - what are demands\n
        - what is his deck
        """
        player:Player|BotPlayer = self.current_player
        print(f'Card on a table: {self.play_deck[0].name}{self.play_deck[0].symbol}')
        if self.demands[0] in ['number', 'colour']:
            print(f'Your are demanded to play: {self.demands[1]}')
        print(f'{player.name} this is your deck:\n{self._deck_to_print(player.deck)}')

    def _handle_frozen_player(self) -> None:
        """Handle cases when player was frozen at the start of his turn"""
        player:Player|BotPlayer = self.current_player
        print(f'{player.name} was frozen.')
        player.frozen_rows -= 1
        # skip his turn in demands to colour/number
        if self.demands[0] in ['number', 'colour']:
            if self.stack_demands > 1:
                self.stack_demands -= 1
            else:
                # can this even happen?
                self.stack_demands = 0
                self.demands = [None]

    def _player_turn(self, player: Player | BotPlayer) -> None:
        """All logic about player's turn"""

        player.played_card = False # have to reset it every new turn so if he dont make it wont show he did from the last turn
        was_frozen:bool = False
        start_deck_size:int = len(self.current_player.deck)
        start_top_card:Card = self.play_deck[0]

        self._display_turn_start_info()

        if player.frozen_rows > 0:
            was_frozen = True
            self._handle_frozen_player()
        else:
            player.have_valid_cards(self.play_deck[0], self.demands)
            pass_or_play:str = ''

            if player.valid_cards:
                pass_or_play = player.play_or_pass()

                if pass_or_play == 'play':
                    self._handle_player_move(player)
                    player.played_card = True

                elif pass_or_play == 'pass' and type(player) == BotPlayer:
                    print('Bot passes his turn.\n')

            if not player.valid_cards or pass_or_play == 'pass':
                self._handle_no_play_action(pass_or_play == 'pass')

        player.turn += 1
        self._collect_data(was_frozen, start_deck_size, start_top_card)
        self._next_player()

        if len(player.deck) == 0:
            self._handle_finisher(player)

    def start_game(self):
        """Starts the game and keeps it on until one player remains"""
        while len(self.players) > 1:
            self.turn += 1
            self._player_turn(self.current_player)

    def show_leaderboard(self):
        """Prints the leaderboard of the game - who had which place and who was last """
        for num, player in enumerate(self.finishers):
            print(f'{num + 1}. place takes: {player.name}')
        print(f'Last place takes: {self.players[0].name}')

    def _collect_data(self, frozen_before:bool, deck_size_before:int, top_card_before:Card) -> None:
        """Takes few datas from the beginning of the turn as arguments, then collects actual data and saves it as dict"""
        turn_data:dict[str,str|int|bool|None] = {
            'Game_move': self.turn,
            'Player_name': self.current_player.name,
            'Is_bot': type(self.current_player) == BotPlayer,
            'Player_turn': self.current_player.turn,
            'Is_finished': len(self.current_player.deck) == 0,
            'Final_place': None,
            'Is_frozen': frozen_before,
            'Player_deck_size': deck_size_before,
            'Top_card_met': str(top_card_before),
            'Played_cards_count': 0,
            'Played_cards_names': '',
            'Pulled_cards_count': 0,
            'Pulled_cards_names': '',
            'Is_card_functional': self.play_deck[0].functional,
            'Card_function': None,
            'Demanded_num': None,
            'Demanded_col': None,
        }

        if len(self.current_player.deck) == 0:
            turn_data['Final_place'] = len(self.finishers) + 1

        if self.current_player.played_card:
            cards_played:int = deck_size_before - len(self.current_player.deck)
            # Normal case
            if cards_played > 0:
                turn_data['Played_cards_count'] = cards_played
                turn_data['Played_cards_names'] = '|'.join([str(self.play_deck[i]) for i in range(cards_played)])
            # didn't say makao
            elif cards_played < 0:
                turn_data['Played_cards_count'] = cards_played + 5
                turn_data['Played_cards_names'] = '|'.join([str(self.play_deck[i]) for i in range(cards_played + 5)])
                turn_data['Pulled_cards_count'] = 5
                turn_data['Pulled_cards_names'] = '|'.join([str(self.current_player.deck[-i]) for i in range(1, 6)])

            else:
                raise Exception('Player played a card but len of his deck didnt change!')

            if self.play_deck[0].functional:
                turn_data['Card_function'] = self.play_deck[0].function[0]

                if self.play_deck[0].function[1] == 'number':
                    turn_data['Demanded_num'] = self.demands[1]

                elif self.play_deck[0].function[1] == 'colour':
                    turn_data['Demanded_col'] = self.demands[1]

        elif not frozen_before:
            card_pulled:int = len(self.current_player.deck) - deck_size_before
            turn_data['Pulled_cards_count'] = card_pulled
            turn_data['Pulled_cards_names'] = '|'.join([str(self.current_player.deck[-i]) for i in range(1, card_pulled + 1)])

        self.game_data.append(turn_data)

    def save_data(self) -> None:
        """Takes list of dicts of data saved from game turns and saves it in .csv file"""
        df = pd.DataFrame(self.game_data, columns=c_dict.CSV_HEADERS)
        df.to_csv(path_or_buf=self._data_file_path(), sep=';', encoding='UTF-8', index=False, header=True)

    def _data_file_path(self) -> str:
        """Returns path where to save data files\n
        Path is set relatively to where method is called for example in main.py\n
        to change that change self.data_dir_path in self.__init__()
        """
        os.makedirs(self.data_dir_path, exist_ok=True)
        base_timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        return f'{self.data_dir_path}/{base_timestamp}.csv'