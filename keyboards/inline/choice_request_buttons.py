from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# callback_request = CallbackData("callback_request", "choice_request_button")


def choice_request():
	request = InlineKeyboardMarkup(row_width = 1, inline_keyboard = [
		[
			InlineKeyboardButton(text = "Назначено инженеру", callback_data = "assigned_to")
		]
	])
	return request
