from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_current_month = KeyboardButton('Текущий месяц')
button_prior_month = KeyboardButton('Предыдущий месяц')
button_back = KeyboardButton('Назад')

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.clean()
main_menu.row(button_current_month)
main_menu.row(button_prior_month)
main_menu.row(button_back)
