from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

from data.employee import Employee


class IsMember(BoundFilter):
	
	async def check(self, message: Message):
		employee = Employee(message.from_user.id)
		member = employee.is_member()
		return bool(member)
