import time
from typing import Optional, Union, Sequence

import httpx
import pylast
import datetime
import logging

from mpd import MPDClient

from mpdscrobble import constants

logger = logging.getLogger(__name__)


class MPDScrobbleTrack:
    """Class to represent a MPD Track."""

    def __init__(
        self,
        artist: str,
        title: str,
        album: str = None,
        track: int = None,
        date: str = None,
        duration: float = 1.0,
        elapsed: float = 0.0,
        timestamp: int = None,
    ) -> None:
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

    def __str__(self) -> str:
        return f"{self.artist} - {self.title} ({self.album} - {self.date})"

    def debug(self) -> str:
        return f"{self.artist} - {self.track} {self.title} ({self.album} - {self.date}) {self.elapsed}/{self.duration} ({self.percentage}%). Timestamp: {self.timestamp}."

    def __eq__(self, other) -> bool:
        return (
            self.artist == other.artist
            and self.title == other.title
            and self.album == other.album
            and self.date == other.date
            and self.duration == other.duration
        )


class MPDScrobbleLastFMNetwork(pylast.LastFMNetwork):
    """Class to interact with Last.FM."""

    def __init__(
        self, username: str, password: str, api_key: str, api_secret: str
    ) -> None:
        self.username = username
        pylast.LastFMNetwork.__init__(
            self,
            username=username,
            password_hash=pylast.md5(password),
            api_key=api_key,
            api_secret=api_secret,
        )

    def __str__(self) -> str:
        return f"last.fm: user {self.username}"

    def mpdscrobble_scrobble(self, track: MPDScrobbleTrack) -> None:
        self.scrobble(
            artist=track.artist,
            title=track.title,
            timestamp=track.timestamp,
            album=track.album,
        )

    def mpdscrobble_update_now_playing(self, track: MPDScrobbleTrack) -> None:
        self.update_now_playing(
            artist=track.artist,
            title=track.title,
            album=track.album,
            duration=int(track.duration),
            track_number=track.track,
        )


class MPDScrobbleMalojaNetwork:
    """Class to interact with Maloja."""

    def __init__(
        self,
        api_key: str = "",
        url: str = "",
    ) -> None:

        self.url = url
        self.api_key = api_key

    def __str__(self) -> str:
        return f"maloja: instance {self.url}"

    def mpdscrobble_scrobble(self, track: MPDScrobbleTrack) -> None:
        payload = {
            "artist": track.artist,
            "title": track.title,
            "time": track.timestamp,
            "album": track.album,
            "key": self.api_key,
        }
        post_url = self.url + "/apis/mlj_1/newscrobble"
        logger.debug("Maloja: sending %s to %s", payload, post_url)
        response = httpx.post(post_url, data=payload)
        logger.debug("Maloja response: %s", response.content)
        response.raise_for_status()

    def mpdscrobble_update_now_playing(self, track: MPDScrobbleTrack) -> None:
        pass


class MPDScrobbleListenBrainzNetwork:
    """Class to interact with ListenBrainz."""

    def __init__(
        self,
        username: str = "",
        api_key: str = "",
    ) -> None:
        self.username = username
        self.api_key = api_key

    def __str__(self) -> str:
        return f"listenbrainz: user {self.username}"

    def mpdscrobble_scrobble(self, track: MPDScrobbleTrack) -> None:
        """Taken from https://listenbrainz.readthedocs.io/en/production/dev/api-usage/"""
        payload = [
            {
                "listened_at": track.timestamp,
                "track_metadata": {
                    "artist_name": track.artist,
                    "track_name": track.title,
                    "release_name": track.album,
                },
            }
        ]
        post_url = "https://{0}/1/submit-listens".format("api.listenbrainz.org")
        logger.debug("ListenBrainz: sending %s to %s", payload, post_url)
        response = httpx.post(
            url=post_url,
            json={
                "listen_type": "single",
                "payload": payload,
            },
            headers={"Authorization": "Token {0}".format(self.api_key)},
        )
        logger.debug("ListenBrainz response: %s", response.content)
        response.raise_for_status()

    def mpdscrobble_update_now_playing(self, track) -> None:
        pass


class MPDScrobbleNetwork:
    """Class to interact with several networks."""

    def __init__(
        self,
        networks: Sequence[
            Union[
                MPDScrobbleLastFMNetwork,
                MPDScrobbleMalojaNetwork,
                MPDScrobbleListenBrainzNetwork,
            ]
        ],
    ) -> None:
        self.networks = networks

    def mpdscrobble_update_now_playing(self, song: MPDScrobbleTrack) -> None:
        for i in self.networks:
            try:
                logger.debug("Update now playing with %s on %s", song, i)
                i.mpdscrobble_update_now_playing(song)
            except Exception as e:
                logger.error(e)

    def mpdscrobble_scrobble(self, song: MPDScrobbleTrack) -> None:
        for i in self.networks:
            try:
                logger.debug("Scrobble %s on %s", song, i)
                i.mpdscrobble_scrobble(song)
            except Exception as e:
                logger.error(e)


class MPDScrobbleMPDConnection(MPDClient):
    """Class to interact with MPD."""

    def __init__(self) -> None:
        MPDClient.__init__(self)

    def mpdscrobble_connect(
        self, host: str = constants.DEFAULT_HOST, port: int = constants.DEFAULT_PORT
    ) -> None:
        self.connect(host, port)

    def mpdscrobble_restart(self) -> None:
        self.close()
        self.disconnect()
        self.mpdscrobble_connect()

    def mpdscrobble_currentsong(self) -> Optional[MPDScrobbleTrack]:
        currentsong = self.currentsong()
        status = self.status()
        if (
            all([x in currentsong for x in ["artist", "title", "duration"]])
            and "elapsed" in status
        ):
            return MPDScrobbleTrack(
                artist=currentsong["artist"],
                title=currentsong["title"],
                track=currentsong["track"][0] if "track" in currentsong else None,
                album=currentsong["album"] if "album" in currentsong else None,
                date=currentsong["date"] if "date" in currentsong else None,
                duration=currentsong["duration"],
                elapsed=status["elapsed"],
            )
        else:
            return None
