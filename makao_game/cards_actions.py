from makao_game.dictionaries import FUNCTIONS_TYPES_NAMES, DEMAND_OPTIONS_NAMES
from makao_game.cards import Card

class CardsActions:
    def __init__(self) -> None:
        self.action_type: str | None = None
        self.demanded_type: str | None = None
        self.demanded_value: str | None = None   # set only when demanded number or colour
        self.pull_stack: int = 0
        self.freeze_stack: int = 0
        self.demands_duration: int = 0
        self.reversed_order: bool = False

    def is_active(self) -> bool:
        """Returns True if actions set"""
        return self.action_type is not None

    def reset_actions(self) -> None:
        """Sets all attributes APART FROM REVERSED_ORDER to initial values"""
        self.action_type = None
        self.demanded_type = None
        self.demanded_value = None
        self.pull_stack = 0
        self.freeze_stack = 0
        self.demands_duration = 0

    def _handle_non_functional_card(self, multi_cards_played: bool) -> None:
        """Reduces demands_duration or reset all actions"""
        if self.demanded_value is not None:
            if (multi_cards_played and self.demanded_value == DEMAND_OPTIONS_NAMES['ACE']) or self.demands_duration == 1:
                self.reset_actions()
            else:
                self.demands_duration -= 1
        else:
            self.reset_actions()

    def _handle_pull_action(self, multiplier: int, num_cards: int) -> None:
        self.action_type = FUNCTIONS_TYPES_NAMES['PULL']
        self.pull_stack += num_cards * multiplier

    def _handle_freeze_action(self, multiplier: int) -> None:
        self.action_type = FUNCTIONS_TYPES_NAMES['FREEZE']
        self.freeze_stack += multiplier

    def _handle_demand_action(self) -> None:
        pass

    def apply_card_effects(self, card_played: Card, num_cards_played: int) -> bool:
        """
        Changes card actions accordingly to what card was played and how many of them,
        returns True if player action is needed -> Ace or Jack played,
        otherwise returns False
        """
        multiple_cards_played: bool = num_cards_played > 1

        if card_played.function is None:
            self._handle_non_functional_card(multiple_cards_played)
            return False


        cards_function_name: str = card_played.function[0]
        function_value: int | str = card_played.function[1]

        if cards_function_name == FUNCTIONS_TYPES_NAMES['PULL']:
            assert isinstance(function_value, int)
            self._handle_pull_action(function_value, num_cards_played)

        elif cards_function_name == FUNCTIONS_TYPES_NAMES['FREEZE']:
            self._handle_freeze_action(num_cards_played)

        elif cards_function_name == FUNCTIONS_TYPES_NAMES['DEMAND']:
            self._handle_demand_action()

        elif cards_function_name == FUNCTIONS_TYPES_NAMES['ABOLISH']:
            self.reset_actions()

        elif cards_function_name == FUNCTIONS_TYPES_NAMES['REVERSE']:
            self.reversed_order = not self.reversed_order
            assert isinstance(function_value, int)
            self._handle_pull_action(function_value, num_cards_played)
        else:
            raise ValueError


        return False