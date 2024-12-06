#!/usr/bin/env python3

"""add_qbt_trackers.py

Description:
This script fetches torrent tracker URLs from plaintext lists hosted on the web
and adds them to each torrent in a qBittorrent instance.

Usage:
    add_qbt_trackers.py (HOSTNAME) (USERNAME) (PASSWORD)
    add_qbt_trackers.py -h

Examples:
    add_qbt_trackers.py "http://localhost:8080" "admin" "adminadmin"

Options:
    -h, --help      show this help message and exit
"""

import requests
from docopt import docopt
from qbittorrentapi import Client


def main():
    args = docopt(__doc__)

    qbt_client = Client(
        host=args["HOSTNAME"], username=args["USERNAME"], password=args["PASSWORD"]
    )

    live_trackers_list_urls = [
        "https://newtrackon.com/api/stable",
        "https://trackerslist.com/best.txt",
        "https://trackerslist.com/http.txt",
        "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt",
    ]

    combined_trackers_urls = [
        "http://tracker.hyperreal.coffee/announce",
        "udp://tracker.hyperreal.coffee:1337",
    ]

    for url in live_trackers_list_urls:
        response = requests.get(url, timeout=60)
        tracker_urls = [x for x in response.text.splitlines() if x != ""]
        combined_trackers_urls.extend(tracker_urls)

    for torrent in qbt_client.torrents_info():
        qbt_client.torrents.add_trackers(
            torrent_hash=torrent.hash, urls=combined_trackers_urls
        )
        print(f"OK: {torrent.name}")


if __name__ == "__main__":
    main()
