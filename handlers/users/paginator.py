from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.types.base import String
from telegram_bot_pagination import InlineKeyboardPaginator
from loader import dp

from data.enquiry import Enquiry
from utils import format_enquiry, get_state_name


# data = ["Q", "A", "Z", "W", "S", "X", "E", "D", "C", "R", "F", "V"]

@dp.callback_query_handler(regexp = '(^page\#\d|^assigned_to|^signed|^setup)')
async def callback_paginator(call: CallbackQuery, state: FSMContext):
	# print(f'-> {str(call.from_user.id)}')
	call_data = call.data
	state_name = ""
	# print(f"call_data = {call_data}")
	
	# if call_data == 'assigned_to' or call_data == 'trip_planned' or call_data == 'signed' or call_data == 'setup':
	if call_data == 'assigned_to' or call_data == 'signed' or call_data == 'setup':
		page = 1
		state_name = get_state_name(str(call_data))
		enquiries = Enquiry(call.from_user.id)
		# fetching data from DB
		entities = enquiries.get_entities(state_name)
		if call_data == "assigned_to":
			second_entities = enquiries.get_entities(get_state_name("trip_planned"))
			entities += second_entities
		await state.update_data(request_data = entities, state_name = state_name, call_data = call_data)
		data_state = await state.get_data()
		request_data = data_state.get("request_data")
		print(f"request_data = {request_data}")
	else:
		data_state = await state.get_data()
		request_data = data_state.get("request_data")
		# print(f"request_data = {request_data}")
		page = int(call.data.split('#')[1])
		# print(f'page={str(page)}')
	paginator = InlineKeyboardPaginator(
			0 if request_data is None else len(request_data),
			current_page = int(page),
			data_pattern = 'page#{page}'
	)
	
	paginator.add_after(InlineKeyboardButton(text = "<< Назад", callback_data = "choice_buttons"))
	if len(request_data) if request_data is not None else 0 > 0:
		# if data_state.get("call_data") == "at_work":
		# 	paginator.add_before(InlineKeyboardButton(text = "Запланировать", call_data = "task_trip_planned#{}".format(request_data[0]["id"])))
		# 	paginator.add_before(InlineKeyboardButton(text = "Закрыть заявку", call_data = ""))
		if data_state.get("call_data") == 'assigned_to':
			# print("task_assign_to#{}".format(request_data[0]["id"]))
			paginator.add_before(InlineKeyboardButton(text = "Запланировать", callback_data = "task_to_plan#{}".format(request_data[0]["id"])))
			paginator.add_before(InlineKeyboardButton(text = "Закрыть заявку", callback_data = "task_close_inquire#{}".format(request_data[0]["id"])))
		if data_state.get("call_data") == 'trip_planned':
			paginator.add_before(InlineKeyboardButton(text = "Установлено", callback_data = "task_trip_planned#{}".format(request_data[0]["id"])))
		if data_state.get("call_data") == 'setup':
			# print("task_setup#{}".format(request_data[0]["id"]))
			paginator.add_before(InlineKeyboardButton(text = "УПД подписан", callback_data = "task_setup#{}".format(request_data[0]["id"])))
		await call.message.edit_text(format_enquiry(data_state.get("state_name"), request_data[page - 1]), reply_markup = paginator.markup) #lambda page: page - 1 if page > 0
