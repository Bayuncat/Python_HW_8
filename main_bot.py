import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def Start_comand(message: types.Message):
    await message.reply("Хотитет узнать погоду в городе!? Пишите город: ")

@dp.message_handler()
async def get_weather(message: types.Message):

    smile_code = {
        "Clear" : "Ясно \U00002600",
        "Clouds" : "Облачно \U00002601",
        "Rain" : "Дождь \U00002614",
        "Drizzle" : "Ливень \U00002614",
        "Thounderstorm" : "Гроза \U000026A1",
        "Snow" : "Снег \U0001F328",
        "Mist" : "Туман \U0001F32B",
    }

    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric")
        data = r.json()


        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_discr = data["weather"][0]["main"]
        if weather_discr in smile_code:
            wd = smile_code[weather_discr]
        else: 
            wd = "Какая-то необычная погода"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        day_length = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(f'Сегодня: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
        f'Погода в городе {city}\nТемпература: {cur_weather}C° {wd}\nВлажность: {humidity}\n'
        f'Давление: {pressure}\nВетер: {wind} м/с\nРассвет: {sunrise}\nПродолжительность часового дня: {day_length}\n')
    
    except: 
        await message.reply("Ну такого города не могу найти")


if __name__ == '__main__':
    executor.start_polling(dp)