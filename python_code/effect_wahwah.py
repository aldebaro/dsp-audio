'''
Demonstrates specific audio effect using digital signal 
processing (DSP).
This effect is called Wah Wah
References: https://ses.library.usyd.edu.au/bitstream/handle/2123/10578/Marion%2C%20Bruno%20-%20Wah%20Wah.pdf
Author: Ailton Oliveira
Date: 27/03/2022
'''
import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize

def wahwah(signal,fs,dp_factor=0.05,width=2000,min_cutoff=250,max_cutoff=2000):
    #Function to return a Wah Wah effect on a signal
    #signal - Input signal that will be modulated (Array);
    #fs - Sampling frequency (Float - Hertz)
    #dp_factor - Damping factor (Float) - dp_factor < 0.5
    #width - effect width (float)
    #min_cutoff - Lower cut-off frequency (Float - Hertz)
    #max_cutoff - Upper cut-off frequency (Float - Hertz)
    
    center_freq = width/fs
    cutoff_freq=list(np.arange(min_cutoff,max_cutoff,center_freq))
    while(len(cutoff_freq) < len(signal)):
        #Add noises until the effect have the same (or bigger) signal size 
        cutoff_freq.extend(np.arange(max_cutoff,min_cutoff,-center_freq)) #Descending
        cutoff_freq.extend(np.arange(min_cutoff,max_cutoff,center_freq)) #Ascending
    cutoff_freq = cutoff_freq[0:len(signal)] #Match the signal size
    cutoff_freq =  np.array(cutoff_freq)#Convert list to array

    #Filtering coefficients
    F1 = 2*np.sin((np.pi*cutoff_freq[0])/fs)
    Q1 = 2*dp_factor

    highpass=np.zeros(len(signal))
    bandpass=np.zeros(len(signal))
    lowpass=np.zeros(len(signal))
    
    #WahWah differential equations
    for n in range(0,len(signal)):
        highpass[n] = signal[n] - lowpass[n-1] - Q1*bandpass[n-1]
        bandpass[n] = F1*highpass[n] + bandpass[n-1]
        lowpass[n] = F1*bandpass[n] + lowpass[n-1]
        F1 = 2*np.sin((np.pi*cutoff_freq[n])/fs)
    
    #Normalized Audio
    Wahsignal  = bandpass/np.amax(abs(bandpass))
    return Wahsignal

if __name__ == '__main__':
    ##Isolated test##
    
    tst_file = '../test_wav_files/sample-16bits.wav'
    fs,signal=wav.read(tst_file)
    normed = wahwah(signal,fs)
    wav.write("wah_wah_example.wav", fs, normed)
    plot_signal= normalize(signal.reshape(-1, 1), norm='max',axis=0)
    _ =input('Want plot the signals ? (y/n)')
    if _ in ['yes','y','sim',True]:
        #Plots
        t1 = np.arange(0,(len(signal)/fs),1/fs)
        plt.plot(t1,plot_signal,label='original')
        plt.title('Original Audio')
        plt.ylabel('Amplitude')
        plt.xlabel('Length (in seconds)')
        
        plt.plot(t1,normed.reshape(-1, 1),label='wah wah')
        plt.title('Wah Wahed Audio')
        plt.ylabel('Amplitude')
        plt.xlabel('Length (in seconds)')
        plt.legend()
        plt.show()
    else:
        print('Finish test')
    


