#!/usr/bin/env python

import os

from transmission_lever.core.label import mk_label, rm_label, find_regex_label
from transmission_lever.core.torrent import mv_data, get_rel_download_dir
from transmission_lever.core.client import get_downloads_dir, get_client, get_torrents_list


def category_prefix(config) -> str:

    """
    Returns the category prefix from configration file
    :param config: valid configuration dictionary
    :return: category prefix
    """

    return config['General']['prefix']['categories']


def enforce_categories(config: dict) -> None:

    """
    Syncs torrent data dir with category label
    :param config: valid configuration dictionary
    :return: None
    """

    client = get_client(config)

    # For every torrent in the torrent list
    for torrent in get_torrents_list(client):

        # We get the torrent relative download directory
        rel_torrent_dir = get_rel_download_dir(client, torrent)
        # We check that there is a category label
        label_exists = find_regex_label(client, torrent.hashString, "@")

        # If the category label exists
        if label_exists:

            # We grab all the torrent labels
            torrent_labels = torrent.labels

            # For every torrent label
            for label in torrent_labels:

                # We check for @ as the first char
                if label[0] == '@':

                    # We get the label relative directory
                    rel_label_dir = label.replace('@', '')

                    # If label rel dir does not equals torrent rel dir
                    if rel_torrent_dir != rel_label_dir:

                        # We enforce the category label directory
                        base_dir = get_downloads_dir(client)
                        final_dir = os.path.join(base_dir, rel_label_dir)
                        mv_data(client, torrent.hashString, final_dir)


def mk_category(config: dict,
                torrent_hash: str,
                category_name: str
                ) -> None:

    """
    Create an emulated category through labels
    :param config: valid configuration dictionary
    :param torrent_hash: hash of a single torrent
    :param category_name: name of the category
    :return: None
    """

    client = get_client(config)

    label = category_prefix(config) + category_name
    mk_label(client, torrent_hash, label)

    directory = os.path.join(get_downloads_dir(client), category_name)
    mv_data(client, torrent_hash, directory)

    return


def rm_category(config: dict,
                torrent_hash: str,
                category_name: str
                ) -> None:

    """
    Delete an emulated category through labels
    :param config: valid configuration dictionary
    :param torrent_hash: hash of a single torrent
    :param category_name: name of the category
    :return: None
    """

    client = get_client(config)

    directory = get_downloads_dir(client)
    mv_data(client, torrent_hash, directory)

    label = category_prefix(config) + category_name
    rm_label(client, torrent_hash, label)

    return
