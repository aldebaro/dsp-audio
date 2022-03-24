'''
Music analysis and synthesis via peak-finding
https://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array
'''
from scipy.io import wavfile
from audio_util import plot_spectrogram
from audio_util import estimate_peaks_via_image_proc
from audio_util import plot_peaks_superimposed
from audio_util import generate_sin
from audio_util import write_wav_16_bits
import numpy as np
from matplotlib import pyplot as plt

input_file_name = '../test_wav_files/sample-16bits.wav'
#input_file_name = '../test_wav_files/sinusoid_2kHz.wav'
# open the WAV file, confirm it is mono and read the signal
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html
sample_rate, original_signal = wavfile.read(input_file_name)
#signal has a shape (100,2) in case of a stereo signal with 100 samples
#or (100,) if that original_signal has a single channel (mono)
num_channels = len(original_signal.shape)
if num_channels != 1:
    raise Exception("Signal must be mono!")

#if original_signal is represented in 16 bits, convert to real numbers to facilitate manipulation
signal = original_signal.astype(np.float)
#normalize it to have amplitues in the range [-1, 1]
signal /= np.max(np.abs(signal))

#estimate peaks
peaks_indices, peaks_time_freq, frequency_interval, time_interval = estimate_peaks_via_image_proc(signal, sample_rate)

#plot spectrogram and peaks
plot_spectrogram(signal, sample_rate)
plot_peaks_superimposed(peaks_time_freq)

#now synthesize sound according to peaks
sampling_period = 1.0/sample_rate
note_duration = time_interval
num_notes = peaks_time_freq.shape[0]
num_samples_per_note = int(note_duration/ sampling_period)
output_signal = np.zeros((num_samples_per_note * num_notes))
current_sample = 0
for i in range(num_notes):
    if (i > 0) & (peaks_time_freq[i-1,1] == peaks_time_freq[i,1]):
        continue #skip same time, and use a single frequency per time interval
    frequency_Hz = peaks_time_freq[i,0]
    current_time = peaks_time_freq[i,1]
    x=generate_sin(frequency_Hz, sampling_period, note_duration)
    assert(len(x)==num_samples_per_note)
    last_sample = current_sample + num_samples_per_note
    output_signal[current_sample:last_sample] = x
    current_sample += num_samples_per_note

#write WAV
file_name = 'synth_after_analysis.wav'
write_wav_16_bits(file_name, sample_rate, output_signal)
print('Wrote file', file_name)
#show plots
plt.show()