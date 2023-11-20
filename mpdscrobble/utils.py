import logging
import configparser
import os

from mpdscrobble import constants
from .mpdscrobble import (
    MPDScrobbleLastFMNetwork,
    MPDScrobbleMalojaNetwork,
    MPDScrobbleNetwork,
    MPDScrobbleListenBrainzNetwork,
)


logger = logging.getLogger(__name__)


def read_config(config_file: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(config_file))
    return config


def get_mpdscrobble_config(config: configparser.ConfigParser) -> tuple[str, int]:
    host = constants.DEFAULT_HOST
    port = constants.DEFAULT_PORT
    if "mpdscrobble" in config:
        if "host" in config["mpdscrobble"]:
            host = config["mpdscrobble"]["host"]
        if "port" in config["mpdscrobble"]:
            port = int(config["mpdscrobble"]["port"])
    return host, port


def create_networks(config: configparser.ConfigParser) -> MPDScrobbleNetwork:
    networks = []
    for i in config.sections():
        if i != "mpdscrobble":
            if i.startswith("maloja"):
                network = MPDScrobbleMalojaNetwork(
                    api_key=config[i].get("api_key"), url=config[i].get("url")
                )  # type: ignore
            elif i.startswith("listenbrainz"):
                network = MPDScrobbleListenBrainzNetwork(
                    api_key=config[i].get("api_key"), username=config[i].get("username")
                )  # type: ignore
            # last.fm is the default service
            else:
                network = MPDScrobbleLastFMNetwork(
                    username=config[i].get("username"),
                    password=config[i].get("password"),
                    api_key=config[i].get("api_key"),
                    api_secret=config[i].get("api_secret"),
                )  # type: ignore
            networks.append(network)
    return MPDScrobbleNetwork(networks)
