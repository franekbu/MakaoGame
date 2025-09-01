import random
# from time import sleep

from makao_game.cards import Card
from makao_game.dictionaries import COLOURS, DEMAND_OPTIONS_NAMES
from makao_game.cards_actions import CardsActions
from makao_game.io_handler import IOHandler

class Player:
    def __init__(self, player_name: str, io_handler: IOHandler) -> None:
        """Creates object that represents player in a game"""
        self.name: str = player_name
        self.deck: list[Card] = []
        self.frozen_rows: int = 0
        self.valid_cards: bool = False
        self.io_handler: IOHandler = io_handler
        self.turn: int = 0
        self.played_card: bool = False

    async def play_or_pass(self) -> str:
        """Ask player if he wants to play in this turn or pass it, returns his answer"""
        response: str = await (self.io_handler.get_user_input('Do you want to play or pass? '))
        # response = response.lower()
        while response.lower() not in ['pass', 'play']:
            await self.io_handler.display_message(
                message='You can only write: pass, play',
                warning=True
            )
            response = await self.io_handler.get_user_input('So what do you do? ')
        return response

    def have_valid_cards(self, cur_card:Card, game_actions: CardsActions) -> None:
        """Checks if player has valid cards and changes his attribute self.valid_cards"""
        for card in self.deck:
            if card.can_be_played(cur_card, game_actions):
                self.valid_cards = True
                return None
        self.valid_cards = False
        return None

    async def _choose_colour_demands(self) -> str:
        """Ask player what colour he wants to demand and returns it"""
        available_colours: list[tuple[str, str]] = [
            (COLOURS[col]['name'].capitalize(), COLOURS[col]['symbol']) for col in COLOURS
        ]
        names_of_colours: list[str] = [COLOURS[col]['name'].capitalize() for col in COLOURS]

        await self.io_handler.display_message(
            message=f'Available colours names: {available_colours}'
        )
        demanded_color: str = await self.io_handler.get_user_input('What colour do you demand?: ')

        while demanded_color.capitalize() not in names_of_colours:
            await self.io_handler.display_message(
                message=f'Wrong colour!\nColours you can use are: {available_colours}\nDo not use symbols!',
                warning=True
            )
            demanded_color = await self.io_handler.get_user_input('So what colour do you demand?: ')

        return demanded_color

    async def _choose_number_demands(self) -> str:
        """Ask player what number he wants to demand and returns it"""
        demanded_number: str
        while True:
            try:
                demanded_number = await self.io_handler.get_user_input('What number do you demand?: ')
                while 4 > int(demanded_number) or int(demanded_number) > 10:
                    await self.io_handler.display_message(
                        message='Wrong number!\nNumbers you can demand are between 5 and 10',
                        warning=True
                    )
                    demanded_number = await self.io_handler.get_user_input('So what number do you demand?: ')
                return demanded_number
            except ValueError:
                await self.io_handler.display_message(
                    message='Typed char must be an int!',
                    warning=True
                )

    async def handle_demanding(self, demand_type: str) -> str:
        """Accordingly to what demand is needed, runs choose_number_demands or choose_colour_demands"""
        if demand_type == DEMAND_OPTIONS_NAMES['JACK']:
            return  await self._choose_number_demands()
        elif demand_type == DEMAND_OPTIONS_NAMES['ACE']:
            return await self._choose_colour_demands()
        else:
            raise ValueError('wrong demand type, passed is nor Jack or Ace')

    async def choose_card(self, cur_card: Card, game_actions: CardsActions) -> list[Card]:
        """Gives player a choice which card/s he wants to play and returns list of them"""
        # TODO 3. Add possibility to pass even after saying play
        async def _cards_from_deck() -> list[int]:
            # checking if cards are in deck
            suc_choice: bool = False
            chosen_nums: list[int] = []
            while not suc_choice:
                p_choice: str = await self.io_handler.get_user_input(
                    message='What card/s you want to play?(give number/s of card/s): '
                )
                p_nums: list[str]
                if ',' in p_choice:
                    p_nums = p_choice.split(',')
                    while len(p_nums) not in [1, 3, 4]:
                        await self.io_handler.display_message(
                            message='You can only play 1 or 3 cards at once!',
                            warning=True
                        )
                        p_choice = await self.io_handler.get_user_input(
                            message='What card/s you want to play?(give number/s of card/s): '
                        )
                        p_nums = p_choice.split(',')
                else:
                    p_nums = [p_choice]

                chosen_nums = []
                for num in p_nums:
                    try:
                        card_num: int = int(num)
                        if card_num < 1 or card_num > len(self.deck):
                            await self.io_handler.display_message(
                                message='Given number must represent a card from deck!',
                                warning=True
                            )
                            break
                        else:
                            chosen_nums.append(card_num - 1)
                    except ValueError:
                        await self.io_handler.display_message(
                            message='You have to get_user_input a number!',
                            warning=True)
                        break
                suc_choice = len(chosen_nums) == len(p_nums)
            return chosen_nums

        # checking if cards can be played on current card in game
        good_cards: bool = False
        chosen_cards: list[Card] = []
        while not good_cards:
            chosen_cards = [self.deck[card] for card in await _cards_from_deck()]

            if chosen_cards[0] == 'King' and len(chosen_cards) > 1:
                await self.io_handler.display_message(
                    message="You can't play few Kings because not all of them are functional",
                    warning=True
                )
                good_cards = False

            elif chosen_cards[0].can_be_played(cur_card, game_actions):
                for card in chosen_cards:
                    if card.name != chosen_cards[0].name:
                        good_cards = False
                        break
                    else:
                        good_cards = True
            else:
                good_cards = False
        return chosen_cards

    async def say_makao(self) -> bool:
        """Gives player a chance to say makao/after makao when he needs,\n
        returns False if he didn't say when he had to"""
        makao_time = await self.io_handler.get_user_input()
        makao_time = makao_time.lower()
        if len(self.deck) == 1 and makao_time != 'makao':
            await self.io_handler.display_message(
                message='FOOLLL!!!\nYou did not said makao\nYou pull 5 cards',
                warning=True
            )
            return False
        elif len(self.deck) == 0 and makao_time != 'after makao':
            await self.io_handler.display_message(
                message='FOOLLL!!!\nYou did not said after makao\nYou pull 5 cards',
                warning=True
            )
            return False
        else:
            return True


class BotPlayer(Player):
    """Creates object which inherits from Player class, makes all choices automative and random"""
    def __init__(self, bot_name: str, io_handler: IOHandler) -> None:
        super().__init__(bot_name, io_handler)
        self._available_deck: list[Card] = []

    async def play_or_pass(self) -> str:
        """Randomly choose whether bot plays or passes with 95% that he plays"""
        response: list[str] = ['play', 'pass']
        return random.choices(response, weights=[19, 1], k=1)[0]

    def _create_available_deck(self, cur_card:Card, game_actions: CardsActions) -> None:
        """Creates a deck of cards that can be played by bot in that turn"""
        self._available_deck.clear()
        for card in self.deck:
            if card.can_be_played(cur_card,  game_actions):
                self._available_deck.append(card)

    async def _choose_colour_demands(self) -> str:
        """If bot played demanding card, returns what colour cards he has most in his deck"""
        cards_colours: list[str] = [card.colour for card in self.deck]
        most_col_name: str = COLOURS[3]['name']
        most_col_num: int = 0
        for colour in cards_colours:
            if cards_colours.count(colour) > most_col_num:
                most_col_num = cards_colours.count(colour)
                most_col_name = colour
        return most_col_name.capitalize()

    async def _choose_number_demands(self) -> str:
        """If bot played demanding card, returns what non-functional number cards he has most in his deck"""

        cards_nums: list[str] = []
        for card in self.deck:
            try:
                if 11 > int(card.name) > 4:
                    cards_nums.append(card.name)
            except ValueError:
                pass
        most_num_name: str = '5'
        most_num_num: int = 0
        for num in cards_nums:
            if cards_nums.count(num) > most_num_num:
                most_num_num = cards_nums.count(num)
                most_num_name = num
        return most_num_name

    async def choose_card(self, cur_card: Card, game_actions: CardsActions) -> list[Card]:
        """Returns list of cards that bot randomly chose based in demands and current card in game"""
        self._create_available_deck(cur_card, game_actions)
        chosen_cards: list[Card] = []
        # playing 3 cards
        cards_names: list[str] = [card.name for card in self.deck]
        for card in self._available_deck:
            if cards_names.count(card.name) > 2 and card.name != 'King':
                chosen_cards.append(card)
                first_card: Card = chosen_cards[0]
                other_cards: list[Card] = [card for card in self.deck if
                                           card.name == first_card.name and card != first_card]
                chosen_cards.extend(other_cards)
                await self.io_handler.display_message(
                    message='Bot played multiple cards:'
                )
                for _card in chosen_cards:
                    await self.io_handler.display_message(
                        message=str(_card)
                    )
                return chosen_cards
        # if not able to play 3 cards
        no_queen_deck: list[Card] = [card for card in self._available_deck if card.name != 'Queen']
        if len(no_queen_deck) > 0:
            chosen_cards = [random.choice(no_queen_deck)]
        else:
            chosen_cards = [random.choice(self._available_deck)]
        await self.io_handler.display_message(
            message=f'Playing {chosen_cards[0]}'
        )
        # sleep(3)
        return chosen_cards

    async def say_makao(self) -> bool:
        """If player needs to say makao, it returns it with 95% chance"""
        options: list[bool] = [True, False]
        saying = random.choices(options, weights=[20, 1], k=1)[0]
        # sleep(3)
        if len(self.deck) == 1:
            if saying:
                await self.io_handler.display_message(
                    message='Makao'
                )
            else:
                await self.io_handler.display_message(
                    message='Should I say something?'
                )
            return saying
        elif len(self.deck) == 0:
            if saying:
                await self.io_handler.display_message(
                    message='After makao'
                )
            else:
                await self.io_handler.display_message(
                    message='Should I say something?'
                )
            return saying
        else:
            return True
