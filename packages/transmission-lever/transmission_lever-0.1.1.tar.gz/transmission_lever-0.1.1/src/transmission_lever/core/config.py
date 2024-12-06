#!/usr/bin/env python

import os
import json
import logging


def get_config() -> dict:
    """
    Get a config dictionary from a json file
    :return: config dictionary
    """

    my_file = __get_file("transmission-lever",
                         "config.json")

    my_json = open(my_file, 'r')
    return json.load(my_json)


def __get_file(dirname: str, filename: str) -> str:
    """
    Check if a file exists on the local system
    :return: string of the config file full path
    """

    default = os.path.join(os.path.dirname(__file__) + "/../tlever.json")

    supported_dirs = [
        os.path.expanduser(f"~/.config/{dirname}/{filename}"),# XDG Standard (User)
        os.path.join(f"/etc/xdg/{dirname}/{filename}"),# XDG Standard (System)
        os.path.expanduser(f"~/.{dirname}/{filename}"),# Legacy user
        os.path.join(f"/etc/{dirname}/{filename}")# System-wide
    ]

    for supported_dir in supported_dirs:
        if os.path.exists(supported_dir):
            return supported_dir

    else:
        logging.warning("Configuration file not found, using default values")
        return default