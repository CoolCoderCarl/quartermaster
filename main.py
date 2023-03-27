# import pandas as pd
import ast
import json
import logging
import os
import time
import urllib
from datetime import datetime
from typing import List

import requests as rq
from httplib2 import Http

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


IDEALISTA_URL = "https://api.idealista.com/"

# API key and secret from Idealista team
APIKEY_SECRET_B64E = os.environ["APIKEY_SECRET_B64E"]

# Telegram variables
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Search params
PROPERTY_TYPE = os.environ["PROPERTY_TYPE"]
OPERATION = os.environ["OPERATION"]
CENTER_GCS = os.environ["CENTER_GCS"]  # GCS (Geographic coordinate system)
# REGION_CODE = os.environ["REGION_CODE"] # "0-EU-ES-61" # 404 for some regions # NUTS not matches with wiki
DISTANCE = os.environ["DISTANCE"]
ITEMS = os.environ["ITEMS"]


def get_oauth_token() -> str:
    """
    Get token from Idealista API
    :return:
    """
    http_obj = Http()

    body = {"grant_type": "client_credentials"}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Authorization": "Basic " + APIKEY_SECRET_B64E,
    }
    try:
        resp, content = http_obj.request(
            IDEALISTA_URL + "/oauth/token",
            method="POST",
            headers=headers,
            body=urllib.parse.urlencode(body),
        )
        return ast.literal_eval(content.decode("UTF-8"))["access_token"]
    except BaseException as base_err:
        logging.error(f"OAuth err: {base_err}")
        return ""


def search_api(token) -> List:
    """
    Search the info about objets in chosen country with chosen filters
    :param token:
    :return:
    """
    http_obj = Http()

    url = (
        IDEALISTA_URL + f"/3.5/es/search?"
        f"propertyType={PROPERTY_TYPE}&"
        f"operation={OPERATION}&"
        # f"center=36.721976,-4.440186&"  # CENTER_GCS - Málaga
        # f"center=42.606119,-5.574742&"  # CENTER_GCS - León
        f"center={CENTER_GCS}&"
        f"distance={DISTANCE}&"
        f"maxItems={ITEMS}"
    )
    # url = (
    #     IDEALISTA_URL
    #     + f"/3.5/es/search?propertyType={PROPERTY_TYPE}&"
    #       f"operation={OPERATION}&"
    #       f"locationId={REGION_CODE}&"
    #       f"maxItems={ITEMS}"
    # )
    headers = {"Authorization": "Bearer " + token}

    try:
        resp, content = http_obj.request(url, method="POST", headers=headers)

        return json.loads(content.decode("UTF-8").replace("'", '"'))[
            "elementList"
        ]  # ast.literal_eval - Did not work
    except BaseException as base_err:
        logging.error(f"Searching err: {base_err}")
        return []


def send_houses_to_telegram(message):
    """
    Send messages to telegram
    :param message:
    :return:
    """
    try:
        response = rq.post(
            TELEGRAM_API_URL,
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": f"Property type: #{message['propertyType']}\n"
                f"\n"
                f"Price: {message['price']} EUR\n"
                f"Operation: #{message['operation']}\n"
                f"\n"
                f"Rooms: {message['rooms']}\n"
                f"Bathrooms: {message['bathrooms']}\n"
                f"\n"
                f"Address: #{message['address']}\n"
                f"Province: #{message['province']}\n"
                f"Municipality: #{message['municipality']}\n"
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
    except KeyError as key_err:
        logging.error(f"Key err while sending to telegram: {key_err}")
    except BaseException as base_err:
        logging.error(f"Err while sending to telegram: {base_err}")


if __name__ == "__main__":
    while True:
        if datetime.now().weekday() in [2, 4, 6]:
            logging.info(
                f"Today is a {datetime.now().strftime('%A')}, a day to search and send found houses"
            )
            try:
                for msg in search_api(get_oauth_token()):
                    send_houses_to_telegram(msg)
                    time.sleep(600)
                else:
                    logging.info("All founded results were sent. Waiting...")
                    time.sleep(10800)
            except json.JSONDecodeError as json_err:
                logging.error(f"JSON err while iterate through the results: {json_err}")
            except BaseException as base_err:
                logging.error(f"Err while iterate through the results: {base_err}")
        else:
            logging.info(
                f"There is a {datetime.now().strftime('%A')}, not a working day. Waiting..."
            )
            time.sleep(10800)
