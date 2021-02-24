from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_requests = KeyboardButton('Мои заявки')
button_statistics = KeyboardButton('Статистика')

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.clean()
main_menu.row(button_requests)
main_menu.row(button_statistics)
