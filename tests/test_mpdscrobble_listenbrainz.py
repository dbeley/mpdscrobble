from mpdscrobble.mpdscrobble import MPDScrobbleListenBrainzNetwork


def test_str_representation():
    listenbrainz_network = MPDScrobbleListenBrainzNetwork(
        username="username", api_key="api_key"
    )

    assert str(listenbrainz_network) == "listenbrainz: user username"
