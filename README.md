# mpdscrobble

A simple Last.fm scrobbler for MPD.

On top of [Last.fm](https://www.last.fm/home), mpdscrobble is also compatible with those services:
- [ListenBrainz](https://listenbrainz.org/)
- [Maloja](https://github.com/krateng/maloja)

If you are searching for a mpd-compatible Last.fm scrobbler, check out first [mpdscribble](https://github.com/MusicPlayerDaemon/mpdscribble), as mpdscrobble has less features than mpdscribble:
- no journal of failed scrobbles
- it needs a pair of Last.fm API key/secret instead of just username/password

If you need to scrobble tracks from an existing mpdscribble journal file, you can use the [`mpdscribble_history.py`](https://github.com/dbeley/mpdscrobble/blob/main/mpdscribble_history.py) script.

## Requirements

- httpx
- mpd-python2
- pylast

## Installation

Classic installation :

```
pip install mpdscrobble
mpdscrobble -h
```
You will then need to create a config file (see the [Configuration](#Configuration) section).

If you want the systemd-service, you will have to install it manually (see the [Scheduling](#Scheduling) section).

### Run from source

#### First method

```
git clone https://github.com/dbeley/mpdscrobble
cd mpdscrobble
python setup.py install --user
mpdscrobble -h
```

#### Second method (with pipenv)

```
git clone https://github.com/dbeley/mpdscrobble
cd mpdscrobble
pipenv install '-e .'
pipenv run mpdscrobble -h
```

### On Archlinux

If you are an Archlinux user, you can install the AUR package [mpdscrobble-git](https://aur.archlinux.org/packages/mpdscrobble-git).

```
yay -S mpdscrobble-git
```

The systemd service file will be automatically installed.

## Configuration

See [`mpdscrobble.example.conf`](https://github.com/dbeley/mpdscrobble/blob/main/mpdscrobble.example.conf) for an example.

By default, `mpdscrobble` search a config file at `~/.config/mpdscrobble/mpdscrobble.conf`, but you can override the default location with the `-c/--config` flag (see the [Usage](#Usage) section).

## Scheduling

If you installed the AUR package on Archlinux, the systemd service is automatically installed.
```
systemctl --user enable --now mpdscrobble
systemctl --user status mpdscrobble
```

Otherwise you will need to manually install the systemd service.
```
curl https://raw.githubusercontent.com/dbeley/mpdscrobble/main/systemd-service/mpdscrobble.service > ~/.config/systemd/user/mpdscrobble.service
systemctl --user daemon-reload
systemctl --user enable --now mpdscrobble
systemctl --user status mpdscrobble
```

## Usage

```
usage: mpdscrobble [-h] [--debug] [-c CONFIG_FILE] [--dry-run]

A simple Last.fm scrobbler for MPD.

optional arguments:
  -h, --help            Show this help message and exit.
  --debug               Display debugging information.
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        Config file (default: ~/.config/mpdscrobble/mpdscrobble.conf).
  --dry-run             Disable scrobbling.
```
