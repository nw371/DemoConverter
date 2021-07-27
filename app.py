import json

import requests
import telebot
from config import TOKEN, ACCESS

class ConverterExceptions(Exception):
    pass


currencies = {
    "доллар": "USD",
    "евро": "EUR",
    "рубль": "RUB",
}
def cross_currency(cur1,cur2):
    return cur1/cur2


bot = telebot.TeleBot(TOKEN)
type_of_data = 'latest'
api_version = 'v1'
base_url = 'api.exchangeratesapi.io'
protocol = 'http'

address = f'{protocol}://{base_url}/{api_version }/{type_of_data}?access_key={ACCESS}&base={currencies["евро"]}&symbols={currencies["рубль"]},{currencies["доллар"]}'

class Exchange:

    @staticmethod
    def process_request(currency_from, currency_to):
        received_data = requests.get(address)
        formatted_data = json.loads(received_data.content)
        print(formatted_data)
        if currencies[currency_from] == "EUR":
            currency_from = 1
            currency_to = formatted_data["rates"][currencies[currency_to]]
        elif currencies[currency_to] == "EUR":
            currency_to = 1
            currency_from = formatted_data["rates"][currencies[currency_from]]
        else:
            currency_to = formatted_data["rates"][currencies[currency_to]]
            currency_from = formatted_data["rates"][currencies[currency_from]]

        conversion = float(currency_to)/float(currency_from)
        return conversion



# print(formatted_data["rates"]["RUB"])
#
# print(received_data.text)
# print(formatted_data)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы получить курс валют введите пару валют через пробел без скобок:\n" \
           "<Имеющаяся валюта> <В какую надо конвертировать> <Количество имеющейся валюты>\n" \
           "Например:\n" \
           "доллар рубль 5"
    bot.send_message(message.chat.id, "Привет " + message.chat.first_name)
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['value'])
def function_name(message: telebot.types.Message):
    text = "Доступные для конвертации валюты"
    for key in currencies.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def reply_to_user(message: telebot.types.Message):
    received = message.text.split(" ")

    if len(received) > 3:
        raise ConverterExceptions("Введено боллее 3 параметров")

    currency_from, currency_to, how_much = received

    if currency_from == currency_to:
        raise ConverterExceptions("Вы идиот?")

    try:
        control = currencies[currency_to]
    except KeyError:
        raise ConverterExceptions(f"Несуществующая валюта: {control}")

    try:
        control = currencies[currency_from]
    except KeyError:
        raise ConverterExceptions(f"Несуществующая валюта: {control}")

    try:
        control = float(how_much)
    except KeyError:
        raise ConverterExceptions(f"Непонятно сколько конвертировать: {control}")

    reply = Exchange.process_request(currency_from, currency_to)
    text = f"Запрошенный курс из {currency_from} в {currency_to}:\n" \
           f"За {how_much} {currency_from} Вы получите {reply} {currency_to}"

    bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)



