import json
from data import config


def get_state_name(key_state: str):
	states = {"assigned_to": "Передан инженеру", "signed": "УПД подписан", "setup": "Установлено"}
	# print(f"STATES = {config.STATES}")
	# # states = json.loads(config.STATES)
	# states = config.STATES
	# print(f"states = {states.encode('utf8')}")
	name_state = states[key_state]
	print(f"name_state = {name_state}")
	return name_state
