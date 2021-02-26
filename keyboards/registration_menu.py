from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.emoji import emojize

button_registration = KeyboardButton('{}  Зарегистрироваться'.format(emojize(":customs:")))

registration_menu = ReplyKeyboardMarkup(resize_keyboard=True)
registration_menu.clean()
registration_menu.row(button_registration)

