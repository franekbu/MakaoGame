from makao_game.dictionaries import FUNCTIONS_TYPES_NAMES, DEMAND_OPTIONS_NAMES

class CardsActions:
    """Creates class responsible for storing and managing current actions in game dictated by played cards functions"""
    def __init__(self) -> None:
        self.action_type: str | None = None
        self.pull_stack: int = 0
        self.freeze_stack: int = 0
        self.demanded_type: str | None = None
        self.demanded_value: str | None = None   # set only when demanded number or colour
        self.demands_duration: int = 0
        self.reversed_order: bool = False
        self.update_player_inputs: bool = False

    def reset_actions(self) -> None:
        """Sets all attributes APART FROM REVERSED_ORDER to initial values"""
        self.action_type = None
        self.pull_stack = 0
        self.freeze_stack = 0
        self.demanded_type = None
        self.demanded_value = None
        self.demands_duration = 0
        self.update_player_inputs = False

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

    def _handle_demand_action(self, demanded_type: str, num_players: int) -> None:
        self.action_type = FUNCTIONS_TYPES_NAMES['DEMAND']
        self.demanded_type = demanded_type
        self.demanded_value = None
        self.demands_duration = num_players
        self.update_player_inputs = True

    def update_actions_with_player_inputs(self, user_input: str) -> None:
        """Updates demanded_value to provided user input, sets back to update_player_inputs

            Should be used only if update_player_inputs is set to True
        """
        self.demanded_value = user_input
        self.update_player_inputs = False

    def apply_card_effects(self,
                           card_played_function: tuple[str, str | int] | None,
                           num_cards_played: int,
                           num_players: int) -> None:
        """
        Changes card actions accordingly to what card was played and how many of them,
        if card with demand action played, sets update_player_inputs to True
        """
        multiple_cards_played: bool = num_cards_played > 1

        if card_played_function is None:
            self._handle_non_functional_card(multiple_cards_played)
            return None


        cards_function_name: str = card_played_function[0]
        function_value: int | str = card_played_function[1]

        if cards_function_name == FUNCTIONS_TYPES_NAMES['PULL']:
            assert isinstance(function_value, int)
            self._handle_pull_action(function_value, num_cards_played)

        elif cards_function_name == FUNCTIONS_TYPES_NAMES['FREEZE']:
            self._handle_freeze_action(num_cards_played)

        elif cards_function_name == FUNCTIONS_TYPES_NAMES['DEMAND']:
            assert isinstance(function_value, str)
            self._handle_demand_action(function_value, num_players)

        elif cards_function_name == FUNCTIONS_TYPES_NAMES['ABOLISH']:
            self.reset_actions()

        elif cards_function_name == FUNCTIONS_TYPES_NAMES['REVERSE']:
            self.reversed_order = not self.reversed_order
            assert isinstance(function_value, int)
            self._handle_pull_action(function_value, num_cards_played)
        else:
            raise ValueError('Card function is not None, and its name is not recognised')
        return None
