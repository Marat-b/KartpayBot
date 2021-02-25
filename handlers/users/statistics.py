from aiogram.types import Message

from data.enquiry import Enquiry
from loader import dp


@dp.message_handler(regexp = "Статистика")
async def statistics_current_month(message: Message):
	print("statistics_current_month ->")
	enquiry = Enquiry(message.from_user.id)
	enquiry.get_entities()
