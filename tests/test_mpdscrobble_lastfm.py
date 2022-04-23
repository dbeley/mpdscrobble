from mpdscrobble.mpdscrobble import MPDScrobbleLastFMNetwork


def test_str_representation(mock_pylast_session_key_generator):
    lastfm_network = MPDScrobbleLastFMNetwork(
        username="username",
        password="password",
        api_key="api_key",
        api_secret="api_secret",
    )

    assert str(lastfm_network) == "last.fm: user username"
