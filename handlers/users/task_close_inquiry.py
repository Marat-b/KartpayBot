from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.utils.emoji import emojize

from data.cloud_storage import CloudStorage
from data.config import STATUS_SETUP
from data.enquiry import Enquiry
from keyboards.inline.inline_act_is_missing import inline_act_is_missing
from keyboards.inline.inline_type_request_menu import inline_type_request_menu
from keyboards.inline.inline_upd_is_missing import inline_upd_is_missing
from loader import dp, bot
from states.task_close_inquire_state import TaskCloseInquiryState
from utils.create_filename import create_filename


@dp.callback_query_handler(regexp = "^task_close_inquire#.+")
async def task_done_start(call: CallbackQuery, state: FSMContext):
	# print(f"task_done_start -> call.data = {call.data}")
	await call.message.edit_text("Введите дату установки в формате дд.мм.гггг:")
	id_task = call.data.split("#")[1]
	await state.update_data(id_task = id_task)
	await TaskCloseInquiryState.PutDate.set()


@dp.message_handler(state = TaskCloseInquiryState.PutDate)
async def task_done_date(message: Message, state: FSMContext):
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
			await message.answer("Введите растояние пробега в км (ноль, если заявка в черте города):")
			await TaskCloseInquiryState.PutDistance.set()
		# await state.finish()
		else:
			await message.answer(
					"{}  Вы ввели неверную дату, дата должна содержать только цифры.\nВведите плановую дату установки оборудования в формате дд.мм.гггг:".format(emojize(
							":exclamation:")))
	else:
		await message.answer("{}  Вы ввели неверную дату, пожалуйста, введите плановую дату установки оборудования в формате дд.мм.гггг:".format(emojize(":exclamation:")))


@dp.message_handler(state = TaskCloseInquiryState.PutDistance)
async def task_done_distance(message: Message, state: FSMContext):
	distance_done = message.text
	if distance_done.isdigit():
		# await state.update_data(distance = distance_done)
		data_state = await state.get_data()
		date_day = data_state.get("date_day")
		date_month = data_state.get("date_month")
		date_year = data_state.get("date_year")
		id_task = data_state.get("id_task")
		full_date = "{}-{}-{} 00:00:00".format(date_year, date_month, date_day)
		enquiry = Enquiry(message.from_user.id)
		
		is_done = enquiry.update_table(id = id_task, f78361 = int(distance_done), f78311 = full_date, f78321 = STATUS_SETUP)
		# if is_done:
		# 	await message.answer("{} Запись в БД успешно обновлена! Заявка № <b>{}</b>, установлена в статус - <b>Установлено</b>".
		# 	                     format(emojize(":white_check_mark:"), str(id_task)))
		# else:
		# 	await message.answer("{} Запись в БД завершилось ошибкой!".format(emojize(":hangbang:")))
		await message.answer("Загрузите фотографию с актом проделанных работ, нажав на иконку {}, или нажмите кнопку <b>Акт отсутствует</b>, если акт будет приложен "
		                     "позднее:".format(
				emojize(
						":paperclip:")), reply_markup = inline_act_is_missing())
		await TaskCloseInquiryState.PutActPhoto.set()
		# await state.finish()
	else:
		await message.answer("Растояние пробега должно быть числом.\nВведите растояние пробега в км (ноль, если заявка в черте города):")


@dp.message_handler(content_types = ContentType.ANY, state = TaskCloseInquiryState.PutActPhoto)
async def task_act_photo(message: Message, state: FSMContext):
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	content_type = message.content_type
	file_id = None
	
	if content_type == "photo":
		file_id = message.photo[-1].file_id
	if content_type == "document":
		if message.document.mime_type.__contains__('image'):
			file_id = message.document.file_id
	
	if file_id is None:
		# await message.answer("Загруженный файл не фотография.\nПовторите попытку!")
		# await message.answer("Файл с фотографией акта не загружен и не сохранён.")
		file_path = ""
	else:
		# await message.answer("Минутку, произвожу запись в БД...")
		source_file = await bot.get_file(file_id)
		# print(f"file_link = {file_link}")
		file_path, is_saved = CloudStorage.save_file(source_file["file_path"], create_filename("photo_act", id_task))
		# if is_saved:
		# 	await message.answer("{}  Файл успешно сохранён и доступен по ссылке - {}".format(emojize(":white_check_mark:"), file_path), disable_web_page_preview = True)
		# else:
		# 	await message.answer("{}  Файл не удалось сохранить.".format(emojize(":hangbang:")))
		await message.delete()
	
	enquiry = Enquiry(message.from_user.id)
	is_done = enquiry.update_table(id = id_task, f81381 = file_path)
	# if is_done:
	# 	await message.answer("{} Запись в БД успешно обновлена! Заявка № <b>{}</b>, установлена в статус - <b>Установлено</b>".
	# 	                     format(emojize(":white_check_mark:"), str(id_task)))
	# else:
	# 	await message.answer("{} Запись в БД завершилось ошибкой!".format(emojize(":hangbang:")))
	await message.answer("Загрузите фотографию УПД, нажав на иконку {}, или нажмите кнопку <b>УПД отсутствует</b>, если УПД будет приложен позднее:".format(
			emojize(
					":paperclip:")), reply_markup = inline_upd_is_missing())
	await TaskCloseInquiryState.PutUpdPhoto.set()


@dp.callback_query_handler(regexp = "^act_is_missing", state = TaskCloseInquiryState.PutActPhoto)
async def act_is_missing(call: CallbackQuery, state: FSMContext):
	await TaskCloseInquiryState.PutUpdPhoto.set()
	await call.message.answer("Загрузите фотографию УПД, нажав на иконку {}, или нажмите кнопку <b>УПД отсутствует</b>, если УПД будет приложен позднее:".format(
			emojize(":paperclip:")), reply_markup = inline_upd_is_missing())


@dp.callback_query_handler(regexp = "^upd_is_missing", state = TaskCloseInquiryState.PutUpdPhoto)
async def act_upd_missing(call: CallbackQuery, state: FSMContext):
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	# print("call.message.from_user.id = {}".format(call.message.from_user.id))
	# print("get me = {}".format(await bot.get_me()))
	enquiry = Enquiry()
	is_done = enquiry.update_table(id = id_task, f78321 = STATUS_SETUP)
	if is_done:
		await call.message.answer("{} Запись в БД успешно обновлена! Заявка № <b>{}</b>, установлена в статус - <b>Установлен</b>.\nЗаявка исполнена, но не доступна к выплате.".
		                     format(emojize(":white_check_mark:"), str(id_task)), reply_markup = inline_type_request_menu())
	else:
		await call.message.answer("{} Запись в БД завершилось ошибкой!".format(emojize(":bangbang:")), reply_markup = inline_type_request_menu())
	await state.finish()


@dp.message_handler(content_types = ContentType.ANY, state = TaskCloseInquiryState.PutUpdPhoto)
async def task_upd_photo(message: Message, state: FSMContext):
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	content_type = message.content_type
	file_id = None
	
	if content_type == "photo":
		file_id = message.photo[-1].file_id
	if content_type == "document":
		if message.document.mime_type.__contains__('image'):
			file_id = message.document.file_id
	
	if file_id is None:
		# await message.answer("Загруженный файл не фотография.\nПовторите попытку!")
		# await message.answer("Файл с фотографией акта не загружен и не сохранён.")
		file_path = ""
		await message.answer("{} Заявка № <b>{}</b>, установлена в статус - <b>Установлен</b>.\nЗаявка исполнена, но не доступна к выплате.".
		                          format(emojize(":white_check_mark:"), str(id_task)), reply_markup = inline_type_request_menu())
	else:
		# await message.answer("Минутку, произвожу запись в БД...")
		source_file = await bot.get_file(file_id)
		# print(f"file_link = {file_link}")
		file_path, is_saved = CloudStorage.save_file(source_file["file_path"], create_filename("photo_upd", id_task))
		# if is_saved:
		# 	await message.answer("{}  Файл успешно сохранён и доступен по ссылке - {}".format(emojize(":white_check_mark:"), file_path), disable_web_page_preview = True)
		# else:
		# 	await message.answer("{}  Файл не удалось сохранить.".format(emojize(":hangbang:")))
		await message.delete()
	
		enquiry = Enquiry(message.from_user.id)
		is_done = enquiry.update_table(id = id_task, f78321 = "УПД подписан", f81301 = file_path)
		if is_done:
			await message.answer("{} Запись в БД успешно обновлена! Заявка № <b>{}</b>, установлена в статус - <b>УПД подписан</b>.\n<u>Заявка доступна к выплате.</u>".
			                     format(emojize(":white_check_mark:"), str(id_task)),reply_markup = inline_type_request_menu())
		else:
			await message.answer("{} Запись в БД завершилось ошибкой!".format(emojize(":bangbang:")), reply_markup = inline_type_request_menu())
	await state.finish()
