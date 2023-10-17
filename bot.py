import json

import telebot
import requests

bot = telebot.TeleBot('')
API = '174b16e79ecc86b81c85c633f2e4ac48'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, я погоднай бот, я могу сказать погоду в твоем городе")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    data = res.json()
    if res.status_code == 200:
        temperature = json.loads(res.text)
        weather_description = data["weather"][0]["main"]
        bot.reply_to(message, f'Сейчас температура: {round(temperature["main"]["temp"])}')
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
            bot.send_message(message.chat.id, wd)
        else:
            bot.send_message(message.chat.id, "Я не знаю какая там погода")

    else:
        bot.send_message(message.chat.id, "Ввод данных не верен")


bot.polling(none_stop=True)
