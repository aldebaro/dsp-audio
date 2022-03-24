'''
Generate a segment of a nice song.
Check FazendoMusicaMATLAB.pdf and exemplo_musica.m
And folow sinusoid_generation.py
'''
import numpy as np
from audio_util import write_wav_16_bits
from audio_util import generate_sin

#define global parameters
sample_rate=44100 #sampling frequency in Hz
sampling_interval = 1/sample_rate #in seconds
single_note_duration = 0.5 #seconds

#define all notes
#TO-DO

#concatenate notes to compose segments

#concatenate segments to compose the final music

#save the song in a WAV file
#write_wav_16_bits(file_name, sample_rate, signal)
#print("Wrote file", file_name)