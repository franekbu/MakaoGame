from makao_game.dictionaries import FUNCTIONS, FUNCTIONS_TYPES_NAMES, DEMAND_OPTIONS_NAMES
from makao_game.cards import Card

# or name it actions????
class Demands:
    def __init__(self) -> None:
        self.current_type: str | None = None
        self.value: str | None = None   # set only when demanded number or colour
        self.pull_stack: int = 0
        self.frozen_stack: int = 0
        self.demands_duration: int = 0
        self.reversed_order: bool = False

    def is_active(self) -> bool:
        """Returns True if demands set"""
        return self.current_type is not None

    def reset_demands(self) -> None:
        """Sets all attributes APART FROM REVERSED_ORDER to initial values"""
        self.current_type = None
        self.value = None
        self.pull_stack = 0
        self.frozen_stack = 0
        self.demands_duration = 0

    def _handle_non_functional_card(self, multi_cards_played: bool) -> None:
        """Reduces demands_duration or reset all demands"""
        if self.value is not None:
            if (multi_cards_played and self.value == DEMAND_OPTIONS_NAMES['ACE']) or self.demands_duration == 1:
                self.reset_demands()
            else:
                self.demands_duration -= 1
        else:
            self.reset_demands()


    def apply_card_effects(self, card_played: Card, num_card_played: int) -> bool:
        # TODO: Finish it
        """
        Changes demands accordingly to what card was played and how many of them,
        returns True if player action is needed -> Ace or Jack played,
        otherwise returns False
        """
        multiple_cards_played: bool = num_card_played > 1

        if not card_played.functional:
            self._handle_non_functional_card(multiple_cards_played)
            return False



        return False