from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.emoji import emojize

from data.enquiry import Enquiry
from keyboards.inline.inline_type_request_menu import inline_type_request_menu
from loader import dp, bot
from states.task_to_plan_state import TaskToPlanState


@dp.callback_query_handler(regexp = "^task_to_plan#.+")
async def task_done_start(call: CallbackQuery, state: FSMContext):
	# print(f"task_done_start -> call.data = {call.data}")
	await call.message.edit_text("Введите плановую дату исполнения в формате дд.мм.гггг:")
	id_task = call.data.split("#")[1]
	await state.update_data(id_task = id_task)
	await TaskToPlanState.PutDate.set()
	# await call.message.delete()
	# message_id = call.message.message_id
	# get_me = await bot.get_me()
	# print("message_id = {}, get_me = {}".format(message_id, get_me))
	


@dp.message_handler(state = TaskToPlanState.PutDate)
async def task_done_date(message: Message, state: FSMContext):
	# await message.answer(f"Data = {message.text}")
	# message_id = message.message_id
	# get_me = await bot.get_me()
	# print("->message_id = {}, get_me = {}".format(message_id, get_me))
	# await bot.delete_message(1666850393, 1016)
	date_done = str(message.text)
	date_full = str(date_done).split(".")
	await message.delete()  # delete message from user (green color)
	# print(len(date_full))
	if len(date_full) == 3:
		if date_full[0].isdigit() and date_full[1].isdigit() and date_full[2].isdigit() and len(date_full[0]) == 2 and len(date_full[1]) == 2 and len(date_full[2]) == 4:
			# print("date_full[1] = {}".format(len(date_full[1])))
			date_day = date_full[0]
			date_month = date_full[1]
			date_year = date_full[2]
			full_date = "{}-{}-{} 00:00:00".format(date_year, date_month, date_day)
			short_date = "{}.{}.{}".format(date_day, date_month, date_year)
			# await state.update_data(date_day = date_day, date_month = date_month, date_year = date_year)
			data_state = await state.get_data()
			id_task = data_state.get("id_task")
			await state.finish()
			enquiry = Enquiry(message.from_user.id)
			# full_date = "2021-02-02 00:00:00"
			is_done = enquiry.update_table(id = id_task, f78311 = full_date, f78321 = "Запланирован выезд")
			# is_done = True
			if is_done:
				await message.answer("{} Заявка № <b>{}</b>, успешно запланирована на дату {}".
				                     format(emojize(":white_check_mark:"), str(id_task), short_date), reply_markup = inline_type_request_menu())
			else:
				await message.answer("{} Запись в БД завершилось ошибкой!".format(emojize(":bangbang:")))
		else:
			await message.answer("{}  Вы ввели неверную дату, дата должна содержать только цифры.\nВведите плановую дату исполнения в формате дд.мм.гггг:".format(emojize(
					":exclamation:")))
	else:
		await message.answer("{}  Вы ввели неверную дату, пожалуйста, введите плановую дату исполнения в формате дд.мм.гггг:".format(emojize(":exclamation:")))

