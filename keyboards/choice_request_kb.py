from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_start = KeyboardButton('Начать работу')

request_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
request_kb.clean()
request_kb.row(button_start)
