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
        nsample= np.array(range(length)) #creates an array of signal length
        r=5000 #delay factor
        a=0.8 #attenuation factor
        revImpulseResponse = revImpulseResponse[revImpulseResponse != 0] #creates a filtered list with non-zero values
        sign = signal.fftconvolve(sig, revImpulseResponse) # convolution between signal and impulse response
        sign /= np.max(np.abs(sig)) # normalize output
        
        #Index for delay
        index= np.round(nsample-r)
        index[index<0]= 0 
        index[index>(length-1)]= length-1

        out_sig= np.zeros(length) #Imput Signal

        for j in range(length): #loop to calculation  each sample
          out_sig[j]= np.float(sig[j]) + a*np.float(sig[int(index[j])]) #Add Delayed signal
        
        #plt.plot(out_sig,'r',sig,'b')
        #plt.show()

        #removing the silence in the end (tail of the convolution)
        energy_out_sig= sum(np.abs(out_sig)**2)#energy  out signal
        energy_interest_out_sig=energy_out_sig*0.99 #energy of interest
        sample_interest_out_sig=np.around(energy_interest_out_sig*length/energy_out_sig) #signal interest sample
        
        #plt.plot(out_sig,'r',sig,'b')

        return sign[1:int(sample_interest_out_sig)]
