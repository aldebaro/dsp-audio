'''
Demonstrates specific audio effect using digital signal 
processing (DSP).
This effect is called Reverb
References:
Author: Mike Aleixo
Date: 27/03/2022
'''
from scipy import signal
import numpy as np

def reverb(sig, revImpulseResponse):
        length= len(sig)
        nsample= np.array(range(length))
        r=5000
        a=0.8
        revImpulseResponse = revImpulseResponse[revImpulseResponse != 0]
        sign = signal.fftconvolve(sig, revImpulseResponse) # using fft for convolution is faster than the usual linear convolution
        sign /= np.max(np.abs(sig)) # normalize output
        

        index= np.round(nsample+r)
        index[index<0]= 0 #Clip delay
        index[index>(length-1)]= length-1
    
        out_sig= np.zeros(length) #Imput Signal

        for j in range(length): #For each sample
          out_sig[j]= np.float(sig[j]) + a*np.float(sig[int(index[j])]) #Add Delayed signal
        
        #plt.plot(out_sig,'r',sig,'b')

        #take out the silence in the end (tail of the convolution)
        return sign
