import midi;
import time;
import copy;
import pygame;
import configparser;
import logging;
import sys;
import threading;

from constants import *;
import pawsload;
import tempo;
import visuals;
import spotifycontrol;

PYGAME_SEEK_API_POLL = pygame.USEREVENT;
PYGAME_API_POLL_RETURN = pygame.USEREVENT + 1;

def backgroundAPIPoll( sc, pre_delay = None ):
	if( pre_delay ):
		time.sleep( pre_delay );
	event = pygame.event.Event( PYGAME_API_POLL_RETURN, message = sc.getPlaybackPosition() );
	pygame.event.post( event );

def playPattern( pattern_original, spotify_uri, delay_audio ):
	pattern = copy.deepcopy( pattern_original );
	
	time_steps = tempo.tempoStepsToTimeSteps( pattern );
	spotify_controller = spotifycontrol.SpotifyController();
	screen_controller = visuals.PawsVisualState( 800, 600, tpsc = 8, gem_height = 4 );	

	quitting = False;
	start_time = time.time();
	spotify_controller.playSong( spotify_uri );

	if( len( spotify_uri ) > 1 ):
		logging.warning( "this song has multiple spotify uris - %s - ongoing position polling will be disabled" % spotify_uri );
		backgroundAPIPoll( spotify_controller, pre_delay = 1 );
	else:
		pygame.time.set_timer( PYGAME_SEEK_API_POLL, 1000 );

	while( not quitting ):
		loop_begin = time.time();
		passed = loop_begin - start_time;
		music_time = passed + delay_audio;

		tick = tempo.timeToTick( time_steps, music_time );
		screen_controller.redrawScreen( pattern[1], tick, passed );
		
		for event in pygame.event.get():
			if( event.type == pygame.QUIT ):
				quitting = True;
			elif( event.type == PYGAME_SEEK_API_POLL ):
				t = threading.Thread( target = backgroundAPIPoll, args = ( spotify_controller, ) );
				t.start();
			elif( event.type == PYGAME_API_POLL_RETURN ):
				start_time = time.time() - event.message;
			elif( event.type == pygame.VIDEORESIZE ):
				w, h = event.dict[ "size" ];
				screen_controller.resize( w, h );
			elif( event.type == pygame.KEYUP ):
				if( event.key == pygame.K_ESCAPE ):
					quitting = True;
				elif( event.key == pygame.K_f ):
					screen_controller.toggleFullscreen();
				elif( event.key == pygame.K_LEFT ):
					delay_audio -= 0.1;
					logging.info( "delay_audio is now %.3f" % delay_audio );
				elif( event.key == pygame.K_RIGHT ):
					delay_audio += 0.1;
					logging.info( "delay_audio is now %.3f" % delay_audio );

		rest_time = loop_begin + 1/30;
		while( time.time() < rest_time ):
			pass;
	spotify_controller.pauseSong();

if __name__ == '__main__':
	logging.basicConfig( level = logging.INFO );

	config_file = sys.argv[1];
	config = configparser.ConfigParser();
	config.read( config_file );

	pattern = pawsload.loadAndProcessPattern( 
		config[ "Song" ][ "MidiFile" ], 
		"medium", True );

	spotify_tracks = config[ "Song" ][ "Spotify" ].split( "," );

	playPattern( pattern, spotify_tracks, float( config[ "Song" ][ "Delay" ] ) );

	