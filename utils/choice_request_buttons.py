from aiogram.types import Message
from aiogram.utils.emoji import emojize

from data.config import main_title
from keyboards.inline.inline_type_request_menu import inline_type_request_menu


async def choice_request_buttons(message: Message):
	await message.delete()
	await message.answer("{}Выберите тип заявки {}".format(main_title, emojize(":point_down:")), reply_markup = inline_type_request_menu(), disable_notification = True)
