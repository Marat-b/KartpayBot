from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cb_current_date = CallbackData("cb_current_date", "button_name", "current_date")

def inline_current_date(current_date):
	request = InlineKeyboardMarkup(row_width = 1, inline_keyboard = [
		[
			InlineKeyboardButton(text = "{}".format(current_date), callback_data = cb_current_date.new(button_name='button_current_date', current_date=current_date))
		]
		])
	return request
