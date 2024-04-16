import asyncio
import datetime
import math

import discord
import requests
from discord.ext import commands
import random, logging
import translators
from config import TOKEN6 as TOKEN

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

my_key = "da4895b36b605ab9ac7b0989b661a7e1"

class WeatherBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.curr_place = 'москва'

    @commands.command(name='help_bot')
    async def help_bot(self, ctx):
        await ctx.send('''Comands:
"!#current" - погода для текущего города
"!#place city" - указать текущий город
"!#forecast days" - предсказать погоду на days дней''')

    @commands.command(name='current')
    async def current(self, ctx):
        try:
            response = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={self.curr_place}&lang=ru&units=metric&appid={my_key}")
            data = response.json()

            city = data["name"]
            cur_temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            wind_dir = data["wind"]["deg"] % 360

            wind_words = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
            wind_dir = wind_words[wind_dir // 45]
            print(wind_dir)

            # получаем время рассвета и преобразуем его в читабельный формат
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

            # то же самое проделаем со временем заката
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

            length_of_the_day = datetime.datetime.fromtimestamp(
                data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

            code_to_smile = {
                "Clear": "Ясно \U00002600",
                "Clouds": "Облачно \U00002601",
                "Rain": "Дождь \U00002614",
                "Drizzle": "Дождь \U00002614",
                "Thunderstorm": "Гроза \U000026A1",
                "Snow": "Снег \U0001F328",
                "Mist": "Туман \U0001F32B"
            }

            weather_description = data["weather"][0]["main"]

            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                # если эмодзи для погоды нет, выводим другое сообщение
                wd = "Посмотри в окно, я не понимаю, что там за погода..."

            await ctx.send(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Погода в городе: {city}\nТемпература: {cur_temp}°C {wd}\n"
            f"Влажность: {humidity}%\nДавление: {math.ceil(pressure / 1.333)} мм.рт.ст\nВетер: {wind_dir} {wind} м/с \n"
            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
            f"Хорошего дня!")
        except Exception as error:
            print(error)
            await ctx.send("Проверьте название города!")

    @commands.command(name='place')
    async def place(self, ctx, city):
        self.curr_place = city
        await ctx.send(f'поменял текущий город на {city}')

    @commands.command(name='forecast')
    async def forecast(self, ctx, days):
        days = int(days)
        if 0 <= days <= 7:
            try:
                response = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?q={self.curr_place}&lang=ru&units=metric&appid={my_key}")
                data = response.json()

                city = data["name"]
                cur_temp = data["main"]["temp"]
                code_to_smile = {
                    "Clear": "Ясно \U00002600",
                    "Clouds": "Облачно \U00002601",
                    "Rain": "Дождь \U00002614",
                }


                await ctx.send(f"Прогноз погоды для города: {city}")

                for i in range(1, days + 1):
                    wd = random.choice(list(code_to_smile.values()))
                    temp = cur_temp + round(random.randint(-500, 500) / 100, 2)

                    date = datetime.datetime.now().date()
                    date += datetime.timedelta(days=i)

                    await ctx.send(f"{date.strftime('%Y-%m-%d')}\n"
                                   f"Температура: {temp}°C {wd}\n"
                                   f"-------------------")
            except Exception as error:
                print(error)
                await ctx.send("Проверьте название города!")
        else:
            await ctx.send(f'кол во дней от 1 до 7')


bot = commands.Bot(command_prefix='!#', intents=intents)


async def main():
    await bot.add_cog(WeatherBot(bot))
    await bot.start(TOKEN)


asyncio.run(main())