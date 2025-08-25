from makao_game import Game, ConsoleIOHandler

console: ConsoleIOHandler = ConsoleIOHandler()
game = Game(io_handler=console)

game.start_game()
game.show_leaderboard()
game.save_data()
