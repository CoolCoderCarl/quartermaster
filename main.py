# import pandas as pd
import ast
import json
import logging
import os
import urllib

# import requests as rq
# import base64
from httplib2 import Http

APIKEY_SECRET_B64E = os.environ["APIKEY_SECRET_B64E"]
IDEALISTA_URL = "https://api.idealista.com/"


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
        + "/3.5/es/search?propertyType=homes&operation=sale&locationId=0-EU-ES-42&maxItems=20"
    )
    headers = {"Authorization": "Bearer " + token}
    resp, content = http_obj.request(url, method="POST", headers=headers)
    return json.loads(content.decode("utf-8").replace("'", '"'))[
        "elementList"
    ]  # ast.literal_eval - Did not work


if __name__ == "__main__":
    print(search_api(get_oauth_token()))
    for i in search_api(get_oauth_token()):
        try:
            print(f"FLOOR: {i['floor']}")
            print(f"PRICE: {i['price']}")
            print(f"PROPERTY TYPE: {i['propertyType']}")
            print(f"OPERATION: {i['operation']}")
            print(f"ROOMS: {i['rooms']}")
            print(f"BATHROOMS: {i['bathrooms']}")
            print(f"ADDRESS: {i['address']}")
            print(f"PROVINCE: {i['province']}")
            print(f"MUNICIPALITY: {i['municipality']}")
            print(f"DISTRICT: {i['district']}")
            print(f"URL: {i['url']}")
            print(f"DESCRIPTION: {i['description']}")
        except KeyError as keyerr:
            logging.error(keyerr)
