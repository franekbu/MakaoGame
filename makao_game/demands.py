from makao_game.dictionaries import FUNCTIONS
from makao_game.cards import Card

JACK_DEMAND: str = FUNCTIONS[11][1]
ACE_DEMAND: str = FUNCTIONS[14][1]


class Demands:
    def __init__(self) -> None:
        self.current_demand:str | None = None
        self.value: str | None = None   # set only when demanded number or colour
        self.pull_stack: int = 0
        self.frozen_stack: int = 0
        self.demands_duration: int = 0
        self.reversed_order: bool = False

    def is_active(self) -> bool:
        """Returns True if demands set"""
        return self.current_demand is not None

    def reset_demands(self) -> None:
        """Sets all attributes APART FROM REVERSED_ORDER to initial values"""
        self.current_demand = None
        self.value = None
        self.pull_stack = 0
        self.frozen_stack = 0
        self.demands_duration = 0

    def _handle_non_functional_card(self, multiple_cards_played: bool) -> None:
        """Reduces demands_duration or reset all demands"""
        if self.value is not None:
            if (multiple_cards_played and self.value == ACE_DEMAND) or self.demands_duration == 1:
                self.reset_demands()
            else:
                self.demands_duration -= 1
        else:
            self.reset_demands()


    def apply_card_effects(self, card_played: Card, num_card_played: int) -> bool:
        """
        Changes demands accordingly to what card was played and how many of them,
        returns True if player action is needed -> Ace or Jack played,
        otherwise returns False
        """
        if not card_played.functional:
            multiple_cards: bool = num_card_played > 1
            self._handle_non_functional_card(multiple_cards)
            return False

        return False