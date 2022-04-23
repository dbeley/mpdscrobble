"""
mpdscrobble: a simple Last.fm scrobbler for MPD.
"""
import logging
import time
import argparse
from typing import Optional

from mpdscrobble import constants
from .utils import (
    read_config,
    create_networks,
)
from .mpdscrobble import MPDScrobbleMPDConnection, MPDScrobbleTrack, MPDScrobbleNetwork

logger = logging.getLogger(__name__)


def loop(
    args: argparse.Namespace,
    networks: MPDScrobbleNetwork,
    client: MPDScrobbleMPDConnection,
    cached_song: Optional[MPDScrobbleTrack],
) -> None:
    try:
        while True:
            time.sleep(constants.LOOP_DELAY)
            current_song = client.mpdscrobble_currentsong()
            if current_song and cached_song:
                logger.debug(
                    f"Current: {current_song.debug()}\nCached: {cached_song.debug()}"
                )
                if cached_song != current_song:
                    if cached_song.percentage > constants.SCROBBLE_PERCENTAGE:
                        if not args.dry_run:
                            networks.mpdscrobble_scrobble(cached_song)
                        else:
                            logger.warning("Dry-run mode enabled.")
                    networks.mpdscrobble_update_now_playing(current_song)
            cached_song = client.mpdscrobble_currentsong()
    except Exception as e:
        logger.error(e)


def main():
    args = parse_args()
    config = read_config(args.config_file)
    if len(config.sections()) == 0:
        raise Exception(
            "Empty config file.\nCreate a valid config file in ~/.config/mpdscrobble/mpdscrobble.conf or use the -c/--config-file flag."
        )

    networks = create_networks(config)

    host = constants.DEFAULT_HOST
    port = constants.DEFAULT_PORT
    if "mpdscrobble" in config:
        if "host" in config["mpdscrobble"]:
            host = config["mpdscrobble"]["host"]
        if "port" in config["mpdscrobble"]:
            port = config["mpdscrobble"]["port"]

    client = MPDScrobbleMPDConnection()
    client.mpdscrobble_connect(host, port)

    # Loop
    cached_song = client.mpdscrobble_currentsong()
    while True:
        timeout = 10
        loop(args, networks, client, cached_song)
        logger.error(
            f"MPD Client crashed. Waiting {timeout} seconds before restarting."
        )
        time.sleep(timeout)
        timeout = timeout * 2
        client.mpdscrobble_restart()
        cached_song = client.mpdscrobble_currentsong()


def parse_args() -> argparse.Namespace:
    format = "%(levelname)s :: %(message)s"
    parser = argparse.ArgumentParser(description="A simple Last.fm scrobbler for MPD.")
    parser.add_argument(
        "--debug",
        help="Display debugging information.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "-c",
        "--config_file",
        help="Config file (default: ~/.config/mpdscrobble/mpdscrobble.conf).",
        type=str,
        default="~/.config/mpdscrobble/mpdscrobble.conf",
    )
    parser.add_argument(
        "--dry-run",
        help="Disable scrobbling.",
        dest="dry_run",
        action="store_true",
    )
    parser.set_defaults(dry_run=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=format)
    return args


if __name__ == "__main__":
    main()
