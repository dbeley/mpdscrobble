import time
from mpdscrobble.mpdscrobble import MPDScrobbleTrack


def test_track_percentage():
    track = MPDScrobbleTrack(
        artist="artist", title="title", album="album", duration=1.0, elapsed=1.0
    )

    assert track.percentage == 100.0


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

    assert track == track2

    assert track != track3


def test_track_str():
    track = MPDScrobbleTrack(artist="artist", title="title", album="album", date="date")

    str_track = "artist - title (album - date)"

    assert str(track) == str_track


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

    assert track.debug() == str_track


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

    assert track.timestamp == int(time.time())
