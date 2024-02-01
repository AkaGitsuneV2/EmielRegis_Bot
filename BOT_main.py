# main.py
import telebot
from telebot import types
from extentions import APIException, CurrencyConverter
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    instructions = ("Добро пожаловать, друг!\n\n"
                    "Чтобы узнать цену определенной валюты, отправьте сообщение в формате:\n"
                    "<имя_валюты_для_проверки> <имя_валюты_для_конвертации> <сумма>\n"
                    "Например: USD EUR 10")
    bot.send_message(message.chat.id, instructions)

@bot.message_handler(commands=['values'])
def handle_values(message):
    available_currencies = "Доступные валюты: USD, EUR, RUB"
    bot.send_message(message.chat.id, available_currencies)

@bot.message_handler(func=lambda message: True)
def handle_currency_conversion(message):
    try:
        input_data = message.text.split()
        base_currency, quote_currency, amount = input_data[0], input_data[1], float(input_data[2])
        result = CurrencyConverter.get_price(base_currency, quote_currency, amount)
        response = f'{amount} {base_currency} = {result} {quote_currency}'
        bot.send_message(message.chat.id, response)
    except (IndexError, ValueError, APIException) as e:
        error_message = f'Ошибка: {type(e).__name__} - {str(e)}'
        bot.send_message(message.chat.id, error_message)

if __name__ == "__main__":
    bot.polling(none_stop=True)
