from data.base_enquiry import BaseEnquiry


class Employee(BaseEnquiry):
	def __init__(self, telegram_user_id):
		super().__init__(telegram_user_id)
		self.__user_id = self._get_user_id(telegram_user_id)
		
	def is_member(self):
		return bool(self.__user_id)
