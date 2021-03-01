import time
import pylast
import datetime
import logging

from mpd import MPDClient


logger = logging.getLogger(__name__)


class MPDScrobbleNetwork:
    """Class to interact with several networks."""

    def __init__(self, networks):
        self.networks = networks

    def mpdscrobble_update_now_playing(self, song):
        for i in self.networks:
            try:
                i.mpdscrobble_update_now_playing(song)
            except Exception as e:
                logger.error(e)

    def mpdscrobble_scrobble(self, song):
        for i in self.networks:
            try:
                i.mpdscrobble_scrobble(song)
            except Exception as e:
                logger.error(e)


class MPDScrobbleLastFMNetwork(pylast.LastFMNetwork):
    """Class to interact with Last.FM."""

    def __init__(self, username, password, api_key, api_secret):
        self.username = username
        pylast.LastFMNetwork.__init__(
            self,
            username=username,
            password_hash=pylast.md5(password),
            api_key=api_key,
            api_secret=api_secret,
        )

    def __str__(self):
        return f"last.fm: user {self.username}."

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
            duration=int(track.duration),
            track_number=track.track,
        )


class MPDScrobbleTrack:
    """Class to represent a MPD Track."""

    def __init__(
        self,
        artist,
        title,
        album=None,
        track=None,
        date=None,
        duration=1.0,
        elapsed=0.0,
        timestamp=None,
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
        self.timestamp = (
            int(time.mktime(datetime.datetime.now().timetuple()))
            if not timestamp
            else timestamp
        )

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

    def mpdscrobble_connect(self, host, port):
        self.connect(host, port)

    def mpdscrobble_restart(self):
        self.close()
        self.disconnect()
        self.mpdscrobble_connect()

    def mpdscrobble_currentsong(self):
        currentsong = self.currentsong()
        status = self.status()
        return MPDScrobbleTrack(
            artist=currentsong["artist"],
            title=currentsong["title"],
            track=currentsong["track"][0] if "track" in currentsong else None,
            album=currentsong["album"] if "album" in currentsong else None,
            date=currentsong["date"] if "date" in currentsong else None,
            duration=currentsong["duration"],
            elapsed=status["elapsed"],
        )
