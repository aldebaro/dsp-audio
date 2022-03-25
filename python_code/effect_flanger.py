'''
Demonstrates specific audio effect using digital signal 
processing (DSP).
This effect is called XXX
References:
Author: Marco Aurelio
Date: 25/03/2022
'''

import numpy as np
def flanger(audioin,Fs):
    length= len(audioin)
    nsample= np.array(range(length))
    
    lfo_freq=1/2 #LFO Freq (Hz)
    lfo_amp=0.008 #LFO Amp (sec)
    lfo=2+signal.sawtooth(2*np.pi*lfo_freq*(nsample)/Fs,0.5) #Generate triangle wave
    
    plt.plot(lfo)
    plt.xlabel ("Sample Index")
    plt.ylabel("Delay Amount (normalized)")
    plt.title("Delay vs Time")
    
    index= np.around[nsample-Fs*lfo_amp*lfo]
    index[index<0]= 0 #Clip delay
    index[index>(length-1)]= length-1
    
    out= np.zeros(length) #Imput Signal
    print(out.shape)
    for j in range(length): #For each sample
       out[j]= np.float(audioin[j]) + np.float(audioin[int(index[j])]) #Add Delayed signal
    return out
