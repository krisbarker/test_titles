#!/usr/bin/env python3

"""
This is script to show something quite simple
"""

import os
import json
import time

import requests

from dotenv import load_dotenv
from functools import wraps

load_dotenv()


def extract_alternative_title(title_data):

    # print(title_data["Hits"][0]["Source"]["AlternateTitles"])

    for item in title_data["Hits"][0]["Source"]["AlternateTitles"]:
        try:
            if item["Country"] == "FR":
                print(f"Country: {item['Country']}  Title: {item['Title']}")
        except KeyError:
            continue


def get_title_data(eidr):

    scan_key = os.getenv("SCANKEY1")
    url2 = os.getenv("URL2")

    headers = {"Ocp-Apim-Subscription-Key": scan_key,
               "accept": "application/json"}

    params = {"Includes": "AlternateTitles",
              "ExternalId": eidr}

    data = requests.post(url=url2, headers=headers, params=params)

    print(data.url)
    print(data.status_code)

    title_data = json.loads(data.text)
    extract_alternative_title(title_data)


def get_edir_list():

    eidr_list = [
        "10.5240/8CE6-6D63-C68A-469F-E4DA-H",
        "10.5240/327D-78F8-6DE8-14F2-1D37-Q"
    ]

    return eidr_list


def main():
    eidr_list = get_edir_list()
    for eidr in eidr_list:
        get_title_data(eidr)


if __name__ == "__main__":
    main()
