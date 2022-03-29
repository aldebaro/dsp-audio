'''
Music analysis and synthesis via peak-finding
'''
import numpy as np
from scipy.io import wavfile
from audio_util import generate_sin
from audio_util import write_wav_16_bits
from matplotlib import pyplot as plt
from scipy.signal import find_peaks

def load_signal(file_name):
    # open the WAV file, confirm it is mono and read the signal
    sample_rate, original_signal = wavfile.read(file_name)
    num_channels = len(original_signal.shape)
    if num_channels != 1:
        raise Exception("Signal must be mono!")

    #if original_signal is represented in 16 bits, convert to real numbers to facilitate manipulation
    signal = original_signal.astype(float)
    #normalize it to have amplitues in the range [-1, 1]
    signal /= np.max(np.abs(signal))

    return signal, sample_rate

def peak_finding(signal, sampling_interval, sample_rate, window_length, num_fft_points, spectrum_resolution):

    powerSpectrum, frequency, time, imageAxis = plt.specgram(signal, NFFT=num_fft_points, scale='dB', Fs=sample_rate, mode='magnitude', noverlap=None, vmin=None)

    num_notes = len(powerSpectrum[1])
    output_signal = np.zeros((num_fft_points * num_notes))
    current_sample = 0
    for i in range(len(powerSpectrum[1])):
        peaks, _ = find_peaks(powerSpectrum[:,i])
        sortead_peak_index = np.argsort(powerSpectrum[peaks,i])
        frequency_index = peaks[sortead_peak_index[-1]]
        frequency_Hz = frequency_index * spectrum_resolution

        note = generate_sin(frequency_Hz, sampling_interval, window_length, initial_phase = 0)
        last_sample = current_sample + num_fft_points
        output_signal[current_sample:last_sample] = note
        current_sample += num_fft_points
    
    return output_signal

def main():
    input_file_name = '../test_wav_files/music_one_note.wav'
    #input_file_name = '../test_wav_files/music_two_note.wav'

    signal, sample_rate = load_signal(input_file_name)
    
    Ts = 1.0 / sample_rate
    window_length = 0.1
    num_fft_points = int(window_length / Ts)
    spectrum_resolution = sample_rate / num_fft_points

    output_signal = peak_finding(signal, Ts, sample_rate, window_length, num_fft_points, spectrum_resolution)

    #save the song in a WAV file
    file_name = '../test_wav_files/music_one_note_after_synthesis.wav'
    #file_name = '../test_wav_files/music_two_note_after_synthesis.wav'
    write_wav_16_bits(file_name, sample_rate, output_signal)
    print("Wrote file", file_name)

if __name__ == "__main__":
    main()