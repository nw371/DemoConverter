import json
import requests
from config import *


class ConverterExceptions(Exception):
    pass


class Exchange:

    @staticmethod
    def get_price(currency_from, currency_to, how_much):
        """
Метод конвертирует валюты из одной в другую в зависимости от количества
        :param currency_from: Имеющаяся валюта
        :param currency_to: Валюта в которую надо сконвертировать
        :param how_much: Количество имеюьейся валюты
        :return: Количество валюты в которую конвертировали
        """
        if currency_from == currency_to:
            raise ConverterExceptions(f"А смысл?")

        try:
            control = currencies[currency_from]
        except KeyError:
            raise ConverterExceptions(f"Несуществующая валюта: {currency_from}")

        try:
            control = currencies[currency_to]
        except KeyError:
            raise ConverterExceptions(f"Несуществующая валюта: {currency_to}")

        try:
            control = float(how_much)
        except KeyError:
            raise ConverterExceptions(f"Непонятно сколько конвертировать: {how_much}")

        address = f'{protocol}://{base_url}/{api_version}/{type_of_data}?access_key={ACCESS}&base={currencies["евро"]}&symbols={currencies["рубль"]},{currencies["доллар"]}'
        received_data = requests.get(address)
        formatted_data = json.loads(received_data.content)

        if currencies[currency_from] == "EUR":
            currency_from = 1
            currency_to = formatted_data["rates"][currencies[currency_to]]
        elif currencies[currency_to] == "EUR":
            currency_to = 1
            currency_from = formatted_data["rates"][currencies[currency_from]]
        else:
            currency_to = formatted_data["rates"][currencies[currency_to]]
            currency_from = formatted_data["rates"][currencies[currency_from]]

        conversion = (float(currency_to) / float(currency_from)) * float(how_much)
        return conversion
