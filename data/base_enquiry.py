import logging

import requests
import json
from data import config, access_id


class BaseEnquiry:
	
	def __init__(self, telegram_user_id = None):
		self.__url_read_table = config.URL_READ_TABLE
		self.__request_telegramuser = config.REQUEST_TABLE_TELEGRAMUSER
		if telegram_user_id is not None:
			self.__request_telegramuser["filter"]["row"][config.f_telegram_id]["value"] = str(telegram_user_id)
		# self.__user_id = self.__get_user_id(telegram_user_id)
	
	def _get_records(self, request_db):
		"""
		Get records of clients once
		:param: db's records
		:return: All records of clients
		"""
		all_clients = list()
		id_access = access_id.Auth.get_access_id()
		print(f'id_access={id_access}')
		if access_id is None:
			return all_clients
		request_db["access_id"] = id_access
		clients, json_table = self._get_all_records(request_db, 0, int(config.MAX_AMOUNT_RECORDS))
		# summary all clients
		all_clients += clients
		amount_returned_records = int(json_table['count'])
		print(f"returned_records = {amount_returned_records}")
		amount_all_records = int(json_table['count_all'])
		if amount_all_records > amount_returned_records:
			clients, _ = self._get_all_records(request_db, amount_returned_records, amount_all_records)
			all_clients += clients
		print(f'base_enquiry._get_records all_clients={all_clients}')
		return all_clients
	
	def _get_all_records(self, request_db, amount_returned_records, amount_all_records):
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
			print(f"self.__url_read_table = {self.__url_read_table}, request_db = {request_db}")
			response_read_table = requests.post(self.__url_read_table, json = request_db)
			# convert records from text to json
			print(f"response_read_table = {response_read_table}, response_read_table.text = {response_read_table.text}")
			if "code" not in response_read_table.text:
				return list(), {"count": 0, "count_all": 0}
			json_table = json.loads(response_read_table.text)
			if int(json_table["code"]) != 0 or not ("data" in json_table.keys()):
				return clients, {"count": 0, "count_all": 0}
			# get data's keys from json with key "data"
			records = [record for record in json_table['data']]
			# get records with key "row"
			clients = [json_table['data'][record]["row"] for record in records]
			return clients, json_table
		except requests.exceptions.ConnectionError:
			logging.log(1, "Connection error is occurred")
			return list(), {"count": 0, "count_all": 0}
	
	def _get_user_id(self, telegram_user_id):
		"""
		Get user ID for Kartpay
		:return: user ID for Kartpay
		"""
		all_records = self._get_records(self.__request_telegramuser)
		print(f"all_records = {all_records}")
		if all_records is None:
			return None
		id_user = None
		for record in all_records:
			if str(telegram_user_id) == record[config.f_telegram_id]:
				id_user = record[config.f_user_id]
				break
		return id_user
