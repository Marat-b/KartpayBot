from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.emoji import emojize

cb_current_date = CallbackData("cb_current_date", "button_name", "current_date")


def inline_current_date(current_date):
	request = InlineKeyboardMarkup(row_width = 2, inline_keyboard = [
		[
			InlineKeyboardButton(text = "{}".format(current_date), callback_data = cb_current_date.new(button_name = 'button_current_date', current_date = current_date)),
			
			InlineKeyboardButton(text = "{} Назад".format(emojize(":leftwards_arrow_with_hook:")), callback_data = cb_current_date.new(button_name = 'button_back',
			                                                                                                                           current_date = current_date))
		]
	])
	return request
