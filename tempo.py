import midi;
import fractions;

def mpqnToSecondsPerTick( m, r ):
  quarter_notes_per_second = fractions.Fraction( 1000000, m );
  ticks_per_second = quarter_notes_per_second * r;
  return fractions.Fraction( ticks_per_second.denominator, ticks_per_second.numerator );

def tempoStepsToTimeSteps( p ):
  # the default tempo per midi standard, although it can and will
  # be replaced if there is a manual tempo event on tick zero
  result = [ ( 0, 0, mpqnToSecondsPerTick( 500000, p.resolution ) ) ];

  running_total_seconds = 0.0;
  seconds_per_tick = 0;
  previous_event = midi.Event( tick = 0 );

  tempo_events = [ x for x in p[ 0 ] if isinstance( x, midi.SetTempoEvent ) ];
  tempo_events.sort( key = lambda x: x.tick );

  for event in tempo_events:
    ticks_since_previous_event = event.tick - previous_event.tick;
    seconds_elapsed_since_previous = ticks_since_previous_event * seconds_per_tick;
    running_total_seconds += seconds_elapsed_since_previous;

    new_seconds_per_tick = mpqnToSecondsPerTick( event.mpqn, p.resolution );

    time_step = ( running_total_seconds, event.tick, new_seconds_per_tick );
    if( event.tick == 0 ):
      result = [ time_step ];
    else:
      result.append( time_step );

    previous_event = event;
    seconds_per_tick = new_seconds_per_tick;

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
