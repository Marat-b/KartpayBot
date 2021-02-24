from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


def inline_act_is_missing():
	request = InlineKeyboardMarkup(row_width = 1, inline_keyboard = [
		[
			InlineKeyboardButton(text = "Акт отсутствует", callback_data = "act_is_missing")
		],
		[
			InlineKeyboardButton(text = "{}  Назад".format(emojize(":leftwards_arrow_with_hook:")), callback_data = "back")
		]
	])
	return request
