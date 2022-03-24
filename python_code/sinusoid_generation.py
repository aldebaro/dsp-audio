'''
Simple example of generating a sinusoid of 400 Hz and
duration 3 seconds and saving it to a WAV file that
can be manipulated with the Audacity software.
'''
import numpy as np
from audio_util import write_wav_16_bits
from audio_util import generate_sin

frequency_Hz = 400
sample_rate=8000 #sampling frequency
sampling_interval = 1/sample_rate
duration = 3 #seconds
initial_phase = np.pi/2
signal=generate_sin(frequency_Hz, sampling_interval, duration, initial_phase = initial_phase)
file_name = "test.wav"
write_wav_16_bits(file_name, sample_rate, signal)
print("Wrote file", file_name)