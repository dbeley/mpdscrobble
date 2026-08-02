from mpdscrobble.mpdscrobble import MPDScrobbleMPDConnection


def current_song():
    return {
        "artist": "song artist",
        "albumartist": "album artist",
        "title": "title",
        "duration": "10",
        "track": "10",
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


def test_restart_reconnects_with_configured_host_port(monkeypatch):
    client = MPDScrobbleMPDConnection()
    connect_calls = []
    monkeypatch.setattr(
        client, "connect", lambda host, port=None: connect_calls.append((host, port))
    )
    monkeypatch.setattr(client, "close", lambda: None)
    monkeypatch.setattr(client, "disconnect", lambda: None)

    client.mpdscrobble_connect("mpd.example.org", 1234)
    client.mpdscrobble_restart()

    assert connect_calls == [
        ("mpd.example.org", 1234),
        ("mpd.example.org", 1234),
    ]


def test_restart_survives_dead_close(monkeypatch):
    client = MPDScrobbleMPDConnection()
    connect_calls = []

    def bad_close():
        raise ConnectionError("socket closed")

    monkeypatch.setattr(client, "close", bad_close)
    monkeypatch.setattr(client, "disconnect", lambda: None)
    monkeypatch.setattr(
        client, "connect", lambda host, port=None: connect_calls.append((host, port))
    )

    client.mpdscrobble_connect("host", 6600)
    client.mpdscrobble_restart()

    assert connect_calls == [("host", 6600), ("host", 6600)]


def test_keeps_full_multi_digit_track_number(monkeypatch):
    client = MPDScrobbleMPDConnection()
    monkeypatch.setattr(client, "currentsong", current_song)
    monkeypatch.setattr(client, "status", status)

    track = client.mpdscrobble_currentsong()

    assert track.track == "10"
