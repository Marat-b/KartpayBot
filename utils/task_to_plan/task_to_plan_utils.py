from aiogram.utils.emoji import emojize

from data.enquiry import Enquiry
from keyboards.inline.inline_type_request_menu import inline_type_request_menu


async def task_to_plan_put_date(current_date, message, state):
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	date_full = str(current_date).split(".")
	if len(date_full) == 3:
		if date_full[0].isdigit() and date_full[1].isdigit() and date_full[2].isdigit() and len(date_full[0]) == 2 and len(date_full[1]) == 2 and len(date_full[2]) == 4:
			# print("date_full[1] = {}".format(len(date_full[1])))
			date_day = date_full[0]
			date_month = date_full[1]
			date_year = date_full[2]
			full_date = "{}-{}-{} 00:00:00".format(date_year, date_month, date_day)
			short_date = "{}.{}.{}".format(date_day, date_month, date_year)
			# await state.update_data(date_day = date_day, date_month = date_month, date_year = date_year)
			
			await state.finish()
			enquiry = Enquiry(message.from_user.id)
			# enquiry = Enquiry('1771817746')
			# full_date = "2021-02-02 00:00:00"
			is_done = enquiry.update_table(id = id_task, f78311 = full_date, f78321 = "Запланирован выезд")
			# is_done = True
			if is_done:
				await message.answer("{} Заявка № <b>{}</b>, успешно запланирована на дату {}".
				                     format(emojize(":white_check_mark:"), str(id_task), short_date), reply_markup = inline_type_request_menu())
			else:
				await message.answer("Заявка № <b>{}</b>\n{} Запись в БД завершилось ошибкой!".format(id_task, emojize(":bangbang:")))
		else:
			await message.answer("Заявка № <b>{}</b>\n{}  Вы ввели неверную дату, дата должна содержать только цифры.\n"
			                     "Введите плановую дату исполнения в формате дд.мм.гггг:".format(id_task, emojize(
					":exclamation:")))
	else:
		await message.answer("Заявка № <b>{}</b>\n{}  Вы ввели неверную дату, "
		                     "пожалуйста, введите плановую дату исполнения в формате дд.мм.гггг:".format(id_task, emojize(":exclamation:")))
