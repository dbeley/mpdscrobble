import logging
import configparser
import os
from .mpdscrobble import MPDScrobbleLastFMNetwork, MPDScrobbleNetwork


logger = logging.getLogger(__name__)


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(config_file))
    return config


def create_network(config):
    networks = []
    for i in config.sections():
        networks.append(
            MPDScrobbleLastFMNetwork(
                config[i]["username"],
                config[i]["password"],
                config[i]["api_key"],
                config[i]["api_secret"],
            )
        )
    return MPDScrobbleNetwork(networks)
