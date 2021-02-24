from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_at_work = KeyboardButton('В работе')
button_installed = KeyboardButton('Установлено')
button_upd_signed = KeyboardButton('УПД подписан')

requests_menu = ReplyKeyboardMarkup(resize_keyboard=True)
requests_menu.clean()
requests_menu.row(button_at_work)
requests_menu.row(button_installed)
requests_menu.row(button_upd_signed)
