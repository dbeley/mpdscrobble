"""
Simple script to scrobble a mpdscribble journal file.
"""
import logging
import argparse
from mpdscrobble.utils import (
    read_config,
    create_network,
)
from mpdscrobble.mpdscrobble import (
    MPDScrobbleMPDConnection,
    MPDScrobbleTrack,
)


logger = logging.getLogger()
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 6600


def read_journal(journal_file):
    with open(journal_file, "r") as f:
        tracklist = f.read().split("\n\n")

    tracks = [[x.split(" = ") for x in y.split("\n") if x] for y in tracklist if y]
    dict_tracks = [{k: v for k, v in x} for x in tracks]
    obj_tracks = [
        {
            "artist": x["a"],
            "title": x["t"],
            "album": x["b"],
            "timestamp": int(x["i"]),
        }
        for x in dict_tracks
    ]
    result = []
    for i in obj_tracks:
        track = MPDScrobbleTrack(
            artist=i["artist"],
            title=i["title"],
            album=i["album"],
            timestamp=i["timestamp"],
        )
        result.append(track)
    return result


def main():
    args = parse_args()
    mpdscribble_journal = read_journal(args.journal_file)
    config = read_config(args.config_file)

    networks = create_network(config)

    host = DEFAULT_HOST
    port = DEFAULT_PORT
    if "mpdscrobble" in config:
        if "host" in config["mpdscrobble"]:
            host = config["mpdscrobble"]["host"]
        if "port" in config["mpdscrobble"]:
            port = config["mpdscrobble"]["port"]

    client = MPDScrobbleMPDConnection()
    client.mpdscrobble_connect(host, port)

    for index, i in enumerate(mpdscribble_journal):
        logger.info(i)
        networks.mpdscrobble_scrobble(i)


def parse_args():
    format = "%(levelname)s :: %(message)s"
    parser = argparse.ArgumentParser(
        description="Simple script to scrobble a mpdscribble journal file."
    )
    parser.add_argument(
        "--debug",
        help="Display debugging information.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "journal_file", nargs="?", type=str, help="mpdscribble journal file path."
    )
    parser.add_argument(
        "-c",
        "--config_file",
        help="Config file (default: ./mpdscrobble.conf).",
        type=str,
        default="mpdscrobble.conf",
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=format)
    return args


if __name__ == "__main__":
    main()
