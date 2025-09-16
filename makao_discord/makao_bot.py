import discord as dsc

from makao_game import Game, Player, BotPlayer
from makao_discord.discord_io_handler import DiscordIOHandler


class MakaoBot(dsc.Client):
    def __init__(self, dsc_intents: dsc.Intents) -> None:
        super().__init__(intents=dsc_intents)
        self.games_on: list[Game] = []

    async def on_ready(self) -> None:
        print(f'We have logged as {self.user}!')

    async def on_message(self, message: dsc.Message) -> None:
        if message.author == self.user:
            return None

        assert isinstance(message.channel.type, dsc.ChannelType)
        channel_type: dsc.ChannelType = message.channel.type

        if channel_type == dsc.ChannelType.private:
            await self._handle_dm_chanel(message)
            return None

        part_msg: list[str] = message.content.split()
        if  part_msg[0] == 'makao':
            part_msg.pop(0)

            assert channel_type in [dsc.ChannelType.text, dsc.ChannelType.voice], \
                f'Unsupported chanel type: {message.channel.type}'

            self._handle_commands(
                command=part_msg.pop(0),
                rest_of_message=part_msg
            )


        return None

    def _handle_commands(self, command: str, rest_of_message) -> None:
        return None

    async def _handle_text_chanel(self, msg: dsc.Message) -> None:
        part_msg: list[str] = msg.content.split()
        if part_msg[1].lower() == 'info':
            # await self._send_info()
            pass
        elif part_msg[1].lower() == 'start':
            players: list[str] = self._prepare_game(msg ,part_msg)
            assert isinstance(msg.channel, dsc.TextChannel)
            discord_io: DiscordIOHandler = DiscordIOHandler(msg.channel)
            game = Game(io_handler=discord_io, players=players)
            self.games_on.append(game)
            await game.run_game()
        else:
            for game in self.games_on:
                assert isinstance(game.io_handler, DiscordIOHandler)
                if game.io_handler.discord_channel.id == msg.channel.id:
                    part_msg.remove('makao')
                    message:str = ' '.join(part_msg)
                    if game.current_player is None:
                        game.io_handler.input_update(message)
                    assert isinstance(game.current_player, Player | BotPlayer)
                    if msg.author.mention == game.current_player.name:
                        game.io_handler.input_update(message)



    @staticmethod
    async def _handle_dm_chanel(msg: dsc.Message) -> None:
        await msg.channel.send('*You should not write to me here*')

    @staticmethod
    def _prepare_game(msg: dsc.Message, msg_parts: list[str]) -> list[str]:
        players_ids: list[str] = []
        for part in msg_parts:
            if part not in ['makao', 'start']:
                try:
                    assert isinstance(msg.channel.guild, dsc.Guild)
                    if isinstance(msg.channel.guild.get_member(int(part.strip('<@>',))), dsc.Member):
                        players_ids.append(part)
                except Exception as e:
                    print(e)

        print(players_ids)
        return players_ids
