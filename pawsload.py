import midi;
import copy;

from constants import *;

difficultyMap = {
	"expert": range( 96, 101 ),
	"hard":   range( 84, 89 ),
	"medium": range( 72, 77 ),
	"easy":   range( 60, 65 )
}

def mapTrackNames( p ):
	nameMap = {};
	for track in range( len( p ) ):
		for event in p[ track ]:
			if( isinstance( event, midi.TrackNameEvent ) ):
				nameMap[ event.text ] = track;
	return nameMap;

def proProcessing( track ):
	# the main purpose of this function is to mark what would otherwise
	# be cymbal hits as toms where they appear alongside special indicator 
	# notes - the notes are 110 (yellow), 111 (blue), and 112 (green).
	# the tick boundaries for the special indicator notes seem to match the
	# underlying cymbal note. we mark toms by transposing them down 12 pitches.

	tom_pairs = { 98: 110, 99: 111, 100: 112 };

	# there are other special pro notes too - rolls (126) and special rolls
	# (127), but I have yet to implement them as I can't seem to work out
	# a good way to display them.

	# we will be working in absolute mode for this
	original_track_relative = track.tick_relative;
	if( original_track_relative ):
		track.make_ticks_abs();

	result_track = copy.deepcopy( track );
	result_track.clear();

	for e in track:
		event = copy.deepcopy( e );
		if( isinstance( event, midi.NoteEvent ) ):
			# we don't port the pro notes directly
			if( event.pitch in proEvents ):
				continue;
			# other notes we will consider
			if( event.pitch in tom_pairs ):
				# test to see if there is a corresponding event of the same
				# type, with the appropriate note, on the same tick
				candidates = [ x for x in track if 
					x.tick == event.tick and
					type( x ) == type( event ) and
					x.pitch == tom_pairs[ event.pitch ] ];
				if( not candidates ):
					# remains as originally coded, a hat
					result_track.append( event );
				else:
					event.pitch -= 12;
					result_track.append( event );
			else:
				result_track.append( event );
		else:
			result_track.append( event );

	result_track.sort( key = lambda x: x.tick );
	if( original_track_relative ):
		result_track.make_ticks_rel();
	return result_track;


def filterDrums( t, diff, pro = True, flense = True ):
	# remove the notes that don't match the selected difficulty, and then
	# remap the notes that remain to use the note numbers normally reserved
	# for "expert". all other messages (except for the special pro signal 
	# notes) are thrown out of the drum track at this point, and note_off
	# is also discarded if flense is set to true.

	note_map = {};
	for src in range( len( difficultyMap[ diff ] ) ):
		note_map[ difficultyMap[ diff ][ src ] ] = difficultyMap[ "expert" ][ src ];
	acceptable_notes = list( note_map.keys() );
	if( pro ):
		acceptable_notes.extend( proEvents );

	filtered_track = copy.deepcopy( t );
	filtered_track.clear();

	for e in t:
		event = copy.deepcopy( e );
		if( not isinstance( event, midi.NoteEvent ) ):
			continue;
		if( flense and not isinstance( event, midi.NoteOnEvent ) ):
			continue;
		if( event.pitch not in acceptable_notes ):
			continue;

		if( event.pitch in note_map ):
			event.pitch = note_map[ event.pitch ];
		filtered_track.append( event );

	if( pro ):
		filtered_track = proProcessing( filtered_track );

	return filtered_track;

def loadAndProcessPattern( fn, difficulty, pro ):
	pattern = midi.read_midifile( fn );
	pattern.make_ticks_abs();
	name_map = mapTrackNames( pattern );
	
	filtered_pattern = copy.deepcopy( pattern );
	filtered_pattern.clear();

	# copy the tempo track
	filtered_pattern.append( pattern[ name_map[ "TEMPO TRACK" ] ] );
	# filter the drums and copy
	f_d_t = filterDrums( pattern[ name_map[ "PART DRUMS" ] ], difficulty, pro );
	filtered_pattern.append( f_d_t );
	return filtered_pattern;
