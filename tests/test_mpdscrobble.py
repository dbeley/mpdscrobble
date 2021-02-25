import time
from mpdscrobble.mpdscrobble import MPDScrobbleTrack


def test_track_percentage():
    track = MPDScrobbleTrack(
        artist="artist", title="title", album="album", duration=1.0, elapsed=1.0
    )

    if not track.percentage == 100.0:
        raise AssertionError()


def test_track_equality():
    track = MPDScrobbleTrack(
        artist="artist", title="title", album="album", duration=1.0, elapsed=1.0
    )

    track2 = MPDScrobbleTrack(
        artist="artist", title="title", album="album", duration=1.0, elapsed=0.5
    )
    track3 = MPDScrobbleTrack(
        artist="artist", title="title", album="album", duration=2.0, elapsed=1.0
    )

    if not track == track2:
        raise AssertionError()

    if not track != track3:
        raise AssertionError()


def test_track_str():
    track = MPDScrobbleTrack(artist="artist", title="title", album="album", date="date")

    str_track = "artist - title (album - date)"

    if not str(track) == str_track:
        raise AssertionError()


def test_track_debug():
    track = MPDScrobbleTrack(
        artist="artist",
        title="title",
        album="album",
        date="date",
        track=1,
        elapsed=1.0,
        duration=2.0,
        timestamp=1000,
    )

    str_track = "artist - 1 title (album - date) 1.0/2.0 (50.0%). Timestamp: 1000."

    if not track.debug() == str_track:
        raise AssertionError()


def test_track_timestamp():
    track = MPDScrobbleTrack(
        artist="artist",
        title="title",
        album="album",
        date="date",
        track=1,
        elapsed=1.0,
        duration=2.0,
    )

    print(track.timestamp)
    print(time.time())

    if not track.timestamp == int(time.time()):
        raise AssertionError()
