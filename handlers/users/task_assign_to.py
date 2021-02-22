from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.emoji import emojize

from data.enquiry import Enquiry
from keyboards.inline.choice_request_buttons import choice_request
from loader import dp


@dp.callback_query_handler(regexp = "^task_assign_to#.+")
async def task_done_start(call: CallbackQuery):
	# print(f"task_done_start -> call.data = {call.data}")
	id_task = call.data.split("#")[1]
	enquiry = Enquiry(call.from_user.id)
	
	is_done = enquiry.update_table(id = id_task, f78321 = "Запланирован выезд")
	if is_done:
		await call.message.edit_text("{}  Запись в БД успешно обновлена! Заявка № <b>{}</b>, установлена в статус - <b>Запланирован выезд</b>".format(emojize(
				":white_check_mark:"), str(id_task)), reply_markup = choice_request())
	else:
		await call.message.edit_text("{}  Запись в БД завершилось ошибкой!".format(emojize(":hangbang:")), reply_markup = choice_request())
