import discord
from config import TOKEN4 as TOKEN
import logging
from random import choice, shuffle

from requests import get

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

all_smiles = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
if len(all_smiles) % 2 == 1:
    all_smiles.pop()
smiles = all_smiles[:]
pl_count = bot_count = 0

class EmojiGame(discord.Client):
    async def on_message(self, message):
        global pl_count, bot_count, smiles
        if message.author == self.user:
            return

        if message.content.isdigit():
            n = int(message.content) % len(smiles)
            pl_em = smiles[n]
            smiles.remove(pl_em)
            bot_em = choice(smiles)
            smiles.remove(bot_em)

            if ord(pl_em) < ord(bot_em):
                pl_count += 1
            else:
                bot_count += 1


            await message.channel.send(f'''Your emoji: {pl_em}
Bot emoji: {bot_em}
Score: You {pl_count} - Bot {bot_count}''')

            if len(smiles) == 0:
                if pl_count > bot_count:
                    winner = 'You win!'
                elif pl_count < bot_count:
                    winner = 'Bot win!'
                else:
                    winner = 'Draw!'
                await message.channel.send(f'''Emoticons are over
Score: You {pl_count} - Bot {bot_count}
{winner}''')
                pl_count = bot_count = 0
                smiles = all_smiles[:]
            print(len(smiles))
            shuffle(smiles)



intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = EmojiGame(intents=intents)
client.run(TOKEN)