from aiogram.types import CallbackQuery

from keyboards.inline.choice_request_buttons import choice_request
from loader import dp


@dp.callback_query_handler(text = "choice_buttons")
async def buttons(call: CallbackQuery):
	await call.message.edit_text("Выберите тип заявки:", reply_markup = choice_request())
