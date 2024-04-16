import asyncio
import discord
from discord.ext import commands
import random, logging
import pymorphy3 as pm
from config import TOKEN2 as TOKEN

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

morph_analyzer = pm.MorphAnalyzer()

class RussianBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help_bot')
    async def help_bot(self, ctx):
        await ctx.send('''Comands:
"!#numerals word num" - связать слово word с числом num
"!#alive word" - узнать слово word одушевлённое или нет
"!#noun word case state" - склонить слово word в числе state(sing, plur) в падеже case(nomn, gent, datv, accs, ablt, loct)
"!#inf word" - вывести слово word в начальной форме
"!#morph word" - полный морфологический анализ слова''')

    @commands.command(name='numerals')
    async def numerals(self, ctx, word, num):
        word_parse = morph_analyzer.parse(word)[0]
        word_num = word_parse.make_agree_with_number(int(num)).word
        await ctx.send(f'{num} {word_num}')

    @commands.command(name='alive')
    async def alive(self, ctx, word):
        word_parse = morph_analyzer.parse(word)[0]
        if "NOUN" not in word_parse.tag:
            await ctx.send('это не существительное')
        else:
            al = ' '
            if "anim" not in word_parse.tag:
                al += 'не '

            if 'femn' in word_parse.tag:
                al += 'живая'
            elif 'masc' in word_parse.tag:
                al += 'живой'
            elif 'neut' in word_parse.tag:
                al += 'живое'
            await ctx.send(word + al)

    @commands.command(name='noun')
    async def noun(self, ctx, word, case, state):
        parse_word = morph_analyzer.parse(word)[0]
        if "NOUN" not in parse_word.tag:
            await ctx.send('Похоже, это не существительное')
        else:
            new_word = parse_word.inflect({case, state}).word
            await ctx.send(new_word)

    @commands.command(name='inf')
    async def inf(self, ctx, word):
        new_word = morph_analyzer.parse(word)[0].normal_form
        await ctx.send(new_word)

    @commands.command(name='morph')
    async def morph(self, ctx, word):
        analyse = morph_analyzer.parse(word)[0]

        await ctx.send(f'''Слово: {analyse.word} ({analyse.tag})
    Начальная форма: {analyse.normal_form}
    {analyse.tag}''')

bot = commands.Bot(command_prefix='!#', intents=intents)


async def main():
    await bot.add_cog(RussianBot(bot))
    await bot.start(TOKEN)


asyncio.run(main())