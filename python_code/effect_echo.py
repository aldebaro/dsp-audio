'''
Demonstrates specific audio effect using digital signal 
processing (DSP).
This effect is called ECHO
References: https://www.hackaudio.com/digital-signal-processing/echo-effects/
Author: Jacivaldo Carvalho
Date: 25/03/2022
'''
import numpy as np

def echo(sig, sample_rate, delay_in_seconds, gain=0.9):

    output_audio = np.zeros(len(sig))

    #calculate the delay.
    output_delay = delay_in_seconds*sample_rate

    #Applies delay on the received signal.
    for count, e in enumerate(sig):

        output_audio[count] = e + gain * sig[count - int(output_delay)]

        sig = output_audio

    return sig