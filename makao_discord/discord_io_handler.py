import discord as dsc
from asyncio import Event

from makao_game import IOHandler, COLOURS


class DiscordIOHandler(IOHandler):
    def __init__(self, channel: dsc.TextChannel) -> None:
        self.discord_channel: dsc.TextChannel = channel
        self._event: Event = Event()
        self._input_message: str = ''

    async def get_user_input(self, message: str = 'Any last words?') -> str:
        await self.discord_channel.send(message)
        await self._event.wait()
        self._event.clear()
        return self._input_message

    async def display_message(self, message: str, warning: bool = False) -> None:
        if warning:
            message = f'*{message}*'
        await self.discord_channel.send(message)

    def input_update(self, message: str) -> None:
        self._input_message = message
        self._event.set()

    def supported_symbols(self) -> dict[str, str]:
        return {COLOURS[col]['name']: f':{COLOURS[col]['name'].lower()}:' for col in COLOURS}