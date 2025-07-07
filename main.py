from classes import Game

game = Game(bots=['bot1', 'bot2', 'bot3', 'goska', 'szymon', 'franek'])

game.start_game()
game.show_leaderboard()
game.save_data()
