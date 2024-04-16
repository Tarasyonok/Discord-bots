import asyncio
import discord
from discord.ext import commands
import random, logging
from time import sleep
from config import TOKEN2 as TOKEN

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class TimerBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help_bot')
    async def help_bot(self, ctx):
        await ctx.send('''Comands:
"!#set_timer h m" - поставить таймер на h часов, m минут''')

    @commands.command(name='set_timer')
    async def set_timer(self, ctx, hours, minutes):
        sleep((int(hours) * 60 * 60 + int(minutes) * 60) / 60)
        await ctx.send('время Х наступило!')

bot = commands.Bot(command_prefix='!#', intents=intents)


async def main():
    await bot.add_cog(TimerBot(bot))
    await bot.start(TOKEN)


asyncio.run(main())