#!/usr/bin/env python3

"""
Pull config from a config.txt file for processing avails
It should cover:

- target file to read for processing
- target file to read for masters lookup
- destination folder for outputs
"""

import configparser


def get_config_details():
    config = configparser.ConfigParser()
    path_to_config = "/Users/kris/PycharmProjects/test_titles/test_titles/genericmodules"
    file_name = "/config.txt"
    target = path_to_config + file_name
    config.read(target)

    return config
