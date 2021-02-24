import time
import pylast
import datetime
import logging
import configparser

from mpd import MPDClient


logger = logging.getLogger(__name__)


class MPDScrobbleNetwork:
    """Class to interact with several networks."""

    def __init__(self, networks):
        self.networks = networks

    def mpdscrobble_update_now_playing(self, song):
        for i in self.networks:
            try:
                logger.debug(f"{i}")
                i.mpdscrobble_update_now_playing(song)
            except Exception as e:
                logger.error(e)

    def mpdscrobble_scrobble(self, song):
        for i in self.networks:
            try:
                logger.debug(f"{i}")
                i.mpdscrobble_scrobble(song)
            except Exception as e:
                logger.error(e)


class MPDScrobbleLibreFMNetwork(pylast.LibreFMNetwork):
    """Class to interact with Libre.FM."""

    def __init__(self, username, password):
        pylast.LibreFMNetwork.__init__(
            self, username=username, password_hash=pylast.md5(password)
        )

    def __str__(self):
        return "libre.fm"

    def mpdscrobble_scrobble(self, track):

        self.scrobble(
            artist=track.artist,
            title=track.title,
            timestamp=track.timestamp,
            album=track.album,
        )

    def mpdscrobble_update_now_playing(self, track):

        self.update_now_playing(
            artist=track.artist,
            title=track.title,
            album=track.album,
            track_number=track.track,
            duration=int(track.duration),
        )


class MPDScrobbleLastFMNetwork(pylast.LastFMNetwork):
    """Class to interact with Last.FM."""

    def __init__(self, username, password, api_key, api_secret):
        pylast.LastFMNetwork.__init__(
            self,
            username=username,
            password_hash=pylast.md5(password),
            api_key=api_key,
            api_secret=api_secret,
        )

    def __str__(self):
        return "last.fm"

    def mpdscrobble_scrobble(self, track):

        self.scrobble(
            artist=track.artist,
            title=track.title,
            timestamp=track.timestamp,
            album=track.album,
        )

    def mpdscrobble_update_now_playing(self, track):

        self.update_now_playing(
            artist=track.artist,
            title=track.title,
            album=track.album,
            track_number=track.track,
            duration=int(track.duration),
        )


class MPDScrobbleTrack:
    """Class to represent a MPD Track."""

    def __init__(
        self, artist, title, album, track=None, date=None, duration=1.0, elapsed=0.0
    ):
        self.artist = artist
        self.title = title
        self.track = track
        self.album = album
        self.date = date
        self.duration = float(duration)
        self.elapsed = float(elapsed)
        self.percentage = (
            0
            if not duration or not elapsed
            else round(self.elapsed / self.duration * 100, 2)
        )
        self.timestamp = int(time.mktime(datetime.datetime.now().timetuple()))

    def __str__(self):
        return f"{self.artist} - {self.title} ({self.album} - {self.date})"

    def debug(self):
        return f"{self.artist} - {self.track} {self.title} ({self.album} - {self.date}) {self.elapsed}/{self.duration} ({self.percentage}%). Timestamp: {self.timestamp}."

    def __eq__(self, other):
        return (
            self.artist == other.artist
            and self.title == other.title
            and self.album == other.album
            and self.date == other.date
            and self.duration == other.duration
        )


class MPDScrobbleMPDConnection(MPDClient):
    """Class to interact with MPD."""

    def __init__(self):
        MPDClient.__init__(self)

    def mpdscrobble_connect(self):
        self.connect("localhost", 6600)

    def mpdscrobble_restart(self):
        self.close()
        self.disconnect()
        self.mpdscrobble_start()

    def mpdscrobble_currentsong(self):
        currentsong = self.currentsong()
        status = self.status()
        return MPDScrobbleTrack(
            artist=currentsong["artist"],
            title=currentsong["title"],
            track=currentsong["track"][0],
            album=currentsong["album"],
            date=currentsong["date"],
            duration=currentsong["duration"],
            elapsed=status["elapsed"],
        )


def read_config(config_file):
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        return config
    except Exception as e:
        logger.error(f"Error reading config file: {e}.")
        logger.error(
            f"Create a valid config file in ~/.config/mpdscrobble/mpdscrobble.conf or use the -c/--config-file flag."
        )


def create_network(config):
    networks = []
    for i in config.sections():
        if config[i]["network"].lower() in ["last.fm", "lastfm"]:
            networks.append(
                MPDScrobbleLastFMNetwork(
                    config[i]["username"],
                    config[i]["password"],
                    config[i]["api_key"],
                    config[i]["api_secret"],
                )
            )
        elif config[i]["network"].lower() in ["libre.fm", "librefm"]:
            networks.append(
                MPDScrobbleLibreFMNetwork(config[i]["username"], config[i]["password"])
            )
    return MPDScrobbleNetwork(networks)
