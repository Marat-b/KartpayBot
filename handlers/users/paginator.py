from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton
from telegram_bot_pagination import InlineKeyboardPaginator
from loader import dp

from data.enquiry import Enquiry
from utils import format_enquiry


# data = ["Q", "A", "Z", "W", "S", "X", "E", "D", "C", "R", "F", "V"]

@dp.callback_query_handler(regexp = '(page\#\d|assigned_to)')
async def callback_paginator(call: CallbackQuery, state: FSMContext):
	# print(f'-> {str(call.from_user.id)}')
	
	if call.data == 'assigned_to':
		page = 1
		enquiries = Enquiry(call.from_user.id, "Передан инженеру")
		await state.update_data(request_data = enquiries.get_entities())
		data_state = await state.get_data()
		request_data = data_state.get("request_data")
		# print(f"request_data = {request_data}")
	else:
		data_state = await state.get_data()
		request_data = data_state.get("request_data")
		# print(f"request_data = {request_data}")
		page = int(call.data.split('#')[1])
	print(f'page={str(page)}')
	paginator = InlineKeyboardPaginator(
			len(request_data),
			current_page = int(page),
			data_pattern = 'page#{page}'
	)
	paginator.add_after(InlineKeyboardButton(text = "<< Назад", callback_data = "choice_buttons"))
	if len(request_data) > 0:
		await call.message.edit_text(format_enquiry(request_data[page - 1]), reply_markup = paginator.markup) #lambda page: page - 1 if page > 0 else 0
