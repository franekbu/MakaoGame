from dotenv import load_dotenv
import discord
import os

load_dotenv()
bot_token: str | None = os.getenv('BOT_TOKEN')
assert bot_token is not None, 'Set BOT_TOKEN in environment'

class MakaoBot(discord.Client):

    async def on_ready(self) -> None:
        print(f'We have logged as {self.user}!')

    async def on_message(self, message: discord.Message):
        print(f'i see {message.content} written by {message.author}')
        if message.author == self.user:
            return None

        if message.content.startswith('$hello'):
            await message.channel.send('Hello, im here to play makao!')





intents = discord.Intents.default()
intents.message_content = True
client = MakaoBot(intents=intents)


client.run(bot_token)
