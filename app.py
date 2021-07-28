import telebot

from config import currencies, TOKEN
from extensions import Exchange, ConverterExceptions

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    """
Обрабатывает команды начала и помощи
    :param message: Полученное от пользователя сообщение с соответствующей командой
    :return: Возвращает пользователю ответ в виде текста с описанием функционала
    """
    text = "тобы получить список доступных валют введите команду /values.\n" \
           "Чтобы получить курс валют введите пару валют через пробел без скобок:\n" \
           "<Имеющаяся валюта> <В какую надо конвертировать> <Количество имеющейся валюты>\n" \
           "Например:\n" \
           "доллар рубль 5"
    bot.send_message(message.chat.id, "Привет " + message.chat.first_name)
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def function_name(message: telebot.types.Message):
    """
Обрабатывает цоманду пользователя по запросу имеющихся валют
    :param message: Полученное от пользователя сообщение с соответствующей командой
    :return: Возвращает пользователю ответ в виде списка доступных валют
    """
    text = "Доступные для конвертации валюты"
    for key in currencies.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def reply_to_user(message: telebot.types.Message):
    """
Обрабатывает сообщение с запрошенными валютами
    :param message: Полученное от пользователя сообщение с валютами и количеством
    :return: Возвращает пользователю ответ в виде курса валюты или сообшения об ошибке
    """
    try:
        received = message.text.split(" ")

        if len(received) != 3:
            raise ConverterExceptions("Неверное количество параметров. Должно быть 3.")

        currency_from, currency_to, how_much = received

        reply = Exchange.get_price(currency_from, currency_to, how_much)

    except ConverterExceptions as e:
        bot.send_message(message.chat.id, f"Произшла ошибка:\n{e}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Что-то пошло не так:\n{e}")

    else:

        text = f"Запрошенный курс из {currency_from} в {currency_to}:\n" \
               f"За {how_much} {currency_from} Вы получите {reply} {currency_to}"

        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
