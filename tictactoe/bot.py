import os
from dotenv import load_dotenv
import discord
import TicTacToeHandler

TICTACTOE_PROMPT = "!1 tt"


class ZeroTwoBot(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        await self.change_presence(activity=discord.Game('in test mode'))

    @staticmethod
    async def on_message(message):
        # a user has requested a TicTacToe game
        if message.content.startswith(TICTACTOE_PROMPT):
            await TicTacToeHandler.start_game(client, message.channel, message.author)


load_dotenv()
client = ZeroTwoBot()
client.run(os.getenv('DISCORD_TOKEN_001'))
