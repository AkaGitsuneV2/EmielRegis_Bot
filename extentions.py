# extensions.py
import requests
import json

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        api_url = f'https://api.exchangerate-api.com/v4/latest/{base}'
        response = requests.get(api_url)

        if response.status_code != 200:
            raise APIException(f'Не удалось получить данные из API. Код состояния: {response.status_code}')

        data = response.json()

        if quote not in data['rates']:
            raise APIException(f'Недопустимая целевая валюта: {quote}')

        rate = data['rates'][quote]
        result = round(amount * rate, 2)

        return result
