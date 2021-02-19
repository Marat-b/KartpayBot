import requests
import json
from data import config, access_id


class Enquiry:
	
	def __init__(self, telegram_user_id):
		self.__url_read_table = config.URL_READ_TABLE
		self.__request_telegramuser = config.REQUEST_TABLE_TELEGRAMUSER
		self.__request_telegramuser["filter"]["row"]["f81371"]["value"] = str(telegram_user_id)
		self.__user_id = self.__get_user_id(telegram_user_id)
	
	def get_entities(self, type_request):
		"""
		get all entities of requests
		:return: all records
		"""
		if self.__user_id is None:
			return list()
		request_db = config.REQUEST_DB.copy()
		request_db["filter"]["row"]["f79831"]["value"] = self.__user_id
		request_db["filter"]["row"]["f78321"]["value"] = type_request
		all_records = self.__get_records(request_db)
		return all_records
	
	def __get_records(self, request_db):
		"""
		Get records of clients once
		:param: db's records
		:return: All records of clients
		"""
		all_clients = list()
		id_access = access_id.Auth.get_access_id()
		if access_id is None:
			return all_clients
		request_db["access_id"] = id_access
		clients, json_table = self.__get_all_records(request_db, 0, int(config.MAX_AMOUNT_RECORDS))
		# summary all clients
		all_clients += clients
		amount_returned_records = int(json_table['count'])
		# print(f"returned_records = {amount_returned_records}")
		amount_all_records = int(json_table['count_all'])
		if amount_all_records > amount_returned_records:
			clients, _ = self.__get_all_records(request_db, amount_returned_records, amount_all_records)
			all_clients += clients
		return all_clients
	
	def __get_all_records(self, request_db, amount_returned_records, amount_all_records):
		"""
		Get added records of clients if amount_all_records greater than amount_returned_records
		:param request_db:
		:param amount_returned_records:
		:param amount_all_records:
		:return: All records of clients
		"""
		clients = list()
		request_db["start"] = amount_returned_records
		request_db["limit"] = amount_all_records
		try:
			# print(f"self.__url_read_table = {self.__url_read_table}, request_db = {request_db}")
			response_read_table = requests.post(self.__url_read_table, json = request_db)
			# convert records from text to json
			# print(f"response_read_table = {response_read_table}, response_read_table.text = {response_read_table.text}")
			json_table = json.loads(response_read_table.text)
			if int(json_table["code"]) != 0 or not ("data" in json_table.keys()):
				return clients, {"count": 0, "count_all": 0}
			# get data's keys from json with key "data"
			records = [record for record in json_table['data']]
			# get records with key "row"
			clients = [json_table['data'][record]["row"] for record in records]
			return clients, json_table
		except requests.exceptions.ConnectionError:
			return list(), {"count": 0, "count_all": 0}
	
	def __get_user_id(self, telegram_user_id):
		"""
		Get user ID for Kartpay
		:return: user ID for Kartpay
		"""
		all_records = self.__get_records(self.__request_telegramuser)
		# print(f"all_records = {all_records}")
		id_user = None
		for record in all_records:
			if str(telegram_user_id) == record["f81371"]:
				id_user = record["f81361"]
				break
		return id_user
	
	def update_act(self, **kwargs):
		"""
		Update record with status
		:param kwargs:
		:return:
		"""
		id_access = access_id.Auth.get_access_id()
		if self.__user_id is None or access_id is None:
			return False
		
		url_update_table = config.URL_UPDATE_TABLE
		update_table_act = config.UPDATE_TABLE_ACT.copy()
		update_table_act["access_id"] = id_access
		update_table_act["data"]["row"]["f78311"] = kwargs["f78311"]  # date of execution
		update_table_act["data"]["row"]["f78361"] = int(kwargs["f78361"])  # distance
		update_table_act["data"]["row"]["f78321"] = kwargs["f78321"]  # status
		update_table_act["data"]["row"]["f81381"] = kwargs["f81381"]  # photo path
		update_table_act["filter"]["row"]["id"]["value"] = kwargs["id"]  # id record
		# print(f"update_table_act = {update_table_act}")
		response_update_table = requests.post(url_update_table, json = update_table_act)
		# print(f"response_update_table = {response_update_table}")
		json_table = json.loads(response_update_table.text)
		# print(f"json_table = {json_table}")
		if int(json_table["code"]) == 0 or int(json_table["count"]) == 1:
			return True
		else:
			return False
		# return True


if __name__ == "__main__":
	r = Enquiry("919930316")
	# rr = Request("*********************", "Передан инженеру")
	clients = r.get_entities("Передан инженеру")
	print(r.get_entities("Передан инженеру"))
	
	for i, client in enumerate(clients):
		print(f"{str(i)}. Клиент = {client['f78201']}, Адрес клиента = {client['f78211']}, ID = {client['id']}, Телефон = {client['f78341']}, Статус = , "
		      f"Срок установки={client['f81181']} ")
