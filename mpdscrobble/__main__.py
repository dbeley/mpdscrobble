"""
mpdscrobble: a simple Last.fm/Libre.fm scrobbler for MPD.
"""
import logging
import time
import argparse
from .utils import (
    MPDScrobbleMPDConnection,
    read_config,
    create_network,
)


logger = logging.getLogger()
# scrobble will be sent if the track had at least a 40% completion
SCROBBLE_PERCENTAGE = 40.0


def loop(args, networks, client, cached_song):
    while True:
        time.sleep(10)
        current_song = client.mpdscrobble_currentsong()
        logger.debug(f"{current_song.debug()}\n{cached_song.debug()}")
        if cached_song != current_song:
            if cached_song.percentage > SCROBBLE_PERCENTAGE:
                if not args.dry_run:
                    logger.info(f"Scrobbling {cached_song}.")
                    networks.mpdscrobble_scrobble(cached_song)
                else:
                    logger.warning("Dry-run mode enabled.")
            logger.debug(f"Updating now playing to {cached_song}.")
            networks.mpdscrobble_update_now_playing(current_song)
        cached_song = client.mpdscrobble_currentsong()


def main():
    args = parse_args()
    config = read_config(args.config_file)
    if len(config.sections()) == 0:
        raise Exception(
            "Empty config file.\nCreate a valid config file in ~/.config/mpdscrobble/mpdscrobble.conf or use the -c/--config-file flag."
        )

    networks = create_network(config)

    client = MPDScrobbleMPDConnection()
    client.mpdscrobble_connect()

    # Init
    cached_song = client.mpdscrobble_currentsong()
    logger.debug(f"Updating now playing to {cached_song}.")
    networks.mpdscrobble_update_now_playing(cached_song)

    # Loop
    while True:
        loop(args, networks, client, cached_song)
        logger.error("MPD Client crashed. Restarting.")
        client.mpdscrobble_restart()
        cached_song = client.mpdscrobble_currentsong()


def parse_args():
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
