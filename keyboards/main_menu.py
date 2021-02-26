from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.emoji import emojize

button_requests = KeyboardButton('{}  Мои заявки'.format(emojize(":memo:")))
button_statistics = KeyboardButton('{}  Статистика'.format(emojize(":bar_chart:")))

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.clean()
main_menu.row(button_requests)
main_menu.row(button_statistics)
