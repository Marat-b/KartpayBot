from aiogram.types import CallbackQuery
from aiogram.utils.emoji import emojize

from keyboards.inline.inline_type_request_menu import inline_type_request_menu
from loader import dp


@dp.callback_query_handler(text = "choice_buttons")
async def buttons(call: CallbackQuery):
	await call.message.edit_text("{}  Выберите тип заявки:".format(emojize(":point_down:")), reply_markup = inline_type_request_menu())
