# p.a.w.s.

p.a.w.s., "play along with spotify" is a deliberately minimal tool for displaying rockband format drum charts, with (non-deliberately) minimal levels of synchronisation to spotify playback. It does not attempt to score your drumming accuracy, and does not require you to have your drums plugged into the computer.

## why

I like to play along to music, but am still learning to improvise. An existing chart gives me something to play along with. This solution has less visual noise than something like (the excellent in its own right) Phase Shift, and the use of spotify means that artists are getting paid for their music and there is no pirate audio files are needed.

## dependencies and other setup

You will need to install pygame (which can be done with pip), [spotipy](https://github.com/plamere/spotipy) by @plamere (the version in pip is out of date) and [python-midi](https://github.com/vishnubob/python-midi) by @vishnubob. I suggest using one of the python3 ports of python-midi, such as [this one](https://github.com/louisabraham/python3-midi/) by @louisabraham. 

You will need to register a spotify app, as described in the [spotipy documentation](https://spotipy.readthedocs.io/en/latest/), and put your client_id and secret into a file, "spotipy_constants.py", along with everything else.

## file formats

You'll need to provide a midi file that conforms to music game notation conventions, and create an ini file to go with it. 

As an example, Magnus Palsson has distributed his track "Positive Force" along with Phase Shift, including a midi file (as "notes.mid"). After renaming the midi file to something more memorable, my ini files look like this:
```
[Song]
MidiFile = Souleye - Positive Force.mid
Spotify = spotify:track:1ExS1EPtsWZKcLtvPq37IH
Delay = -0.3
```

Worth noting, the Spotify key in these files can span multiple tracks - Note that in this example, the midi file spans two spotify tracks. In the special case of midi files with multiple tracks, e.g. `Spotify = spotify:track:3WBXyS9Isg4aQBPCuX2GwL,spotify:track:2tQfSfnEFo9OnhYm3mNMj8
`. In this case, p.a.w.s. won't attempt to continually resync its track position with spotify once per second, as it would do otherwise - it will just sync once, one second into playback.

## controls

escape exits, "f" toggles fullscreen, and left and right arrow let you adjust the midi / spotify delay in 0.1 second increments.

## known bugs

Sometimes, the program can't take control of spotify if you haven't recently played something in it (i.e. you have no current session with the spotify servers.) Usually playing and pausing anything should fix this.

It's ugly. Full-screen mode (f) doesn't use native resolutions for some reason.

Hasn't been tested on non-Windows platforms.