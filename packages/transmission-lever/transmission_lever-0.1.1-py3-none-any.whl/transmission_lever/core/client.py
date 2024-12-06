#!/usr/bin/env python

import sys
import logging
from transmission_rpc import Client, Torrent


def get_client(config: dict) -> Client:
    """
    Get a transmission RPC client
    :param config: valid configuration dictionary
    :return: transmission session
    """

    try:
        client = Client(host=config["Client"]["host"],
                        port=int(config["Client"]["port"]),
                        username=config["Client"]["username"],
                        password=config["Client"]["password"])
        return client

    except:
        logging.error("Authorization failed")
        sys.exit()


def get_rpc_semver(client: Client) -> str:
    """
    Get RPC server version
    :param client: valid transmission session
    :return: version of the RPC server
    """

    return client.get_session().rpc_version_semver


def get_transmission_version(client: Client) -> str:
    """
    Get transmission server version
    :param client: valid transmission session
    :return: version of the transmission server
    """

    return client.get_session().version


def get_downloads_dir(client: Client) -> str:
    """
    Get global download directory of transmission
    :param client: valid transmission session
    :return: global download directory
    """

    return client.get_session().download_dir


def get_torrents_list(client: Client) -> list[Torrent]:
    """
    List all torrent in the current session
    :param client: valid transmission session
    :return: list of torrent objects
    """

    return client.get_torrents()


def start_torrent(client: Client,
                  torrent_hash: str
                  ) -> None:
    """
    Resume a paused torrent
    :param torrent_hash:
    :param client: valid transmission session
    :return: None
    """

    client.start_torrent(ids=[torrent_hash])
