import json
from time import strftime, strptime
from telebot import TeleBot, types
from fastapi import FastAPI
from datetime import datetime
from env import TOKEN, W_TOKEN
import requests

import uvicorn

app = FastAPI()

bot = TeleBot(TOKEN)

W_URL = "http://api.weatherapi.com/v1"



# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.ReplyKeyboardMarkup()
#     btn1 = types.KeyboardButton("Стоп")
#     markup.add(btn1)
#     bot.send_message(message.from_user.id, "Выберите город", reply_markup=markup)

# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     print(message)
#     markup = types.ReplyKeyboardMarkup()
#     if message.text == 'Начать':
#         print()
#         markup.add(btn1)
#         bot.send_message(message.from_user.id, 'Выберите город', reply_markup=markup)
#     elif message.text == 'Стоп':
#         btn1 = types.KeyboardButton("Начать")
#         markup.add(btn1)
#         bot.send_message(message.from_user.id, "Работа остановлена", reply_markup=markup)

# bot.polling(none_stop=True, interval=0)

@app.get('/')
async def root(city: str = 'moscow'):
    res = requests.get(W_URL + "/current.json", params={'key': W_TOKEN, 'q': city, 'lang': 'ru'})
    return json.loads(res.text)

@app.get('/get_temp')
async def get_temp(city: str = 'moscow'):
    res = requests.get(W_URL + "/current.json", params={'key': W_TOKEN, 'q': city, 'lang': 'ru'})
    text = json.loads(res.text)['current']
    last_updated = datetime.strptime(text['last_updated'], '%Y-%m-%d %H:%M').time().__format__('%H:%M')
    time = datetime.now().time().__format__('%H:%M')
    temperature = text['temp_c']
    condition = text['condition']['text']
    return {'Город': city, 'Время': time, 'Время обновления': last_updated, 'Температура': temperature, 'Состояние': condition}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, log_level="info")