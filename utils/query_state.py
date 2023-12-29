import json
from data import config


def get_state_name(key_state: str) -> str:
	# states = {"assigned_to": "Передан инженеру", "trip_planned": "Запланирован выезд", "signed": "УПД подписан", "setup": "Установлено"}
	states = {
		"assigned_to": "Передан инженеру", "trip_planned": "Запланирована", "signed": "УПД подписан",
		"setup": "Выполнено"
	}
	name_state = states[key_state]
	return name_state
