# import pandas as pd
import ast
import json
import logging
import os
import urllib

import requests as rq
from httplib2 import Http

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


APIKEY_SECRET_B64E = os.environ["APIKEY_SECRET_B64E"]
IDEALISTA_URL = "https://api.idealista.com/"

TELE_BOT_TOKEN = os.environ["TELE_BOT_TOKEN"]
TELE_API_URL = f"https://api.telegram.org/bot{TELE_BOT_TOKEN}/sendMessage"
TELE_CHAT_ID = os.environ["TELE_CHAT_ID"]


def get_oauth_token():
    http_obj = Http()

    body = {"grant_type": "client_credentials"}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Authorization": "Basic " + APIKEY_SECRET_B64E,
    }
    resp, content = http_obj.request(
        IDEALISTA_URL + "/oauth/token",
        method="POST",
        headers=headers,
        body=urllib.parse.urlencode(body),
    )
    # return content
    return ast.literal_eval(content.decode("UTF-8"))["access_token"]


def search_api(token):
    http_obj = Http()
    # url = IDEALISTA_URL+"/3.5/es/search?center=40.123,-3.242&country=es&maxItems=20" \
    #       "&numPage=1&distance=60000&propertyType=homes&operation=sale"
    # url = IDEALISTA_URL+
    # "/3.5/es/search?propertyType=homes&operation=sale&center=36.717358,-4.442123&distance=600&maxItems=20"
    url = (
        IDEALISTA_URL
        + "/3.5/es/search?propertyType=homes&operation=sale&locationId=0-EU-ES-42&maxItems=5"
    )
    headers = {"Authorization": "Bearer " + token}
    resp, content = http_obj.request(url, method="POST", headers=headers)
    return json.loads(content.decode("UTF-8").replace("'", '"'))[
        "elementList"
    ]  # ast.literal_eval - Did not work


def send_houses_to_telegram(message):
    """
    Send messages to telegram
    :param message:
    :return:
    """
    try:
        response = rq.post(
            TELE_API_URL,
            json={
                "chat_id": TELE_CHAT_ID,
                "text": f"Property type: {message['propertyType']}\n"
                f"\n"
                f"Price: {message['price']} EUR\n"
                f"\n"
                f"Operation: {message['operation']}\n"
                f"\n"
                f"Rooms: {message['rooms']}\n"
                f"\n"
                f"Bathrooms: {message['bathrooms']}\n"
                f"\n"
                f"Address: {message['address']}\n"
                f"\n"
                f"Province: {message['province']}\n"
                f"\n"
                f"Municipality: {message['municipality']}\n"
                f"\n"
                f"URL: {message['url']}\n"
                f"\n"
                f"Description: {message['description']}\n",
            },
        )
        if response.status_code == 200:
            logging.info(
                f"Sent: {response.reason}. Status code: {response.status_code}"
            )
        else:
            logging.error(
                f"Not sent: {response.reason}. Status code: {response.status_code}"
            )
    except KeyError as keyerr:
        logging.error(keyerr)
    except Exception as err:
        logging.error(err)


if __name__ == "__main__":
    # print(search_api(get_oauth_token()))
    for msg in search_api(get_oauth_token()):
        send_houses_to_telegram(msg)
    # for i in search_api(get_oauth_token()):
    #     try:
    #         print(f"PRICE: {i['price']}")
    #         print(f"PROPERTY TYPE: {i['propertyType']}")
    #         print(f"OPERATION: {i['operation']}")
    #         print(f"ROOMS: {i['rooms']}")
    #         print(f"BATHROOMS: {i['bathrooms']}")
    #         print(f"ADDRESS: {i['address']}")
    #         print(f"PROVINCE: {i['province']}")
    #         print(f"MUNICIPALITY: {i['municipality']}")
    #         print(f"URL: {i['url']}")
    #         print(f"DESCRIPTION: {i['description']}")
    #     except KeyError as keyerr:
    #         logging.error(keyerr)
