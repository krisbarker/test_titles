#!/usr/bin/env python3

"""
This is script to show something quite simple
"""

import os
import json

import requests
import pandas as pd

from dotenv import load_dotenv

from genericmodules.vendorid_lookup import vendor_id_lookup
from genericmodules.get_config import get_config_details


load_dotenv()


def build_output_dictionary(unique_eidrs):

    export_df = pd.DataFrame(columns=['Title ID', 'Vendor ID', 'Title', 'Local Language Title'])

    output_dict = {}

    for eidr in unique_eidrs:
        alt_id = "None"
        catalog_id = "None"

        options = {"eidr": True, "catalog_id": False, "alt_id": False}
        details_list = [eidr, catalog_id, alt_id]

        title_exists, vendor_id, title = vendor_id_lookup(*details_list, **options)

        if title_exists:

            alternative_title = get_title_data(eidr)
            output_dict['Title ID'] = eidr
            output_dict['Vendor ID'] = vendor_id
            output_dict['Title'] = title
            output_dict['Local Language Title'] = alternative_title

            export_df = write_data(export_df, output_dict)

        else:
            print(f"This {eidr} isn't in the master file")

    return export_df


def extract_alternative_title(title_data):

    # print(title_data["Hits"][0]["Source"]["AlternateTitles"])

    alternative_title = "None"

    try:
        for item in title_data["Hits"][0]["Source"]["AlternateTitles"]:
            try:
                if item["Country"] == "FR":
                    print(f"Country: {item['Country']}  Title: {item['Title']}")
                    alternative_title = item['Title']
            except KeyError:
                alternative_title = "None"
                continue
    except (IndexError, KeyError):
        print("Response looks odd - Index Error")
        alternative_title = "None"

    return alternative_title


def get_title_data(eidr):

    scan_key = os.getenv("SCANKEY2")
    url2 = os.getenv("URL2")

    headers = {"Ocp-Apim-Subscription-Key": scan_key,
               "accept": "application/json"}

    params = {"Includes": "AlternateTitles",
              "ExternalId": eidr}

    data = requests.post(url=url2, headers=headers, params=params)

    print(data.url)
    print(data.status_code)

    title_data = json.loads(data.text)
    alternative_title = extract_alternative_title(title_data)

    return alternative_title


def get_unique_eidrs():

    config = get_config_details()
    dir = config['input_avail_details']['dir']
    file = config['input_avail_details']['file']
    target = dir + file

    import_data = pd.read_excel(target)

    unique_eidrs = import_data["Title ID"].unique()

    return unique_eidrs


def get_edir_list():

    eidr_list = [
        "10.5240/8CE6-6D63-C68A-469F-E4DA-H",
        "10.5240/327D-78F8-6DE8-14F2-1D37-Q"
    ]

    return eidr_list


def write_data(export_df, output_dict):
    """
    :param export_df:
    :param output_dict:
    :return:
    """
    df_new_row = pd.DataFrame([output_dict])
    export_df = pd.concat([export_df, df_new_row])

    return export_df


def write_file(export_df):
    config = get_config_details()
    dir = config['alternate_title_export']['dir']
    file = config['alternate_title_export']['file']
    target = dir + file

    export_df.to_csv(target, encoding="utf-8", index=False)


def main():
    eidr_list = get_edir_list()
    for eidr in eidr_list:
        get_title_data(eidr)

    unique_eidrs = get_unique_eidrs()
    print(f"There are {len(unique_eidrs)} in the list")

    export_df = build_output_dictionary(unique_eidrs)
    print(export_df.head())
    print(len(export_df))

    write_file(export_df)


if __name__ == "__main__":
    main()
