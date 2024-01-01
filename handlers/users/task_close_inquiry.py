from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.utils.emoji import emojize

from data.cloud_storage import CloudStorage
from data.config import STATUS_SETUP
from data.enquiry import Enquiry
from keyboards.inline.inline_act_is_missing import inline_act_is_missing
from keyboards.inline.inline_current_date import cb_current_date, inline_current_date
from keyboards.inline.inline_type_request_menu import inline_type_request_menu
from keyboards.inline.inline_upd_is_missing import inline_upd_is_missing
from loader import dp, bot
from states.task_close_inquire_state import TaskCloseInquiryState
from utils.create_date import get_date_DMY
from utils.create_filename import create_filename


##################################################################
############### Закрыть заявку ###################################
##################################################################
from utils.task_close_inquiry.task_close_inquiry_utils import task_close_inquiry_put_date


@dp.callback_query_handler(regexp = "^task_close_inquire#.+")
async def task_done_start(call: CallbackQuery, state: FSMContext):
	# print(f"task_done_start -> call.data = {call.data}")
	id_task = call.data.split("#")[1]
	current_date = get_date_DMY()
	await call.message.edit_text("Заявка № <b>{}</b>\nВведите дату установки в формате дд.мм.гггг,"
	                             "или нажмите кнопку для ввода текущей даты.".format(id_task), reply_markup = inline_current_date(current_date))
	
	await state.update_data(id_task = id_task)
	await TaskCloseInquiryState.PutDate.set()


@dp.callback_query_handler(cb_current_date.filter(button_name = 'button_current_date'), state = TaskCloseInquiryState.PutDate)
async def current_date_was_pressed(call: CallbackQuery, callback_data: dict, state: FSMContext):
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
	await task_close_inquiry_put_date(current_date, call.message, state, TaskCloseInquiryState)


# await TaskToPlanState.PutDate.set()
# await call.message.answer(f'Дата установлена в {current_date}')


@dp.message_handler(state = TaskCloseInquiryState.PutDate)
async def task_done_date(message: Message, state: FSMContext):
	# await message.answer(f"Data = {message.text}")
	
	date_done = str(message.text)
	await task_close_inquiry_put_date(date_done, message, state, TaskCloseInquiryState)
	# print(len(date_full))
	

@dp.message_handler(state = TaskCloseInquiryState.PutDistance)
async def task_done_distance(message: Message, state: FSMContext):
	distance_done = message.text
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	if distance_done.isdigit():
		# await state.update_data(distance = distance_done)
		
		date_day = data_state.get("date_day")
		date_month = data_state.get("date_month")
		date_year = data_state.get("date_year")
		
		full_date = "{}-{}-{} 00:00:00".format(date_year, date_month, date_day)
		enquiry = Enquiry(message.from_user.id)
		
		is_done = enquiry.update_table(id = id_task, f81971 = int(distance_done), f81791 = full_date, f81771 = STATUS_SETUP)
		# if is_done:
		# 	await message.answer("{} Запись в БД успешно обновлена! Заявка № <b>{}</b>, установлена в статус - <b>Установлено</b>".
		# 	                     format(emojize(":white_check_mark:"), str(id_task)))
		# else:
		# 	await message.answer("{} Запись в БД завершилось ошибкой!".format(emojize(":hangbang:")))
		await message.answer(
				"Заявка № <b>{}</b>\nЗагрузите фотографию с актом проделанных работ, нажав на иконку {}, или нажмите кнопку <b>Акт отсутствует</b>, если акт будет приложен "
				"позднее:".format(id_task,
				                  emojize(
						                  ":paperclip:")), reply_markup = inline_act_is_missing())
		await TaskCloseInquiryState.PutActPhoto.set()
	# await state.finish()
	else:
		await message.answer("Заявка № <b>{}</b>\nРастояние пробега должно быть числом.\nВведите растояние пробега в км (ноль, если заявка в черте города):".format(id_task))


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
	is_done = enquiry.update_table(id = id_task, f82111 = file_path)
	# if is_done:
	# 	await message.answer("{} Запись в БД успешно обновлена! Заявка № <b>{}</b>, установлена в статус - <b>Установлено</b>".
	# 	                     format(emojize(":white_check_mark:"), str(id_task)))
	# else:
	# 	await message.answer("{} Запись в БД завершилось ошибкой!".format(emojize(":hangbang:")))
	await message.answer("Заявка № <b>{}</b>\nЗагрузите фотографию УПД, нажав на иконку {},"
	                     " или нажмите кнопку <b>УПД отсутствует</b>, если УПД будет приложен позднее:".format(id_task,
	                                                                                                           emojize(
			                                                                                                           ":paperclip:")), reply_markup = inline_upd_is_missing())
	await TaskCloseInquiryState.PutUpdPhoto.set()


@dp.callback_query_handler(regexp = "^act_is_missing", state = TaskCloseInquiryState.PutActPhoto)
async def act_is_missing(call: CallbackQuery, state: FSMContext):
	await TaskCloseInquiryState.PutUpdPhoto.set()
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	await call.message.answer("Заявка № <b>{}</b>\nЗагрузите фотографию УПД, нажав на иконку {},"
	                          " или нажмите кнопку <b>УПД отсутствует</b>, если УПД будет приложен позднее:".format(id_task,
	                                                                                                                emojize(":paperclip:")), reply_markup =
	                          inline_upd_is_missing())


@dp.callback_query_handler(regexp = "^upd_is_missing", state = TaskCloseInquiryState.PutUpdPhoto)
async def act_upd_missing(call: CallbackQuery, state: FSMContext):
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	# print("call.message.from_user.id = {}".format(call.message.from_user.id))
	# print("get me = {}".format(await bot.get_me()))
	enquiry = Enquiry()
	is_done = enquiry.update_table(id = id_task, f81771 = STATUS_SETUP)
	if is_done:
		await call.message.answer("{} Запись в БД успешно обновлена! Заявка № <b>{}</b>, установлена в статус - <b>Установлен</b>.\nЗаявка исполнена, но не доступна к выплате.".
		                          format(emojize(":white_check_mark:"), str(id_task)), reply_markup = inline_type_request_menu())
	else:
		await call.message.answer("Заявка № <b>{}</b>\n{} Запись в БД завершилось ошибкой!".format(id_task, emojize(":bangbang:")), reply_markup = inline_type_request_menu())
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
		is_done = enquiry.update_table(id = id_task, f81771 = "УПД подписан", f82101 = file_path)
		if is_done:
			await message.answer("{} Запись в БД успешно обновлена! Заявка № <b>{}</b>, установлена в статус - <b>УПД подписан</b>.\n<u>Заявка доступна к выплате.</u>".
			                     format(emojize(":white_check_mark:"), str(id_task)), reply_markup = inline_type_request_menu())
		else:
			await message.answer("Заявка № <b>{}</b>\n{} Запись в БД завершилось ошибкой!".format(id_task, emojize(":bangbang:")), reply_markup = inline_type_request_menu())
	await state.finish()
