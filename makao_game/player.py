import random
# from time import sleep

from makao_game.cards import Card
from makao_game.utils import colour_string
from makao_game.dictionaries import COLOURS

class Player:
    def __init__(self, player_name:str) -> None:
        """Creates object that represents player in a game"""
        self.name:str = player_name
        self.deck:list[Card] = []
        self.frozen_rows:int = 0
        self.valid_cards:bool = False
        self.turn:int = 0
        self.played_card:bool = False

    @staticmethod
    def play_or_pass() -> str:
        """Ask player if he wants to play in this turn or pass it, returns his answer"""
        response:str = input('Do you want to play or pass? ').lower()
        while response not in ['pass', 'play']:
            print(colour_string('You can only write: pass, play', 'red'))
            response = input('So what do you do? ').lower()
        return response

    @staticmethod
    def checking_card(new_c:Card, cur_c:Card, demands:list[str|int|None]) -> bool:
        """Checks if given card can be played, return True if so"""
        if cur_c.name == 'Queen' or new_c.name == 'Queen':
            return True
        elif demands[0] is None:
            return new_c.name == cur_c.name or new_c.colour == cur_c.colour
        elif demands[0] == 'colour':
            return new_c.colour == demands[1] or new_c.name == 'Ace' and cur_c.name == 'Ace'
        elif demands[0] == 'number':
            return new_c.name == demands[1] or new_c.name == 'Jack' and cur_c.name == 'Jack'
        elif demands[0] == 'pause':
            return new_c.function[0] == demands[0]
        elif demands[0] == 'add' or demands[0] == 'subtract':
            return (new_c.function[0] == 'add' or new_c.function[0] == 'subtract') and\
                (new_c.colour == cur_c.colour or new_c.name == cur_c.name)
        else:
            print('you fucked up checking card')
            raise ValueError

    def have_valid_cards(self, cur_c:Card, demands:list[str|int|None]) -> None:
        """Checks if player has valid cards and changes his attribute self.valid_cards"""
        for card in self.deck:
            if self.checking_card(card, cur_c, demands):
                self.valid_cards = True
                return None
        self.valid_cards = False
        return None

    def choose_colour_demands(self) -> str:
        """Ask player what colour he wants to demand and returns it"""
        available_colours: list[tuple[str, str]] = [
            (COLOURS[col]['name'].lower(), COLOURS[col]['symbol']) for col in COLOURS
        ]

        print(f'Available colours names: {available_colours}')
        demanded_color:str = input('What colour do you demand?: ').lower()

        while demanded_color not in available_colours:
            print(colour_string(text=f'Wrong colour!\nColours you can use are: {available_colours}',
                                colour='red'))
            print(colour_string('Do not use symbols!', 'red'))
            demanded_color = input('So what colour do you demand?: ').lower()

        return demanded_color

    def choose_number_demands(self) -> str:
        """Ask player what number he wants to demand and returns it"""
        demanded_number: str
        while True:
            try:
                demanded_number = input('What number do you demand?: ')
                while 4 > int(demanded_number) or int(demanded_number) > 10:
                    print(colour_string(text='Wrong number!\nNumbers you can demand are between 5 and 10',
                                        colour='red'))
                    demanded_number = input('So what number do you demand?: ')
                return demanded_number
            except ValueError:
                print(colour_string(text='Typed char must be an int!',
                                    colour='red'))


    def choose_card(self, cur_c:Card, demands:list[str | int | None]) -> list[Card]:
        """Gives player a choice which card/s he wants to play and returns list of them"""
        # TODO 3. Add possibility to pass even after saying play
        def _cards_from_deck() -> list[int]:
            # checking if cards are in deck
            suc_choice:bool = False
            chosen_nums:list[int] = []
            while not suc_choice:
                p_choice:str = input('What card/s you want to play?(give number/s of card/s): ')
                p_nums: list[str]
                if ',' in p_choice:
                    p_nums = p_choice.split(',')
                    while len(p_nums) not in [1, 3, 4]:
                        print(colour_string('You can only play 1 or 3 cards at once!', 'red'))
                        p_choice = input('What card/s you want to play?(give number/s of card/s): ')
                        p_nums = p_choice.split(',')
                else:
                    p_nums = [p_choice]

                chosen_nums = []
                for num in p_nums:
                    try:
                        card_num:int = int(num)
                        if card_num < 1 or card_num > len(self.deck):
                            print(colour_string('Given number must represent a card from deck!', 'red'))
                            break
                        else:
                            chosen_nums.append(card_num - 1)
                    except ValueError:
                        print(colour_string('You have to input a number!','red'))
                        break
                suc_choice = len(chosen_nums) == len(p_nums)
            return chosen_nums

        # checking if cards can be played on current card in game
        good_cards:bool = False
        chosen_cards:list[Card] = []
        while not good_cards:
            chosen_cards = [self.deck[card] for card in _cards_from_deck()]

            if chosen_cards[0] == 'King' and len(chosen_cards) > 1:
                print(colour_string("You can't play few Kings because not all of them are functional", 'red'))
                good_cards = False

            elif self.checking_card(chosen_cards[0], cur_c, demands):
                for card in chosen_cards:
                    if card.name != chosen_cards[0].name:
                        good_cards = False
                        break
                    else:
                        good_cards = True
            else:
                good_cards = False
        return chosen_cards

    def say_makao(self) -> bool:
        """Gives player a chance to say makao/after makao when he needs,\n
        returns False if he didn't say when he had to"""
        makao_time = input().lower()
        if len(self.deck) == 1 and makao_time != 'makao':
            print(colour_string('FOOLLL!!!\nYou did not said makao\nYou pull 5 cards', 'red'))
            return False
        elif len(self.deck) == 0 and makao_time != 'after makao':
            print(colour_string('FOOLLL!!!\nYou did not said after makao\nYou pull 5 cards', 'red'))
            return False
        else:
            return True


class BotPlayer(Player):
    """Creates object which inherits from Player class, makes all choices automative and random"""
    def __init__(self, bot_name:str) -> None:
        super().__init__(bot_name)
        self.available_deck:list[Card] = []

    @staticmethod
    def play_or_pass() -> str:
        """Randomly choose whether bot plays or passes with 95% that he plays"""
        response:list[str] = ['play', 'pass']
        return random.choices(response, weights=[19, 1], k=1)[0]

    def __create_available_deck(self, cur_c:Card, demands:list[str|int|None]) -> None:
        """Creates a deck of cards that can be played by bot in that turn"""
        self.available_deck.clear()
        for card in self.deck:
            if self.checking_card(card, cur_c, demands):
                self.available_deck.append(card)

    def choose_colour_demands(self) -> str:
        """If bot played demanding card, returns what colour cards he has most in his deck"""
        cards_colours:list[str] = [card.colour for card in self.deck]
        most_col_name:str = 'Hearts'
        most_col_num:int = 0
        for colour in cards_colours:
            if cards_colours.count(colour) > most_col_num:
                most_col_num = cards_colours.count(colour)
                most_col_name = colour
        return most_col_name

    def choose_number_demands(self) -> str:
        """If bot played demanding card, returns what non-functional number cards he has most in his deck"""

        cards_nums:list[str] = []
        for card in self.deck:
            try:
                if 11 > int(card.name) > 4:
                    cards_nums.append(card.name)
            except ValueError:
                pass
        most_num_name:str = '5'
        most_num_num:int = 0
        for num in cards_nums:
            if cards_nums.count(num) > most_num_num:
                most_num_num = cards_nums.count(num)
                most_num_name = num
        return most_num_name

    def choose_card(self, cur_c:Card, demands:list[str | int | None]) -> list[Card]:
        """Returns list of cards that bot randomly chose based in demands and current card in game"""
        self.__create_available_deck(cur_c, demands)
        chosen_cards:list[Card] = []
        # playing 3 cards
        cards_names:list[str] = [card.name for card in self.deck]
        for card in self.available_deck:
            if cards_names.count(card.name) > 2 and card.name != 'King':
                chosen_cards.append(card)
                first_card: Card = chosen_cards[0]
                other_cards:list[Card] = [card for card in self.deck if
                                           card.name == first_card.name and card != first_card]
                chosen_cards.extend(other_cards)
                print('Bot played multiple cards:')
                for _card in chosen_cards:
                    print(_card)
                return chosen_cards
        # if not able to play 3 cards
        no_queen_deck:list[Card] = [card for card in self.available_deck if card.name != 'Queen']
        if len(no_queen_deck) > 0:
            chosen_cards = [random.choice(no_queen_deck)]
        else:
            chosen_cards = [random.choice(self.available_deck)]
        print(f'Playing {chosen_cards[0]}')
        # sleep(3)
        return chosen_cards

    def say_makao(self) -> bool:
        """If player needs to say makao, it returns it with 95% chance"""
        options:list[bool] = [True, False]
        saying = random.choices(options, weights=[20, 1], k=1)[0]
        # sleep(3)
        if len(self.deck) == 1:
            if saying:
                print('Makao')
            else:
                print('Should I say something?')
            return saying
        elif len(self.deck) == 0:
            if saying:
                print('After makao')
            else:
                print('Should I say something?')
            return saying
        else:
            return True


# if __name__ == '__main__':
