'''
Demonstrates specific audio effect using digital signal
processing (DSP).
This effect is called XXX
References:
Author:
Date:
'''
import math
import cmath
import numpy as np

def distortion(sig):


    a = 0.9
    kdist = 2*a/1-a #complex

    signal = sig.astype(np.float) #Copy of the array, cast to a specified type.
    signal /= np.max(np.abs(signal)) #get the highest element in absolute value in a numpy matrix

    xdist = (1+kdist)*(signal)/(1+kdist*abs(signal)) #Calculation of signal nonlinearity

    return xdist
