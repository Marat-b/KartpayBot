from environs import Env
import json

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

############################ Kartpay data #####################################

AUTH_KEY = env.str("AUTH_KEY")
MAX_AMOUNT_RECORDS = env.str("MAX_AMOUNT_RECORDS")
URL_GET_SALT = env.str("url_get_salt")
DATA_GET_SALT = json.loads(env.str("data_get_salt"))
URL_USER_AUTH = env.str("url_user_auth")
DATA_USER_AUTH = json.loads(env.str("data_user_auth"))
URL_READ_TABLE = env.str("url_read_table")
print(env.str("request_db"))
REQUEST_DB = json.loads(env.str("request_db"))
