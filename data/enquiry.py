import requests
import json
from data import config, access_id


class Enquiry:
	# __request_db = {"table_id": 6101, "cals": True, "fields": {"row": ["f78201", "f78211", "id", "f78341", "f81181"]},
	#                 "filter": {"row": {
	# 	                "status": {"term": "=", "value": 0, "union": "AND"},
	# 	                "f79831": {"term": "=", "value": "", "union": "AND"},
	# 	                "f78321": {"term": "=", "value": "", "union": "AND"}
	#                 }},
	#                 "sort": {"row": {"f81181": "ASC"}}, "start": 0, "limit": 0}
	# __url_read_table = "https://kartpay.clientbase.ru/api/data/read"
	
	def __init__(self, telegram_user_id, type_request):
		self.__user_id = self.__get_user_id(telegram_user_id)
		self.__url_read_table = config.URL_READ_TABLE
		self.__request_db = config.REQUEST_DB.copy()
		self.__request_db["cals"] = True
		self.__request_db["filter"]["row"]["f79831"]["value"] = self.__user_id
		self.__request_db["filter"]["row"]["f78321"]["value"] = type_request
	
	def get_records(self):
		"""
		Get records of clients once
		:return: All records of clients
		"""
		if self.__user_id is None:
			return list()
		all_clients = list()
		id_access = access_id.Auth.get_access_id()
		if access_id is None:
			return all_clients
		self.__request_db["access_id"] = id_access
		clients, json_table = self.__get_all_records(0, int(config.MAX_AMOUNT_RECORDS))
		# summary all clients
		all_clients += clients
		amount_returned_records = int(json_table['count'])
		# print(f"returned_records = {amount_returned_records}")
		amount_all_records = int(json_table['count_all'])
		if amount_all_records > amount_returned_records:
			clients, _ = self.__get_all_records(amount_returned_records, amount_all_records)
			all_clients += clients
		return all_clients
	
	def __get_all_records(self, amount_returned_records, amount_all_records):
		"""
		Get added records of clients if amount_all_records greater than amount_returned_records
		:param amount_returned_records:
		:param amount_all_records:
		:return: All records of clients
		"""
		clients = list()
		# for start in range(amount_returned_records, amount_all_records, step):
		self.__request_db["start"] = amount_returned_records
		self.__request_db["limit"] = amount_all_records
		# post_read_table3["access_id"] = Auth.get_access_id()
		try:
			# print(f"self.__url_read_table = {self.__url_read_table}, self.__request_db = {self.__request_db}")
			response_read_table = requests.post(self.__url_read_table, json = self.__request_db)
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
		id = None
		for user_id in config.ADMINS:
			if str(telegram_user_id) == user_id:
				id = "3421"
				break
		return id
		# if str(telegram_user_id) == str(config.ADMINS):
		# 	return "3421"
		# else:
		# 	return None


if __name__ == "__main__":
	r = Enquiry("919930316", "Передан инженеру")
	# rr = Request("*********************", "Передан инженеру")
	clients = r.get_records()
	print(r.get_records())
	
	for i, client in enumerate(clients):
		print(f"{str(i)}. Клиент = {client['f78201']}, Адрес клиента = {client['f78211']}, ID = {client['id']}, Телефон = {client['f78341']}, Статус = , "
		      f"Срок установки={client['f81181']} ")
