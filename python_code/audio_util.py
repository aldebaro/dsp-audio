'''
Variety of useful methods.
'''
import numpy as np
from scipy.io.wavfile import write
from matplotlib import pyplot as plt
from skimage.feature.peak import peak_local_max
import copy

'''
https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html
Take in account that 16 bits allow representing the
range [-32768, 32767] and fit everything in [-32767,32767]
to use almost all dynamic range. 
'''
def write_wav_16_bits(file_name, sample_rate, signal):
    max_abs_value = np.max(np.abs(signal))
    if max_abs_value == 0:
        raise Exception('Maximum value is zero!')
    signal = signal.astype(np.float)
    signal /= max_abs_value #normalize to fit [-1,1]
    #print(max_abs_value) #answer is 1
    signal *= 2**15 - 1 #normalize to fit [-32767,32767]
    #print(np.max(np.abs(signal))) #answer is 32767
    write(file_name, sample_rate, signal.astype(np.int16))

'''
Makes sure the duration takes in account the last sample 
represents an interval of sampling_interval.
Avoid numerical errors by first generating discrete-time n
and then multiplying it by sampling_interval to obtain t in 
seconds.
'''
def generate_sin(frequency_Hz, sampling_interval, duration, initial_phase = 0):
    num_samples = round(duration/sampling_interval)
    n=np.arange(0,num_samples)
    t=n*sampling_interval
    x=np.sin(2*np.pi*frequency_Hz*t + initial_phase)
    return x

'''
Find the peaks of a spectrogram using morphological image processing
as implemented in peak_local_max, described at
https://scikit-image.org/docs/0.8.0/api/skimage.feature.peak.html
'''
def estimate_peaks_via_image_proc(signal, Fs):
    # define values
    num_fft_points = 2048
    noverlap = int(np.minimum(128, num_fft_points/2)) #impose at least 50% of overlap

    # calculate spectrogram
    powerSpectrum, frequency, time, imageAxis = plt.specgram(signal, NFFT=num_fft_points, scale='dB', Fs=Fs, mode='magnitude', noverlap = noverlap, vmin=-80)

    #get interval in seconds between two samples in time axis
    Ts = 1.0 / Fs
    window_length = num_fft_points # this is assumed by specgram function
    window_shift = window_length - noverlap # in samples
    time_interval = Ts*window_shift

    #get interval in Hertz between two samples in frequency axis
    frequency_interval = Fs/num_fft_points # this is always the case when using FFT

    #get total number of windows
    num_windows = int(np.floor( (len(signal)-window_length) / window_shift)) + 1 #number of windows
    assert(num_windows == powerSpectrum.shape[1]) #should be the same
    #print('num_windows', num_windows)

    #assume number of peaks is the number of windows such that there will potentially
    #one peak per window, unless a given window has more than one peaks
    num_peaks = num_windows

    #find the peaks using min_distance = 0
    peaks_indices = peak_local_max(powerSpectrum, indices=True, min_distance=0, num_peaks=num_peaks)
    
    #sort peaks according to time (the second column, with index 1)
    #https://stackoverflow.com/questions/2828059/sorting-arrays-in-numpy-by-column
    peaks_indices = peaks_indices[peaks_indices[:, 1].argsort()]

    #create another array and normalize it such that time is given in
    #seconds and frequency in Hertz
    peaks_time_freq = copy.deepcopy(peaks_indices.astype(np.float))
    peaks_time_freq[:,0] *= frequency_interval
    peaks_time_freq[:,1] *= time_interval

    return peaks_indices, peaks_time_freq, frequency_interval, time_interval

'''
Plot (but not show) the spectrogram.
'''
def plot_spectrogram(signal, Fs):
    num_fft_points = 2048
    noverlap = int(np.minimum(128, num_fft_points/2)) #impose at least 50% of overlap
    plt.specgram(signal, NFFT=num_fft_points, scale='dB', Fs=Fs, mode='magnitude', noverlap = noverlap, vmin=-80)
    plt.colorbar()
    plt.title('Spectrogram (dB)')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')

'''
Plot each peak in time versus frequency plane.
'''
def plot_peaks_superimposed(peaks_time_freq):
    num_peaks = peaks_time_freq.shape[0]
    for i in range(num_peaks):
        plt.plot(peaks_time_freq[i,1], peaks_time_freq[i,0], 'x')
