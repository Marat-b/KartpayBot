import requests
import json
import hashlib
from data import config

class Auth:
	
	@classmethod
	def _get_salt(cls):
		try:
			response = requests.post(config.URL_GET_SALT, json = config.DATA_GET_SALT)
			# print(f"config.URL_GET_SALT = {config.URL_GET_SALT}, config.DATA_GET_SALT = {config.DATA_GET_SALT}")
			# print(f"response = {response}")
			# print(f"response.text = {response.text}")
			if "code" not in response.text:
				return None
			json_data = json.loads(response.text)
			if json_data['code'] == 0:
				return json_data['salt']
			else:
				return None
		except requests.exceptions.ConnectionError:
			print("exception _get_salt")
			return None
	
	@classmethod
	def get_access_id(cls):
		salt = cls._get_salt()
		# print(f"get_access_id -> salt = {salt}")
		if salt is None:
			return None
		templ_hash = "{}{}".format(salt, config.AUTH_KEY)
		hash_user = hashlib.md5(templ_hash.encode("utf-8")).hexdigest()
		data_user_auth = config.DATA_USER_AUTH.copy()
		# print(f"data_user_auth = {data_user_auth}")
		data_user_auth["hash"] = hash_user
		try:
			response_user_auth = requests.post(config.URL_USER_AUTH, json = data_user_auth)
			json_data = json.loads(response_user_auth.text)
			if json_data['code'] == 0:
				return json_data["access_id"]
			else:
				return None
		except requests.exceptions.ConnectionError:
			print("exception _get_access_id")
			return None
