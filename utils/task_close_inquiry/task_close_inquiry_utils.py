from aiogram.utils.emoji import emojize


async def task_close_inquiry_put_date(current_date, message, state, TaskCloseInquiryState):
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	date_full = str(current_date).split(".")
	if len(date_full) == 3:
		if date_full[0].isdigit() and date_full[1].isdigit() and date_full[2].isdigit() and len(date_full[0]) == 2 and len(date_full[1]) == 2 and len(date_full[2]) == 4:
			# print("date_full[1] = {}".format(len(date_full[1])))
			date_day = date_full[0]
			date_month = date_full[1]
			date_year = date_full[2]
			await state.update_data(date_day = date_day, date_month = date_month, date_year = date_year)
			await message.answer("Заявка № <b>{}</b>\nВведите растояние пробега в км (ноль, если заявка в черте города):".format(id_task))
			await TaskCloseInquiryState.PutDistance.set()
		# await state.finish()
		else:
			await message.answer("Заявка № <b>{}</b>\n"
			                     "{}  Вы ввели неверную дату, дата должна содержать только цифры.\n"
			                     "Введите плановую дату установки оборудования в формате дд.мм.гггг:".format(id_task, emojize(
					":exclamation:")))
	else:
		await message.answer("Заявка № <b>{}</b>\n{}  Вы ввели неверную дату, пожалуйста,"
		                     " введите плановую дату установки оборудования в формате дд.мм.гггг:".format(id_task, emojize(":exclamation:")))
