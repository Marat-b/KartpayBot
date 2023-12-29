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
# REQUEST_TABLE_EMPLOYEES = json.loads(env.str("request_table_employees"))
UPDATE_TABLE_ACT = json.loads(env.str("update_table_act"))
UPDATE_TABLE_UPD = json.loads(env.str("update_table_upd"))

STATUS_SETUP = env.str("STATUS_SETUP") #.encode('cp1251').decode('utf-8')
STATUS_UPD_SIGNED = env.str("STATUS_UPD_SIGNED") #.encode('cp1251').decode('utf-8')
STATUS_PLANNED = env.str("STATUS_PLANNED") #.encode('cp1251').decode('utf-8')
STATUS_ASSIGNED = env.str("STATUS_ASSIGNED") #.encode('cp1251').decode('utf-8')

TEST = env.str("TEST") #.encode('cp1251').decode('utf-8')
# print(sys.getwindowsversion())
main_title = ('{}Внимание{} При работе с одной заявкой, выбрав операцию с ней, доведите её до конца. Далее можно '
			  'переходить к работе с другой заявкой.\n')\
		.format(emojize(':heavy_exclamation_mark:'), emojize(':heavy_exclamation_mark:'))

# ----------- fields ---------------------
f_id = env.str("f_id")
f_client = env.str("f_client")
f_reqeust_id = env.str("f_reqeust_id")
f_point_address = env.str("f_point_address")
f_phone = env.str("f_phone")
f_execution_date = env.str("f_execution_date")
f_target_date = env.str("f_target_date")
f_mileage = env.str("f_mileage")
f_request_cost = env.str("f_request_cost")
f_act_photo = env.str("f_act_photo")
f_upd_photo = env.str("f_upd_photo")
f_paid_to_performer = env.str("f_paid_to_performer")
f_delivery = env.str("f_delivery")
f_point_photo = env.str("f_point_photo")
f_executor = env.str("f_executor")
f_status = env.str("f_status")
f_telegram_id = env.str("f_telegram_id") # table f6291
f_user_id = env.str("f_user_id")		# table f6291
f_application_total = env.str("f_application_total")
f_client_bank = env.str("f_client_bank")
f_work_type = env.str("f_work_type")
f_app_description = env.str("f_app_description")
f_equipment = env.str("f_equipment")
# f_telegram_link_id = env.str("f_telegram_link_id") # link table f6331 with table f1651

