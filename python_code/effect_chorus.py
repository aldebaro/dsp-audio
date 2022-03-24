'''
Demonstrates specific audio effect using digital signal 
processing (DSP).
This effect is called XXX
References:
Author: 
Date: 
'''
from numpy import random
import numpy as np
import copy

def chorus(sig, ts, level: float=0.1, rate: float=5000, LFO: bool=True):
        """
        Function to replicate chorus effect on a signal.
        The chorus idea is to simulate the feeling of an ensemble of sounds, that
        is the same sequence of sound being heard with slight variations either in
        tone and/or time (small delays, usually 10-50ms), such that it sounds like
        multiple and different sources are producing the same notes. This "randomness"
        can be done digitally by using a sinusoid that represents a low frequency
        oscillator or a random number generator to vary the delay values between
        two extremes and apply it multiple times with small offsets between each
        application.
        
        :level: level of the effect to be applied
        :rate: frequency of the LFO in Hz
        """
        fs=1.0/ts
        #sig = self.normalize(self.sig)
        t = np.arange(0, len(sig)*ts, ts) # time array
        delayMin = 10e-3 # ms
        delayMax = 25*1e-3 # ms
        delayMean = (delayMin + delayMax)/2
        if LFO: 
            lfo = delayMean*np.sin(2*np.pi*t*(rate/fs)) + delayMean
            lfo *= fs # from time to samples
            idxs = np.arange(len(sig)) # array of indices
            currDelay = np.int64(np.round(idxs - lfo)) # assure the integer values
        else:
            # Uniform distrution random number generator
            rnd = random.uniform(delayMin, delayMax/2, len(sig))
            rnd *= fs
            idxs = np.arange(len(sig)) # array of indices
            currDelay = np.int64(np.round(idxs - rnd)) # assure the integer values
        newsignal = copy.deepcopy(sig) #deep, instead of shallow copy
        # Adding delayed copies of the signal
        for i in np.arange(0, 4*ts, 2*ts,dtype=np.int64):
            newsignal += level*(sig[currDelay - i])
        #sig = self.denormalize(sig)
        return newsignal
