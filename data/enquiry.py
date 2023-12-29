import requests
import json
from data import config, access_id
from data.base_enquiry import BaseEnquiry
from data.config import f_act_photo, f_execution_date, f_executor, f_id, f_mileage, f_paid_to_performer, f_status, \
	f_telegram_id


class Enquiry(BaseEnquiry):
	
	def __init__(self, telegram_user_id = None):
		super().__init__(telegram_user_id)
		# self.telegram_user_id = telegram_user_id
		if telegram_user_id is None:
			self.__user_id = None
		else:
			self.__user_id = self._get_user_id(telegram_user_id)
	
	def get_entities(self, type_request):
		"""
		get all entities of requests
		:return: all records
		"""
		if self.__user_id is None:
			return list()
		request_db = config.REQUEST_DB.copy()
		request_db["filter"]["row"][f_executor]["value"] = self.__user_id
		# request_db["filter"]["row"][f_telegram_id]["value"] = self.telegram_user_id
		request_db["filter"]["row"][f_status]["value"] = type_request
		all_records = self._get_records(request_db)
		return all_records
	
	def get_entities_for_statistics(self, type_request: str):
		"""
		get count entities of requests
		:return: Number of records
		"""
		if self.__user_id is None:
			print('User is None')
			return []
		# request_db_str = config.REQUEST_FOR_COUNT_STATUS.replace("X", first_date).replace("Y", end_date)
		request_db = config.REQUEST_FOR_COUNT_STATUS.copy()
		request_db["filter"]["row"][f_executor]["value"] = self.__user_id
		request_db["filter"]["row"][f_status]["value"] = type_request
		request_db["filter"]["row"][f_paid_to_performer]["value"] = "Нет"
		print(f'request_db={request_db}')
		all_records = self._get_records(request_db)
		print(f'enquiry.get_entities_for_statistics all_records={all_records}')
		return all_records
	
	def get_entities_for_payed(self):
		"""
		get payed entities of requests
		:return: Number of records
		"""
		if self.__user_id is None:
			return []
		# request_db_str = config.REQUEST_FOR_PAYED.replace("X", first_date).replace("Y", end_date)
		# print(request_db_str)
		# request_db = json.loads(request_db_str)
		request_db = config.REQUEST_FOR_PAYED.copy()
		request_db["filter"]["row"][f_executor]["value"] = self.__user_id
		request_db["filter"]["row"][f_paid_to_performer]["value"] = "Да"
		all_records = self._get_records(request_db)
		return all_records
	
	def get_entities_for_paying(self, type_request, yes_no):
		"""
		get all entities for paying (f82091 - negative, f81771 - upd is signed)
		:return: all records
		"""
		if self.__user_id is None:
			return list()
		request_db = config.REQUEST_FOR_PAYING.copy()
		request_db["filter"]["row"][f_executor]["value"] = self.__user_id
		request_db["filter"]["row"][f_status]["value"] = type_request
		request_db["filter"]["row"][f_paid_to_performer]["value"] = yes_no
		all_records = self._get_records(request_db)
		return all_records
	
	def get_entity_by_id(self, id_entity):
		"""
		Get information's entity by ID's entity
		:param id_entity: ID entity
		:return: record of information's entity
		"""
		if self.__user_id is None:
			return 0
		request_db = config.REQUEST_BY_ID.copy()
		request_db["filter"]["row"][f_executor]["value"] = self.__user_id
		request_db["filter"]["row"][f_id]["value"] = id_entity
		all_records = self._get_records(request_db)
		return all_records
	
	def update_act(self, **kwargs):
		"""
		Update record with status
		:param kwargs:
		:return:
		"""
		id_access = access_id.Auth.get_access_id()
		if access_id is None:
			return False
		
		url_update_table = config.URL_UPDATE_TABLE
		update_table_act = config.UPDATE_TABLE_ACT.copy()
		update_table_act["access_id"] = id_access
		update_table_act["data"]["row"][f_execution_date] = kwargs[f_execution_date]  # date of execution
		update_table_act["data"]["row"][f_mileage] = int(kwargs[f_mileage])  # distance
		update_table_act["data"]["row"][f_status] = kwargs[f_status]  # status
		update_table_act["data"]["row"][f_act_photo] = kwargs[f_act_photo]  # photo path
		update_table_act["filter"]["row"][f_id]["value"] = kwargs[f_id]  # id record
		# print(f"update_table_act = {update_table_act}")
		response_update_table = requests.post(url_update_table, json = update_table_act)
		# print(f"response_update_table = {response_update_table}")
		json_table = json.loads(response_update_table.text)
		# print(f"json_table = {json_table}")
		if int(json_table["code"]) == 0 or int(json_table["count"]) == 1:
			return True
		else:
			return False
	
	def update_table(self, **kwargs):
		id_access = access_id.Auth.get_access_id()
		if access_id is None:
			return False
		
		url_update_table = config.URL_UPDATE_TABLE
		update_table = config.UPDATE_TABLE_UPD.copy()
		update_table["access_id"] = id_access
		update_table["filter"]["row"][f_id]["value"] = kwargs[f_id]  # id record
		for args in kwargs:
			if args[0] == "f":
				update_table["data"]["row"][args] = kwargs[args]
		response_update_table = requests.post(url_update_table, json = update_table)
		# print(f"response_update_table = {response_update_table}")
		json_table = json.loads(response_update_table.text)
		# print(f"json_table = {json_table}")
		if int(json_table["code"]) == 0 or int(json_table["count"]) == 1:
			return True
		else:
			return False
		
	


if __name__ == "__main__":
	r = Enquiry("147166708")
	# rr = Request("*********************", "Передан инженеру")
	# clients = r.get_entities("Передан инженеру")
	# print(r.get_entities("Передан инженеру"))
	# print(r.get_entities_for_statistics("Установлено", "2021-02-01 00:00:00", "2021-02-28 23:59:59"))
	# print(r.get_entities_for_statistics("Установлено", "2021-03-01 00:00:01", "2021-03-31 23:59:59"))
	print(r.get_entities_for_statistics("Установлено"))
	print((r.get_entities_for_payed()))
	print(r.get_entity_by_id("1100"))
	
	# for i, client in enumerate(clients):
	# 	print(f"{str(i)}. Клиент = {client['f78201']}, Адрес клиента = {client['f78211']}, ID = {client['id']}, Телефон = {client['f78341']}, Статус = , "
	# 	      f"Срок установки={client['f81181']} ")
	#
	# print(r.update_table(f78321 = "78321", f81301 = "81301", id = f_id))
