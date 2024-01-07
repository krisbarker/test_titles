#!/usr/bin/env python3

"""
Returns Vendor ID and Title when provided an eidr, catalog_id or alt_id
"""

import time
from functools import wraps

import pandas as pd

from genericmodules.get_config import get_config_details


def file_setup():
    """

    :return:
    """
    config = get_config_details()
    masters_dir = config['master_details']['dir']
    file = config['master_details']['file']
    target = masters_dir + file

    import_data = pd.read_csv(target)

    return import_data


def timethis(func):
    """

    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result

    return wrapper


def vendor_id_lookup(*args, **kwargs):
    """
    Returns Vendor ID and Title where they exist.
    Does a look_up for any of catalog_id, eidr or alt_id
    :param args:  alt_id, catalog_id or eidr (or None)
    :param kwargs: defines whether the lookup is catalog_id, eidr or alt_id
    :return: Vendor ID and Title
    """

    master_data = file_setup()

    eidr = args[0]
    catalog_id = args[1]
    alt_id = args[2]

    set_alt_id = kwargs["alt_id"]
    set_catalog_id = kwargs["catalog_id"]
    set_eidr = kwargs["eidr"]

    eidr_answer = 0
    eidr_title = "None"
    altid_answer = 0
    altid_title = "None"
    catid_answer = 0
    catid_title = "None"

    if set_eidr is True:
        try:
            eidr_answer = master_data.loc[
                master_data["EIDR-2"] == eidr, "Vendor Identifier"
            ].iloc[0]
            eidr_title = master_data.loc[
                master_data["EIDR-2"] == eidr, "Title"
            ].iloc[0]
        except Exception:
            eidr_answer = 0
            eidr_title = "None"

    if set_catalog_id is True:
        try:
            catid_answer = master_data.loc[
                master_data["Catalog ID"] == catalog_id, "Vendor Identifier"
            ].iloc[0]
            catid_title = master_data.loc[
                master_data["Catalog ID"] == catalog_id, "Title"
            ].iloc[0]
        except Exception:
            catid_answer = 0
            catid_title = "None"

    if set_alt_id is True:
        try:
            altid_answer = master_data.loc[
                master_data["Alt ID"] == alt_id, "Vendor Identifier"
            ].iloc[0]
            altid_title = master_data.loc[
                master_data["Alt ID"] == alt_id, "Title"
            ].iloc[0]
        except Exception:
            altid_answer = 0
            altid_title = "None"

    if eidr_answer != 0:
        return True, eidr_answer, eidr_title
    elif catid_answer != 0:
        return True, catid_answer, catid_title
    elif altid_answer != 0:
        return True, altid_answer, altid_title
    else:
        return False, "None", "None"


@timethis
def main():
    alt_id = "5723_OV"
    catalog_id = "1593"
    eidr = "10.5240/9A59-E0A2-C760-F12E-8738-6"

    options = {"eidr": True, "catalog_id": False, "alt_id": False}
    details_list = [eidr, catalog_id, alt_id]

    title_exists, vendor_id, title = vendor_id_lookup(*details_list, **options)

    print(f"Title Exists: {title_exists}")
    print(f"Vendor ID: {vendor_id}")
    print(f"Title: {title}")


if __name__ == "__main__":
    main()
