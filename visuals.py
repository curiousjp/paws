import pygame;
import midi;
from constants import *;

class PawsVisualState:
	def __init__( self, w, h, tpsc = 4, gem_height = 4 ):
		self._ticks_per_screen_coefficient = tpsc;
		self._gem_height = gem_height;
		self._fullscreen = False;
		self.resize( w, h );

	def resize( self, w, h ):
		self._windowed_w = w;
		self._windowed_h = h;
		self._screen = pygame.display.set_mode( ( w, h ),
			pygame.HWSURFACE |
			pygame.DOUBLEBUF |
			pygame.RESIZABLE );
		pygame.display.set_caption( "p.a.w.s." );
		self._buildAssets();

	def toggleFullscreen( self ):
		if( self._fullscreen ):
			self._fullscreen = False;
			self.resize( self._windowed_w, self._windowed_h );
		else:
			self._fullscreen = True;
			self._screen = pygame.display.set_mode( 
				( 0, 0 ),
				pygame.HWSURFACE |
				pygame.DOUBLEBUF |
				pygame.FULLSCREEN );
			self._buildAssets();

	def _buildAssets( self ):
		width, height = self._screen.get_size();
		self._size = ( width, height );
		self._ticks_per_screen = self._ticks_per_screen_coefficient * height;

		def makeSurface( r, g, b, width ):
			result = pygame.Surface( ( width, self._gem_height ) );
			result.fill( ( r, g, b ) );
			return result;

		def stripeSurface( s, r, g, b, xpos, stripe_width ):
			w, h = s.get_size();
			stripe = pygame.Rect( xpos - stripe_width / 2, 0, stripe_width, h );
			s.fill( ( r / 8, g / 8, b / 8 ), rect = stripe );

		# notional screen element layout -
		#  1:
		#  2:
		#  3: yellow hat
		#  4: yellow hat
		#  5: 
		#  6: blue hat
		#  7: blue hat
		#  8:
		#  9: red
		# 10: red
		# 11:
		# 12: yellow
		# 13:
		# 14: blue
		# 15:
		# 16: green hat
		# 17: green hat
		# 18:
		# 19: green
		# 20:
		# 21: 

		block_width = width / 21.0;

		self._assets_s = {};
		self._assets_p = {};

		self._assets_s[ "bg" ] = pygame.Surface( ( width, height ) );
		self._assets_s[ "bg" ].fill( (0,0,0) );

		self._assets_s[ "strike" ] = makeSurface( 255, 255, 255, width );
		self._assets_p[ "strike" ] = 0;

		# kick pedal
		self._assets_s[ 96 ] = makeSurface( 128, 82, 0, width );
		self._assets_p[ 96 ] = 0;

		# snare
		self._assets_s[ 97 ] = makeSurface( 255, 0, 0, block_width * 2 );
		self._assets_p[ 97 ] = block_width * 8;
		stripeSurface( self._assets_s[ "bg" ], 255, 0, 0, self._assets_p[ 97 ] + block_width, block_width );

		# yellow tom
		self._assets_s[ 86 ] = makeSurface( 128, 128, 0, block_width );
		self._assets_p[ 86 ] = block_width * 11;
		stripeSurface( self._assets_s[ "bg" ], 128, 128, 0, self._assets_p[ 86 ] + ( block_width / 2 ), block_width / 2 );

		# yellow hat
		self._assets_s[ 98 ] = makeSurface( 255, 255, 0, block_width * 2 );
		self._assets_p[ 98 ] = block_width * 2;
		stripeSurface( self._assets_s[ "bg" ], 255, 255, 0, self._assets_p[ 98 ] + block_width, block_width );

		# blue tom
		self._assets_s[ 87 ] = makeSurface( 0, 0, 128, block_width );
		self._assets_p[ 87 ] = block_width * 13;
		stripeSurface( self._assets_s[ "bg" ], 0, 0, 128, self._assets_p[ 87 ] + ( block_width / 2 ), block_width / 2 );

		# blue hat
		self._assets_s[ 99 ] = makeSurface( 0, 0, 255, block_width * 2 );
		self._assets_p[ 99 ] = block_width * 5;
		stripeSurface( self._assets_s[ "bg" ], 0, 0, 255, self._assets_p[ 99 ] + block_width, block_width );
		
		# green tom
		self._assets_s[ 88 ] = makeSurface( 0, 128, 0, block_width );
		self._assets_p[ 88 ] = block_width * 18;
		stripeSurface( self._assets_s[ "bg" ], 0, 128, 0, self._assets_p[ 88 ] + ( block_width / 2 ), block_width / 2 );

		# green hat
		self._assets_s[ 100 ] = makeSurface( 0, 255, 0, block_width * 2 );
		self._assets_p[ 100 ] = block_width * 15;
		stripeSurface( self._assets_s[ "bg" ], 0, 255, 0, self._assets_p[ 100 ] + block_width, block_width );

	def redrawScreen( self, track, tick, secs ):
		w, h = self._size;

		self._screen.blit( self._assets_s[ "bg" ], ( 0, 0 ) );

		tick_offset = self._ticks_per_screen / 8;
		starting_tick = tick - tick_offset;
		ending_tick = starting_tick + self._ticks_per_screen;

		relevant_events = [x for x in track if 
			x.tick >= starting_tick and 
			x.tick < ending_tick and
			isinstance( x, midi.NoteOnEvent ) and
			x.pitch in self._assets_s ];

		for event in relevant_events:
			percent_position = ( event.tick - starting_tick ) / self._ticks_per_screen;
			pixel_row = h - ( percent_position * h ) - 1;
			self._screen.blit( self._assets_s[ event.pitch ], ( self._assets_p[ event.pitch ], pixel_row - self._gem_height ) );

		self._screen.blit( self._assets_s[ "strike" ], ( self._assets_p["strike"], h * (7/8) ) );		

		pygame.display.flip();

pygame.init();