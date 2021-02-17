from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from loader import dp
from states.task_done_state import TaskDoneState

from datetime import date
from data.enquiry import Enquiry


@dp.callback_query_handler(regexp = "task_done#.+")
async def task_done(call: CallbackQuery, state: FSMContext):
	print("-> task_done call.data = {}".format(call.data))
	await call.message.edit_text("Введите дату установки в формате дд.мм.гггг:")
	# await call.message.answer(str(date.today()))
	id_task = call.data.split("#")[1]
	await state.update_data(id_task = id_task)
	await TaskDoneState.PutDate.set()


@dp.message_handler(state = TaskDoneState.PutDate)
async def task_done_date(message: types.Message, state: FSMContext):
	# await message.answer(f"Data = {message.text}")
	date_done = str(message.text)
	date_full = str(date_done).split(".")
	# print(len(date_full))
	if len(date_full) == 3:
		if date_full[0].isdigit() and date_full[1].isdigit() and date_full[2].isdigit() and len(date_full[0]) == 2 and len(date_full[1]) == 2 and len(date_full[2]) == 4:
			# print("date_full[1] = {}".format(len(date_full[1])))
			date_day = date_full[0]
			date_month = date_full[1]
			date_year = date_full[2]
			await state.update_data(date_day = date_day, date_month = date_month, date_year = date_year)
			await message.answer("Введите растояние пробега в км:")
			await TaskDoneState.PutDistance.set()
		# await state.finish()
		else:
			await message.answer("Формат даты неверен, дата должна содержать только цифры.\nВведите дату установки в формате дд.мм.гггг:")
	else:
		await message.answer("Формат даты неверен.\nВведите дату установки в формате дд.мм.гггг:")


@dp.message_handler(state = TaskDoneState.PutDistance)
async def task_done_distance(message: types.Message, state: FSMContext):
	distance_done = message.text
	if distance_done.isdigit():
		await state.update_data(distance = distance_done)
		await TaskDoneState.PutPhoto.set()
	# await state.finish()
	else:
		await message.answer("Растояние пробега должно быть числом.\nВведите растояние пробега в км:")


@dp.message_handler(state = TaskDoneState.PutPhoto)
async def task_done_photo(message: types.Message, state: FSMContext):
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	distance = data_state.get("distance")
	date_day = data_state.get("date_day")
	date_month = data_state.get("date_month")
	date_year = data_state.get("date_year")
	full_date = "{}-{}-{} 00:00:00".format(date_year, date_month, date_day)
	enquiry = Enquiry(message.from_user.id)
	is_done = enquiry.update_act(id = id_task, f78361 = int(distance), f78311 = full_date, f78321 = "Установлено", f81381 = "hhhtttp")
	if is_done:
		print("record is changed")
	else:
		print("record is not changed")

	await state.finish()
