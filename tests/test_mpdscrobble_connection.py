from mpdscrobble.mpdscrobble import MPDScrobbleMPDConnection


def current_song():
    return {
        "artist": "song artist",
        "albumartist": "album artist",
        "title": "title",
        "duration": "10",
    }


def status():
    return {"elapsed": "5", "state": "play"}


def test_uses_track_artist_by_default(monkeypatch):
    client = MPDScrobbleMPDConnection()
    monkeypatch.setattr(client, "currentsong", current_song)
    monkeypatch.setattr(client, "status", status)

    track = client.mpdscrobble_currentsong()

    assert track.artist == "song artist"


def test_uses_album_artist_when_enabled(monkeypatch):
    client = MPDScrobbleMPDConnection(use_album_artist=True)
    monkeypatch.setattr(client, "currentsong", current_song)
    monkeypatch.setattr(client, "status", status)

    track = client.mpdscrobble_currentsong()

    assert track.artist == "album artist"
