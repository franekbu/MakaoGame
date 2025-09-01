import asyncio
from makao_game import Game, ConsoleIOHandler

async def main() -> None:
    console: ConsoleIOHandler = ConsoleIOHandler()
    game = Game(io_handler=console)

    await game.run_game()
    await game.show_leaderboard()
    game.save_data()

if __name__ == '__main__':
    asyncio.run(main())
