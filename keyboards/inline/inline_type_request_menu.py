from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


def inline_type_request_menu():
	request = InlineKeyboardMarkup(row_width = 1, inline_keyboard = [
		[
			InlineKeyboardButton(text = "{}  В работе".format(emojize(":hammer:")), callback_data = "assigned_to")
		],
		[
			InlineKeyboardButton(text = "{}  Установлено".format(emojize(":calling:")), callback_data = "setup")
		],
		[
			InlineKeyboardButton(text = "{}  УПД подписан".format(emojize(":pencil2:")), callback_data = "signed")
		]
	
	])
	return request
