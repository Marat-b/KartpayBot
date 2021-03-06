import sys

from aiogram.utils.emoji import emojize
from environs import Env
import json
# import locale

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
# locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
MANAGERS = env.list("MANAGERS")

YANDEX_TOKEN = env.str("YANDEX_TOKEN")
CLOUD_FILE_PATH = env.str("CLOUD_FILE_PATH")
TELEGRAM_FILE_PATH = env.str("TELEGRAM_FILE_PATH")
CLOUD_PUBLIC_FILE_PATH = env.str("CLOUD_PUBLIC_FILE_PATH")

############################ Kartpay data #####################################

AUTH_KEY = env.str("AUTH_KEY")
MAX_AMOUNT_RECORDS = env.str("MAX_AMOUNT_RECORDS")
# STATES = env.str("states").encode("cp1251").decode('utf8') #.encode('utf8')
# print(STATES)
URL_GET_SALT = env.str("url_get_salt")
DATA_GET_SALT = json.loads(env.str("data_get_salt"))
URL_USER_AUTH = env.str("url_user_auth")
DATA_USER_AUTH = json.loads(env.str("data_user_auth"))
URL_READ_TABLE = env.str("url_read_table")
URL_UPDATE_TABLE = env.str("url_update_table")
# print(env.str("request_db"))
REQUEST_DB = json.loads(env.str("request_db"))
REQUEST_BY_ID = json.loads(env.str("request_by_id"))
REQUEST_FOR_PAYING = json.loads(env.str("request_for_paying"))
REQUEST_FOR_COUNT_STATUS = json.loads(env.str("request_for_count_status"))
REQUEST_FOR_PAYED = json.loads(env.str("request_for_payed"))
REQUEST_TABLE_TELEGRAMUSER = json.loads(env.str("request_table_telegramuser"))
UPDATE_TABLE_ACT = json.loads(env.str("update_table_act"))
UPDATE_TABLE_UPD = json.loads(env.str("update_table_upd"))

STATUS_SETUP = env.str("STATUS_SETUP").encode('cp1251').decode('utf-8')
STATUS_UPD_SIGNED = env.str("STATUS_UPD_SIGNED").encode('cp1251').decode('utf-8')
STATUS_PLANNED = env.str("STATUS_PLANNED").encode('cp1251').decode('utf-8')
STATUS_ASSIGNED = env.str("STATUS_ASSIGNED").encode('cp1251').decode('utf-8')

TEST = env.str("TEST").encode('cp1251').decode('utf-8')
# print(sys.getwindowsversion())
main_title = '{}Внимание{} При работе с одной заявкой, выбрав операцию с ней, доведите ёё до конца. Далее можно переходить к работе с другой заявкой.\n'\
		.format(emojize(':heavy_exclamation_mark:'), emojize(':heavy_exclamation_mark:'))
