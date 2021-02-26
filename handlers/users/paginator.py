from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.types.base import String
from aiogram.utils.emoji import emojize
from telegram_bot_pagination import InlineKeyboardPaginator
from loader import dp

from data.enquiry import Enquiry
from states.task_edit_state import TaskEditState
from utils import format_enquiry, get_state_name


# data = ["Q", "A", "Z", "W", "S", "X", "E", "D", "C", "R", "F", "V"]
from utils.format_enquiry import format_enquiry_for_paying


@dp.callback_query_handler(regexp = '(^page\#\d|^assigned_to|^setup)', state = "*")
async def callback_paginator(call: CallbackQuery, state: FSMContext):
	# print(f'callback_paginator -> {str(call.from_user.id)}')
	await state.reset_state(with_data = False)
	call_data = call.data
	state_name = ""
	# print(f"call_data = {call_data}")
	
	if call_data == 'assigned_to' or call_data == 'setup':
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
		# print(f"request_data = {request_data}")
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
	
	if len(request_data) if request_data is not None else 0 > 0:
		if data_state.get("call_data") == 'assigned_to':
			# print("task_assign_to#{}".format(request_data[0]["id"]))
			paginator.add_after(InlineKeyboardButton(text = "{}  Запланировать".format(emojize(":clipboard:")), callback_data = "task_to_plan#{}".format(request_data[0]["id"])))
			paginator.add_after(InlineKeyboardButton(text = "{}  Закрыть заявку".format(emojize(":closed_book:")), callback_data = "task_close_inquire#{}".format(request_data[0][
				                                                                                                                                                 "id"])))
		if data_state.get("call_data") == 'setup':
			# print("task_setup#{}".format(request_data[0]["id"]))
			paginator.add_after(InlineKeyboardButton(text = "{}  Редактировать пробег".format(emojize(":car:")), callback_data = "task_edit_distance#{}".format(request_data[0][
				                                                                                                                                                 "id"])))
			paginator.add_after(InlineKeyboardButton(text = "{}  Загрузить акт".format(emojize(":page_facing_up:")), callback_data = "task_edit_act#{}".format(request_data[0][
				                                                                                                                                                 "id"])))
			paginator.add_after(InlineKeyboardButton(text = "{}  Загрузить УПД".format(emojize(":inbox_tray:")), callback_data = "task_edit_upd#{}".format(request_data[0]["id"])))
			
		paginator.add_after(InlineKeyboardButton(text = "{}  Назад".format(emojize(":leftwards_arrow_with_hook:")), callback_data = "choice_buttons"))
		await call.message.edit_text(format_enquiry(data_state.get("state_name"), request_data[page - 1]), reply_markup = paginator.markup)


@dp.callback_query_handler(regexp = '(^page\&\d|^signed)', state = "*")
async def callback_paginator_for_paying(call: CallbackQuery, state: FSMContext):
	# print(f'callback_paginator  for paying -> {str(call.from_user.id)}')
	await state.reset_state(with_data = False)
	call_data = call.data
	state_name = ""
	# print(f"call_data = {call_data}")
	if call_data == 'signed':
		page = 1
		state_name = get_state_name(str(call_data))
		enquiries = Enquiry(call.from_user.id)
		# fetching data from DB
		entities = enquiries.get_entities_for_paying(state_name, "Нет")
		await state.update_data(request_data = entities, state_name = state_name, call_data = call_data)
		data_state = await state.get_data()
		request_data = data_state.get("request_data")
		# print(f"request_data = {request_data}")
	else:
		data_state = await state.get_data()
		request_data = data_state.get("request_data")
		# print(f"request_data = {request_data}")
		page = int(call.data.split('&')[1])
		# print(f'page={str(page)}')
	paginator = InlineKeyboardPaginator(
			0 if request_data is None else len(request_data),
			current_page = int(page),
			data_pattern = 'page&{page}'
	)
	
	if len(request_data) if request_data is not None else 0 > 0:
		if data_state.get("call_data") == 'signed':
			paginator.add_after(InlineKeyboardButton(text = "{}  Запросить выплату".format(emojize(":bell:")), callback_data = "task_sign&{}".format(request_data[0]["id"])))
		
		paginator.add_after(InlineKeyboardButton("{}  Назад".format(emojize(":leftwards_arrow_with_hook:")), callback_data = "choice_buttons"))
		await call.message.edit_text(format_enquiry_for_paying(request_data[page - 1]), reply_markup = paginator.markup)
