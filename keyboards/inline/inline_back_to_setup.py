from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


def inline_back_to_setup():
	request = InlineKeyboardMarkup(row_width = 1, inline_keyboard = [
		[
			InlineKeyboardButton(text = "{}  Назад".format(emojize(":leftwards_arrow_with_hook:")), callback_data = "setup")
		]
	
	])
	return request
