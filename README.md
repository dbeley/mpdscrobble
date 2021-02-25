# mpdscrobble

A simple Last.fm scrobbler for MPD.

If you are searching for a mpd-compatible last.fm scrobbler, check out first [mpdscribble](https://github.com/MusicPlayerDaemon/mpdscribble), as mpdscrobble has less features than mpdscribble:
- no journal of failed scrobbles
- it needs a pair of Last.fm API key/secret instead of just username/password

The script [`mpdscribble_history.py`](https://github.com/dbeley/mpdscrobble/blob/main/mpdscribble_history.py) can be used to scrobble a list of tracks from a mpdscribble journal file.

## Requirements

- mpd-python2
- pylast

## Installation

Classic installation :

```
pip install mpdscrobble
mkdir -p ~/.config/mpdscrobble
curl https://raw.githubusercontent.com/dbeley/mpdscrobble/main/mpdscrobble.example.conf > ~/.config/mpdscrobble/mpdscrobble.conf
mpdscrobble -h
```

If you need the systemd-service, you will have to install it manually (see *Scheduling* section).

### Run from source

#### First method
```
git clone https://github.com/dbeley/mpdscrobble
cd mpdscrobble
python setup.py install
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
mkdir -p ~/.config/mpdscrobble
curl https://raw.githubusercontent.com/dbeley/mpdscrobble/main/mpdscrobble.example.conf > ~/.config/mpdscrobble/mpdscrobble.conf
systemctl --user daemon-reload
systemctl --user enable --now mpdscrobble
```

## Configuration

See [`mpdscrobble.example.conf`](https://github.com/dbeley/mpdscrobble/blob/main/mpdscrobble.example.conf) for an example.

## Scheduling

```
wget https://raw.githubusercontent.com/dbeley/mpdscrobble/main/systemd-service/mpdscrobble.service > ~/.config/systemd/user/mpdscrobble.service
systemctl --user daemon-reload
systemctl --user enable --now mpdscrobble
```

If you installed mpdscrobble from source you can also use:

```
cp systemd-service/* ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now mpdscrobble
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
