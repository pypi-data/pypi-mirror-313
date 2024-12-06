#!/usr/bin/env python

import curses
import traceback

from transmission_lever.core.client import get_client
from transmission_lever.core.torrent import get_stub_info


def prettify_stub_info(config,
                       torrent_hash
                       ) -> dict:
    """
    Pretty format info of a torrent
    :param config: valid configuration dictionary
    :param torrent_hash: hash of a single torrent
    :return: a prettified formatted dictionary
    """

    client = get_client(config)
    prefixes = {
        "category": config['General']['prefix']['categories'],
        "tier": config['General']['prefix']['tiers'],
        "tag": config['General']['prefix']['tags']
    }
    info = get_stub_info(client, torrent_hash, prefixes)

    output = {
        'Name': info.name,
        'Hash': info.hash,
        'Ratio': info.ratio_pretty,
        'Progress': info.progress,
        'Status': info.status,
        'Group': info.group,
        'Tier': info.tier,
        'Category': info.category,
        'Tag': info.tag,
        'Up Speed': info.up_pretty,
        'Down Speed': info.down_pretty,
        'ETA': info.eta
    }

    return output


def curses_single(config, torrent_hash):
    """
    Wrapper for Terminal Interface for ncurses
    :return: None
    """

    def ncurses_app(stdscr) -> None:

        """
        Terminal Interface for ncurses
        :return: None
        """

        try:
            # init curses
            ch = ''
            stdscr = curses.initscr()
            curses.cbreak()
            stdscr.timeout(2000)

            # while non-quit char
            while ch != ord('q'):

                info = prettify_stub_info(config, torrent_hash=torrent_hash)

                i = 0
                p = '     '
                for k, v in info.items():
                    stdscr.addstr(1 + i, 1, f"  {k}: {v}{p}", curses.A_NORMAL)
                    i += 1

                stdscr.clrtoeol()
                stdscr.refresh()
                ch = stdscr.getch()

        except:
            traceback.print_exc()
        finally:
            curses.endwin()

    curses.wrapper(ncurses_app)
