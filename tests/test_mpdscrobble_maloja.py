from mpdscrobble.mpdscrobble import MPDScrobbleMalojaNetwork


def test_str_representation():
    maloja_network = MPDScrobbleMalojaNetwork(api_key="api_key", url="url")

    assert str(maloja_network) == "maloja: instance url"
