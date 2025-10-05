import asyncio
from datetime import datetime
import pandas as pd  # type: ignore
import random
import os

from makao_game.player import Player, BotPlayer
from makao_game import dictionaries as c_dict
from makao_game.utils import get_data_path
from makao_game.cards import Card
from makao_game.cards_actions import CardsActions
from makao_game.io_handler import IOHandler, IODataType, ConsoleIOHandler

class Game:
    def __init__(self, 
                io_handler: IOHandler = ConsoleIOHandler(), 
                data_dir_path: str = get_data_path(), 
                **names: list[str]) -> None:
        
        """available kwargs: players, bots\n
        Creates class that handles all logic in a game
        """
        self.io_handler: IOHandler = io_handler

        self._names: dict[str, list[str]] = names
        self._players: list[Player | BotPlayer] = []
        self._current_player: Player | BotPlayer | None = None
        self._finishers: list[Player | BotPlayer] = []

        self._main_deck: list[Card] = []
        self._play_deck: list[Card] = []
        self._actions: CardsActions = CardsActions()

        self._turn: int = 0
        self._game_data: list[dict[str, str | int | bool | None]] = []
        self._data_dir_path: str = data_dir_path

    def __str__(self):
        return f'Game players: {[player.name for player in self._players]}'

    async def run_game(self):
        """Starts the game and keeps it on until one player remains"""
        await self._prepare_game()
        while len(self._players) > 1:
            self._turn += 1

            assert isinstance(self._current_player, Player | BotPlayer)
            await self._player_turn(self._current_player)

    async def _prepare_game(self) -> None:
        self._players = (await asyncio.gather(self._handle_players_creation()))[0]
        self._current_player = self._players[0]

        self._main_deck = self._create_deck()
        self._dealing_cards()
        self._play_deck = [self._start_card()]

    async def _handle_players_creation(self) -> list[Player | BotPlayer]:
        """available kwargs: players, bots\n
        If no kwargs used ask user what names and how may human or bot players he wants\n
        returns list of objects of players from class Player and BotPlayer
        """
        all_players: list[Player | BotPlayer]
        if self._names:
            all_players = self._create_players_from_kwargs(
                pre_players_names=self._names.get('players', []),
                pre_bots_names=self._names.get('bots', []))
        else:
            all_players = await self._create_input_players()

        shuffle: str = await self.io_handler.get_user_input(
            data_type=IODataType.YES_NO,
            username=None,
            message='Do you want to shuffle the order of players?'
        )
        if shuffle.lower() in ['yes', 'y']:
            random.shuffle(all_players)
        return all_players

    def _create_players_from_kwargs(self, pre_players_names: list[str], pre_bots_names: list[str]) -> list[Player | BotPlayer]:
        """Checks if names from kwargs pass conditions, then creates from them players and bots and returns them"""
        len_p: int = len(pre_players_names)
        len_b: int = len(pre_bots_names)
        non_duplicated_names: set[str] = set(pre_players_names + pre_bots_names)

        if len_p + len_b < 2 or len_p + len_b > c_dict.MAX_NUM_OF_PLAYERS:
            raise ValueError('Too many or too little bots and players names given as kwargs!')
        elif len(non_duplicated_names) != len_b + len_p:
            raise ValueError('Duplicated names provided!')
        else:
            players: list[Player] = []
            bots: list[BotPlayer] = []

            for name in pre_players_names:
                players.append(
                    Player(
                        player_name=name,
                        io_handler=self.io_handler
                    )
                )

            for name in pre_bots_names:
                bots.append(
                    BotPlayer(
                        bot_name=name,
                        io_handler=self.io_handler
                    )
                )

        return [*players, *bots]

    async def _create_input_players(self) -> list[Player | BotPlayer]:
        """Ask player how many players: human or bot, he wants to play, and returns the list of them"""

        play_with_bots: str = await self.io_handler.get_user_input(
            data_type=IODataType.YES_NO,
            username=None,
            message='Do you want to play with bots?'
        )
        num_players: int = 0
        num_bots: int = 0
        if play_with_bots.lower() in ['y', 'yes']:
            while True:
                try:
                    num_players = int(await self.io_handler.get_user_input(
                        data_type=IODataType.GAME,
                        username=None,
                        message='How many human players do you want to play?')
                    )
                    num_bots = int(await self.io_handler.get_user_input(
                        data_type=IODataType.GAME,
                        username=None,
                        message='How many bots players do you want to play?')
                    )
                    if num_players + num_bots < 2 or num_players + num_bots > c_dict.MAX_NUM_OF_PLAYERS:
                        await self.io_handler.display_message(
                            message='Number of all players combined (humans and bots) must be within 2 and {c_dict.MAX_NUM_OF_PLAYERS}!',
                            warning=True
                        )
                    else:
                        break

                except ValueError:
                    await self.io_handler.display_message(
                        message='Invalid input!\nPlease input only numbers',
                        warning=True
                    )
                    continue
        else:
            while True:
                try:
                    num_players = int(await self.io_handler.get_user_input(
                        data_type=IODataType.GAME,
                        username=None,
                        message='How many human players do you want to play?')
                    )
                    if num_players < 2 or num_players > c_dict.MAX_NUM_OF_PLAYERS:
                        await self.io_handler.display_message(
                            message=f'Number of all players must be within 2 and {c_dict.MAX_NUM_OF_PLAYERS}!',
                            warning=True
                        )
                    else:
                        break

                except ValueError:
                    await self.io_handler.display_message(
                        message='Invalid input!\nPlease input only numbers',
                        warning=True
                    )
                    continue

        used_names: list[str] = []
        players: list[Player] = []
        bots: list[BotPlayer] = []

        name: str
        for i in range(num_players):
            name = await self.io_handler.get_user_input(
                data_type=IODataType.GAME,
                username=None,
                message=f'What is {i + 1}. player name?'
            )
            while name.replace(" ", "") in used_names:
                await self.io_handler.display_message(
                    message='Names cannot repeat!',
                    warning=True
                )
                name = await self.io_handler.get_user_input(
                    data_type=IODataType.GAME,
                    username=None,
                    message=f'What is {i + 1}. player name?'
                )
            players.append(
                Player(
                    player_name=name,
                    io_handler=self.io_handler
                )
            )
            used_names.append(name)

        for i in range(num_bots):
            name = await self.io_handler.get_user_input(
                data_type=IODataType.GAME,
                username=None,
                message=f'What is {i + 1}. bot name?'
            )
            while name.replace(" ", "") in used_names:
                await self.io_handler.display_message(
                    message='Names cannot repeat!',
                    warning=True
                )
                name = await self.io_handler.get_user_input(
                    data_type=IODataType.GAME,
                    username=None,
                    message=f'What is {i + 1}. bot name?'
                )
            bots.append(
                BotPlayer(
                    bot_name=name,
                    io_handler=self.io_handler
                )
            )
            used_names.append(name)

        return [*players, *bots]

    def _create_deck(self) -> list[Card]:
        """Returns list of card, representing whole standard cards deck"""
        deck: list = []
        symbols: dict[str, str] = self.io_handler.supported_symbols()
        for num in range(2, 15):
            for colour in range(1, 5):
                deck.append(
                    Card(
                        num=num,
                        colour_series=colour,
                        display_symbols=symbols
                    )
                )
        return deck

    def _dealing_cards(self):
        """Deals cards among players\n
        if number of players is grater than 3 deals each 5 cards, else 7
        """
        random.shuffle(self._main_deck)
        if len(self._players) < 4:
            num_of_cards = 7
        else:
            num_of_cards = 5
        for num in range(0, num_of_cards):
            for player in self._players:
                card = self._main_deck.pop(0)
                player.deck.append(card)

    def _start_card(self) -> Card:
        """Chose from deck one card that is put at the start of play_deck\n
        card is non-functional and is not a King
        """
        card = random.choice(self._main_deck)
        while isinstance(card.function, tuple) or card.name == 'King':
            card = random.choice(self._main_deck)
        self._main_deck.remove(card)
        return card

    async def _player_turn(self, player: Player | BotPlayer) -> None:
        """All logic about player's turn"""

        player.played_card = False # have to reset it every new turn so if he doesn't make it won't show he did from the last turn
        was_frozen: bool = False
        start_deck_size: int = len(player.deck)
        start_top_card: Card = self._play_deck[0]

        await self._display_turn_start_info()

        if player.frozen_rows > 0:
            was_frozen = True
            await self._handle_frozen_player()
        else:
            player.have_valid_cards(self._play_deck[0], self._actions)
            pass_or_play: str = ''

            if player.valid_cards:
                pass_or_play = await player.play_or_pass()

                if pass_or_play == 'play':
                    await self._handle_player_move()
                    player.played_card = True

                elif pass_or_play == 'pass' and isinstance(player, BotPlayer):
                    await self.io_handler.display_message(
                        message='Bot passes his turn.\n'
                    )

            if not player.valid_cards or pass_or_play == 'pass':
                await self._handle_no_play_action(pass_or_play == 'pass')

        player.turn += 1
        self._collect_data(was_frozen, start_deck_size, start_top_card)
        self._next_player()

        if len(player.deck) == 0:
            await self._handle_finisher(player)

    async def _display_turn_start_info(self) -> None:
        """Display info at the beginning of player's turn such as:\n
        - what card is on the table\n
        - what are demands\n
        - what is his deck
        """
        assert isinstance(self._current_player, Player | BotPlayer)
        player: Player | BotPlayer = self._current_player

        await self.io_handler.display_message(
            message=f'Card on a table: {self._play_deck[0]}'
        )
        if self._actions.action_type == c_dict.FUNCTIONS_TYPES_NAMES['DEMAND']:
            await self.io_handler.display_message(
                message=f'Your are demanded to play: {self._actions.demanded_value}'
            )
        await self.io_handler.display_message(
            message=f'{player.name} this is your deck:\n{self._deck_to_print(player.deck)}'
        )

    @staticmethod
    def _deck_to_print(deck_to_show: list[Card]) -> str:
        """Returns string of cards in chosen deck that is ready to be printed"""
        return ', '.join([f'{i + 1}:{card}' for i, card in enumerate(deck_to_show)])

    async def _handle_frozen_player(self) -> None:
        """Handle cases when player was frozen at the start of his turn"""
        assert isinstance(self._current_player, Player | BotPlayer)
        player: Player | BotPlayer = self._current_player

        await self.io_handler.display_message(
            message=f'{player.name} was frozen.'
        )
        player.frozen_rows -= 1
        # skip his turn in demands to colour/number
        if self._actions.action_type == c_dict.FUNCTIONS_TYPES_NAMES['DEMAND']:
            if self._actions.demands_duration > 1:
                self._actions.demands_duration -= 1
            else:
                # can this even happen?
                self._actions.reset_actions()

    async def _handle_player_move(self) -> None:
        """PLayer chooses and plays the cards and then if needed says makao"""
        assert isinstance(self._current_player, Player | BotPlayer)
        player: Player | BotPlayer = self._current_player

        cards_to_play: list[Card] = await player.choose_card(self._play_deck[0], self._actions)
        for card in cards_to_play:
            self._play_deck.insert(0, card)
            player.deck.remove(card)

        self._actions.apply_card_effects(self._play_deck[0].function, len(cards_to_play), len(self._players))
        if self._actions.update_player_inputs:
            assert isinstance(self._actions.demanded_type, str)
            demand: str = await player.handle_demanding(self._actions.demanded_type)
            self._actions.update_actions_with_player_inputs(demand)

        if not await player.say_makao():
            player.deck.extend(await self._pull_cards(5))

    async def _handle_no_play_action(self, passed: bool) -> None:
        """Handles logic when player didn't have valid cards or passed his turn
        accordingly changes demands, stacks and decide how much player has to pull
        """
        assert isinstance(self._current_player, Player | BotPlayer)
        player: Player | BotPlayer = self._current_player
        # TODO 2. Make available to play first pulled card if it can be played
        if self._actions.action_type == c_dict.FUNCTIONS_TYPES_NAMES['FREEZE']:
            player.frozen_rows = self._actions.freeze_stack - 1  # - 1 because already he is frozen in this round
            self._actions.reset_actions()

        elif self._actions.action_type == c_dict.FUNCTIONS_TYPES_NAMES['DEMAND']:
            player.deck.extend(await self._pull_cards(1))
            await self.io_handler.display_message(
                message=f'{player.name} did not have valid cards, he pulled new card'
            )
            if self._actions.demands_duration > 1:
                self._actions.demands_duration -= 1
            else:
                self._actions.reset_actions()

        elif self._actions.action_type == c_dict.FUNCTIONS_TYPES_NAMES['PULL']:
            player.deck.extend(await self._pull_cards(self._actions.pull_stack))
            await self.io_handler.display_message(
                message=f'{player.name} did not have valid cards, he pulled {self._actions.pull_stack} new cards'
            )
            self._actions.reset_actions()

        else:
            player.deck.extend(await self._pull_cards(1))
            self._actions.reset_actions()
            if passed:
                await self.io_handler.display_message(
                    message=f'{player.name} did not want to play his cards, he pulled new one'
                )
            else:
                await self.io_handler.display_message(
                    message=f'{player.name} did not have valid cards, he pulled new card'
                )

    def _next_player(self) -> None:
        """Sets new current player for a next round"""
        assert isinstance(self._current_player, Player | BotPlayer)
        c_player =  self._players.index(self._current_player)
        if not self._actions.reversed_order:
            try:
                self._current_player = self._players[c_player + 1]
            except IndexError:
                self._current_player = self._players[0]
        else:
            try:
                self._current_player = self._players[c_player - 1]
            except IndexError:
                self._current_player = self._players[-1]

    async def _handle_finisher(self, player: Player | BotPlayer):
        """Removes player from active players list adds him to finishers and checks if demands len should be shortened"""
        # checking if he just played demands card
        if (self._actions.action_type == c_dict.FUNCTIONS_TYPES_NAMES['DEMAND'] and
                self._actions.demands_duration == len(self._players)):
            self._actions.demands_duration -= 1

        await self.io_handler.display_message(
            message='Congrats!!! You finished the game!',
            warning=True
        )
        self._finishers.append(player)
        self._players.remove(player)

    async def _pull_cards(self, num_of_cards) -> list[Card]:
        """Returns list of cards for player to pull"""
        new_cards: list[Card] = []
        for num in range(0, num_of_cards):
            if len(self._main_deck) == 0:
                self._update_main_deck()
            try:
                new_cards.append(self._main_deck[0])
                self._main_deck.pop(0)
            except IndexError:
                await self.io_handler.display_message(
                    message='You ran out of cards to pull\nPlay your damn cards!',
                    warning=True
                )
                return []
        return new_cards

    def _update_main_deck(self) -> None:
        """Takes cards from overstocking play_deck and returns them to main_deck so players can pull them from it"""
        if len(self._main_deck) < 21:
            while len(self._play_deck) > 1:
                self._main_deck.append(self._play_deck[-1])
                self._play_deck.pop(-1)
        random.shuffle(self._main_deck)

    def _collect_data(self, frozen_before: bool, deck_size_before: int, top_card_before: Card) -> None:
        """Takes few data from the beginning of the turn as arguments, then collects actual data and saves it as dict"""
        assert isinstance(self._current_player, Player | BotPlayer)
        turn_data: dict[str, str | int | bool | None] = {
            'Game_move': self._turn,
            'Player_name': self._current_player.name,
            'Is_bot': isinstance(self._current_player, BotPlayer),
            'Player_turn': self._current_player.turn,
            'Is_finished': len(self._current_player.deck) == 0,
            'Final_place': None,
            'Is_frozen': frozen_before,
            'Player_deck_size': deck_size_before,
            'Top_card_met': repr(top_card_before),
            'Played_cards_count': 0,
            'Played_cards_names': '',
            'Pulled_cards_count': 0,
            'Pulled_cards_names': '',
            'Is_card_functional': isinstance(self._play_deck[0].function, tuple),
            'Card_function': None,
            'Demanded_num': None,
            'Demanded_col': None,
        }

        if len(self._current_player.deck) == 0:
            turn_data['Final_place'] = len(self._finishers) + 1

        if self._current_player.played_card:
            cards_played: int = deck_size_before - len(self._current_player.deck)
            # Normal case
            if cards_played > 0:
                turn_data['Played_cards_count'] = cards_played
                turn_data['Played_cards_names'] = '|'.join([repr(self._play_deck[i]) for i in range(cards_played)])
            # didn't say makao
            elif cards_played < 0:
                turn_data['Played_cards_count'] = cards_played + 5
                turn_data['Played_cards_names'] = '|'.join([repr(self._play_deck[i]) for i in range(cards_played + 5)])
                turn_data['Pulled_cards_count'] = 5
                turn_data['Pulled_cards_names'] = '|'.join([repr(self._current_player.deck[-i]) for i in range(1, 6)])

            else:
                raise ValueError("Player played a card but len of his deck didn't change!")

            if isinstance(self._play_deck[0].function, tuple):
                turn_data['Card_function'] = self._play_deck[0].function[0]

                if self._play_deck[0].function[1] == c_dict.DEMAND_OPTIONS_NAMES['JACK']:
                    turn_data['Demanded_num'] = self._actions.demanded_value

                elif self._play_deck[0].function[1] == c_dict.DEMAND_OPTIONS_NAMES['ACE']:
                    turn_data['Demanded_col'] = self._actions.demanded_value

        elif not frozen_before:
            card_pulled: int = len(self._current_player.deck) - deck_size_before
            turn_data['Pulled_cards_count'] = card_pulled
            turn_data['Pulled_cards_names'] = '|'.join([repr(self._current_player.deck[-i]) for i in range(1, card_pulled + 1)])

        self._game_data.append(turn_data)

    async def show_leaderboard(self):
        """Prints the leaderboard of the game - who had which place and who was last """
        for num, player in enumerate(self._finishers):
            await self.io_handler.display_message(
                message=f'{num + 1}. place takes: {player.name}'
            )
        await self.io_handler.display_message(
            message=f'Last place takes: {self._players[0].name}'
        )

    def save_data(self) -> None:
        """Takes list of dicts of data saved from game turns and saves it in .csv file"""
        df: pd.DataFrame = pd.DataFrame(self._game_data, columns=c_dict.CSV_HEADERS)
        df.to_csv(path_or_buf=self._data_file_path(), sep=';', encoding='UTF-8', index=False, header=True)

    def _data_file_path(self) -> str:
        """Returns path where to save data files\n
        Path is set relatively to where method is called for example in main.py\n
        to change that change self.data_dir_path in self.__init__()
        """
        os.makedirs(self._data_dir_path, exist_ok=True)
        base_timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        return f'{self._data_dir_path}/{base_timestamp}.csv'

    def get_game_status(self) -> dict[str, str | list[str]]:
        """
            Returns dict with data of current state of game\n
            Provided data:
            - top card,
            - current player,
            - players,
            - finishers,
            - turn,
        """
        return {
            'top_card': str(self._play_deck[0]) if self._play_deck else 'None',
            'current_player': self._current_player.name if self._current_player else 'None',
            'players': [player.name for player in self._players],
            'finishers': [player.name for player in self._finishers],
            'turn_number': str(self._turn),
        }