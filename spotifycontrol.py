import spotipy;
import sys;
import spotipy.util;

from spotipy_constants import spotipy_client_id, spotipy_client_secret;

scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming';

spotipy_redirect_url ='https://localhost/paws/'

username = "curious.jp@gmail.com";

class SpotifyController:
	def __init__( self ):
		self._token = spotipy.util.prompt_for_user_token(username, scope,
			client_id = spotipy_client_id,
			client_secret = spotipy_client_secret, 
			redirect_uri = spotipy_redirect_url );
		self._playing = False;
		self._handle = spotipy.Spotify( auth = self._token );

	def playSong( self, track_uris ):
		self._handle.start_playback( uris = track_uris );
	
	def getPlaybackPosition( self ):
		c_pb = self._handle.current_playback();
		if( "progress_ms" in c_pb ):
			return c_pb[ "progress_ms" ] / 1000;
		return 0;

	def pauseSong( self ):
		self._handle.pause_playback();
