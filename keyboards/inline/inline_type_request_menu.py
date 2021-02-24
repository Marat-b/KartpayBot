from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_type_request_menu():
	request = InlineKeyboardMarkup(row_width = 1, inline_keyboard = [
		[
			InlineKeyboardButton(text = "В работе", callback_data = "assigned_to")
		],
		[
			InlineKeyboardButton(text = "Установлено", callback_data = "setup")
		],
		[
			InlineKeyboardButton(text = "УПД подписан", callback_data = "signed")
		]
	
	])
	return request
