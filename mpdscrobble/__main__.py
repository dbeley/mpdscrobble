"""
mpdscrobble: a simple Last.fm scrobbler for MPD.
"""

import argparse
import logging
import time
from typing import Optional

from mpd import MPDError

from mpdscrobble import constants

from .mpdscrobble import MPDScrobbleMPDConnection, MPDScrobbleNetwork, MPDScrobbleTrack
from .utils import create_networks, get_mpdscrobble_config, read_config

logger = logging.getLogger(__name__)
logging.getLogger("pylast").setLevel(logging.WARNING)
logging.getLogger("mpd").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


def loop(
    args: argparse.Namespace,
    networks: MPDScrobbleNetwork,
    client: MPDScrobbleMPDConnection,
    cached_song: Optional[MPDScrobbleTrack],
) -> Optional[MPDScrobbleTrack]:
    """Poll MPD once, scrobble/update as needed and return the song to cache."""
    current_song = client.mpdscrobble_currentsong()
    if current_song and cached_song:
        logger.debug(
            "Current: %s\nCached: %s", current_song.debug(), cached_song.debug()
        )
        if cached_song != current_song:
            if cached_song.percentage >= constants.SCROBBLE_PERCENTAGE:
                if not args.dry_run:
                    logger.info("Sending scrobble for %s.", cached_song)
                    networks.mpdscrobble_scrobble(cached_song)
                else:
                    logger.warning(
                        "Dry-run mode enabled. Would have scrobbled %s.",
                        cached_song,
                    )
            networks.mpdscrobble_update_now_playing(current_song)
    if not current_song and cached_song:
        if cached_song.percentage >= constants.SCROBBLE_PERCENTAGE:
            if not args.dry_run:
                logger.info(
                    "Sending scrobble for %s. Detected stopped playback.",
                    cached_song,
                )
                networks.mpdscrobble_scrobble(cached_song)
            else:
                logger.warning(
                    "Dry-run mode enabled. Would have scrobbled %s.",
                    cached_song,
                )
    return current_song


def main():
    args = parse_args()
    config = read_config(args.config_file)
    if len(config.sections()) == 0:
        raise Exception(
            "Empty config file.\n"
            "Create a valid config file in ~/.config/mpdscrobble/mpdscrobble.conf"
            "or use the -c/--config-file flag."
        )

    host, port, use_album_artist = get_mpdscrobble_config(config)

    client = MPDScrobbleMPDConnection(use_album_artist=use_album_artist)

    # Connection and network setup are retried as well: MPD or the scrobbling
    # services can be temporarily unreachable, which should not kill the daemon.
    connected = False
    cached_song = None
    timeout = constants.DEFAULT_RESTART_DELAY
    while True:
        try:
            if connected:
                client.mpdscrobble_restart()
            else:
                client.mpdscrobble_connect(host, port)
                connected = True
            networks = create_networks(config)
            # Keep the cached song so a track interrupted by the reconnection can
            # still be scrobbled.
            cached_song = loop(args, networks, client, cached_song)
        except (MPDError, OSError) as error:
            # MPD going away (restart, suspend, idle timeout) is expected: just
            # reconnect, no traceback and no growing delay.
            logger.warning("Lost connection to MPD (%s). Reconnecting.", error)
            time.sleep(timeout)
        except Exception:
            logger.exception(
                "mpdscrobble crashed. Waiting %s seconds before restarting.",
                timeout,
            )
            time.sleep(timeout)
            timeout = min(timeout * 2, constants.MAX_RESTART_DELAY)
        else:
            # A full successful poll: forget the previous failures.
            timeout = constants.DEFAULT_RESTART_DELAY
            time.sleep(constants.LOOP_DELAY)


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
