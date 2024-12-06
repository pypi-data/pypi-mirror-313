from scamp import Session, playback_settings, Envelope, wait
from random import random, choice
from enum import Enum


class Instrument(Enum):
    PIANO = 'piano'
    CELLO = 'cello'
    CLARINET = 'clarinet'
    OBOE = 'oboe'
    GUITAR = 'guitar'
    VIOLIN = 'violin'

# Inspiration: https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
class Note(Enum):
    """
    Pitches, from letters to numbers, to make easier 
    working with this MIDI notes.
    """
    A3 = 57
    B3 = 59
    C4 = 60
    D4 = 62
    E4 = 64
    F4 = 65
    G4 = 67
    A4 = 69
    B4 = 71
    C5 = 72

class InstrumentPlayer:
    session = None
    session_tempo = 60
    __parts = {}

    def __init__(self, session_tempo: int = 60):
        if not session_tempo:
            session_tempo = 60

        # TODO: Check more stuff maybe

        self.session_tempo = session_tempo

    def __start_session(self):
        if not self.session:
            self.session = Session(self.session_tempo)

        return self.session
    
    def __get_instrument_part(self, instrument: Instrument):
        """
        Gets the existing session instrument part or creates it
        and then returns it.
        """
        if not instrument:
            raise Exception('No "instrument" provided.')
        
        if not self.session:
            self.__start_session()

        if not instrument.value in self.__parts:
            self.__parts[instrument.value] = self.session.new_part(instrument.value)

        return self.__parts[instrument.value]
    
    def play_note(self, instrument: Instrument, note: Note, seconds: float = 1):
        """
        Playes the provided 'note' with the also provided 'instrument'
        during the given 'seconds'.
        """
        # TODO: By now I'm not strict with 'note' being a Note because
        # I don't have all notes registered so I could pass some int
        # values as well (by now)
        instrument_part = self.__get_instrument_part(instrument)
        instrument_part.play_note(note.value, 1, seconds)

    def play_notes(self, instrument: Instrument, notes: list[Note]):
        for note in notes:
            self.play_note(instrument, note)

    # session.start_transcribing()
    # session.stop_transcribing()


def __play_instrument_randomly(instrument: Instrument):
    #playback_settings.recording_file_path = "chello.wav"

    session = Session()
    session.tempo = 60 

    instrument = session.new_part(instrument.value)

    pitches = [60, 62, 64, 60, 64, 65, 67, 64, 67, 69, 72, 64, 72, 60] # "Frère Jacques"
    pitches = [67, 67, 69, 69, 71, 71, 69, 67, 65, 65, 67, 65, 67, 69, 67] # "Ode to Joy" de Beethoven
    pitches = [60, 62, 65, 62, 60, 62, 67, 65, 64, 62, 60] * 4
    pitches = [67, 67, 69, 71, 69, 67, 65, 64, 62, 62, 64, 65, 67, 69, 71, 69, 67] * 4

    for pitch in pitches:
        instrument.play_note(pitch, 1, 0.05)

def __test():
    """
    This method is so experimental. It uses a library that allows
    creating instrumental part of a song by using instruments and
    telling the songs you want to listen.

    TODO: This need a lot of work, investigation and refactor
    """
    # Thanks to:
    # https://www.youtube.com/watch?v=vpv686Rasds

    # This is for saving the generated audio, that is based on:
    # https://scampsters.marcevanstein.com/t/can-we-send-scamp-output-to-a-wav-file/314
    playback_settings.recording_file_path = "chello.wav"

    session = Session()
    session.tempo = 60 

    cello = session.new_part('cello')

    #session.start_transcribing()

    forte_piano = Envelope.from_levels_and_durations(
        [0.8, 0.4, 1.0], [0.2, 0.8], curve_shapes = [0, 3]
    )

    diminuendo = Envelope.from_levels([0.8, 0.3])

    def wrap_in_range(value, low, high):
        return (value - low) % (high - low) + low
    
    for pitch in (48, 53, 64, 75, 80):
        cello.play_note(pitch, 1.0, 1.0)

    interval = 1
    cello_pitch = 48

    do_continue = True
    while do_continue:
        if random() < 0.7:
            cello.play_note(cello_pitch, forte_piano, choice([1.0, 1.5]))
        else:
            cello.play_note(cello_pitch, diminuendo, choice([2.0, 2.5, 3.0]))
            wait(choice([1.0, 1.5]))
        cello_pitch = wrap_in_range(cello_pitch + interval, 36, 60)
        interval += 1

        if interval == 20:
            do_continue = False

    # ImportError: abjad was not found; LilyPond output is not available.
    #session.stop_transcribing().to_score(time_signature = '3/8').show()
    #session.stop_transcribing()

    return