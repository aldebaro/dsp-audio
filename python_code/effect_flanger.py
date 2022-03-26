'''
Demonstrates specific audio effect using digital signal 
processing (DSP).
This effect is called FLANGER
References:
Author: Marco Aurelio
Date: 25/03/2022
'''
import numpy as np
def flanger(audioin,Fs):
    length= len(audioin)
    nsample= np.array(range(length))
    
    lfo_freq=0.1 #LFO Freq (Hz)
    lfo_amp=0.1 #LFO Amp (sec)
    lfo=np.sin(2*np.pi*lfo_freq*(nsample)/Fs) #Generate triangle wave
    
    index= np.round(nsample-Fs*lfo_amp*lfo)
    index[index<0]= 0 #Clip delay
    index[index>(length-1)]= length-1
    
    out= np.zeros(length) #Imput Signal
    print(out.shape)
    for j in range(length): #For each sample
       out[j]= np.float(audioin[j]) + np.float(audioin[int(index[j])]) #Add Delayed signal
    plt.plot(out,'r',audioin,'b')
    plt.xlabel ("Sample Index")
    plt.ylabel("Delay Amount (normalized)")
    plt.title("Delay vs Time")
    return out
