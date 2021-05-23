from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.utils.emoji import emojize

from data.cloud_storage import CloudStorage
from data.config import STATUS_UPD_SIGNED
from data.enquiry import Enquiry
from keyboards.inline.inline_back_to_setup import inline_back_to_setup
from keyboards.inline.inline_type_request_menu import inline_type_request_menu
from loader import dp, bot
from states.task_edit_state import TaskEditState
from utils.create_filename import create_filename


@dp.callback_query_handler(regexp = "^task_edit_distance#.+")
async def task_edit_distance(call: CallbackQuery, state: FSMContext):
	id_task = call.data.split("#")[1]
	await call.message.edit_text("Заявка № <b>{}</b>\nВведите растояние пробега в км (ноль, если заявка в черте города):".format(id_task))
	# await call.message.answer(str(date.today()))
	
	await state.update_data(id_task = id_task)
	await TaskEditState.PutDistance.set()


@dp.message_handler(state = TaskEditState.PutDistance)
async def task_edit_distance_done(message: Message, state: FSMContext):
	distance_done = message.text
	if distance_done.isdigit():
		# await state.update_data(distance = distance_done)
		data_state = await state.get_data()
		id_task = data_state.get("id_task")
		enquiry = Enquiry()
		
		is_done = enquiry.update_table(id = id_task, f78361 = int(distance_done))
		if is_done:
			await message.answer("Заявка № <b>{}</b>\n{} Пробег по заявке № <b>{}</b> успешно отредактирован".format(id_task, emojize(":white_check_mark:"), str(id_task)),
			                     reply_markup = inline_back_to_setup())
		else:
			await message.answer("Заявка № <b>{}</b>\n{} Запись в БД завершилось ошибкой!".format(id_task, emojize(":hangbang:")))
		
		await state.finish()
	else:
		await message.answer("{}  Растояние пробега должно быть числом.\nВведите растояние пробега в км (ноль, если заявка в черте города):".format(emojize(":exclamation:")),
		                     reply_markup = inline_back_to_setup())


@dp.callback_query_handler(regexp = "^task_edit_act#.+")
async def task_edit_distance(call: CallbackQuery, state: FSMContext):
	id_task = call.data.split("#")[1]
	await call.message.edit_text("Заявка № <b>{}</b>\nЗагрузите фотографию с актом выполненных работ, нажав на иконку {}, или нажмите кнопку 'Назад', для отмены:".format(id_task,
	                                                                                                                                                                   emojize(
		                                                                                                                                                                   ":paperclip:")),
	                             reply_markup = inline_back_to_setup())
	# await call.message.answer(str(date.today()))
	
	await state.update_data(id_task = id_task)
	await TaskEditState.PutActPhoto.set()


@dp.message_handler(content_types = ContentType.ANY, state = TaskEditState.PutActPhoto)
async def task_act_photo(message: Message, state: FSMContext):
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	content_type = message.content_type
	file_id = None
	await message.delete()
	
	if content_type == "photo":
		file_id = message.photo[-1].file_id
	if content_type == "document":
		if message.document.mime_type.__contains__('image'):
			file_id = message.document.file_id
	
	if file_id is None:
		await message.answer("Заявка № <b>{}</b>\n{}  Загруженный файл не фотография.\nПовторите попытку!".format(id_task, emojize(":exclamation:")), reply_markup =
		inline_back_to_setup())
		# await message.answer("Файл с фотографией акта не загружен и не сохранён.")
		file_path = ""
	else:
		# await message.answer("Минутку, произвожу запись в БД...")
		source_file = await bot.get_file(file_id)
		# print(f"file_link = {file_link}")
		file_path, is_saved = CloudStorage.save_file(source_file["file_path"], create_filename("photo_act", id_task))
		if is_saved:
			# await message.answer("{}  Файл успешно сохранён и доступен по ссылке - {}".format(emojize(":white_check_mark:"), file_path), disable_web_page_preview = True)
			enquiry = Enquiry()
			is_done = enquiry.update_table(id = id_task, f81381 = file_path)
			if is_done:
				await message.answer("{} Акт выполненных работ по заявке № <b>{}</b>, успешно загружен.".
				                     format(emojize(":white_check_mark:"), str(id_task)), reply_markup = inline_back_to_setup())
			
			else:
				await message.answer("Заявка № <b>{}</b>\n{} Запись в БД завершилось ошибкой!".format(id_task, emojize(":bangbang:")), reply_markup = inline_back_to_setup())
		
		else:
			await message.answer("Заявка № <b>{}</b>\n{}  Файл не удалось сохранить.".format(id_task, emojize(":bangbang:")), reply_markup = inline_back_to_setup())
		await state.finish()
		await message.delete()


################## Task UPD #########################################

@dp.callback_query_handler(regexp = "^task_edit_upd#.+")
async def task_edit_upd(call: CallbackQuery, state: FSMContext):
	id_task = call.data.split("#")[1]
	await call.message.edit_text("Заявка № <b>{}</b>\nЗагрузите фотографию с УПД, нажав на иконку {}, или нажмите кнопку 'Назад', для отмены:".format(id_task,
			emojize(":paperclip:")), reply_markup = inline_back_to_setup())
	# await call.message.answer(str(date.today()))
	
	await state.update_data(id_task = id_task)
	await TaskEditState.PutUpdPhoto.set()


@dp.message_handler(content_types = ContentType.ANY, state = TaskEditState.PutUpdPhoto)
async def task_act_photo(message: Message, state: FSMContext):
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	content_type = message.content_type
	file_id = None
	await message.delete()
	
	if content_type == "photo":
		file_id = message.photo[-1].file_id
	if content_type == "document":
		if message.document.mime_type.__contains__('image'):
			file_id = message.document.file_id
	
	if file_id is None:
		await message.answer("Заявка № <b>{}</b>\n{}  Загруженный файл не фотография.\nПовторите попытку!".format(id_task, emojize(":exclamation:")), reply_markup =
		inline_back_to_setup())
		# await message.answer("Файл с фотографией акта не загружен и не сохранён.")
		file_path = ""
	else:
		# await message.answer("Минутку, произвожу запись в БД...")
		source_file = await bot.get_file(file_id)
		# print(f"file_link = {file_link}")
		file_path, is_saved = CloudStorage.save_file(source_file["file_path"], create_filename("photo_upd", id_task))
		if is_saved:
			# await message.answer("{}  Файл успешно сохранён и доступен по ссылке - {}".format(emojize(":white_check_mark:"), file_path), disable_web_page_preview = True)
			enquiry = Enquiry()
			is_done = enquiry.update_table(id = id_task, f78321 = STATUS_UPD_SIGNED, f81301 = file_path)
			if is_done:
				await message.answer("{} УПД по заявке № <b>{}</b>, успешно загружен.".
				                     format(emojize(":white_check_mark:"), str(id_task)), reply_markup = inline_back_to_setup())
			
			else:
				await message.answer("Заявка № <b>{}</b>\n{} Запись в БД завершилось ошибкой!".format(id_task, emojize(":bangbang:")), reply_markup = inline_back_to_setup())
		
		else:
			await message.answer("Заявка № <b>{}</b>\n{}  Файл не удалось сохранить.".format(id_task, emojize(":bangbang:")), reply_markup = inline_back_to_setup())
		await state.finish()
