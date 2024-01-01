from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.utils.emoji import emojize

from keyboards.inline.choice_request_buttons import choice_request
from loader import dp, bot
from states.task_done_state import TaskDoneState
import aiohttp

from datetime import date
from data.enquiry import Enquiry
from data.cloud_storage import CloudStorage


################# Не участвует в процессе ##############################

@dp.callback_query_handler(regexp = "^task_trip_planned#.+")
async def task_done_start(call: CallbackQuery, state: FSMContext):
	# print("-> task_done call.data = {}".format(call.data))
	id_task = call.data.split("#")[1]
	await call.message.edit_text("Заявка № <b>{}</b>\nВведите дату установки в формате дд.мм.гггг:".format(id_task))
	# await call.message.answer(str(date.today()))
	
	await state.update_data(id_task = id_task)
	await TaskDoneState.PutDate.set()


@dp.message_handler(state = TaskDoneState.PutDate)
async def task_done_date(message: types.Message, state: FSMContext):
	# await message.answer(f"Data = {message.text}")
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
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
			await message.answer("Заявка № <b>{}</b>\nВведите растояние пробега в км:".format(id_task))
			await TaskDoneState.PutDistance.set()
		# await state.finish()
		else:
			await message.answer("Заявка № <b>{}</b>\nФормат даты неверен, дата должна содержать только цифры.\nВведите дату установки в формате дд.мм.гггг:".format(id_task))
	else:
		await message.answer("Заявка № <b>{}</b>\nФормат даты неверен.\nВведите дату установки в формате дд.мм.гггг:".format(id_task))


@dp.message_handler(state = TaskDoneState.PutDistance)
async def task_done_distance(message: types.Message, state: FSMContext):
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	distance_done = message.text
	if distance_done.isdigit():
		await state.update_data(distance = distance_done)
		await message.answer("Заявка № <b>{}</b>\nЗагрузите фотографию с актом проделанных работ, нажав на иконку {},"
		                     " или неберите слово 'нет', если акта нет:".format(id_task, emojize(":paperclip:")))
		await TaskDoneState.PutPhoto.set()
	# await state.finish()
	else:
		await message.answer("Заявка № <b>{}</b>\nРастояние пробега должно быть числом.\nВведите растояние пробега в км:".format(id_task))


@dp.message_handler(content_types = ContentType.ANY, state = TaskDoneState.PutPhoto)
async def task_done_photo(message: types.Message, state: FSMContext):
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	distance = data_state.get("distance")
	date_day = data_state.get("date_day")
	date_month = data_state.get("date_month")
	date_year = data_state.get("date_year")
	full_date = "{}-{}-{} 00:00:00".format(date_year, date_month, date_day)
	
	file_id = None
	content_type = message.content_type
	
	if content_type == "photo":
		file_id = message.photo[-1].file_id
	if content_type == "document":
		if message.document.mime_type.__contains__('image'):
			file_id = message.document.file_id
	
	if file_id is None:
		# await message.answer("Загруженный файл не фотография.\nПовторите попытку!")
		await message.answer("Заявка № <b>{}</b>\nФайл с фотографией акта не загружен и не сохранён.".format(id_task))
		file_path = ""
	else:
		await message.answer("Минутку, произвожу запись в БД...")
		dest_file = "photo_act_{}{}{}_{}.jpg".format(date_year, date_month, date_day, id_task)
		source_file = await bot.get_file(file_id)
		# print(f"file_link = {file_link}")
		file_path, is_saved = CloudStorage.save_file(source_file["file_path"], dest_file)
		await message.delete()
		if is_saved:
			await message.answer("Заявка № <b>{}</b>\n{}  Файл успешно сохранён и доступен по ссылке - {}".format(id_task, emojize(":white_check_mark:"), file_path),
			                     disable_web_page_preview = True)
		else:
			await message.answer("Заявка № <b>{}</b>\n{}  Файл не удалось сохранить.".format(id_task, emojize(":hangbang:")))
	enquiry = Enquiry(message.from_user.id)
	# full_date = "2021-02-02 00:00:00"
	# distance = 1
	is_done = enquiry.update_act(id = id_task, f81971 = int(distance), f81791 = full_date, f81771 = "Установлено", f82111 = file_path)
	if is_done:
		await message.answer("{} Запись в БД успешно обновлена! Заявка № <b>{}</b>, установлена в статус - <b>Установлено</b>".
		                     format(emojize(":white_check_mark:"), str(id_task)), reply_markup = choice_request())
	else:
		await message.answer("Заявка № <b>{}</b>\n{} Запись в БД завершилось ошибкой!".format(id_task, emojize(":hangbang:")))
	
	await state.finish()
