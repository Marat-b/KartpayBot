import json
from dataclasses import dataclass

import requests

from data.access_id import Auth
from data.config import URL_USER_LIST


@dataclass
class Users:
    @classmethod
    def get_user_fio(cls, user_id: str) -> str:
        response = requests.post(URL_USER_LIST, json={"access_id": Auth.get_access_id()})
        jsons=json.loads(response.text)
        return jsons["data"][user_id]["fio"] if jsons["data"][user_id] else ""