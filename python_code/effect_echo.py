'''
Demonstrates specific audio effect using digital signal 
processing (DSP).
This effect is called ECHO
References: https://www.hackaudio.com/digital-signal-processing/echo-effects/
Author: Jacivaldo Carvalho
Date: 29/03/2022
'''
from turtle import delay
import numpy as np
import matplotlib.pyplot as plt

def echo(signal, sample_rate, delay_in_seconds, gain=0.9):

    #calculate the delay.
    number_sample_zeros =  int(delay_in_seconds*sample_rate)

    echo = np.zeros(len(signal))
    
    #scales the echo vector.
    echo[number_sample_zeros:len(signal)] = signal[0:len(signal)- number_sample_zeros]
    
    #generates the echoed audio signal.
    signal_echo = signal + gain*echo

    #It asks the user if he wants to generate the graphics of the original and the echoed audio.
    choice = input("Do you want to display signals in the time and frequency domain?(y/n)\n")

    if(choice == 'y'):
        plot_signal(signal, signal_echo)
        plot_spectrogram(signal,signal_echo,sample_rate)
        return signal_echo
    else:
        return signal_echo

def plot_signal(signal_original, signal_echo):

    #plot signal original.
    plt.subplot(1,2,1)
    plt.plot(signal_original)
    plt.title("Signal Original")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")

    #plot signal echo.
    plt.subplot(1,2,2)
    plt.plot(signal_echo)
    plt.title("Signal Echo")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")

    plt.suptitle("Comparison between original and echoed audio.")
    plt.show()

def plot_spectrogram(signal, signal_echo, sample_rate):
    num_fft_points = 2048
    noverlap = int(np.minimum(128, num_fft_points/2)) 

    #plot spectrogram signal original.
    plt.subplot(1,2,1)
    plt.specgram(signal, NFFT=num_fft_points, scale='dB', Fs=sample_rate, mode='magnitude', noverlap = noverlap, vmin=-80)
    plt.colorbar()
    plt.title('Signal Original')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')

    #plot spectrogram signal echo.
    plt.subplot(1,2,2)
    plt.specgram(signal_echo, NFFT=num_fft_points, scale='dB', Fs=sample_rate, mode='magnitude', noverlap = noverlap, vmin=-80)
    plt.colorbar()
    plt.title('Signal Echo')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')

    plt.suptitle("Spectrogram of the original and echoed audio.")
    plt.show()
