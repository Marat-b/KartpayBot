import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType
from aiogram.utils.emoji import emojize

from data.cloud_storage import CloudStorage
from data.enquiry import Enquiry
from keyboards.inline.choice_request_buttons import choice_request
from loader import dp, bot
from states.task_setup_state import TaskSetupState


@dp.callback_query_handler(regexp = "^task_setup#.+")
async def task_setup(call: CallbackQuery, state: FSMContext):
	# print(f"task_done_start -> call.data = {call.data}")
	await call.message.edit_text("Загрузите фотографию с подписанным УПД, нажав на иконку {}, или неберите слово 'нет', если УПД нет:".format(emojize(":paperclip:")))
	# await call.message.answer(str(date.today()))
	id_task = call.data.split("#")[1]
	await state.update_data(id_task = id_task)
	await TaskSetupState.PutPhoto.set()


@dp.message_handler(content_types = ContentType.ANY, state = TaskSetupState.PutPhoto)
async def task_done_photo(message: types.Message, state: FSMContext):
	data_state = await state.get_data()
	id_task = data_state.get("id_task")
	date_day = (lambda x: "0" + x if len(x) == 1 else x)(str(datetime.date.today().day))
	date_month = (lambda x: "0" + x if len(x) == 1 else x)(str(datetime.date.today().month))
	date_year = str(datetime.date.today().year)
	
	file_id = None
	content_type = message.content_type
	
	if content_type == "photo":
		file_id = message.photo[-1].file_id
	if content_type == "document":
		if message.document.mime_type.__contains__('image'):
			file_id = message.document.file_id
	
	if file_id is None:
		# await message.answer("Загруженный файл не фотография.\nПовторите попытку!")
		await message.answer("Файл с фотографией УПД не загружен и не сохранён.")
		file_path = ""
	else:
		await message.answer("Минутку, произвожу запись в БД...")
		dest_file = "photo_upd_{}{}{}_{}.jpg".format(date_year, date_month, date_day, id_task)
		source_file = await bot.get_file(file_id)
		# print(f"file_link = {dest_file}")
		file_path, is_saved = CloudStorage.save_file(source_file["file_path"], dest_file)
		await message.delete()
		if is_saved:
			await message.answer("{}  Файл успешно сохранён и доступен по ссылке - {}".format(emojize(":white_check_mark:"), file_path), disable_web_page_preview = True)
		else:
			await message.answer("{}  Файл не удалось сохранить.".format(emojize(":hangbang:")))
	enquiry = Enquiry(message.from_user.id)
	
	is_done = enquiry.update_table(id = id_task, f78321 = "УПД подписан", f81301 = file_path)
	if is_done:
		await message.answer("{}  Запись в БД успешно обновлена! Заявка № <b>{}</b>, установлена в статус - <b>УПД подписан</b>".format(emojize(
			":white_check_mark:"), str(id_task)), reply_markup = choice_request())
	else:
		await message.answer("{} Запись в БД завершилось ошибкой!".format(emojize(":hangbang:")))
	
	await state.finish()
