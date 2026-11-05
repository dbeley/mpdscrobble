import configparser

from mpdscrobble.mpdscrobble import MPDScrobbleLastFMNetwork
from mpdscrobble.utils import create_networks


def test_str_representation(mock_pylast_session_key_generator):
    lastfm_network = MPDScrobbleLastFMNetwork(
        username="username",
        password="password",
        api_key="api_key",
        api_secret="api_secret",
    )

    assert str(lastfm_network) == "last.fm: user username"


def test_scrobbles_with_a_session_key_and_no_password(
    mock_pylast_session_key_generator,
):
    lastfm_network = MPDScrobbleLastFMNetwork(
        username="username",
        password=None,
        api_key="api_key",
        api_secret="api_secret",
        session_key="session_key",
    )

    assert lastfm_network.session_key == "session_key"
    assert lastfm_network.password_hash is None


def test_create_networks_forwards_the_session_key(mock_pylast_session_key_generator):
    config = configparser.ConfigParser()
    config.read_string(
        "[last.fm]\n"
        "api_key = api_key\n"
        "api_secret = api_secret\n"
        "session_key = session_key\n"
    )

    networks = create_networks(config)

    assert networks.networks[0].session_key == "session_key"
