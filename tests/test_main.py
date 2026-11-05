import argparse

from mpdscrobble import __main__ as main_mod


class FakeClient:
    def __init__(self, use_album_artist=False):
        self.restarts = 0

    def mpdscrobble_connect(self, host, port):
        pass

    def mpdscrobble_currentsong(self):
        return None

    def mpdscrobble_restart(self):
        self.restarts += 1


def test_restart_backoff_doubles(monkeypatch):
    args = argparse.Namespace(config_file="nope", dry_run=True)
    sleeps = []

    def fake_loop(*_):
        raise Exception("crashed")

    def fake_sleep(seconds):
        sleeps.append(seconds)
        if len(sleeps) >= 2:
            raise SystemExit

    monkeypatch.setattr(main_mod, "parse_args", lambda: args)
    monkeypatch.setattr(
        main_mod,
        "read_config",
        lambda _: type("C", (), {"sections": lambda self: ["mpdscrobble"]})(),
    )
    monkeypatch.setattr(main_mod, "create_networks", lambda _: None)
    monkeypatch.setattr(
        main_mod, "get_mpdscrobble_config", lambda _: ("host", 6600, False)
    )
    monkeypatch.setattr(main_mod, "MPDScrobbleMPDConnection", FakeClient)
    monkeypatch.setattr(main_mod, "loop", fake_loop)
    monkeypatch.setattr(main_mod.time, "sleep", fake_sleep)

    try:
        main_mod.main()
    except SystemExit:
        pass

    assert sleeps == [10, 20]


def test_loop_fetches_song_once_per_call():
    args = argparse.Namespace(dry_run=True)
    fetches = []

    class FakeClient:
        def mpdscrobble_currentsong(self):
            fetches.append(1)
            return None

    class FakeNetworks:
        def mpdscrobble_scrobble(self, song):
            pass

        def mpdscrobble_update_now_playing(self, song):
            pass

    assert main_mod.loop(args, FakeNetworks(), FakeClient(), None) is None
    assert len(fetches) == 1


def test_scrobbles_track_at_exactly_40_percent():
    from mpdscrobble.mpdscrobble import MPDScrobbleTrack

    args = argparse.Namespace(dry_run=False)
    scrobbled = []

    class FakeClient:
        def mpdscrobble_currentsong(self):
            return None

    class FakeNetworks:
        def mpdscrobble_scrobble(self, song):
            scrobbled.append(song)

        def mpdscrobble_update_now_playing(self, song):
            pass

    track = MPDScrobbleTrack(artist="a", title="t", duration=1.0, elapsed=0.4)
    main_mod.loop(args, FakeNetworks(), FakeClient(), track)

    assert scrobbled == [track]


def test_retries_when_the_mpd_connection_fails(monkeypatch):
    args = argparse.Namespace(config_file="nope", dry_run=True)
    sleeps = []
    connects = []

    class FakeClient:
        def __init__(self, use_album_artist=False):
            pass

        def mpdscrobble_connect(self, host, port):
            connects.append(1)
            if len(connects) == 1:
                raise ConnectionError("MPD is not up yet")

        def mpdscrobble_currentsong(self):
            return None

        def mpdscrobble_restart(self):
            pass

    def fake_loop(*_):
        raise SystemExit

    def fake_sleep(seconds):
        sleeps.append(seconds)

    monkeypatch.setattr(main_mod, "parse_args", lambda: args)
    monkeypatch.setattr(
        main_mod,
        "read_config",
        lambda _: type("C", (), {"sections": lambda self: ["mpdscrobble"]})(),
    )
    monkeypatch.setattr(main_mod, "create_networks", lambda _: None)
    monkeypatch.setattr(
        main_mod, "get_mpdscrobble_config", lambda _: ("host", 6600, False)
    )
    monkeypatch.setattr(main_mod, "MPDScrobbleMPDConnection", FakeClient)
    monkeypatch.setattr(main_mod, "loop", fake_loop)
    monkeypatch.setattr(main_mod.time, "sleep", fake_sleep)

    try:
        main_mod.main()
    except SystemExit:
        pass

    assert len(connects) == 2
    assert sleeps == [10]


def _run_main(monkeypatch, client_class, fake_loop, sleeps, networks):
    """Run main() with fakes until the fake sleep asks to stop."""

    class Stop(Exception):
        pass

    def fake_sleep(seconds):
        sleeps.append(seconds)
        if len(sleeps) >= 3:
            raise Stop

    args = argparse.Namespace(config_file="nope", dry_run=False)
    monkeypatch.setattr(main_mod, "parse_args", lambda: args)
    monkeypatch.setattr(
        main_mod,
        "read_config",
        lambda _: type("C", (), {"sections": lambda self: ["mpdscrobble"]})(),
    )
    monkeypatch.setattr(main_mod, "create_networks", lambda _: networks)
    monkeypatch.setattr(
        main_mod, "get_mpdscrobble_config", lambda _: ("host", 6600, False)
    )
    monkeypatch.setattr(main_mod, "MPDScrobbleMPDConnection", client_class)
    monkeypatch.setattr(main_mod, "loop", fake_loop)
    monkeypatch.setattr(main_mod.time, "sleep", fake_sleep)
    monkeypatch.setattr(main_mod.constants, "LOOP_DELAY", 0)

    try:
        main_mod.main()
    except Stop:
        pass


def test_restart_delay_is_reset_after_a_successful_poll(monkeypatch):
    sleeps = []
    polls = []

    class FakeClient:
        def __init__(self, use_album_artist=False):
            pass

        def mpdscrobble_connect(self, host, port):
            pass

        def mpdscrobble_currentsong(self):
            return None

        def mpdscrobble_restart(self):
            pass

    def fake_loop(*_):
        polls.append(1)
        if len(polls) != 2:
            raise Exception("crashed")

    _run_main(monkeypatch, FakeClient, fake_loop, sleeps, networks=None)

    # 10 after the first crash, LOOP_DELAY after the successful poll, then the
    # delay must be back to 10 instead of 20.
    assert sleeps == [10, 0, 10]


def test_keeps_song_cached_across_a_reconnection(monkeypatch):
    from mpd import ConnectionError as MPDConnectionError

    from mpdscrobble.mpdscrobble import MPDScrobbleTrack

    track = MPDScrobbleTrack(artist="a", title="t", duration=100.0, elapsed=90.0)
    scrobbled = []
    sleeps = []
    calls = []

    class FakeClient:
        def __init__(self, use_album_artist=False):
            pass

        def mpdscrobble_connect(self, host, port):
            pass

        def mpdscrobble_restart(self):
            pass

        def mpdscrobble_currentsong(self):
            calls.append(1)
            if len(calls) == 1:
                return track
            if len(calls) == 2:
                raise MPDConnectionError("Connection lost while reading line")
            # MPD restarted by a rebuild: playback is stopped, nothing cached
            # from the new connection.
            return None

    class FakeNetworks:
        def mpdscrobble_scrobble(self, song):
            scrobbled.append(song)

        def mpdscrobble_update_now_playing(self, song):
            pass

    _run_main(monkeypatch, FakeClient, main_mod.loop, sleeps, networks=FakeNetworks())

    assert scrobbled == [track]


def test_reconnects_with_restart_after_a_lost_connection(monkeypatch):
    """connect() raises "Already connected" on a stale socket: use restart()."""
    from mpd import ConnectionError as MPDConnectionError

    sleeps = []
    calls = {"connect": 0, "restart": 0}

    class FakeClient:
        def __init__(self, use_album_artist=False):
            pass

        def mpdscrobble_connect(self, host, port):
            calls["connect"] += 1

        def mpdscrobble_restart(self):
            calls["restart"] += 1

        def mpdscrobble_currentsong(self):
            raise MPDConnectionError("Connection lost while reading line")

    _run_main(monkeypatch, FakeClient, main_mod.loop, sleeps, networks=None)

    assert calls == {"connect": 1, "restart": 2}
