# mpdscrobble

A simple Last.fm scrobbler for MPD.

If you are searching for a mpd-compatible last.fm scrobbler, check out first mpdscribble, as mpdscrobble has less features than mpdscribble:
- no journal of failed scrobbles
- it needs a pair of Last.fm API key/secret instead of just username/password

The script `mpdscribble_history.py` can be used to scrobble a list of tracks in a mpdscribble journal file.

## Requirements

- mpd-python2
- pylast

## Installation

```
git clone https://github.com/dbeley/mpdscrobble
cd mpdscrobble
python setup.py install
mpdscrobble -h
```

## Configuration

See mpdscrobble.example.conf
