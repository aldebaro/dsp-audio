'''
Generate a segment of a nice song and write to WAV file.
Check FazendoMusicaMATLAB.pdf and exemplo_musica.m
And folow sinusoid_generation.py
'''
import cgi
from this import d
import numpy as np
from audio_util import write_wav_16_bits
from audio_util import generate_sin

from audio_util import plot_spectrogram
import matplotlib.pyplot as plt
import os

#define global parameters
sample_rate=44100 #sampling frequency in Hz
sampling_interval = 1/sample_rate #in seconds
single_note_duration = 0.5 #seconds

#define all notes
c_frequency = [16.35, 32.70, 65.41, 130.81, 261.63, 523.25, 1046.50, 2093.00]
c_notes = np.zeros((round(single_note_duration/sampling_interval), len(c_frequency)))
for i in range(0, len(c_frequency)):
    c_notes[:, i] = generate_sin(c_frequency[i], sampling_interval, single_note_duration, initial_phase = 0)

cd_frequency = [17.35, 34.65, 69.30, 138.59, 277.18, 554.37, 1108.73, 2217.46]
cd_notes = np.zeros((round(single_note_duration/sampling_interval), len(cd_frequency)))
for i in range(0, len(cd_frequency)):
    cd_notes[:, i] = generate_sin(cd_frequency[i], sampling_interval, single_note_duration, initial_phase = 0)

d_frequency = [18.35, 36.71, 73.42, 146.83, 293.66, 587.33, 1174.66, 2349.32]
d_notes = np.zeros((round(single_note_duration/sampling_interval), len(d_frequency)))
for i in range(0, len(d_frequency)):
    d_notes[:, i] = generate_sin(d_frequency[i], sampling_interval, single_note_duration, initial_phase = 0)

de_frequency = [19.45, 38.89, 77.78, 155.56, 311.13, 622.25, 1244.51, 2489.02]
de_notes = np.zeros((round(single_note_duration/sampling_interval), len(de_frequency)))
for i in range(0, len(de_frequency)):
    de_notes[:, i] = generate_sin(de_frequency[i], sampling_interval, single_note_duration, initial_phase = 0)

e_frequency = [20.60, 41.20, 82.41, 164.81, 329.63, 659.26, 1318.51, 2637.02]
e_notes = np.zeros((round(single_note_duration/sampling_interval), len(e_frequency)))
for i in range(0, len(e_frequency)):
    e_notes[:, i] = generate_sin(e_frequency[i], sampling_interval, single_note_duration, initial_phase = 0)

f_frequency = [21.83, 43.65, 87.31, 174.61, 349.23, 698.46, 1396.91, 2793.83]
f_notes = np.zeros((round(single_note_duration/sampling_interval), len(f_frequency)))
for i in range(0, len(f_frequency)):
    f_notes[:, i] = generate_sin(f_frequency[i], sampling_interval, single_note_duration, initial_phase = 0)

fg_frequency = [23.12, 46.25, 92.50, 185.00, 369.99, 739.99, 1479.98, 2959.96]
fg_notes = np.zeros((round(single_note_duration/sampling_interval), len(fg_frequency)))
for i in range(0, len(fg_frequency)):
    fg_notes[:, i] = generate_sin(fg_frequency[i], sampling_interval, single_note_duration, initial_phase = 0)

g_frequency = [24.50, 49.00, 98.00, 196.00, 392.00, 783.99, 1567.98, 3135.96]
g_notes = np.zeros((round(single_note_duration/sampling_interval), len(g_frequency)))
for i in range(0, len(g_frequency)):
    g_notes[:, i] = generate_sin(g_frequency[i], sampling_interval, single_note_duration, initial_phase = 0)

ga_frequency = [25.96, 51.91, 103.83, 207.65, 415.30, 830.61, 1661.22, 3322.44]
ga_notes = np.zeros((round(single_note_duration/sampling_interval), len(ga_frequency)))
for i in range(0, len(ga_frequency)):
    ga_notes[:, i] = generate_sin(ga_frequency[i], sampling_interval, single_note_duration, initial_phase = 0)

a_frequency = [27.50, 55.00, 110.00, 220.00, 440.00, 880.00, 1760.00, 3520.00]
a_notes = np.zeros((round(single_note_duration/sampling_interval), len(a_frequency)))
for i in range(0, len(a_frequency)):
    a_notes[:, i] = generate_sin(a_frequency[i], sampling_interval, single_note_duration, initial_phase = 0)

ab_frequency = [29.14, 58.27, 116.54, 233.08, 466.16, 932.33, 1864.66, 3729.31]
ab_notes = np.zeros((round(single_note_duration/sampling_interval), len(ab_frequency)))
for i in range(0, len(ab_frequency)):
    ab_notes[:, i] = generate_sin(ab_frequency[i], sampling_interval, single_note_duration, initial_phase = 0)

b_frequency = [30.87, 61.74, 123.47, 246.94, 493.88, 987.77, 1975.53, 3951.07]
b_notes = np.zeros((round(single_note_duration/sampling_interval), len(b_frequency)))
for i in range(0, len(b_frequency)):
    b_notes[:, i] = generate_sin(b_frequency[i], sampling_interval, single_note_duration, initial_phase = 0)

#concatenate notes to compose segments
linha1 = np.concatenate((a_notes[:,4], a_notes[:,4], e_notes[:,5], e_notes[:,5], fg_notes[:,5], fg_notes[:,5], e_notes[:,5], e_notes[:,5]), axis=0)
linha2 = np.concatenate((d_notes[:,5], d_notes[:,5], cd_notes[:,5], cd_notes[:,5], b_notes[:,4], b_notes[:,4], a_notes[:,4], a_notes[:,4]), axis=0)
linha3 = np.concatenate((e_notes[:,5], e_notes[:,5], d_notes[:,5], d_notes[:,5], cd_notes[:,5], cd_notes[:,5], b_notes[:,4], b_notes[:,4]), axis=0)

#concatenate segments to compose the final music
music = np.concatenate((linha1, linha2, linha3, linha3, linha1, linha2), axis=0)

#save the song in a WAV file
file_name = os.path.abspath(r'..\ ') + r'\test_wav_files\music.wav'
write_wav_16_bits(file_name, sample_rate, music)
print("Wrote file", file_name)

#Plot spectrogram
plot_spectrogram(music, sample_rate)
plt.ylim(0, 1000)
plt.yticks(np.arange(0, 1001, step=50))
plt.xticks(np.arange(0, 25, step=1))
plt.show()