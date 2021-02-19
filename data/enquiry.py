import requests
import json
from data import config, access_id
from data.base_enquiry import BaseEnquiry


class Enquiry(BaseEnquiry):
	
	def __init__(self, telegram_user_id):
		super().__init__(telegram_user_id)
		self.__user_id = self._get_user_id(telegram_user_id)
	
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
		all_records = self._get_records(request_db)
		return all_records
	
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


if __name__ == "__main__":
	r = Enquiry("919930316")
	# rr = Request("*********************", "Передан инженеру")
	clients = r.get_entities("Передан инженеру")
	print(r.get_entities("Передан инженеру"))
	
	for i, client in enumerate(clients):
		print(f"{str(i)}. Клиент = {client['f78201']}, Адрес клиента = {client['f78211']}, ID = {client['id']}, Телефон = {client['f78341']}, Статус = , "
		      f"Срок установки={client['f81181']} ")
