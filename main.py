import asyncio
from makao_game import Game, ConsoleIOHandler

async def main() -> None:

    game = Game()

    await game.run_game()
    await game.show_leaderboard()
    game.save_data()

if __name__ == '__main__':
    asyncio.run(main())
