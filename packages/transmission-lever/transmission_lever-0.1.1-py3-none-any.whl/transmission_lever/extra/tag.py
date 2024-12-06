#!/usr/bin/env python

from transmission_lever.core.label import mk_label, rm_label
from transmission_lever.core.client import get_client


def tag_prefix(config) -> str:
    return config['General']['prefix']['tags']


def mk_tag(config: dict,
           torrent_hash: str,
           tag_name: str
           ) -> bool:

    """
    Add a tag on a torrent object
    :param config: valid configuration dictionary
    :param torrent_hash: hash of a single torrent
    :param tag_name: name if the tag
    :return: True if the tag is created, False if it already exists
    """

    client = get_client(config)

    tag = tag_prefix(config) + tag_name
    return mk_label(client, torrent_hash, tag)


def rm_tag(config: dict,
           torrent_hash: str,
           tag_name: str
           ) -> bool:

    """
    Remove a tag from a torrent object
    :param config: valid configuration dictionary
    :param torrent_hash: hash of a single torrent
    :param tag_name: name of the tag
    :return: True if the tag is removed, False if it does not exist
    """

    client = get_client(config)

    tag = tag_prefix(config) + tag_name
    return rm_label(client, torrent_hash, tag)

