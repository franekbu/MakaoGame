MAIN_COMMAND: str = 'makao'

SUB_COMMANDS: dict[str, str] = {
    'start': 'start',
    'save': 'save',
    'end': 'kill',
    'play': 'play',
    'pass': 'pass',
    'update': 'update',
    'info': 'info',
    'help': 'help',
    'name': 'name',
}

FLAGS: dict[str, tuple[str, str | None]] = {
    'say': ('say', 's'),
    'demand': ('demand', 'd'),
    'cards': ('cards', 'c'),
    'players': ('players', None),
    'bots': ('bots', None),
    'game': ('game', 'g'),
    'end': ('kill', 'k'),
    'name': ('name', 'n')
}

SUPPORTED_FLAGS: dict[str, list[tuple[str, str | None]] | None] = {
    SUB_COMMANDS['start']: [FLAGS['name'], FLAGS['players'], FLAGS['bots']],
    SUB_COMMANDS['save']: [FLAGS['game'], FLAGS['end']],
    SUB_COMMANDS['end']: None,
    SUB_COMMANDS['play']: [FLAGS['cards'], FLAGS['demand'], FLAGS['say']],
    SUB_COMMANDS['pass']: None,
    SUB_COMMANDS['update']: [FLAGS['demand'], FLAGS['say']],
    SUB_COMMANDS['info']: [FLAGS['game']],
    SUB_COMMANDS['help']: None,
    SUB_COMMANDS['name']: None,
}

HELP: dict[str, dict[str, str]] = {
    'SUB_COMMANDS': {
        SUB_COMMANDS['start']: "starts a game with provided players' mentions and bots names",
        SUB_COMMANDS['save']: "save game progress, so it can be continued from that moment in the future",
        SUB_COMMANDS['end']: "ends game without saving progress",
        SUB_COMMANDS['play']: "play your turn",
        SUB_COMMANDS['pass']: "pass your turn",
        SUB_COMMANDS['update']: "if any needed data was't provided by flags earlier, use this to update it when asked",
        SUB_COMMANDS['info']: "display info about game",
        SUB_COMMANDS['help']: "display sub_commands and flags instructions",
        SUB_COMMANDS['name']: "name a game for future references, need to be done if more than one game is planed to be on"
    },
    'FLAGS': {
        FLAGS['say'][0]: f"use to say makao or after makao, -{FLAGS['say'][1]}",
        FLAGS['demand'][0]: f"use to set what you demand, -{FLAGS['demand'][1]}",
        FLAGS['cards'][0]: f"use to say which cards you play, -{FLAGS['cards'][1]}",
        FLAGS['players'][0]: f"use to say who's gonna play, -{FLAGS['players'][1]}",
        FLAGS['bots'][0]: f"use to say how many bots of which names're gonna play, -{FLAGS['bots'][1]}",
        FLAGS['game'][0]: f"indicate which game you mean, -{FLAGS['game'][1]}",
        FLAGS['end'][0]: f"same as sub_command, -{FLAGS['end'][1]}",
        FLAGS['name'][0]: f"same as sub_command, -{FLAGS['name'][1]}",
    },
}

assert len(HELP['SUB_COMMANDS']) == len(SUB_COMMANDS), 'all sub_commands must have HELP description'
assert len(HELP['FLAGS']) == len(FLAGS), 'all flags must have HELP description'