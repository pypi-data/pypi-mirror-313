#!/usr/bin/env python

from transmission_lever.core.client import get_client, get_torrents_list
from transmission_lever.core.torrent import change_upload_throttle


def set_clog(config: dict) -> None:
    """
    Set bandwidth limits to torrents above last tier
    :param config: valid configuration dictionary
    """

    client = get_client(config)
    limits = {
        "seed_idle_limit": 30,
        "seed_idle_mode": 2,
        "seed_ratio_limit": 5,
        "seed_ratio_mode": 2,
        "upload_limit": 50,
        "upload_limited": True
    }

    for torrent in get_torrents_list(client):

        # Check if torrent is complete
        if torrent.progress != 100:
            continue

        elif 50 < torrent.ratio < 70:
            change_upload_throttle(client, torrent.hashString, limits)

        elif 70 < torrent.ratio:
            limits["upload_limit"] = 25
            change_upload_throttle(client, torrent.hashString, limits)


def unset_clog(config: dict) -> None:
    client = get_client(config)
    limits = {
        "seed_idle_limit": 30,
        "seed_idle_mode": 2,
        "seed_ratio_limit": 5,
        "seed_ratio_mode": 2,
        "upload_limit": 50,
        "upload_limited": False
    }

    for torrent in get_torrents_list(client):

        if torrent.progress != 100:
            continue

        elif torrent.ratio > 50:
            change_upload_throttle(client, torrent.hashString, limits)