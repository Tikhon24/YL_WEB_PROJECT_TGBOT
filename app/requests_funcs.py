import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv("SERVER")


def get(route, params=None):
    try:
        response = requests.get(f"{SERVER}{route}", params=params)
        response.raise_for_status()

        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_ex:
        print(f"HTTP ошибка: {http_ex}")
    except Exception as ex:
        print(f"Ошибка: {ex}")


def post(rout, payload):
    try:
        response = requests.post(f"{SERVER}{rout}", json=payload)
        response.raise_for_status()

        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_ex:
        print(f"HTTP ошибка: {http_ex}")
    except Exception as ex:
        print(f"Ошибка: {ex}")
