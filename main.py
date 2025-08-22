from makao_game import Game, ConsoleIOHandler

io_connection: ConsoleIOHandler = ConsoleIOHandler()
game = Game(io_connection)

game.start_game()
game.show_leaderboard()
game.save_data()
