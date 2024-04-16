import discord
from config import TOKEN1 as TOKEN
import logging

from requests import get

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class RandomCat(discord.Client):
    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            logger.info(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return

        response = None
        if any((cat in message.content.lower() for cat in ['кот', 'кошк'])):
            response = get('https://api.thecatapi.com/v1/images/search')
            img = get(response.json()[0]['url'])
        elif any((cat in message.content.lower() for cat in ['собак', 'собачк', 'пес', 'пёс'])):
            response = get('https://dog.ceo/api/breeds/image/random')
            img = get(response.json()['message'])

        if response:
            img_file = "img.png"
            with open(img_file, "wb") as file:
                file.write(img.content)
            await message.channel.send(file=discord.File('img.png'))


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = RandomCat(intents=intents)
client.run(TOKEN)