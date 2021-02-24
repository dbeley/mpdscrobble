# mpdscrobble

A simple Last.fm scrobbler for MPD.

If you are searching for a mpd-compatible last.fm scrobbler, check out first mpdscribble, as mpdscrobble has less features than mpdscribble:
- no journal of failed scrobbles
- it needs a pair of Last.fm API key/secret instead of just username/password

The script `mpdscribble_history.py` can be used to scrobble a list of tracks from a mpdscribble journal file.

## Requirements

- mpd-python2
- pylast

## Installation

Classic installation :

```
pip install mpdscrobble
```

If you are an Archlinux user, you can install the AUR package [mpdscrobble-git](https://aur.archlinux.org/packages/mpdscrobble-git).

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

## Configuration

See mpdscrobble.example.conf
