#!/usr/bin/env python

import re
import logging
from transmission_rpc import Client


def find_label(client: Client,
               torrent_hash: str,
               label_name: str,
               ) -> bool:
    """
    Find a label on a torrent object
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param label_name: name of the label
    :return: True if the label is found, False otherwise
    """

    torrent_labels = client.get_torrent(torrent_hash).labels

    for label in torrent_labels:
        if label == label_name:
            logging.info(f"Found label {label_name} in torrent with hash {torrent_hash}")
            return True

    logging.info(f"No label {label_name} in torrent with hash {torrent_hash}")
    return False


def find_regex_label(client: Client,
                     torrent_hash: str,
                     label_regex: str
                     ) -> bool:

    """
    Find a label on a torrent object using regex
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param label_regex: name of the label regex
    :return: True if one or more matches are found, False otherwise
    """

    torrent_labels = client.get_torrent(torrent_hash).labels
    labels_flattened_list = ','.join(torrent_labels)

    exists = re.search(label_regex, labels_flattened_list)

    if not exists:
        return False
    return True


def sw_label(client: Client,
             torrent_hash: str,
             old_label_name: str,
             new_label_name: str
             ) -> bool:
    """
    Swap a label on a torrent object
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param old_label_name: name of the label to remove
    :param new_label_name: name of the label to add
    :return: True on swap, False if old label does not exist
    """

    exists = find_label(client, torrent_hash, old_label_name)

    if not exists:
        logging.info(
            f"Skipping label deletion in torrent with hash {torrent_hash}: label {old_label_name} does not exist")
        mk_label(client, torrent_hash, new_label_name)
        return False

    else:
        rm_label(client, torrent_hash, old_label_name)
        mk_label(client, torrent_hash, new_label_name)
        logging.info(f"Swapped label {old_label_name} with new label {new_label_name} in torrent with hash {torrent_hash}")
        return True


def mk_label(client: Client,
             torrent_hash: str,
             label_name: str
             ) -> bool:
    """
    Add a label on a torrent object
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param label_name: name of the label
    :return: True if the label is created, False if it already exists
    """

    exists = find_label(client, torrent_hash, label_name)

    if not exists:
        torrent_labels = client.get_torrent(torrent_hash).labels
        torrent_labels.append(label_name)
        client.change_torrent(ids=[torrent_hash], labels=torrent_labels)
        logging.info(f"Added label {label_name} in torrent with hash {torrent_hash}")
        return True

    else:
        logging.info(f"Skipping label creation in torrent with hash {torrent_hash}: label {label_name} already exists")
        return False


def rm_label(client: Client,
             torrent_hash: str,
             label_name: str
             ) -> bool:
    """
    Remove a label from a torrent object
    :param client: valid transmission session
    :param torrent_hash: hash of a single torrent
    :param label_name: name of the label
    :return: True if the label is removed, False if it does not exist
    """

    exists = find_label(client, torrent_hash, label_name)

    if not exists:
        logging.info(
            f"Skipping label deletion in torrent with hash {torrent_hash}: label {label_name}  does not exists")
        return False

    else:
        torrent_labels = client.get_torrent(torrent_hash).labels
        torrent_labels_new = []

        for label in torrent_labels:
            if label == label_name:
                pass
            else:
                torrent_labels_new.append(label)

        client.change_torrent(ids=[torrent_hash], labels=torrent_labels_new)
        logging.info(f"Removed label {label_name} in torrent with hash {torrent_hash}")
        return True
