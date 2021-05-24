from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.emoji import emojize

from data.enquiry import Enquiry
from keyboards.inline.inline_current_date import inline_current_date, cb_current_date
from keyboards.inline.inline_type_request_menu import inline_type_request_menu
from loader import dp, bot
from states.task_to_plan_state import TaskToPlanState

##############################################################
########## Запланировать ####################################
#############################################################
from utils import format_enquiry
from utils.choice_request_buttons import choice_request_buttons
from utils.create_date import get_date_DMY
from utils.task_to_plan.task_to_plan_utils import task_to_plan_put_date


@dp.callback_query_handler(regexp = "^task_to_plan#.+")
async def task_done_start(call: CallbackQuery, state: FSMContext):
	# print(f"task_done_start -> call.data = {call.data}")
	# await call.message.delete()
	# enquiries = Enquiry(call.from_user.id)
	# Get ID task
	id_task = call.data.split("#")[1]
	# Get inquiry's entity by ID task
	# entity = enquiries.get_entity_by_id(id_task)
	# print(f'task_done_start -> entity={entity[0]}')
	# Show information about inquiry
	# await call.message.answer(format_enquiry(entity[0]))
	current_date = get_date_DMY()
	await state.update_data(id_task = id_task)
	await call.message.answer("Заявка № <b>{}</b>\nВведите плановую дату исполнения в формате дд.мм.гггг, "
	                          "или нажмите кнопку для ввода текущей даты.:".format(id_task),
	                          reply_markup = inline_current_date(current_date))
	
	# print('task_done_start -> Before TaskToPlanState.PutDate.set()')
	await TaskToPlanState.PutDate.set()


@dp.callback_query_handler(cb_current_date.filter(button_name = 'button_current_date'), state = TaskToPlanState.PutDate)
async def current_date_button_was_pressed(call: CallbackQuery, callback_data: dict, state: FSMContext):
	"""
	If user pressed button 'Current date' instead to put date manually
	:param call:
	:param callback_data:
	:param state:
	:return:
	"""
	await call.answer(cache_time = 60)
	# , callback_data: dict, state: FSMContext
	# print(f'call.data={call.data}')
	# print(f'callback_data={callback_data}')
	current_date = callback_data.get('current_date')
	await state.update_data(current_date = current_date)
	# await TaskToPlanState.PutDate.set()
	# await call.message.answer(f'Дата установлена в {current_date}')
	await task_to_plan_put_date(current_date, call.message, state)


@dp.callback_query_handler(cb_current_date.filter(button_name = 'button_back'), state = TaskToPlanState.PutDate)
async def back_button_was_pressed(call: CallbackQuery, state: FSMContext):
	await call.answer(cache_time = 60)
	# await call.message.delete()
	await choice_request_buttons(call.message)


@dp.message_handler(state = TaskToPlanState.PutDate)
async def task_done_date(message: Message, state: FSMContext):
	# await message.answer(f"Data = {message.text}")
	# message_id = message.message_id
	# get_me = await bot.get_me()
	# print("->message_id = {}, get_me = {}".format(message_id, get_me))
	# await bot.delete_message(1666850393, 1016)
	# data_state = await state.get_data()
	# current_date = data_state.get("current_date")
	# print(f'task_done_date -> current_date={current_date}')
	date_done = str(message.text)
	# await message.delete_reply_markup()
	# await message.delete()  # delete message from user (green color)
	# await message.delete()
	await task_to_plan_put_date(date_done, message, state)
