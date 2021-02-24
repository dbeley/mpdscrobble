# mpdscrobble

A simple Last.fm/Libre.fm scrobbler for MPD.

If you are searching for a mpd-compatible last.fm or libre.fm scrobbler, check out first mpdscribble.

Be aware that mpdscrobble has less features than mpdscribble:
- no journal of failed scrobbles
- it needs a pair of API key/secret

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
