'''
Demonstrates specific audio effect using digital signal
processing (DSP).
This effect is called XXX
References:
Author: Tatiane Ferraz Balbinot
Date: 29/03/2022
'''
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt

def distortion(sig, alpha: float=0.9):


    if alpha >= 1 :
        print("Valor acima do permitido")
        alpha = 0.9

    elif alpha < 0 :
        print("Valor abaixo do intervalo permitido")
        alpha = 0.9

    #a = 0.9
    kdist = 2*alpha/1-alpha #complex


    signal = sig.astype(np.float) #Copy of the array, cast to a specified type.
    signal /= np.max(np.abs(signal)) #get the highest element in absolute value in a numpy matrix

    xdist = (1+kdist)*(signal)/(1+kdist*abs(signal)) #Calculation of signal nonlinearity

    alpha_vet = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] #definition of alpha values of array
    kdist_ord = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] #null array to calculate in for
    i = 0 #index

    for alpha_u in alpha_vet:
        kdist_ord[i] = ((2*alpha_u)/(1-alpha_u))
        i = i+1

    plt.plot(alpha_vet, kdist_ord)
    plt.xlabel('alpha')
    plt.ylabel('kdist')
    plt.show()

    plt.plot(signal, xdist)
    plt.xlabel('signal(x)')
    plt.ylabel('xdist')
    plt.show()

    return xdist
