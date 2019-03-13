import midi;

def tempoToSecondsPerTick( t, r ):
  seconds_per_tick = 60 / t / r;
  return seconds_per_tick;

def tempoStepsToTimeSteps( p ):
  resolution = p.resolution;
  tempo_track = p[ 0 ];

  # the default tempo per midi standard, although it can and will
  # be replaced if there is a manual tempo event on tick zero
  default = ( 0, 0, tempoToSecondsPerTick( 120, resolution ) );
  result = [ default ];

  running_total = 0;
  previous_tick = 0;
  current_ttspt = 0;
  
  tempo_track.sort( key = lambda x: x.tick );
  for event in tempo_track:
    if( not isinstance( event, midi.SetTempoEvent ) ):
      continue;

    tempo_step = ( event.tick, event.bpm );
    running_total += ( tempo_step[0] - previous_tick ) * current_ttspt;
    current_ttspt = tempoToSecondsPerTick( tempo_step[1], resolution );
    previous_tick = tempo_step[0];

    # if this is a new tick zero tempo, we can get rid of the default one
    if( event.tick == 0 ):
      result.remove( default );

    result.append( ( running_total, tempo_step[0], current_ttspt ) );
  
  result.sort( key = lambda x: x[0] );
  return result;

# time_steps must be sorted or this isn't going to work!
def timeToTick( time_steps, time ):
  nearest_step = [ x for x in time_steps if x[0] <= time ];
  if( len( nearest_step ) == 0 ):
    return 0;
  nearest_step = nearest_step[-1];
  time_difference = time - nearest_step[0];
  return round( nearest_step[1] + ( time_difference / nearest_step[2] ) );
