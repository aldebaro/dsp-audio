'''
Demonstrates specific audio effect using digital signal 
processing (DSP).
This effect is called XXX
References:
Author: 
Date: 
'''
from scipy import signal
import numpy as np

    # Reverb effect
def reverb(sig, revImpulseResponse):
        """
        Function to replicate reverb effect on a signal.
        The reverb effect is the replication of the reflections of a sound wave
        on a ambient.
        """
        #sig = self.normalize(self.sig)
        #revfs, revImpulseResponse = wavfile.read(file)
        revImpulseResponse = revImpulseResponse[revImpulseResponse != 0]
        sig = signal.fftconvolve(sig, revImpulseResponse) # using fft for convolution is faster than the usual linear convolution
        sig /= np.max(np.abs(sig)) # normalize output
        #sig = self.denormalize(sig)

        #TO-DO
        #take out the silence in the end (tail of the convolution)
        return sig
