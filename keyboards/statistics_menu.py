from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.emoji import emojize

from keyboards.main_menu import main_menu

button_current_month = KeyboardButton('{}  Текущий месяц'.format(emojize(":date:")))
button_prior_month = KeyboardButton('{}  Предыдущий месяц'.format(emojize(":calendar:")))
button_back = KeyboardButton('{}  Назад'.format(emojize(":leftwards_arrow_with_hook:")))

statistics_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.clean()
statistics_menu.row(button_current_month)
statistics_menu.row(button_prior_month)
statistics_menu.row(button_back)
