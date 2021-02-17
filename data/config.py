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
REQUEST_TABLE_TELEGRAMUSER = json.loads(env.str("request_table_telegramuser"))
UPDATE_TABLE_ACT = json.loads(env.str("update_table_act"))
UPDATE_TABLE_UPD = json.loads(env.str("update_table_upd"))
