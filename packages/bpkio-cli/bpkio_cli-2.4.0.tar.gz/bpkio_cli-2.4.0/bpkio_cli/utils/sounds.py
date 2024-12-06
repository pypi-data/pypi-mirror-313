import os
import threading

import simpleaudio as sa

# Get directory containing this script file
here = os.path.dirname(os.path.realpath(__file__))


def chime_down():
    _chime("G4-C4")


def chime_up():
    _chime("C4-G4")


def chime_uphigh():
    _chime("C4-C5")


def chime():
    _chime("E4-E4")


def _chime(filename):
    def play_sound():
        file = os.path.join(here, f"../assets/{filename}.wav")
        wave_obj = sa.WaveObject.from_wave_file(file)
        wave_obj.play()

    # Create a thread to play the sound
    thread = threading.Thread(target=play_sound)
    thread.start()
