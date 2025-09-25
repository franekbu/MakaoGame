from enum import Enum

MAIN_COMMAND: str = 'makao'

class SUB_COMMANDS(Enum):
    start = 'start'
    save = 'save'
    end = 'kill'
    play = 'play'
    pass_ = 'pass'
    update = 'update'
    info = 'info'
    help_ = 'help'
    name_ = 'name'        

class FLAGS(Enum):
    say = ('say', 's')
    demand = ('demand', 'd')
    cards = ('cards', 'c')
    players = ('players', None)
    bots = ('bots', None)
    game = ('game', 'g')
    end = ('kill', 'k')
    name_ = ('name', 'n')

    def __init__(self, long_flag: str, short_flag: str | None) -> None:
        self._long_flag = long_flag
        self._short_flag = short_flag

    @property
    def long_flag(self) -> str:
        return self._long_flag

    @property
    def short_flag(self) -> str | None:
        return self._short_flag

SUPPORTED_FLAGS: dict[SUB_COMMANDS, list[FLAGS] | None] = {
    SUB_COMMANDS.start: [FLAGS.name_, FLAGS.players, FLAGS.bots],
    SUB_COMMANDS.save: [FLAGS.game, FLAGS.end],
    SUB_COMMANDS.end: None,
    SUB_COMMANDS.play: [FLAGS.cards, FLAGS.demand, FLAGS.say],
    SUB_COMMANDS.pass_: None,
    SUB_COMMANDS.update: [FLAGS.demand, FLAGS.say],
    SUB_COMMANDS.info: [FLAGS.game],
    SUB_COMMANDS.help_: None,
    SUB_COMMANDS.name_: None,
}

HELP: dict[str, dict[SUB_COMMANDS | FLAGS, str]] = {
    'SUB_COMMANDS': {
        SUB_COMMANDS.start: "starts a game with provided players' mentions and bots names",
        SUB_COMMANDS.save: "save game progress, so it can be continued from that moment in the future",
        SUB_COMMANDS.end: "ends game without saving progress",
        SUB_COMMANDS.play: "play your turn",
        SUB_COMMANDS.pass_: "pass your turn",
        SUB_COMMANDS.update: "if any needed data wasn't provided by flags earlier, use this to update it when asked",
        SUB_COMMANDS.info: "display info about game",
        SUB_COMMANDS.help_: "display sub_commands and flags instructions",
        SUB_COMMANDS.name_: "name a game for future references, need to be done if more than one game is planned to be on"
    },
    'FLAGS': {
        FLAGS.say: f"use to say makao or after makao, -{FLAGS.say.short_flag}",
        FLAGS.demand: f"use to set what you demand, -{FLAGS.demand.short_flag}",
        FLAGS.cards: f"use to say which cards you play, -{FLAGS.cards.short_flag}",
        FLAGS.players: f"use to say who's gonna play, -{FLAGS.players.short_flag}",
        FLAGS.bots: f"use to say how many bots of which names're gonna play, -{FLAGS.bots.short_flag}",
        FLAGS.game: f"indicate which game you mean, -{FLAGS.game.short_flag}",
        FLAGS.end: f"same as sub_command, -{FLAGS.end.short_flag}",
        FLAGS.name_: f"same as sub_command, -{FLAGS.name_.short_flag}",
    },
}

assert len(HELP['SUB_COMMANDS']) == len(SUB_COMMANDS), 'all sub_commands must have HELP description'
assert len(HELP['FLAGS']) == len(FLAGS), 'all flags must have HELP description'

'makao play --cards "1,2,3" -d "diamonds" -s "makao"'