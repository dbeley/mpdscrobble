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
    monkeypatch.setattr(main_mod, "read_config", lambda _: type("C", (), {"sections": lambda self: ["mpdscrobble"]})())
    monkeypatch.setattr(main_mod, "create_networks", lambda _: None)
    monkeypatch.setattr(main_mod, "get_mpdscrobble_config", lambda _: ("host", 6600, False))
    monkeypatch.setattr(main_mod, "MPDScrobbleMPDConnection", FakeClient)
    monkeypatch.setattr(main_mod, "loop", fake_loop)
    monkeypatch.setattr(main_mod.time, "sleep", fake_sleep)

    try:
        main_mod.main()
    except SystemExit:
        pass

    assert sleeps == [10, 20]


def test_loop_fetches_song_once_per_iteration(monkeypatch):
    args = argparse.Namespace(dry_run=True)
    fetches = []
    sleeps = []

    class FakeClient:
        def mpdscrobble_currentsong(self):
            fetches.append(1)
            return None

    class FakeNetworks:
        def mpdscrobble_scrobble(self, song):
            pass

        def mpdscrobble_update_now_playing(self, song):
            pass

    def stop(seconds):
        sleeps.append(1)
        if len(sleeps) >= 3:
            raise SystemExit

    monkeypatch.setattr(main_mod.time, "sleep", stop)
    try:
        main_mod.loop(args, FakeNetworks(), FakeClient(), None)
    except SystemExit:
        pass

    assert len(fetches) == len(sleeps) - 1
