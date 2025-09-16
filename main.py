import asyncio
from dotenv import load_dotenv
import os
import discord as dsc


async def main() -> None:
    from makao_game import Game, ConsoleIOHandler

    console: ConsoleIOHandler = ConsoleIOHandler()
    game = Game(io_handler=console)

    await game.run_game()
    await game.show_leaderboard()
    game.save_data()

def get_token() -> str:
    load_dotenv()
    token: str | None = os.getenv('BOT_TOKEN')
    assert token is not None, 'Set BOT_TOKEN in environment'
    return token

def main2() -> None:
    from makao_discord.makao_bot import MakaoBot
    bot_token: str = get_token()

    intents = dsc.Intents.default()
    intents.message_content = True
    intents.members = True

    client = MakaoBot(dsc_intents=intents)

    client.run(bot_token)


if __name__ == '__main__':
    n: str = input()
    if n == '1':
        asyncio.run(main())
    else:
        main2()
