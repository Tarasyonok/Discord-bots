import asyncio
import discord
from discord.ext import commands
import random, logging
import translators
from config import TOKEN5 as TOKEN

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class RussianBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lang_src = 'en'
        self.lang_dest = 'ru'

    @commands.command(name='help_bot')
    async def help_bot(self, ctx):
        await ctx.send('''Comands:
"!#set_lang lang" - указать язык lang (на него будут переводиться фразы)
"!#text text" - перевести фразу text''')

    @commands.command(name='text')
    async def text(self, ctx, *words):
        try:
            text = ' '.join(words)
            trans = translators.translate_text(text, to_language=self.lang_dest)
            if not trans:
                trans = 'Не получилось'
            await ctx.send(trans)
        except Exception as error:
            await ctx.send(error)

    @commands.command(name='set_lang')
    async def set_lang(self, ctx, lang):
        self.lang_src, self.lang_dest = lang.split('-')
        await ctx.send(f'поменял язык на {lang}')


bot = commands.Bot(command_prefix='!#', intents=intents)


async def main():
    await bot.add_cog(RussianBot(bot))
    await bot.start(TOKEN)


asyncio.run(main())